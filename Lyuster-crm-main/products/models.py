from django.db import models
from django.utils import timezone

from users.models import User


class Mahsulotlar(models.Model):
    image = models.ImageField(upload_to='mahsulotlar/')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Received = models.PositiveIntegerField(verbose_name='Поступлено')
    Remainder = models.PositiveIntegerField(verbose_name='Остаток')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class Product(models.Model):
    image = models.ImageField(upload_to='products/', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    uzs_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField() # количество 
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=100, unique=True)
    inventory_status = models.BooleanField(default=True)
    rating = models.IntegerField()
    sold_quantity = models.IntegerField(default=0) # проданное количество
    cost_price = models.DecimalField(max_digits=10, decimal_places=5) # sebestoimost

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='OrderProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id} - Product {self.product.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    