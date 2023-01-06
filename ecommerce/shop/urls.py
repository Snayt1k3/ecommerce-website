from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('<str:category>/', views.prod_by_category, name='pr_by_cat'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='one_pr'),
]
