from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Car(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='car_images', blank=True)
    description = models.TextField()
    fuel_type = models.CharField(max_length=50,
                                 choices=[('petrol','Petrol'),
                                          ('electric','Electric')])
    condition = models.CharField(max_length=50, choices=[('new', 'New'), ('used', 'Used')])

    def __str__(self):
        return f"{self.make} {self.model} - {self.year}"
    


