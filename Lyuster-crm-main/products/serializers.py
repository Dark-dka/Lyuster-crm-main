import decimal

from rest_framework import serializers

from user_view.serializers import UserSerializer


from .models import Cart, CartItem, ClientsProductView, OrderItem, OrderProduct, Product, Mahsulotlar, Order








class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = ['user', 'created_at', 'updated_at', 'total_price', 'status', 'items']






class ClientsProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientsProductView
        fields = '__all__'




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
        print(f"Product instance: {instance.__dict__}")
        print(f"Category field value: {instance.category}")
        representation['price'] = f"{instance.price:,.2f}"
        return representation





class MahsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']
        

class OrderSerializer(serializers.ModelSerializer):
    orderproduct_set = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('orderproduct_set')
        order = Order.objects.create(**validated_data)

        for product_data in products_data:
            product = product_data['product']  # This is an ID now
            quantity = product_data['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

            # Update the sold quantity of the product
            product_obj = Product.objects.get(id=product)
            product_obj.sold_quantity += quantity
            product_obj.save()

        return order

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product
