from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Student, User, Studentfundingsource


class StudentAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'user',
        'year_of_birth',
        'university',
        'university_department',
        'university_reg_no',
        'degree_program_level',
        'degree_program_name',
        'intake_year',
        'grad_expected',
        'grad_actual',
        'thesis_title',
        'cohort',
        'supervisor1',
        'supervisor2',
        'supervisor3',
        # 'research_abstract',
        'grant_type',
    ]


admin.site.register(Student, StudentAdmin)


class UserAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'business_email',

    ]
    search_fields = ['id', 'first_name', 'last_name', 'business_email']


admin.site.register(User, UserAdmin)


class StudentFundingSourceAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'student',
        'funder',
        'items',
        'amount',
    ]


admin.site.register(Studentfundingsource, StudentFundingSourceAdmin)
