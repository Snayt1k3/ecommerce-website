from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:category>/', views.prod_by_category, name='pr_by_cat'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='one_pr'),
    path('shop/cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/delete/<int:product_id>', views.cart_delete, name='cart_delete'),
    path('shop/login/', views.UserLogView.as_view(), name='login_user'),
    path('shop/signup/', views.UserRegView.as_view(), name='reg_user'),
    path('shop/logout/', views.signoutview, name='logout_user')
]
