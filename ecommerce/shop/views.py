import json
import random

from django.shortcuts import render
from decimal import Decimal

from django.views.generic import ListView

from .models import Category, Product
# Create your views here.


class HomeView(ListView):
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
def prod_by_category(request, category):
    cat = Category.objects.get(category_name=category)
    products = Product.objects.filter(category=cat)
    return render(request, 'shop/base.html', context={
        'products': products,
        'categories': Category.objects.all(),
    })