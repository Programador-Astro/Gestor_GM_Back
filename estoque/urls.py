from rest_framework.routers import DefaultRouter
from estoque.views.produto_view import ProdutoViewSet
from estoque.views.insumo_view import InsumoViewSet
from estoque.views.movimentacao_view import MovimentacaoEstoqueViewSet
from estoque.views.requisicao_view import RequisicaoViewSet

router = DefaultRouter()

router.register('produtos', ProdutoViewSet)
router.register('insumos', InsumoViewSet)
router.register('movimentacoes', MovimentacaoEstoqueViewSet)
router.register('requisicoes', RequisicaoViewSet)

urlpatterns = router.urls
