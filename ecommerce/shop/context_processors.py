
from .models import Category, Cart, WishList


def menu_links(request):
	"""Категории в Context"""
	links = Category.objects.all()
	return dict(links=links)


def count_product_in_cart(request):
	items = Cart.objects.filter(user=request.user)
	return dict(count_product_in_cart=len(items))


def count_product_in_wishlist(request):
	items = WishList.objects.filter(user=request.user)
	return dict(count_product_in_wishlist=len(items))
