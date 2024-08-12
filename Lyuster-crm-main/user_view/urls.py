from django.urls import path, include
from .views import UserListView
from rest_framework.routers import DefaultRouter
from users.views import ClientUserViewSet

router = DefaultRouter()
router.register(r'client-users', ClientUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='user-list'),
]
