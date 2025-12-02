from rest_framework.routers import DefaultRouter
from estoque.views.produto_view import ProdutoViewSet
from estoque.views.insumo_view import InsumoViewSet
from estoque.views.movimentacao_view import MovimentacaoEstoqueViewSet
from estoque.views.requisicao_view import RequisicaoViewSet
from estoque.views.entrada_view import EntradaMultiplaEstoqueViewSet

router = DefaultRouter()

router.register('produtos', ProdutoViewSet)
router.register('insumos', InsumoViewSet)
router.register('movimentacoes', MovimentacaoEstoqueViewSet)
router.register('requisicoes', RequisicaoViewSet)
router.register('entrada', EntradaMultiplaEstoqueViewSet, basename='entrada')

urlpatterns = router.urls
