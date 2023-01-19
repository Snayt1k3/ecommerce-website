from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Category, Cart, WishList


def menu_links(request):
    """Категории в Context"""
    links = Category.objects.all()
    return dict(links=links)


@login_required
def count_product_in_cart(request):
    user = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=user)
    return dict(count_product_in_cart=len(items))


@login_required
def count_product_in_wishlist(request):
    user = User.objects.get(id=request.user.id)
    items = WishList.objects.filter(user=user)
    return dict(count_product_in_wishlist=len(items))
