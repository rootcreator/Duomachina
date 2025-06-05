from rest_framework import generics
from .models import Product, Order, OrderItem, Commission
from .serializers import ProductSerializer, OrderSerializer, CommissionSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        total_price = sum(item['price'] * item['quantity'] for item in self.request.data['items'])
        order = serializer.save(user=self.request.user, total_price=total_price)
        
        # Create order items
        for item in self.request.data['items']:
            product = Product.objects.get(id=item['product'])
            OrderItem.objects.create(
                order=order, 
                product=product, 
                quantity=item['quantity'], 
                price=item['price']
            )
            
            # Calculate commissions for artists
            commission_amount = product.price * 0.1  # Example: 10% commission
            Commission.objects.create(
                artist=product.artist,
                order_item=order.items.last(),
                amount=commission_amount
            )

class CommissionListView(generics.ListAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
