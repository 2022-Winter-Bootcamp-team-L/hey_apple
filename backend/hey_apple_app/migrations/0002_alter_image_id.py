# Generated by Django 4.1.5 on 2023-01-12 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hey_apple_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]