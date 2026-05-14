from django.urls import path
from grocery import views


urlpatterns=[
        path('', views.homepage),
        path('lists/<int:id>/', views.list_detail, name='list_detail'),
        path('items/<int:id>/toggle/', views.toggle_item, name='toggle_item'),
        path('register/', views.register, name='register'),
        path('create-list/', views.create_list, name='create_list'),
        path('lists/<int:id>/add-item/', views.add_item, name='add_item'),
        path('lists/<int:id>/filter/', views.filter_items, name='filter_items'),
        path('recipes/<int:id>/ingredients/',views.recipe_ingredients, name='recipe_ingredients'),
        path('create-recipe/', views.create_recipe, name='create_recipe'),
        path('recipes/<int:id>/add-ingredient/',views.add_ingredient, name='add_ingredient'),
        path('inventory/',views.inventory, name='inventory'),
        path('items/<int:id>/delete/', views.delete_item, name='delete_item'),
        path('items/<int:id>/use/',views.use_item,name='use_item'),
        path('items/<int:id>/edit/',views.edit_item,name='edit_item'),
    
]