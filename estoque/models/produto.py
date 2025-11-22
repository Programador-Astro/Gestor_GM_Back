from django.db import models
import uuid


class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=120)

    codigo_barras = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="EAN-13 ou outro código válido"
    )

    unidade_medida = models.CharField(max_length=20)  # Ex: 10L, 1L, 500ml
    categoria = models.CharField(max_length=50)       # Açaí, Creme, etc

    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ativo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
