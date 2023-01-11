"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include ,path
from rest_framework import routers
from hey_apple_app import views

router = routers.DefaultRouter()
# schema_url_patterns = [ ?? 이거 뭔지 잘 모르겠음
#     path('api/v1/', include('hey_apple_app.urls')),
#     # path('api/v1/images/', include('images.urls')),
# ]


urlpatterns = [
    path('api/v1/', include('hey_apple_app.urls'), name='fruits')
]




