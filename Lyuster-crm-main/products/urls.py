from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, MahsulotlarViewSet, OrderList, ProductCreate, OrderCreate

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'mahsulotlar', MahsulotlarViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderList.as_view()),
    path('create/product/', ProductCreate.as_view()),
    path('create/order/', OrderCreate.as_view()),
]
