from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:category>/', views.prod_by_category, name='pr_by_cat'),
    path('product/<slug:slug>/', views.detail_view, name='one_pr'),

    path('shop/login/', views.UserLogView.as_view(), name='login_user'),
    path('shop/signup/', views.UserRegView.as_view(), name='reg_user'),
    path('shop/logout/', views.signoutview, name='logout_user'),

    path('wishlist', views.viewwishlist, name='wishlist'),
    path('add_to_wish', views.addtowish),
    path('delete_from_wish', views.deletewishlist),
]
