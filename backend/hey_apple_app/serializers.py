from rest_framework.serializers import ModelSerializer
from .models import fruit, image, orderpayment, fruitorder


class FruitSerializer(ModelSerializer):
    class Meta:
        model = fruit
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = image
        fields = '__all__'


class OrderpaymentSerializer(ModelSerializer):
    class Meta:
        model = orderpayment
        fields = '__all__'


class FruitorderSerializer(ModelSerializer):
    class Meta:
        model = fruitorder
        fields = '__all__'
