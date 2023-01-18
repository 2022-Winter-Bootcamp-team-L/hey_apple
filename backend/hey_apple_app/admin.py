from django.contrib import admin

from .models import fruit, image, orderbill, fruitorderbill


@admin.register(fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'harvest', 'content', 'price', 'calorie', 'created_at', 'updated_at', 'is_deleted']


@admin.register(image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 's3_image_url', 's3_result_image_url', 'created_at', 'updated_at', 'is_deleted']


@admin.register(orderbill)
class OrderBillAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_id', 'date_of_purchase', 'total_price', 'created_at', 'updated_at', 'is_deleted']

@admin.register(fruitorderbill)
class FruitOrderBillAdmin(admin.ModelAdmin):
    list_display = ['id', 'fruit_id', 'orderbill_id', 'count', 'created_at', 'updated_at', 'is_deleted']
