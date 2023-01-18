from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('fruits/<int:id>', views.get_fruit, name='fruits'),

    # image IO
    #path('orders', views.get_order_bill, name='orders'),
    path('orders/tasks', views.get_task_id),

    #path('orders', views.get_order_bill, name='orders'),
    path('bills', views.send_email_api),
    path('orders/tasks/<task_id>', views.response_result)
]
