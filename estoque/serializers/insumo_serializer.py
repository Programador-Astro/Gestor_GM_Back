from rest_framework import serializers
from estoque.models import Insumo

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'
