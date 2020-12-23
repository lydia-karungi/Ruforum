from .models import TempReport
from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempReport
        fields = '__all__'