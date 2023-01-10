
from .models import Category


def menu_links(request):
	"""Категории в Context"""
	links = Category.objects.all()
	return dict(links=links)
