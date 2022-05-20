from rest_framework import serializers
from .models import Package

class PackageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        flights = validated_data.pop('flight', None)
        package = Package.objects.create(**validated_data, code=Package.generate_unique_code())
        package.flight.set(flights)
        return package

    class Meta:
        model = Package
        exclude = ('code',)
