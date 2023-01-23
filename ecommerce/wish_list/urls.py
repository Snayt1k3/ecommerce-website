from django.urls import path

from . import views

urlpatterns = [
    # Wish List
    path('wishlist/', views.wish_list, name='wishlist'),
    path('add_to_wish/', views.add_to_wish_list),  # AJAX
    path('delete_from_wish/', views.delete_from_wish_list),  # AJAX
]
