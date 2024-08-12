from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_joined = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    languages_known = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}" 



class ClientUser(models.Model):

    first_name = models.CharField(max_length=222)
    last_name = models.CharField(max_length=222)
    image = models.ImageField(upload_to="clients/image/")
    phone_number = models.CharField(max_length=13)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Client: {self.first_name}"
    
    