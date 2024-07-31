import decimal

from rest_framework import serializers

from .models import Product, Mahsulotlar, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        # Ensure the price is a numeric value
        if not isinstance(value, (int, float, decimal.Decimal)):
            raise serializers.ValidationError("Price should be a numeric value")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = f"${instance.price:,.2f}"
        return representation


class MahsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'description', 'category', 'price', 'quantity', 'profit')
        model = Product
