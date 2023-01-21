from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    # Profile
    path('<str:username>', views.profile_user_view, name='profile'),
    path('edit/<str:username>', views.profile_user_edit_view, name='edit_profile'),

    # Email Confirmation
    path('email/send', views.email_sent_view),  # AJAX
    path('email/confirm', views.email_confirm_view),  # AJAX

]
