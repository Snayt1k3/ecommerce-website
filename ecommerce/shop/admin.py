from django.contrib import admin

from .models import Category, Product, Review, ReviewImages, WishList, Cart

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ReviewImages)
admin.site.register(WishList)
admin.site.register(Cart)


