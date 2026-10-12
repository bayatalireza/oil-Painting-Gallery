from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:artwork_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/address/', views.checkout_address, name='checkout_address'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/confirm/', views.checkout_confirm, name='checkout_confirm'),
    path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),

]
