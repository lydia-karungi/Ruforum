from rest_framework import serializers
from .models import Grantapplication, Grantappreview
from django.db.models import Avg

# grant application seriazers
class GrantApplicationSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source='get_nationality_display')
    call = serializers.SlugRelatedField(many=False,read_only=True, slug_field='call_id')
    country = serializers.CharField(source='get_country_display')
    status = serializers.CharField(source='get_status_display')
    user = serializers.SerializerMethodField(method_name='get_full_name')
    first_name = serializers.SerializerMethodField(method_name='get_applicant')
    gender = serializers.CharField(source='get_gender_display')


    class Meta:
        model = Grantapplication
        fields ='__all__'
    
    def get_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)
    
    def get_applicant(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField(method_name='get_reviewer')
    recommendation = serializers.CharField(source='get_recommendation_display')
   
    class Meta:
        model = Grantappreview
        fields = '__all__'
    
    def get_reviewer(self, obj):
        return '{} {}'.format(obj.reviewer.first_name, obj.reviewer.last_name)
   

class GrantApplicationReviewSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source='get_nationality_display')
    call = serializers.SlugRelatedField(many=False,read_only=True, slug_field='call_id')
    country = serializers.CharField(source='get_country_display')
    status = serializers.CharField(source='get_status_display')
    user = serializers.SerializerMethodField(method_name='get_full_name')
    first_name = serializers.SerializerMethodField(method_name='get_applicant')
    gender = serializers.CharField(source='get_gender_display')
    reviews = ReviewSerializer(many=True, read_only=True)
    grant_manager = serializers.SerializerMethodField(method_name='get_average_score')

  

    class Meta:
        model = Grantapplication
        fields ='__all__'
    
    def get_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)
    
    def get_applicant(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    def get_average_score(self,obj):
        total_score = obj.reviews.aggregate(Avg('score'))
        
        return total_score