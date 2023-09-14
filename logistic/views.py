from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .filters import ProductFilter
from .models import Product, Stock, StockProduct
from .serializers import ProductSerializer, StockSerializer, StockProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    filterset_class = ProductFilter


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['address', 'positions__product__title']


class StockProductViewSet(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockProductSerializer


class StockListView(ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        if search_query:
            return Stock.objects.filter(products__title__icontains=search_query)
        return Stock.objects.all()
