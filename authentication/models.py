
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    SETORES = [
        ("PRODUCAO", "Produção"),
        ("ESTOQUE", "Estoque"),
        ("CAMARA", "Câmara Fria"),
        ("ADM", "Administração"),
    ]
    CARGOS = [
            ("GERENTE", "Gerente"),
            ("GESTOR", "Gestor"),
            ("OPERADOR", "Operador Camara-Fria"),
            ("CONFERENTE", "Conferente"),
            ("PRODUTOR", "Produtor"),
            ("ADM", "Administrador(a)"),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    setor = models.CharField(max_length=20, choices=SETORES)
    cargo = models.CharField(max_length=20, choices=CARGOS)
    def __str__(self):
        return f"{self.user.username} - {self.setor}"
