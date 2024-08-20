from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Car
from django.http import HttpResponse
from .models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, car_id):
    car = Car.objects.get(id = car_id)
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(car=car, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            car = car,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
   
   
    return redirect('cart:cart')


def cart(request,total=0, quantity=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.car.price * cart_item.quantity)
            quantity += cart_item.quantity
    except CartItem.DoesNotExist:
          pass
    context = {
        'cart':cart,
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity
    }

    return render(request, 'cart/cart.html',context)

def remove_cart_item(request,cart_id):
    cart_item = get_object_or_404(CartItem,id=cart_id)
    cart_item.delete()
    return redirect('cart:cart')
    
