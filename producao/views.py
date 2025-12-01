from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from producao.models import ProducaoDiaria, ItemProducaoDiaria
from producao.serializers import ProducaoDiariaSerializer, ItemProducaoDiariaSerializer


from producao.models import ProducaoDiaria
from producao.services.finalizar_producao import finalizar_producao



class ProducaoDiariaViewSet(viewsets.ModelViewSet):
    queryset = ProducaoDiaria.objects.all().order_by("-data")
    serializer_class = ProducaoDiariaSerializer


class ItemProducaoDiariaViewSet(viewsets.ModelViewSet):
    queryset = ItemProducaoDiaria.objects.all()
    serializer_class = ItemProducaoDiariaSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        
        # 🔥 BLOQUEIA EDIÇÃO SE PRODUÇÃO FINALIZADA
        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível editar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()

        # 🔥 BLOQUEIA PATCH TAMBÉM
        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível editar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()

        # 🔥 BLOQUEIA DELETE
        if item.producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível remover itens."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        producao_id = request.data.get("producao")
        from producao.models import ProducaoDiaria

        producao = ProducaoDiaria.objects.get(pk=producao_id)

        # 🔥 BLOQUEIA CRIAÇÃO DE NOVO ITEM
        if producao.status == "FINALIZADO":
            return Response(
                {"erro": "Produção finalizada. Não é possível adicionar itens."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

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