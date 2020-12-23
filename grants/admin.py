from django.contrib import admin
from .models import Grant, Studentmembership
from reversion.admin import VersionAdmin

class StudentmembershipInline(admin.TabularInline):
    model = Studentmembership

#admin.site.register(Grant)
#admin.site.register(Studentmembership)

class GrantAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'grant_application',
        'title',
        #'summary',
        'budget',
        'start_date',
        'end_date',
        'new_end_date',
        'theme',
        'value_chain',
        'duration',
        'pi',
        'approval_status',
        'approved_by',
        'grant_id',
        'project_objectives',
        'collaborators',
        'has_reports',
    ]
    search_fields = ['title','grant_id','pi__first_name','pi__last_name']
    inlines = [
        StudentmembershipInline
    ]

admin.site.register(Grant, GrantAdmin)
