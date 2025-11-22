from rest_framework import serializers
from estoque.models import Requisicao, RequisicaoItem, Insumo

class RequisicaoItemSerializer(serializers.ModelSerializer):
    insumo_nome = serializers.CharField(source='insumo.nome', read_only=True)

    class Meta:
        model = RequisicaoItem
        fields = [
            'id',
            'insumo',
            'insumo_nome',
            'quantidade_solicitada',
            'quantidade_atendida',
            'atendido',
        ]
        read_only_fields = ['quantidade_atendida', 'atendido']


class RequisicaoSerializer(serializers.ModelSerializer):
    itens = RequisicaoItemSerializer(many=True)

    class Meta:
        model = Requisicao
        fields = [
            'id',
            'setor',
            'observacao',
            'status',
            'created_at',
            'itens'
        ]
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        requisicao = Requisicao.objects.create(**validated_data)

        for item in itens_data:
            RequisicaoItem.objects.create(
                requisicao=requisicao,
                **item
            )

        return requisicao
