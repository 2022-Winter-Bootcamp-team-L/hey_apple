# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.utils import timezone
from django.db import models


class Fruit(models.Model):
    id = models.BigAutoField(primary_key=True , null=False)
    name = models.CharField(max_length=20 , null=False)
    harvest = models.CharField(max_length=20 , null=False)
    content = models.CharField(max_length=512 , null=False)
    price = models.IntegerField(null=False)
    calorie = models.IntegerField(null=False)
    create_at = models.DateTimeField(default=timezone.now ,null=False)
    upload_at = models.DateTimeField(default=timezone.now ,null=False)
    is_deleted = models.IntegerField(null=False , default=1)

        
class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    s3_image_url = models.CharField(max_length=512 ,null=False)
    s3_result_image_url = models.CharField(max_length=512, blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now ,null=False)
    upload_at = models.DateTimeField(default=timezone.now ,null=False)
    is_deleted = models.IntegerField(null=False , default=1)

class Orderbill(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_id = models.ForeignKey("Image" , related_name="image" , on_delete=models.CASCADE, db_column="image_id")
    date_of_purchase = models.DateTimeField()
    total_price = models.BigIntegerField(blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now ,null=False)
    upload_at = models.DateTimeField(default=timezone.now ,null=False)
    is_deleted = models.IntegerField(null=False , default=1)

class Fruitorderbill(models.Model):
    id = models.BigAutoField(primary_key=True)
    fruit_id = models.ForeignKey("Fruit" , related_name="fruit", on_delete=models.CASCADE ,db_column="fruit_id")
    Orderbill_id = models.ForeignKey("Orderbill" , related_name="orderbill", on_delete=models.CASCADE ,db_column="orderbill_id")
    count = models.IntegerField(null=True)
    create_at = models.DateTimeField(default=timezone.now ,null=False)
    upload_at = models.DateTimeField(default=timezone.now ,null=False)
    is_deleted = models.IntegerField(null=False , default=1)