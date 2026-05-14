from django.db import migrations

def link_products(apps, schema_editor):
    GroceryItem = apps.get_model('grocery', 'GroceryItem')
    Product = apps.get_model('grocery', 'Product')
    for item in GroceryItem.objects.all():
        product, created = Product.objects.get_or_create(name=item.name)
        item.product = product
        item.save()

class Migration(migrations.Migration):
    dependencies = [
        ('grocery', '0005_groceryitem_product'),
    ]
    operations = [
        migrations.RunPython(link_products),
    ]