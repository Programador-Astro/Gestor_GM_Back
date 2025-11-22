from rest_framework.viewsets import ModelViewSet
from estoque.models import Insumo
from estoque.serializers.insumo_serializer import InsumoSerializer

class InsumoViewSet(ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
