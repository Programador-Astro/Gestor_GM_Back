from rest_framework import serializers

class EntradaMultiplaItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2)


class EntradaMultiplaSerializer(serializers.Serializer):
    nf_numero = serializers.CharField()
    insumos = EntradaMultiplaItemSerializer(many=True)

    def validate(self, data):
        if not data["nf_numero"]:
            raise serializers.ValidationError("Número da NF é obrigatório.")

        if len(data["insumos"]) == 0:
            raise serializers.ValidationError("Nenhum insumo enviado.")

        return data
