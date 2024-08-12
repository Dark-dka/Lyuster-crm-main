from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Cart, ClientsProductView, Product, Mahsulotlar, Order
from .permissions import IsSuperUserOrReadOnly
from .serializers import CartSerializer, ClientsProductViewSerializer, ProductSerializer, MahsulotlarSerializer, OrderSerializer, ProductCreateSerializer
import datetime
from django.utils import timezone
from django.db.models import Sum, F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated




class ClientsProductViewSet(viewsets.ModelViewSet):
    queryset = ClientsProductView.objects.all()
    serializer_class = ClientsProductViewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
        



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer = ProductSerializer

class CartRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """GET /orders/ - List all orders"""
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """GET /orders/{id}/ - Retrieve a specific order"""
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """POST /orders/ - Create a new order"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
    # Save the order and associate it with the current user
        order = serializer.save(user=self.request.user)
        
        # Update the sold quantity for each product in the order
        for order_product in order.orderproduct_set.all():
            product = order_product.product
            product.sold_quantity += order_product.quantity
            product.save()
            
    





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


class FinancialDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now()

        # Общая прибыль
        total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

        # Месячный доход за прошлый месяц
        first_day_of_current_month = today.replace(day=1)
        first_day_of_last_month = (first_day_of_current_month - datetime.timedelta(days=1)).replace(day=1)
        last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)

        last_month_revenue = Order.objects.filter(
            sold_date__range=[first_day_of_last_month, last_day_of_last_month]
        ).aggregate(total=Sum('total_price'))['total'] or 0

        # Месячная чистая прибыль
        last_month_orders = Order.objects.filter(
            sold_date__range=[first_day_of_last_month, last_day_of_last_month]
        )

        last_month_profit = last_month_orders.annotate(
            profit_per_order=F('sold_quantity') * (F('total_price') - F('product__price'))
        ).aggregate(total=Sum('profit_per_order'))['total'] or 0

        # Общая чистая прибыль
        total_profit = Order.objects.annotate(
            profit_per_order=F('sold_quantity') * (F('total_price') - F('product__price'))
        ).aggregate(total=Sum('profit_per_order'))['total'] or 0

        # Разница прибыли между прошлым и позапрошлым месяцами
        first_day_of_two_months_ago = (first_day_of_last_month - datetime.timedelta(days=1)).replace(day=1)
        last_day_of_two_months_ago = first_day_of_last_month - datetime.timedelta(days=1)

        two_months_ago_profit = Order.objects.filter(
            sold_date__range=[first_day_of_two_months_ago, last_day_of_two_months_ago]
        ).annotate(
            profit_per_order=F('sold_quantity') * (F('total_price') - F('product__price'))
        ).aggregate(total=Sum('profit_per_order'))['total'] or 0

        profit_difference = last_month_profit - two_months_ago_profit

        # Количество продуктов
        product_count = Product.objects.count()

        data = {
            'total_revenue': total_revenue,
            'last_month_revenue': last_month_revenue,
            'last_month_profit': last_month_profit,
            'total_profit': total_profit,
            'profit_difference': profit_difference,
            'product_count': product_count,
        }
        return Response(data, status=status.HTTP_200_OK)
