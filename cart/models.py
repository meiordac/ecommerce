from __future__ import unicode_literals

from django.db import models
from catalog.models import Product

class CartItem(models.Model):
    """
    Corresponds to one type of item in the Cart
    """
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False)
    cart_session = models.CharField(default='', max_length=50)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def total(self):
        """ Total returns the total value of the item in the Cart
        """
        return self.quantity*self.product.price
    def name(self):
        """ Name returns the name of the item """
        return self.product.name
    def price(self):
        """ Price returns the price of this particular item """
        return self.product.price
    def augment_quantity(self, quantity):
        """ Adds one to the quantity of products """
        self.quantity = self.quantity+int(quantity)
        self.save()
