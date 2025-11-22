from rest_framework.viewsets import ModelViewSet
from estoque.models import Produto
from estoque.serializers.produto_serializer import ProdutoSerializer

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
