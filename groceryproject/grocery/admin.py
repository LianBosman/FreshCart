from django.contrib import admin
from .models import GroceryList, GroceryItem, Product, Recipe, RecipeIngredients

admin.site.register(GroceryList)
admin.site.register(GroceryItem)
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)