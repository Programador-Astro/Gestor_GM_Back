from django.db import models
from django.utils import timezone

class Requisicao(models.Model):
    STATUS_CHOICES = (
        ('SOLICITADO', 'Solicitado'),
        ('PARCIAL', 'Atendido Parcialmente'),
        ('ATENDIDO', 'Atendido'),
        ('CANCELADO', 'Cancelado'),
    )

    setor = models.CharField(max_length=50, default="PRODUCAO")  # Quem pediu
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SOLICITADO')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Requisição #{self.id} - {self.status}"


class RequisicaoItem(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE, related_name="itens")
    insumo = models.ForeignKey('estoque.Insumo', on_delete=models.PROTECT)

    quantidade_solicitada = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_atendida = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    atendido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.insumo.nome} - {self.quantidade_solicitada}"
