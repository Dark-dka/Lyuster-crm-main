from rest_framework import serializers
from .models import ClientUser, User, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_staff'] = self.user.is_staff
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'status', 'role', 'country', 'date_joined',
            'languages_known', 'phone_number', 'telegram', 'email', 'location'
        ]


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'date_joined', 'email',
            'first_name', 'last_name', 'role', 'phone_number',
            'is_active', 'is_staff', 'groups', 'user_permissions', 'profile'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.groups.set(validated_data.get('groups', instance.groups.all()))
        instance.user_permissions.set(validated_data.get('user_permissions', instance.user_permissions.all()))
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.status = profile_data.get('status', profile.status)
        profile.role = profile_data.get('role', profile.role)
        profile.country = profile_data.get('country', profile.country)
        profile.languages_known = profile_data.get('languages_known', profile.languages_known)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.telegram = profile_data.get('telegram', profile.telegram)
        profile.email = profile_data.get('email', profile.email)
        profile.location = profile_data.get('location', profile.location)
        profile.save()

        return instance
