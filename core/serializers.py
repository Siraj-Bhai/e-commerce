from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem

User = get_user_model()

# User Registration Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_seller', 'is_buyer']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_seller=validated_data.get('is_seller', False),
            is_buyer=validated_data.get('is_buyer', False),
        )
        return user


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'seller']


# OrderItem Serializer (nested in Order)
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'order_date', 'status', 'items']


# Order Create Serializer
class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Order
        fields = ['items']

    def create(self, validated_data):
        buyer = self.context['request'].user
        items_data = validated_data.pop('items')
        order = Order.objects.create(buyer=buyer)

        for item in items_data:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']

            # Ensure there's enough stock available
            if product.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")

            # Create the OrderItem
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price * quantity
            )

            # Optionally update stock
            product.stock -= quantity
            product.save()

        order.refresh_from_db()
        return order