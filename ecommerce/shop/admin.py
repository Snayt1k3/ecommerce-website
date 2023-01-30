from django.contrib import admin

from .models import Category, Product, Review, Orders, PersonalArea, PromoCode, ReviewSeller

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(PersonalArea)
admin.site.register(PromoCode)
admin.site.register(ReviewSeller)


@admin.register(Orders)
class AdminStore(admin.ModelAdmin):
    filter_horizontal = ['order_items']
