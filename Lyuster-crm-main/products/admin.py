from django.contrib import admin
from .models import Cart, CartItem, ClientsProductView, OrderItem, Product, Mahsulotlar, Order



@admin.register(ClientsProductView)
class ClientsProductViewAdmin(admin.ModelAdmin):
    list_display = ('client_user', 'sale_date', 'seller_user', 'products')
    search_fields = ('client_user__first_name', 'client_user__last_name', 'seller_user__username', 'products__name')
    list_filter = ('sale_date', 'seller_user')

    autocomplete_fields = ['client_user', 'seller_user', 'products']
    

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


# @admin.register(Order)
class MahsulotlarAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'sold_quantity', 'total_price', 'initial_quantity', 'left_quantity', 'sold_date')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')





# Maniki
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'inventory_status', 'rating', 'sold_quantity')
    search_fields = ('name', 'category', 'code')
    list_filter = ('category', 'inventory_status')
    ordering = ('name',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'total_price', 'status')
    search_fields = ('user__username',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
