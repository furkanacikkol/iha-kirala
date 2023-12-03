from rest_framework import serializers
from .models import IHA, Rental

class IHASerializer(serializers.ModelSerializer):
    class Meta:
        model = IHA
        fields = ['id', 'brand', 'model', 'weight', 'range', 'payload_capacity', 'max_speed', 'category']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'iha', 'user', 'start_datetime', 'end_datetime']
