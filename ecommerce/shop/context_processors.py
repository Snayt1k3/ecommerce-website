from django.contrib.auth.models import User

from .models import Category, Cart, WishList


def menu_links(request):
    """Категории в Context"""
    links = Category.objects.all()
    return dict(links=links)


def count_product_in_cart(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        items = Cart.objects.filter(user=user)
    else:
        items = ''
    return dict(count_product_in_cart=len(items))


def count_product_in_wishlist(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        items = WishList.objects.filter(user=user)
    else:
        items = ''
    return dict(count_product_in_wishlist=len(items))
