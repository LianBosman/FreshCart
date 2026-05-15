from django.shortcuts import render, redirect
from .models import GroceryList, GroceryItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import GroceryListForm, GroceryItemForm,RecipeForm, RecipeIngredientForm, UseItemForm, EditItemForm
from .models import GroceryList, GroceryItem, Product,Recipe,RecipeIngredients
from django.contrib import messages
from django.http import HttpResponse

@login_required
def homepage(request):
    lists = GroceryList.objects.filter(is_recipe_list=False)
    recipe = Recipe.objects.all()
    inventory = GroceryItem.objects.filter(bought=True, used=False, grocery_list__is_recipe_list=False)
    return render(request, 'grocery/homepage.html', {'lists': lists, 'recipe': recipe, 'inventory': inventory})

@login_required
def list_detail(request, id):
    grocery_list= GroceryList.objects.get(id=id)
    items=GroceryItem.objects.filter(grocery_list=grocery_list).order_by('bought', '-date_added')
    stores=items.values_list('store',flat=True).distinct().exclude(store='')    
    return render(request, 'grocery/list_detail.html',{'grocery_list':grocery_list,'items':items, 'stores':stores} )

@login_required
def toggle_item(request, id):
    grocery_item= GroceryItem.objects.get(id=id)
    grocery_item.bought= not grocery_item.bought

    if grocery_item.bought:
        grocery_item.remaining_quantity = grocery_item.quantity
    
    else:
        grocery_item.remaining_quantity = None
    
    grocery_item.save()
    return render(request, 'grocery/item.html',{'grocery_item': grocery_item})


def register(request):
    if(request.method=='POST'):
        form= UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            
            return redirect('/accounts/login/')
    else:
        form= UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})

@login_required
def create_list(request):
    if(request.method=='POST'):
         form= GroceryListForm(request.POST)
         if(form.is_valid()):
                grocery_list= form.save(commit=False)
                grocery_list.created_by= request.user
                grocery_list.save()
                return redirect('/')
    else:
        form= GroceryListForm()
    return render(request, 'grocery/create_list.html', {'form':form})

@login_required
def add_item(request, id):
    grocery_list = GroceryList.objects.get(id=id)
    if request.method == 'POST':
        form = GroceryItemForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_product_name')
            new_category = form.cleaned_data.get('new_product_category')
            new_store = form.cleaned_data.get('new_product_store')
            quantity = form.cleaned_data.get('quantity')
            unit = form.cleaned_data.get('unit')
            if new_name:
                product, created = Product.objects.get_or_create(
                    name=new_name,
                    defaults={'category': new_category}
                )
            else:
                product = form.cleaned_data.get('product')
            existing_item = GroceryItem.objects.filter(
                grocery_list=grocery_list,
                product=product
            ).first()
            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                item = GroceryItem(grocery_list=grocery_list, product=product, store=new_store, quantity=quantity, unit=unit)
                item.save()
            return redirect('list_detail', id=grocery_list.id)
    else:
        form = GroceryItemForm()
    return render(request, 'grocery/add_item.html', {'form': form, 'grocery_list': grocery_list})

@login_required
def filter_items(request, id):
    grocery_list= GroceryList.objects.get(id=id)
    items= GroceryItem.objects.filter(grocery_list= grocery_list).order_by('bought', '-date_added')
    store=request.GET.get('store')
    filter= request.GET.get('filter')

    if store:
        items=items.filter(store=store)

    if(filter=='bought'):
        items= items.filter(bought=True)
        
    elif(filter=='unbought'):
        items=items.filter(bought=False)
        
    items=items.order_by('-date_added')
    return render(request,'grocery/item_list.html', {'items':items})

@login_required
def recipe_ingredients(request, id):
    recipe=Recipe.objects.get(id=id)
    recipeingredients=RecipeIngredients.objects.filter(recipe=recipe)
    print(recipeingredients)

    return render(request, 'grocery/recipe_ingredients.html',{'recipe':recipe, 'recipeingredients':recipeingredients}) 


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            grocery_list = GroceryList.objects.create(
                name=f"{recipe.name} ingredients",
                created_by=request.user,
                is_recipe_list=True
            )
            recipe.grocery_list = grocery_list
            recipe.save()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'grocery/create_recipe.html', {'form': form})

