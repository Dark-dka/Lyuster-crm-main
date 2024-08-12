from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartRetrieveUpdateAPIView, OrderViewSet, ClientsProductViewSet, ProductRetrieveUpdateDestroyAPIView, ProductViewSet, MahsulotlarViewSet, OrderList, ProductCreate, OrderCreate, FinancialDataAPIView


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'mahsulotlar', MahsulotlarViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'clients-product-view', ClientsProductViewSet)


urlpatterns = [

    # path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('cart/', CartRetrieveUpdateAPIView.as_view(), name='cart-detail'),



    path('', include(router.urls)),
    # path('orders/', OrderList.as_view()),
    path('create/product/', ProductCreate.as_view()),
    path('create/order/', OrderCreate.as_view()),
    path('financial-data/', FinancialDataAPIView.as_view(), name='financial-data'),
]
