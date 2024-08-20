from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.homePage, name='home'),
    path('cars/<int:id>/', views.detail_page, name='car_detail')
]