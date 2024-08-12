from rest_framework import viewsets, status, generics, permissions
from .models import ClientUser, User
from .serializers import ClientUserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ClientUserViewSet(viewsets.ModelViewSet):

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()



class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
