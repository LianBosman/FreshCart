from django.db import models
from django.contrib.auth.models import User




class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200, blank=True)
    

    def __str__(self):
        return self.name
        
UNIT_CHOICES=[
    ('g','Grams'),
    ('kg','Kilograms'),
    ('l','Litres'),
    ('units','Units ')
]

class GroceryList(models.Model):
    name=models.CharField(max_length=200)
    date_created=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_recipe_list=models.BooleanField(default=False)
    
    def __str__(self): 
        return self.name

class GroceryItem(models.Model):
    bought=models.BooleanField(default=False)
    grocery_list=models.ForeignKey(GroceryList, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    store=models.CharField(max_length=200, blank=True)
    quantity=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit=models.CharField(choices=UNIT_CHOICES, max_length=10, null=True, blank=True)
    used=models.BooleanField(default=False)
    remaining_quantity=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.product.name if self.product else 'Unknown'



class Recipe(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    grocery_list=models.OneToOneField(GroceryList, null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=6, decimal_places=2)
    unit=models.CharField(choices=UNIT_CHOICES, max_length=10)

    def __str__(self):
        return self.product.name if self.product else 'Unknown'