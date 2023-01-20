from django.contrib import admin

from .models import Category, Product, Review, ReviewImages, WishList, Cart, Orders, PersonalArea

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ReviewImages)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(PersonalArea)


@admin.register(Orders)
class AdminStore(admin.ModelAdmin):
    filter_horizontal = ['order_items']