@login_required
def add_ingredient(request, id):
    recipe = Recipe.objects.get(id=id)
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_product_name')
            new_category = form.cleaned_data.get('new_product_category')
            new_store = form.cleaned_data.get('new_product_store')
            quantity = form.cleaned_data.get('quantity')
            unit = form.cleaned_data.get('unit')
            if new_name:
                product, created = Product.objects.get_or_create(
                    name=new_name,
                    defaults={'category': new_category}
                )
            else:
                product = form.cleaned_data.get('product')
            existing_ingredient = RecipeIngredients.objects.filter(
                recipe=recipe,
                product=product
            ).first()
            if existing_ingredient:
                existing_ingredient.quantity += quantity
                existing_ingredient.save()
            else:
                ingredient = form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.product = product
                ingredient.save()
            if recipe.grocery_list:
                existing_item = GroceryItem.objects.filter(
                    grocery_list=recipe.grocery_list,
                    product=product
                ).first()
                if existing_item:
                    existing_item.quantity += quantity
                    existing_item.save()
                else:
                    GroceryItem.objects.create(
                        grocery_list=recipe.grocery_list,
                        product=product,
                        quantity=quantity,
                        unit=unit
                    )
            return redirect('/')
    else:
        form = RecipeIngredientForm()
    return render(request, 'grocery/add_ingredient.html', {'form': form, 'recipe': recipe})

@login_required
def inventory(request):
    items=GroceryItem.objects.filter(bought=True, used=False)
    return render(request, 'grocery/inventory.html', {'items':items})

@login_required
def delete_item(request, id):
    item = GroceryItem.objects.get(id=id)
    item.delete()
    inventory = GroceryItem.objects.filter(bought=True, used=False)
    return render(request, 'grocery/inventory.html', {'inventory': inventory})
@login_required
def use_item(request, id):
    item = GroceryItem.objects.get(id=id)
    if request.method == 'POST':
        form = UseItemForm(request.POST)
        if form.is_valid():
            quantity_used = form.cleaned_data.get('quantity_used')
            
            # unit conversion for remaining
            remaining_qty = item.remaining_quantity
            if item.unit == 'kg' and quantity_used:
                remaining_qty = remaining_qty * 1000
                quantity_used_converted = quantity_used
            else:
                quantity_used_converted = quantity_used
            
            remaining = remaining_qty - quantity_used_converted
            
            if item.unit == 'kg':
                remaining = remaining / 1000

            if remaining <= 0:
                if item.grocery_list.is_recipe_list:
                    # reset for recipe items
                    item.bought = False
                    item.remaining_quantity = None
                    item.save()
                else:
                    item.delete()
            else:
                
                print(f"quantity: {item.quantity}")
                print(f"remaining: {remaining}")
                item.remaining_quantity = remaining
                item.save()

            inventory = GroceryItem.objects.filter(bought=True, used=False, grocery_list__is_recipe_list=False)
            return render(request, 'grocery/inventory.html', {'inventory': inventory})
    else:
        form = UseItemForm()
    return render(request, 'grocery/use_item.html', {'form': form, 'item': item})


@login_required
def inventory_partial(request):
    inventory = GroceryItem.objects.filter(bought=True, used=False)
    return render(request, 'grocery/inventory.html', {'inventory': inventory})

@login_required
def edit_item(request, id):
    item = GroceryItem.objects.get(id=id)
    if request.method == 'POST':
        form = EditItemForm(request.POST)
        if form.is_valid():
            item.product.name = form.cleaned_data.get('product')
            item.product.save()
            item.quantity = form.cleaned_data.get('quantity')
            item.unit = form.cleaned_data.get('unit')
            item.save()
            return render(request, 'grocery/item.html', {'grocery_item': item})
    else:
        form = EditItemForm(initial={
            'product': item.product.name,
            'quantity': item.quantity,
            'unit': item.unit
        })
    return render(request, 'grocery/edit_item.html', {'form': form, 'item': item})

