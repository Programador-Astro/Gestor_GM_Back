from django.db import models
from .produto import Produto
from .insumo import Insumo

class MovimentacaoEstoque(models.Model):
    TIPO_MOV = [
        ('ENT', 'Entrada'),
        ('SAI', 'Saída'),
    ]

    ORIGEM = [
        ('PRODUCAO', 'Produção'),
        ('DEVOLUCAO', 'Devolução'),
        ('AJUSTE', 'Ajuste manual'),
        ('EXPEDICAO', 'Expedição'),
        ('AVARIA', 'Avaria'),
        ('COMPRA', 'Compra de insumo'),
        ('CONSUMO', 'Consumo de insumo na produção'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True, blank=True)

    tipo = models.CharField(max_length=3, choices=TIPO_MOV)
    origem = models.CharField(max_length=20, choices=ORIGEM)

    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    criado_em = models.DateTimeField(auto_now_add=True)

    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        nome = self.produto.nome if self.produto else self.insumo.nome
        return f"{nome} - {self.tipo} - {self.quantidade}"
