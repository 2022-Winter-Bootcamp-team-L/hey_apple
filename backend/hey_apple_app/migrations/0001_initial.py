# Generated by Django 4.1.5 on 2023-01-12 13:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fruit',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('harvest', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=512)),
                ('price', models.IntegerField()),
                ('calorie', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'fruit',
            },
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('s3_image_url', models.CharField(max_length=512)),
                ('s3_result_image_url', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'image',
            },
        ),
        migrations.CreateModel(
            name='orderbill',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_of_purchase', models.DateTimeField()),
                ('total_price', models.BigIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.IntegerField(default=1)),
                ('image_id', models.ForeignKey(db_column='image_id', on_delete=django.db.models.deletion.CASCADE, related_name='image', to='hey_apple_app.image')),
            ],
            options={
                'db_table': 'orderbill',
            },
        ),
        migrations.CreateModel(
            name='fruitorderbill',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('count', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.IntegerField(default=1)),
                ('fruit_id', models.ForeignKey(db_column='fruit_id', on_delete=django.db.models.deletion.CASCADE, related_name='fruit', to='hey_apple_app.fruit')),
                ('orderbill_id', models.ForeignKey(db_column='orderbill_id', on_delete=django.db.models.deletion.CASCADE, related_name='orderbill', to='hey_apple_app.orderbill')),
            ],
            options={
                'db_table': 'fruitorderbill',
            },
        ),
    ]
