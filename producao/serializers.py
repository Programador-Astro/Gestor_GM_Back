from rest_framework import serializers
from producao.models import ProducaoDiaria, ItemProducaoDiaria


class ItemProducaoDiariaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)

    class Meta:
        model = ItemProducaoDiaria
        fields = [
            "id",
            "producao",
            "produto",
            "produto_nome",
            "quantidade_esperada",
            "quantidade_conferida",
            "status",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["status"]


class ProducaoDiariaSerializer(serializers.ModelSerializer):
    itens = ItemProducaoDiariaSerializer(many=True, read_only=True)

    class Meta:
        model = ProducaoDiaria
        fields = [
            "id",
            "data",
            "observacao",
            "status",
            "itens",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["status"]
