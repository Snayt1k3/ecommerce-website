from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home, product by category, detail products
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:category>/', views.prod_by_category, name='pr_by_cat'),
    path('product/<slug:slug>/', views.detail_view, name='one_pr'),

    # Auth
    path('shop/login/', views.UserLogView.as_view(), name='login_user'),
    path('shop/signup/', views.UserRegView.as_view(), name='reg_user'),
    path('shop/logout/', views.sign_out, name='logout_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Wish List
    path('wishlist', views.wish_list, name='wishlist'),
    path('add_to_wish', views.add_to_wish_list),
    path('delete_from_wish', views.delete_from_wish_list),

    # Cart
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart),
    path('delete_from_cart', views.delete_from_cart),
    path('plus_quantity', views.plus_quantity),
    path('minus_quantity', views.minus_quantity),

    path('checkout', views.checkout, name='checkout'),
    path('checkout/success', views.CheckSuccess.as_view(), name='checkout_success'),
    path('checkout/failed', views.CheckFailed.as_view(), name='checkout_failed'),
]
