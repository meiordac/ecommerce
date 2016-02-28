from __future__ import unicode_literals

from django.db import models
from catalog.models import Product
# Create your models here.

class CartItem(models.Model):
	date_added = models.DateTimeField(auto_now_add=True)
	quantity=models.IntegerField(default=1)
	product=models.ForeignKey('catalog.Product', unique=False)
	cart_session=models.CharField(default='',max_length=50)

	class Meta:
		db_table = 'cart_items'
		ordering=['date_added']

	def total(self):
		return self.quantity*self.product.price
	def name(self):
		return self.product.name
	def price(self):
		return self.product.price
	def augment_quantity(self,quantity):
		self.quantity=self.quantity+int(quantity)
		self.save()