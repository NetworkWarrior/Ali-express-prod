from django.urls import path
from .views import ProductListView, ProductDetailView, ProductPaymentView, SellProductListView, CheckoutView, DeleteProductView, DeleteProductReviewView, EditProductReviewView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('checkout/<int:id>/', CheckoutView.as_view(), name='checkout_payment'),
    path('payment/', ProductPaymentView.as_view(), name='product_payment'),
    path('sell/', SellProductListView.as_view(), name='product_sell'),
    path('delete/<int:id>/', DeleteProductView.as_view(), name='product_delete'),
    path('review/delete/<int:id>/', DeleteProductReviewView.as_view(), name='review_delete'),
    path('review/edit/<int:id>/', EditProductReviewView.as_view(), name='review_edit'),
]

