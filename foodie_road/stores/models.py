from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'

class Store(models.Model):
    category = models.ForeignKey('stores.Category', on_delete=models.SET_NULL, 
                                         null=True, related_name='store')
    store_name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'

class StoreImage(models.Model):
    store = models.ForeignKey('stores.Store', on_delete=models.SET_NULL,
                                   null=True, related_name='image')
    image_urls = models.CharField(max_length=500, null=False, default=None)

    class Meta:
        db_table = 'store_images'

class StoreMenu(models.Model):
    store = models.ForeignKey('stores.Store', on_delete=models.SET_NULL,
                                   null=True, related_name='menu')
    menu_name = models.CharField(max_length=100, null=False)
    menu_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_urls = models.CharField(max_length=500, null=False, default=None)

    class Meta:
        db_table = 'store_menu'