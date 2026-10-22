from django.urls import path
from . import views

urlpatterns = [
    path("add-dress/", views.add_dress_with_deposit, name="add_dress"),
    path("delete/<int:dress_id>/", views.delete_dress_with_refund, name="delete_dress"),
path("list/", views.list_dresses),
    path('rentorder/create/', views.create_rent_order, name='create_rent_order'),
path("seller-orders/<str:seller_username>/", views.seller_orders, name="seller_orders"),
path("create-payment/", views.create_payment, name="create_payment"),
    path("deposits/", views.list_security_deposits, name="list_security_deposits"),
    path("toggle_freeze_deposit/<int:deposit_id>/", views.toggle_freeze_deposit, name="toggle_freeze_deposit"),
path('my-orders/', views.get_my_orders, name='api_get_my_orders'),
    path('orders/<int:order_no>/delete/', views.delete_order, name='delete_order'),
]


