from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:car_id>/', views.add_cart, name='add_cart'),
    path('delete_item/<int:cart_id>/', views.remove_cart_item, name='delete_cart_item')
]