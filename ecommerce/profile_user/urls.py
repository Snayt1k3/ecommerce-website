from django.urls import path

from . import views

urlpatterns = [

    # Profile
    path('<str:username>', views.profile_user_view, name='profile'),
    path('edit/<str:username>', views.profile_user_edit_view, name='edit_profile'),

    # Email Confirmation
    path('email/send', views.email_sent_view),  # AJAX
    path('email/confirm', views.email_confirm_view),  # AJAX

    # BecomeSeller
    path('become-seller/', views.become_seller, name='become_seller'),
    path('become-seller/success', views.BecomeSellerSuccess.as_view(), name='become_seller_success'),

    # Seller
    path('seller/', views.seller_view, name='seller'),
    path('seller/product', views.product_seller_view, name='product_seller'),
    path('seller/product/success', views.ProductSellerSuccess.as_view(), name='seller_product_ok'),

]
