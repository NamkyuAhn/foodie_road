from django.db import models

class Order(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                                   null=True, related_name='user_order')
    store = models.ForeignKey('stores.Store', on_delete=models.SET_NULL,
                                   null=True, related_name='store_order')
    menu = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'orders'

    
