from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import (
    Grantapplication,
    Collaborator, Supportingletter, Grantappreview
)


class CollaboratorInline(admin.TabularInline):
    model = Collaborator



class SupportingletterInline(admin.TabularInline):
    model = Supportingletter

class GrantappreviewInline(admin.TabularInline):
    model = Grantappreview

class GrantapplicationReviewersInline(admin.TabularInline):
    model = Grantapplication.reviewers.through

class GrantapplicationAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'user_id',
        'user',
        'call',
        'title',
        'proposal_title',
        'total_budget',
        'dean_contact',
        'duration_months',
        'students_to_train',

    ]
    search_fields = ['proposal_title','title','user__first_name','user__last_name']

    inlines = [
        CollaboratorInline,
        SupportingletterInline,
        GrantappreviewInline,
    ]
    exclude = ('reviewers',)

admin.site.register(Grantapplication, GrantapplicationAdmin)

class GrantapplicationReviewAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'application',
        'reviewer',
        'date',
        'score',
        'recommendation',
        'comments'
   

    ]
    search_fields = ['application__title','reviewer__first_name','reviewer__last_name','date','score']
admin.site.register(Grantappreview,GrantapplicationReviewAdmin)