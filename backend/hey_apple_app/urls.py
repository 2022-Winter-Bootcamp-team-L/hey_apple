from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('fruits/<int:id>', views.get_fruit, name='fruits'),
    path('orders', views.get_order_bill, name='orders')
]
