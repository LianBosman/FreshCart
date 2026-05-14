from django import forms

from .models import GroceryList, GroceryItem, Product, Recipe,RecipeIngredients,UNIT_CHOICES

class GroceryListForm(forms.ModelForm):
    class Meta:
        model=GroceryList
        fields=['name']

class GroceryItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False, label='Existing Product')
    new_product_name = forms.CharField(required=False, label='New Product Name')
    new_product_category = forms.CharField(required=False, label='New Product Category')
    new_product_store = forms.CharField(required=False, label='Available Store')
    quantity = forms.DecimalField(max_digits=6, decimal_places=2)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        new_name = cleaned_data.get('new_product_name')
        if not product and not new_name:
            raise forms.ValidationError('Please select an existing product or enter a new product name.')
        return cleaned_data

    class Meta:
        model = GroceryItem
        fields = ['product']

class RecipeForm(forms.ModelForm):
    
    class Meta:
        model=Recipe
        fields=['name','description']

class RecipeIngredientForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False, label='Existing Product')
    new_product_name = forms.CharField(required=False, label='New Product Name')
    new_product_category = forms.CharField(required=False, label='New Product Category')
    new_product_store = forms.CharField(required=False, label='Available Store')
    quantity = forms.DecimalField(max_digits=6, decimal_places=2)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        new_name = cleaned_data.get('new_product_name')
        if not product and not new_name:
            raise forms.ValidationError('Please select an existing product or enter a new product name.')
        return cleaned_data

    class Meta:
        model = RecipeIngredients
        fields = ['product', 'quantity', 'unit']

class UseItemForm(forms.Form):
    quantity_used=forms.DecimalField(max_digits=6, decimal_places=2)

class EditItemForm(forms.Form):
    product=forms.CharField(label=' Edit Product Name')
    quantity=forms.DecimalField(max_digits=6, decimal_places=2, label='Edit quantity')
    unit=forms.ChoiceField(choices=UNIT_CHOICES, label='Edit unit')
