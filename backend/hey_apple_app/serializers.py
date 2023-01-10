from rest_framework.serializers import ModelSerializer
from .models import Fruit,Image,Orderbill,Fruitorderbill

class FruitSerializer(ModelSerializer):
    class Meta:
        model = Fruit
        fields = '__all__'
        
class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class OrderbillSerializer(ModelSerializer):
    class Meta:
        model = Orderbill
        fields = '__all__'
        
class FruitorderbillSerializer(ModelSerializer):
    class Meta:
        model = Fruitorderbill
        fields = '__all__'