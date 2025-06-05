from rest_framework import serializers
from .models import Product, Order, OrderItem, Commission
from users.models import User

class ProductSerializer(serializers.ModelSerializer):
    artist_username = serializers.CharField(source='artist.username', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'product_type', 'artist', 'artist_username', 'created_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'user_username', 'total_price', 'is_paid', 'created_at', 'items')

class CommissionSerializer(serializers.ModelSerializer):
    artist_username = serializers.CharField(source='artist.username', read_only=True)

    class Meta:
        model = Commission
        fields = ('id', 'artist', 'artist_username', 'order_item', 'amount', 'created_at')
