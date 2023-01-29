from cart.cart import Cart
from wish_list.favourites import Favourites

from .models import Category, PersonalArea


def is_seller(request):
    is_seller_bool = False
    if request.user.is_authenticated:
        is_seller_bool = PersonalArea.objects.get(user=request.user).is_seller

    return dict(is_seller=is_seller_bool)


def menu_links(request):
    """Категории в Context"""
    links = Category.objects.all()
    return dict(links=links)
