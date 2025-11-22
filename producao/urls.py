from rest_framework.routers import DefaultRouter
from producao.views import ProducaoDiariaViewSet, ItemProducaoDiariaViewSet
from django.urls import path, include
from .views import finalizar_producao_view

router = DefaultRouter()
router.register(r'producao', ProducaoDiariaViewSet)
router.register(r'producao-itens', ItemProducaoDiariaViewSet, basename='producao-itens')

urlpatterns = [
    path("producao/<int:pk>/finalizar/", finalizar_producao_view),
    path("", include(router.urls)),
]
