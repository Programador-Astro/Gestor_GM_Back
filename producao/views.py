from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal

from producao.models import ProducaoDiaria, ItemProducaoDiaria, InsumoProducao
from producao.serializers import ProducaoDiariaSerializer, ItemProducaoDiariaSerializer
from producao.services.finalizar_producao import finalizar_producao

from estoque.models.insumo import Insumo


# =====================================================================
# 🔵 VIEWSET PRINCIPAL — PRODUÇÃO DIÁRIA
# =====================================================================
class ProducaoDiariaViewSet(viewsets.ModelViewSet):
    queryset = ProducaoDiaria.objects.all().order_by("-data")
    serializer_class = ProducaoDiariaSerializer

    # ===============================================================
    # 🆕 GERA LISTA DE INSUMOS AUTOMATICAMENTE AO CRIAR PRODUÇÃO
    # ===============================================================
   
    def create(self, request, *args, **kwargs):
        with transaction.atomic():

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            producao = serializer.save()

            # ❌ REMOVE a geração automática anterior
            # insumos = Insumo.objects.filter(ativo=True)
            # for insumo in insumos:
            #     ...

            # ✅ Agora a lista começa vazia
            lista_gerada = []

            headers = self.get_success_headers(serializer.data)

            return Response(
                {
                    "mensagem": "Produção criada! Lista de insumos iniciada vazia.",
                    "producao": serializer.data,
                    "insumos": lista_gerada
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )

    # ===============================================================
    # 🆕 GET — RETORNAR LISTA DE INSUMOS
    # ===============================================================
    @action(detail=True, methods=["get"], url_path="lista-insumos")
    def lista_insumos(self, request, pk=None):
        producao = self.get_object()

        insumos = InsumoProducao.objects.filter(producao=producao)

        # Se não tem lista, retorna vazio
        if not insumos.exists():
            return Response({"insumos": []}, status=status.HTTP_200_OK)

        data = []
        for item in insumos:
            data.append({
                "id": item.id,
                "insumo_id": item.insumo.id,
                "nome": item.insumo.nome,
                "quantidade_necessaria": float(item.quantidade_necessaria),
                "quantidade_recebida": float(item.quantidade_recebida),
                "status": item.status,
                "unidade_medida": item.insumo.unidade_medida,
            })

        return Response({"insumos": data}, status=status.HTTP_200_OK)

    # ===============================================================
    # 🔄 POST — SUBSTITUIR TOTALMENTE A LISTA DE INSUMOS
    # ===============================================================
    @action(detail=True, methods=["post"], url_path="gerar-lista-insumos")
    def gerar_lista_insumos(self, request, pk=None):
        producao = self.get_object()
        insumos_body = request.data.get("insumos", [])

        # IDs enviados pelo frontend
        enviados_ids = [i["insumo_id"] for i in insumos_body]

        # Itens já existentes no banco
        existentes = InsumoProducao.objects.filter(producao=producao)
        existentes_map = {item.insumo_id: item for item in existentes}

        novos = []
        atualizados = []
        removidos = []

        with transaction.atomic():

            # 1️⃣ ATUALIZAR OU CRIAR
            for item in insumos_body:
                insumo_id = item["insumo_id"]
                qtde = item.get("quantidade_necessaria", 0)

                try:
                    insumo = Insumo.objects.get(id=insumo_id)
                except Insumo.DoesNotExist:
                    return Response({"erro": f"Insumo {insumo_id} não existe."}, status=400)

                if insumo_id in existentes_map:
                    # 🔵 JÁ EXISTE → ATUALIZA APENAS A QUANTIDADE NECESSÁRIA
                    existente = existentes_map[insumo_id]
                    existente.quantidade_necessaria = qtde
                    existente.save()
                    atualizados.append(existente)
                else:
                    # 🆕 NÃO EXISTE → CRIAR
                    novo = InsumoProducao.objects.create(
                        producao=producao,
                        insumo=insumo,
                        quantidade_necessaria=qtde,
                        quantidade_recebida=0,
                        status="PENDENTE"
                    )
                    novos.append(novo)

            # 2️⃣ REMOVER ITENS QUE NÃO FORAM ENVIADOS
            for insumo_id, item in existentes_map.items():
                if insumo_id not in enviados_ids:
                    removidos.append(item.insumo.nome)
                    item.delete()

        # 3️⃣ RETORNAR LISTA FINAL
        lista_final = [
            {
                "id": item.id,
                "insumo_id": item.insumo.id,
                "nome": item.insumo.nome,
                "quantidade_necessaria": float(item.quantidade_necessaria),
                "quantidade_recebida": float(item.quantidade_recebida),
                "status": item.status
                
            }
            for item in InsumoProducao.objects.filter(producao=producao)
        ]

        return Response({
            "mensagem": "Lista de insumos atualizada com sucesso!",
            "novos": [i.insumo.nome for i in novos],
            "atualizados": [i.insumo.nome for i in atualizados],
            "removidos": removidos,
            "insumos": lista_final
        }, status=200)

    @action(detail=True, methods=["post"], url_path="insumo/(?P<insumo_id>[^/.]+)/fornecer")
    def fornecer_insumo(self, request, pk=None, insumo_id=None):
        try:
            item = InsumoProducao.objects.get(producao_id=pk, insumo_id=insumo_id)
        except InsumoProducao.DoesNotExist:
            return Response({"erro": "Insumo não encontrado nesta produção"}, status=404)

        quantidade = request.data.get("quantidade", None)

        if quantidade is None:
            return Response({"erro": "Informe a quantidade a fornecer"}, status=400)

        try:
            quantidade = Decimal(str(quantidade))  # CONVERTE PARA DECIMAL
        except:
            return Response({"erro": "Quantidade inválida"}, status=400)

        # 🔥 SOMA DA MANEIRA CORRETA (Decimal + Decimal)
        item.quantidade_recebida = item.quantidade_recebida + quantidade

        # 🔥 Atualiza automaticamente o status
        if item.quantidade_recebida == 0:
            item.status = "PENDENTE"
        elif item.quantidade_recebida < item.quantidade_necessaria:
            item.status = "PARCIAL"
        else:
            item.status = "COMPLETO"

        item.save()

        return Response({
            "mensagem": "Quantidade registrada com sucesso",
            "insumo": item.insumo.nome,
            "quantidade_necessaria": item.quantidade_necessaria,
            "quantidade_recebida": item.quantidade_recebida,
            "status": item.status
        })

# =====================================================================
# 🔵 ITENS DE PRODUÇÃO (CRUD)
# =====================================================================
class ItemProducaoDiariaViewSet(viewsets.ModelViewSet):
    queryset = ItemProducaoDiaria.objects.all()
    serializer_class = ItemProducaoDiariaSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível editar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível editar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível remover itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        producao_id = request.data.get("producao")
        producao = ProducaoDiaria.objects.get(pk=producao_id)

        if producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível adicionar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


# =====================================================================
# 🔵 FINALIZAR PRODUÇÃO
# =====================================================================
@api_view(["POST"])
def finalizar_producao_view(request, pk):
    try:
        producao = ProducaoDiaria.objects.get(pk=pk)
    except ProducaoDiaria.DoesNotExist:
        return Response({"erro": "Produção não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    try:
        finalizar_producao(producao)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"mensagem": "Produção finalizada com sucesso!"}, status=status.HTTP_200_OK)
