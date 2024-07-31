from rest_framework import generics
from rest_framework import viewsets

from .models import Product, Mahsulotlar, Order
from .permissions import IsSuperUserOrReadOnly
from .serializers import ProductSerializer, MahsulotlarSerializer, OrderSerializer, ProductCreateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class MahsulotlarViewSet(viewsets.ModelViewSet):
    queryset = Mahsulotlar.objects.all()
    serializer_class = MahsulotlarSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['product', 'user']


class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

