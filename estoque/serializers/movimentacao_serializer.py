from rest_framework import serializers
from estoque.models import MovimentacaoEstoque


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentacaoEstoque
        fields = '__all__'
