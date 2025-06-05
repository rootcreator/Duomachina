from django.urls import path
from .views import ProductListView, ProductDetailView, OrderCreateView, CommissionListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('commissions/', CommissionListView.as_view(), name='commission-list'),
]
