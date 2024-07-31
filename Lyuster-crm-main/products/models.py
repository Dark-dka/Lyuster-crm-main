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
    CATEGORY_CHOICES = [
        ('Accessories', 'Accessories'),
        ('Clothing', 'Clothing'),
        ('Electronics', 'Electronics'),
        ('Fitness', 'Fitness'),
    ]
    # image = models.ImageField(upload_to='products/', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    sold_quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    initial_quantity = models.IntegerField()
    left_quantity = models.PositiveIntegerField()
    sold_date = models.DateField(default=timezone.now)
