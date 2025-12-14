from rest_framework import serializers
from producao.models import ProducaoDiaria, ItemProducaoDiaria, InsumoProducao
from estoque.models.insumo import Insumo


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
            "quantidade_conferida_producao",
            "quantidade_conferida_camara",
            "status",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["status"]


class InsumoProducaoSerializer(serializers.ModelSerializer):
    insumo_nome = serializers.CharField(source="insumo.nome", read_only=True)

    class Meta:
        model = InsumoProducao
        fields = [
            "id",
            "producao",
            "insumo",
            "insumo_nome",
            "quantidade_necessaria",
            "quantidade_recebida",
            "status",
            "criado_em",
            "atualizado_em",
        ]


class ProducaoDiariaSerializer(serializers.ModelSerializer):
    itens = ItemProducaoDiariaSerializer(many=True, read_only=True)
    insumos = InsumoProducaoSerializer(many=True, read_only=True)

    class Meta:
        model = ProducaoDiaria
        fields = [
            "id",
            "data",
            "observacao",
            "status",
            "itens",
            "insumos",   # <-- AGORA RETORNA A LISTA DE INSUMOS DA PRODUÇÃO
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["status"]
