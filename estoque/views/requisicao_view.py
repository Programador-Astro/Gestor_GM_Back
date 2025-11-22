from rest_framework.viewsets import ModelViewSet
from estoque.models import Requisicao
from estoque.serializers.requisicao_serializer import RequisicaoSerializer

class RequisicaoViewSet(ModelViewSet):
    queryset = Requisicao.objects.all().prefetch_related("itens__insumo")
    serializer_class = RequisicaoSerializer
