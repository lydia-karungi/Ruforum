from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import (
    Month12Report, Month18Report, Month24Report, LastReport,
    FirstReport, Studentmonth12Report, Studentmonth18Report, Studentmonth24Report,
    LastStudentReport, FirstStudentReport, Technology,Beneficiary
)

class FirstReportAdim(VersionAdmin):
    list_display = [
        'id',
        'month',
        'grant',
        'status',
        
        
    ]
    search_fields = ['grant__title']
   
admin.site.register(FirstReport, FirstReportAdim)
class FirstStudentReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
       
        
        
    ]
    search_fields = ['month_6_report__grant__grant_id','student__user__first_name']

admin.site.register(FirstStudentReport, FirstStudentReportAdim)

class Month12ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
        'grant',
        'status',
        
        
    ]
    search_fields = ['grant__title']

admin.site.register(Month12Report, Month12ReportAdim)

class Month18ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
        'grant',
        'status',
        
        
    ]
    search_fields = ['grant__title']
admin.site.register(Month18Report, Month18ReportAdim)

class Month24ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
        'grant',
        'status',
        
        
    ]
    search_fields = ['grant__title']

admin.site.register(Month24Report, Month24ReportAdim)

class LastReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
        'grant',
        'status',
        
        
    ]
    search_fields = ['grant__title']

admin.site.register(LastReport, LastReportAdim)

class Studentmonth12ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
       
        
        
    ]
    search_fields = ['month_12_report__grant__grant_id','student__user__first_name']
admin.site.register(Studentmonth12Report, Studentmonth12ReportAdim)
class Studentmonth18ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
       
        
        
    ]
    search_fields = ['month_18_report__grant__grant_id','student__user__first_name']
admin.site.register(Studentmonth18Report, Studentmonth18ReportAdim)

class Studentmonth24ReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
       
        
        
    ]
    search_fields = ['month_24_report__grant__grant_id','student__user__first_name']
admin.site.register(Studentmonth24Report, Studentmonth24ReportAdim)

class LastStudentReportAdim(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
       
        
        
    ]
    search_fields = ['month_30_report__grant__grant_id','student__user__first_name']

admin.site.register(LastStudentReport, LastStudentReportAdim)
admin.site.register(Technology)
admin.site.register(Beneficiary)

