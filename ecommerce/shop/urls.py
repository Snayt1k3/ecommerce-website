from django.urls import path

from . import views

urlpatterns = [
    # Home, product by category, detail products
    path('', views.HomeView.as_view(), name='home'),
    path('<str:category>/', views.prod_by_category, name='pr_by_cat'),
    path('product/<slug:slug>/', views.detail_view, name='one_pr'),

    # Auth
    path('shop/login/', views.UserLogView.as_view(), name='login_user'),
    path('shop/signup/', views.UserRegView.as_view(), name='reg_user'),
    path('shop/logout/', views.sign_out, name='logout_user'),

    # Wish List
    path('wishlist', views.wish_list, name='wishlist'),
    path('add_to_wish', views.add_to_wish_list),
    path('delete_from_wish', views.delete_from_wish_list),

    # Cart
    path('add_to_cart', views.add_to_cart)
]
