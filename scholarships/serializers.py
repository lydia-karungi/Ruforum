from rest_framework import serializers
from .models import Scholarship,Scholarshipapplication,Scholarshipappreview


class ScholarshipSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(method_name='get_student')
    scholarship_type = serializers.SerializerMethodField(method_name='get_scholarship_type')
    approval_status =serializers.CharField(source='get_approval_status_display')

    class Meta:
        model = Scholarship
        fields = '__all__'

    def get_scholarship_type(self, obj):
        return '{}'.format(obj.application.call.get_scholarship_type_display())
    
    def get_student(self, obj):

        return '{} {}'.format(obj.application.first_name,obj.application.last_name)