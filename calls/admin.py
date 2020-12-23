from django.contrib import admin
from .models import Call
from reversion.admin import VersionAdmin

from .models import (
    Commodityfocus, Theme, Subtheme,Granttype,GrantCall,FellowshipCall,FellowshipType
)

admin.site.register(Commodityfocus)
admin.site.register(Subtheme)
admin.site.register(FellowshipType)

class SubthemeInline(admin.TabularInline):
    model = Subtheme

class ThemeAdmin(VersionAdmin):
    
    inlines = [
        SubthemeInline
    ]

admin.site.register(Theme, ThemeAdmin)
class CallAdmin(VersionAdmin):
    list_display = [
        'id',
        'title',
        'call_id',
        'submission_deadline',
        'text',
        'start_date',
        'end_date',
        'scholarship_type',
    ]
    search_fields = ['title','id']
    

admin.site.register(Call, CallAdmin)


class GrantCallAdmin(VersionAdmin):
    list_display = [
        'id',
        'title',
        'call_id',
        'submission_deadline',
        'text',
        'start_date',
        'end_date',
        'grant_type',
    ]
    search_fields = ['title','id']
admin.site.register(GrantCall, GrantCallAdmin)

class FellowshipCallAdmin(VersionAdmin):
    list_display = [
        'id',
        'title',
        'call_id',
        'submission_deadline',
        'goal',
        'objectives',
        'start_date',
        'end_date',
        
    ]
    search_fields = ['title','id']
admin.site.register(FellowshipCall, FellowshipCallAdmin)