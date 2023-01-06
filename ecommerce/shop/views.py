import json
import random

from django.shortcuts import render
from decimal import Decimal

from django.views.generic import ListView

from .models import Category, Product
# Create your views here.


class HomeView(ListView):
    paginate_by = 20
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'
