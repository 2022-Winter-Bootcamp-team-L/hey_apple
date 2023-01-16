from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('fruits/<int:id>', views.get_fruit, name='fruits'),

    # image IO
    path('orders/tasks', views.get_task_id),

]
