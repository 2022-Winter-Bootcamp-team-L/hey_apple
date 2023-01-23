from django.contrib import admin

from .models import fruit, image, orderpayment, fruitorder


@admin.register(fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'harvest', 'content', 'price', 'calorie', 'created_at', 'updated_at', 'is_deleted']


@admin.register(image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'orderpayment_id', 's3_image_url', 's3_result_image_url', 'created_at', 'updated_at', 'is_deleted']


@admin.register(orderpayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'created_at', 'updated_at', 'is_deleted']

@admin.register(fruitorder)
class FruitOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'fruit_id', 'image_id', 'count', 'created_at', 'updated_at', 'is_deleted']
