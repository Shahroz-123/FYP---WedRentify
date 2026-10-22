from django.urls import path
from . import views

urlpatterns = [
    path("buyer/signup/", views.buyer_signup),
    path("buyer/login/", views.buyer_login),
    path("seller/signup/", views.seller_signup),
    path("seller/login/", views.seller_login),
    path("users/", views.list_all_users, name="list_all_users"),
    path("delete_user/<str:user_type>/<int:user_id>/", views.delete_user, name="delete_user"),
path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
]
