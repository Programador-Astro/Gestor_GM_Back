from django.shortcuts import render

from rest_framework import generics
from .models import Produto, MovimentoEstoque
from .serializers import ProdutoSerializer, MovimentoEstoqueSerializer

class ProdutoListCreateView(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class ProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class MovimentoEstoqueListCreateView(generics.ListCreateAPIView):
    queryset = MovimentoEstoque.objects.all().order_by("-created_at")
    serializer_class = MovimentoEstoqueSerializer
