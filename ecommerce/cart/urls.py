from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Cart
    path('', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart),  # AJAX
    path('delete_from_cart', views.delete_from_cart),  # AJAX
    path('plus_quantity', views.plus_quantity),  # AJAX
    path('minus_quantity', views.minus_quantity),  # AJAX

]

