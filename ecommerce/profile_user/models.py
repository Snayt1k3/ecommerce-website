from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


# Create your models here.

class SellerStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_cart = models.IntegerField()
    remove_cart = models.IntegerField()
    add_wish_list = models.IntegerField()
    remove_wish_list = models.IntegerField()
    bought = models.IntegerField()
