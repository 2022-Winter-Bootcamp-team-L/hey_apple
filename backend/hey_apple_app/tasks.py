from __future__ import absolute_import, unicode_literals
from backend.celery import app
from django.http import JsonResponse

from .views import get_order_bill

@app.task
def ai_task(request):
    url = get_order_bill(request)

# ai task

    return JsonResponse({"image_url": url})
