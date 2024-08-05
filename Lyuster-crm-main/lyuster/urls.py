from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi  # type: ignore
from drf_yasg.views import get_schema_view  # type: ignore
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lyuster.serializers import CustomTokenObtainPairSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import UserProfileSerializer
from rest_framework.exceptions import NotFound


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return user
        except User.DoesNotExist:
            raise NotFound("UserProfile does not exist for this user.")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="A sample API for learning DRF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/', include('products.urls')),
    path('api/', include('user_view.urls')),
    path('swagger/', schema_view.with_ui(  # new
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(  # new
        'redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
