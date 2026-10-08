from rest_framework import serializers
from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name field cannot be empty.")
        return value
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a positive number.")
        return value

    def validate(self, data):
        price = data.get('price')
        stock = data.get('stock')
        if price > 10000 and stock < 5:
            raise serializers.ValidationError("Expensive products must have at least 5 items in stock.")

    class Meta:
        model = Product
        fields = '__all__'
