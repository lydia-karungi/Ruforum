from django.contrib import admin
from .models import (Role,StaffProfile,Leave,
Funder,Competency, LeadershipCompetency,LeaveType,LeaveAssignment,LeaveApplication,Month6Appraisal,Month6AppraisalActivity,Month6PlannedAppraisalActivity)
from reversion.admin import VersionAdmin

# Register your models here.
admin.site.register(Role)
admin.site.register(StaffProfile)
admin.site.register(Funder)
admin.site.register(Competency)
admin.site.register(LeadershipCompetency)

admin.site.register(LeaveType)

class LeaveAssignmentAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [

        'leave_type',
        'start_date',
        'leave_days',
        'year'
    ]
    search_fields = ['leave_type__leave_name','year','leave_days']

admin.site.register(LeaveAssignment, LeaveAssignmentAdmin)

class LeaveApplicationAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [

        'leave_assignment',
        'staff',
        'from_date',
        'end_date',
        'leave_days_requested'
    ]
    search_fields = ['staff__user','leave_assignment__leave_type','from_date','end_date']
    
admin.site.register(LeaveApplication, LeaveApplicationAdmin)


class LeaveAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
      
        'leave_application',
        'start',
        'end',
        'leave_days'
    ]
    search_fields = ['leave_application__leave_assignment__leave_type__leave_name','start','end','leave_days']
    
admin.site.register(Leave, LeaveAdmin)

class Month6AppraisalAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
      
        'staff',
        'current_job_title',
        'supervisor',
        'implementation_activites',
        'implementation_activites2'

    ]
    search_fields = ['staff__first_name','current_job_title','supervisor__first_name','implementation_activites']
    
admin.site.register(Month6Appraisal, Month6AppraisalAdmin)

class Month6AppraisalActivityAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
      
        'appraisal',
        'name',
        'achievement'

    ]
    search_fields = ['name','achievement']
    
admin.site.register(Month6AppraisalActivity, Month6AppraisalActivityAdmin)

class Month6PlannedAppraisalActivityAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
      
        'appraisal',
        'name',
        'start_date',
        'end_date'

    ]
    search_fields = ['name','achievement']
    
admin.site.register(Month6PlannedAppraisalActivity, Month6PlannedAppraisalActivityAdmin)