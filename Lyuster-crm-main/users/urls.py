from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login, CustomTokenObtainPairView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', login, name='login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
]
