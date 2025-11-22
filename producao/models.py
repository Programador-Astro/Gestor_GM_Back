from django.db import models
from estoque.models.produto import Produto


class ProducaoDiaria(models.Model):
    STATUS_CHOICES = [
        ("RASCUNHO", "Rascunho"),
        ("AGUARDANDO_CONF", "Aguardando Conferência"),
        ("CONFERIDO", "Conferido"),
        ("FINALIZADO", "Finalizado"),
    ]

    data = models.DateField()
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="RASCUNHO")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Produção {self.data} - {self.status}"


class ItemProducaoDiaria(models.Model):
    STATUS_ITEM = [
        ("PENDENTE", "Pendente"),
        ("AGUARDANDO_CONF", "Aguardando Conferência"),
        ("DIVERGENTE", "Divergente"),
        ("OK", "Conferido"),
    ]

    producao = models.ForeignKey(ProducaoDiaria, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    quantidade_esperada = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_conferida = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_ITEM, default="PENDENTE")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def diferenca(self):
        return self.quantidade_conferida - self.quantidade_esperada

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade_esperada}u"
