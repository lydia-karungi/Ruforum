from rest_framework import serializers
from .models import Call, Subtheme, Theme, GrantCall, FellowshipCall


# scholarship call serializers
class ScholarshipCallSerializer(serializers.ModelSerializer):
    review_form = serializers.FileField()
    scholarship_type = serializers.CharField(source='get_scholarship_type_display')
    applications = serializers.CharField(source='applications.all.count')
   
    class Meta:
        model = Call
        fields = ('id','title','call_id', 'submission_deadline', 'text', 'start_date', 'end_date', 'scholarship_type','review_form','applications')

   
# grant calls serializers
class GrantCallSerializer(serializers.ModelSerializer):
    applications = serializers.CharField(source='grant_applications.all.count')
    grant_type = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    commodity_focus = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    proposal_theme = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    proposal_sub_theme = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
   
    class Meta:
        model = GrantCall
        fields = ('id','title','call_id', 'submission_deadline', 'text', 'start_date',
         'end_date', 'grant_type','applications','commodity_focus','proposal_theme',
         'proposal_sub_theme','minimum_qualification')


#fellowship call seriazers
# grant calls serializers
class FellowshipCallSerializer(serializers.ModelSerializer):
    applications = serializers.CharField(source='applications.all.count')
    fellowship_type = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
  
   
    class Meta:
        model = FellowshipCall
        fields = ('id','title','call_id', 'submission_deadline', 'start_date', 'end_date',
         'duration', 'member_university','home_institute_obligations','host_institute','goal',
         'objectives','who_can_apply','financial_support','institute_obligations','fellowship_type','applications')