from rest_framework import viewsets, status
from rest_framework.response import Response
from estoque.models import MovimentacaoEstoque, Produto, Insumo
from estoque.serializers import MovimentacaoEstoqueSerializer
from decimal import Decimal

class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoEstoque.objects.all().order_by('-criado_em')
    serializer_class = MovimentacaoEstoqueSerializer

    def create(self, request, *args, **kwargs):
        # Valida o serializer primeiro
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        produto_id = serializer.validated_data.get("produto")
        insumo_id = serializer.validated_data.get("insumo")
        tipo = serializer.validated_data.get("tipo")   # ENT ou SAI
        quantidade = Decimal(str(serializer.validated_data['quantidade']))

        # ================================
        # REGRAS DE VALIDAÇÃO
        # ================================
        if not produto_id and not insumo_id:
            return Response(
                {"erro": "Informe 'produto' OU 'insumo'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if produto_id and insumo_id:
            return Response(
                {"erro": "Não envie 'produto' e 'insumo' ao mesmo tempo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ================================
        # MOVIMENTAÇÃO DE PRODUTO
        # ================================
        if produto_id:
            try:
                produto = Produto.objects.get(id=produto_id.id)
            except Produto.DoesNotExist:
                return Response({"erro": "Produto não encontrado."}, status=404)

            if tipo == "ENT":
                produto.estoque_atual += quantidade

            elif tipo == "SAI":
                if quantidade > produto.estoque_atual:
                    return Response(
                        {"erro": "Saída maior que o estoque disponível."},
                        status=400
                    )
                produto.estoque_atual -= quantidade

            produto.save()

        # ================================
        # MOVIMENTAÇÃO DE INSUMO
        # ================================
        if insumo_id:
            try:
                insumo = Insumo.objects.get(id=insumo_id.id)
            except Insumo.DoesNotExist:
                return Response({"erro": "Insumo não encontrado."}, status=404)

            if tipo == "ENT":
                insumo.estoque_atual += quantidade

            elif tipo == "SAI":
                if quantidade > insumo.estoque_atual:
                    return Response(
                        {"erro": "Saída maior que o estoque disponível."},
                        status=400
                    )
                insumo.estoque_atual -= quantidade

            insumo.save()

        # ================================
        # SALVA MOVIMENTAÇÃO
        # ================================
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
