from .models import LeaveApplication, LeaveType, LeaveAssignment, LeaveApplication, Leave, Month6Appraisal
from rest_framework import serializers

class LeaveSerializer(serializers.ModelSerializer):
  
    count_holidays = serializers.SerializerMethodField(method_name='count_holidays_bool',source='count_holidays')
    paid_leave = serializers.SerializerMethodField(method_name='paid_bool',source='paid_leave')
    eligible_groups = serializers.CharField(source='get_eligible_groups_display')

    class Meta:
        model = LeaveType
        fields = '__all__'

    def count_holidays_bool(self, instance):
        if instance.count_holidays == True:
            return "Yes"
        else:
            return "No"
    
    def paid_bool(self, instance):
        if instance.paid_leave == True:
            return "Yes"
        else:
            return "No"

class LeaveAssignmentSerializer(serializers.ModelSerializer):
    staff = serializers.SlugRelatedField(many=False,read_only=True, slug_field='get_name')
    leave_type = serializers.SlugRelatedField(many=False,read_only=True, slug_field='leave_name')


    class Meta:
        model = LeaveAssignment
        fields = '__all__'

class LeaveApplicationsSerializer(serializers.ModelSerializer):
    staff = serializers.SlugRelatedField(many=False,read_only=True, slug_field='get_name')
    leave_assignment = serializers.SlugRelatedField(many=False,read_only=True, slug_field='get_leave_type')
    approval = serializers.CharField(source='get_approval_display')


    class Meta:
        model = LeaveApplication
        fields = '__all__'

class ApprovedLeaveSerializer(serializers.ModelSerializer):
    staff = serializers.CharField(source='get_staff', read_only=True)
    leave = serializers.CharField(source='get_leave_name', read_only=True)
    #approval = serializers.CharField(source='get_approval_display')


    class Meta:
        model = Leave
        fields = ['id','staff','leave','start','end','leave_days','leave_application']

class Month6AppraisalSerializer(serializers.ModelSerializer):
    staff = serializers.SlugRelatedField(many=False,read_only=True, slug_field='get_name')
    supervisor = serializers.SlugRelatedField(many=False,read_only=True, slug_field='get_name')


    class Meta:
        model = Month6Appraisal
        fields = '__all__'
