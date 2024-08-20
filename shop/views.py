from django.shortcuts import render,get_object_or_404
from .models import Car

# Create your views here.

def homePage(request):
    cars = Car.objects.all()
    context = {
        'cars':cars, 
    }
    return render(request, 'shop/home.html', context)

def detail_page(request, id):
    cars = get_object_or_404(Car, id=id)
    context = {'cars': cars}
    return render(request, 'shop/detail_page.html', context)

