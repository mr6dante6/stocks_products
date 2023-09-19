from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        extra_kwargs = {
            'product': {'write_only': True},
        }


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position_data in positions_data:
            StockProduct.objects.update_or_create(stock=stock, product=position_data['product'], defaults=position_data)

        return stock
