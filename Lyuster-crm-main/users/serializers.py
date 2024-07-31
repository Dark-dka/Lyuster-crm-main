from rest_framework import serializers

from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'status', 'role', 'country',
            'languages_known', 'phone_number', 'telegram', 'email', 'location'  # Yangi location maydoni
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'date_joined', 'profile']
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
        profile.location = profile_data.get('location', profile.location)  # Yangi location maydoni
        profile.save()

        return instance
