from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Home, product by category, detail products
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:category>/', views.ProductCategoryView.as_view(), name='pr_by_cat'),
    path('product/<slug:slug>/', views.detail_view, name='one_pr'),

    # Auth
    path('shop/login/', views.UserLogView.as_view(), name='login_user'),
    path('shop/signup/', views.UserRegView.as_view(), name='reg_user'),
    path('shop/logout/', views.sign_out, name='logout_user'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='shop/registration/password_reset_form.html'),
         name='reset_password'),
    path('reset_password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='shop/registration/password_reset_confirm.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='shop/registration/password_reset.html'),
         name='password_reset_confirm'),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name='shop/registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password/change',
         auth_views.PasswordChangeView.as_view(template_name='shop/registration/password_change.html'),
         name='password_change'),

    # Payment
    path('checkout', views.checkout, name='checkout'),

    # get_order
    path('my_order', views.get_order_for_anonymous, name='get_order'),

    path('seller/<str:username>', views.SellerProductsView.as_view(), name='list_seller_products'),
    path('seller/feedback/<str:username>', views.feedback_seller, name='feedback_seller'),

]
