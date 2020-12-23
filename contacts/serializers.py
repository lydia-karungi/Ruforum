from rest_framework import serializers
from .models import User, Student




class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    country = serializers.CharField(source='get_country_display')
    nationality = serializers.CharField(source='get_nationality_display')
    gender = serializers.CharField(source='get_gender_display')
   

    class Meta:
        model = User
        fields = ('id','business_email','full_name', 'title', 'first_name', 'last_name', 'gender', 'contact_type', 'passport_no', 
        'home_address', 'business_address', 'country', 'nationality', 'job_title', 'institution', 
        'area_of_specialisation', 'personal_email', 'home_tel', 'business_tel', 'mobile', 'picture', 'department',
        'highest_qualification', 'groups')

    def get_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)