from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_donation, name="add_donation"),
    path("list/", views.list_donations, name="list_donations"),
    path("delete/<int:id>/", views.delete_donation, name="delete_donation"),
]
