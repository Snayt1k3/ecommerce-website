from django.urls import path

from . import views

urlpatterns = [

    # Profile
    path('<str:username>', views.profile_user_view, name='profile'),
    path('edit/<slug:slug>', views.ProfileUserUpdate.as_view(), name='edit_profile'),

    # Profile order detail
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail_pk'),

    # Email Confirmation
    path('email/send', views.email_sent_view),  # AJAX
    path('email/confirm', views.email_confirm_view),  # AJAX
    path('email/change', views.change_email, name='email_change'),

    # BecomeSeller
    path('become-seller/', views.become_seller, name='become_seller'),
    path('become-seller/success', views.BecomeSellerSuccess.as_view(), name='become_seller_success'),

    # Seller
    path('seller/', views.seller_view, name='seller'),
    path('seller/product', views.product_seller_view, name='product_seller'),
    path('seller/product/success', views.ProductSellerSuccess.as_view(), name='seller_product_ok'),
    path('seller/product/edit/<slug:slug>', views.SellerProductUpdateView.as_view(), name='update_product'),
    path('seller/feedback/<str:username>', views.SellerFeedbackView.as_view(), name='seller_feedback_list'),
    path('seller/stats/<str:username>/<int:pk>', views.SellerStatsDetail.as_view(), name='stats_detail'),
    path('seller/product/delete', views.delete_product)  # Ajax,

]
