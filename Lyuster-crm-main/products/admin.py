from django.contrib import admin
from .models import Product, Mahsulotlar, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'price', 'quantity', 'profit')
    search_fields = ('name', 'description')
    list_filter = ('category', 'price')



@admin.register(Mahsulotlar)
class MahsulotlarAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'Received', 'Remainder')
    search_fields = ('title',)
    list_filter = ('price',)


@admin.register(Order)
class MahsulotlarAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'sold_quantity', 'total_price', 'initial_quantity', 'left_quantity', 'sold_date')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')
