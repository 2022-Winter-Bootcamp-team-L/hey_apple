from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('fruits/<int:id>', views.get_fruit, name='fruits'),
    # path('<Id>', views.delete_images, name='delete_images'),
    # path('list/history', views.get_history, name='get_history'),#나중에 알맞은 이름으로 수정
    # path('results/tasks/<task_id>',views.get_task_result),
]
