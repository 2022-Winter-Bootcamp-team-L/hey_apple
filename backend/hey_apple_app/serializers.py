from rest_framework.serializers import ModelSerializer
from .models import fruit, image, orderbill, fruitorderbill


class FruitSerializer(ModelSerializer):
    class Meta:
        model = fruit
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = image
        fields = '__all__'


class OrderbillSerializer(ModelSerializer):
    class Meta:
        model = orderbill
        fields = '__all__'


class FruitorderbillSerializer(ModelSerializer):
    class Meta:
        model = fruitorderbill
        fields = '__all__'
