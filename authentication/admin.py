from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "setor", "cargo")
    list_filter = ("setor", "cargo")
    search_fields = ("user__username", "user__email")

admin.site.register(Perfil, PerfilAdmin)
