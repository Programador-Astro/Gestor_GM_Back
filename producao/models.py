from django.db import models
from estoque.models.produto import Produto
from estoque.models.insumo import Insumo

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
    quantidade_conferida_producao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_conferida_camara = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_ITEM, default="PENDENTE")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def diferenca(self):
        return self.quantidade_conferida - self.quantidade_esperada

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade_esperada}u"

class InsumoProducao(models.Model):
    STATUS = [
        ("PENDENTE", "Pendente"),
        ("PARCIAL", "Parcial"),
        ("COMPLETO", "Completo"),
    ]

    producao = models.ForeignKey(ProducaoDiaria, on_delete=models.CASCADE, related_name="insumos")
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)

    quantidade_necessaria = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_recebida = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS, default="PENDENTE")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    # 🔥 LÓGICA DE MUDANÇA AUTOMÁTICA DE STATUS
    def atualizar_status(self):
        # COMPLETO: recebeu tudo que precisava (>= necessário e necessário > 0)
        if self.quantidade_recebida >= self.quantidade_necessaria and self.quantidade_necessaria > 0:
            self.status = "COMPLETO"

        # PARCIAL: recebeu > 0, mas menos que o necessário
        elif self.quantidade_recebida > 0:
            self.status = "PARCIAL"

        # PENDENTE: não recebeu nada
        else:
            self.status = "PENDENTE"

    def save(self, *args, **kwargs):
        self.atualizar_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.insumo.nome} - {self.quantidade_necessaria}u"
