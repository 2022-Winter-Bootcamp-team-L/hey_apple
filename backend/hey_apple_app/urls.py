from django.contrib import admin
from django.urls import path, include
from . import views
from .views import FruitsInfo, FruitsImage, FruitsPayment, EmailPost


urlpatterns = [
    path('fruits/<int:id>', FruitsInfo.as_view()),
    path('orders/tasks', FruitsImage.as_view()),
    path('orders/tasks/<task_id>', FruitsPayment.as_view()),
    path('bills', EmailPost.as_view())
]
