from django.db import models

class Insumo(models.Model):
    TIPO_CHOICES = [
        ('MP', 'Matéria-prima'),
        ('EMB', 'Embalagem'),
        ('ING', 'Ingrediente'),
        ('OUT', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=30, unique=True)
    unidade_medida = models.CharField(max_length=20)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)

    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.unidade_medida})"
