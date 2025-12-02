from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal

from estoque.models import Insumo, MovimentacaoEstoque
from estoque.serializers.entrada_serializer  import EntradaMultiplaSerializer


class EntradaMultiplaEstoqueViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="entrada-multipla")
    def entrada_multipla(self, request):

        # ===========================
        # 🚨 VERIFICA SETOR DO PERFIL
        # ===========================
        perfil = getattr(request.user, "perfil", None)

        if not perfil:
            return Response(
                {"erro": "Usuário não possui perfil associado."},
                status=status.HTTP_403_FORBIDDEN
            )

        if perfil.setor != "ESTOQUE":
            return Response(
                {"erro": "Apenas usuários do setor ESTOQUE podem realizar esta operação."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ========================
        # 📌 VALIDA PAYLOAD
        # ========================
        serializer = EntradaMultiplaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nf_numero = serializer.validated_data["nf_numero"]
        itens = serializer.validated_data["insumos"]

        resultados = []

        # =========================
        # 🔄 PROCESSA EM TRANSAÇÃO
        # =========================
        with transaction.atomic():
            for item in itens:
                insumo_id = item["id"]
                quantidade = Decimal(item["quantidade"])

                try:
                    insumo = Insumo.objects.get(id=insumo_id)
                except Insumo.DoesNotExist:
                    continue

                # Atualiza estoque
                insumo.estoque_atual += quantidade
                insumo.save()

                # Registra movimentação
                MovimentacaoEstoque.objects.create(
                    insumo=insumo,
                    tipo="ENT",
                    origem="COMPRA",
                    quantidade=quantidade,
                    observacao=f"Entrada múltipla - NF {nf_numero}"
                )

                resultados.append({
                    "id": insumo.id,
                    "nome": insumo.nome,
                    "quantidade_adicionada": str(quantidade),
                    "novo_estoque": str(insumo.estoque_atual)
                })

        return Response({
            "mensagem": "Entrada múltipla registrada com sucesso.",
            "nf": nf_numero,
            "itens_processados": resultados
        }, status=status.HTTP_201_CREATED)
