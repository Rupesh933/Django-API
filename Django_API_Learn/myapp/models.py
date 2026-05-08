from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # blank=True allows the field to be optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # delete product if category deleted
        related_name='products'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # automatically set the field to now when the object is first created
    updated_at = models.DateTimeField(auto_now=True)  # automatically set the field to now every time the object is saved

    def __str__(self):
        return f'{self.name} - ({self.stock})'
    
    class Meta:
        ordering = ['-created_at']
