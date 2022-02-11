from rest_framework import serializers
from .models import Cooker

class CookerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cooker
        fields = '__all__'
