from django.contrib import admin
from .models import Fellowship, FellowshipStudentmembership
from reversion.admin import VersionAdmin


class FellowshipStudentmembershipInline(admin.TabularInline):
    model = FellowshipStudentmembership

#admin.site.register(Fellowship)
admin.site.register(FellowshipStudentmembership)

class FellowshipAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'title',
        #'summary',
        'budget',
        'start_date',
        'end_date',
        'new_end_date',
        
        'duration',
        'pi',
        'approval_status',
        'approved_by',
        'fellowship_id',
        
        
        
    ]
    inlines = [
        FellowshipStudentmembershipInline
    ]

admin.site.register(Fellowship, FellowshipAdmin)
