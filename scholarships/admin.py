from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import (
    Typeoffloor, Typeofhousewall, Typeofroofingmaterial, Homeassets,
    Incomecontributor, Scholarshipapplication,
    Additionalfundingsource, Communityservice, Currentvolunteering,
    Employmenthistory, Groupassociationclub, Householdincomesource,
    Mastercardeducation, Mastercardscholarshipapplication,
    Othereducation, Otherscholarshipapplication, Parent, Referenceletter,
    Scholarshipappreview, Transcriptfile, Workexperience,ScholarShipType,ResearchAndPublication,
    Leadershipposition,Scholarship
)

admin.site.register(Typeoffloor)
admin.site.register(Typeofhousewall)
admin.site.register(Typeofroofingmaterial)
admin.site.register(Homeassets)
admin.site.register(Incomecontributor)
admin.site.register(Othereducation)
admin.site.register(Employmenthistory)
admin.site.register(Referenceletter)
admin.site.register(Scholarshipappreview)
admin.site.register(Transcriptfile)
admin.site.register(Workexperience)
admin.site.register(Otherscholarshipapplication)
admin.site.register(ScholarShipType)
admin.site.register(Parent)
admin.site.register(Mastercardeducation)
admin.site.register(ResearchAndPublication)
admin.site.register(Leadershipposition)
admin.site.register(Householdincomesource)
admin.site.register(Groupassociationclub)
admin.site.register(Currentvolunteering)
admin.site.register(Communityservice)
admin.site.register(Additionalfundingsource)
admin.site.register(Scholarship)
class AdditionalfundingsourceInline(admin.TabularInline):
    model = Additionalfundingsource

class CommunityserviceInline(admin.TabularInline):
    model = Communityservice 

class CurrentvolunteeringInline(admin.TabularInline):
    model = Currentvolunteering  

class EmploymenthistoryInline(admin.TabularInline):
    model = Employmenthistory

class GroupassociationclubInline(admin.TabularInline):
    model = Groupassociationclub

class HouseholdincomesourceInline(admin.TabularInline):
    model = Householdincomesource

class MastercardeducationInline(admin.TabularInline):
    model = Mastercardeducation

'''
class MastercardscholarshipapplicationInline(admin.TabularInline):
    model = Mastercardscholarshipapplication
'''

class MastercardscholarshipapplicationInline(admin.StackedInline):
    model = Mastercardscholarshipapplication
    can_delete = False
    #verbose_name_plural = 'Otherscholarshipapplication'
    #fk_name = 'user'


class OthereducationInline(admin.TabularInline):
    model = Othereducation

'''
class OtherscholarshipapplicationInline(admin.TabularInline):
    model = Otherscholarshipapplication
'''

class OtherscholarshipapplicationInline(admin.StackedInline):
    model = Otherscholarshipapplication
    can_delete = False
    #verbose_name_plural = 'Otherscholarshipapplication'
    #fk_name = 'user'



class ParentInline(admin.TabularInline):
    model = Parent

class ReferenceletterInline(admin.TabularInline):
    model = Referenceletter

class ScholarshipappreviewInline(admin.TabularInline):
    model = Scholarshipappreview

class TranscriptfileInline(admin.TabularInline):
    model = Transcriptfile

class WorkexperienceInline(admin.TabularInline):
    model = Workexperience


class ApplicationAssetsInline(admin.TabularInline):
    model = Mastercardscholarshipapplication.home_assets.through

class ApplicationIcomeContribInline(admin.TabularInline):
    model = Mastercardscholarshipapplication.income_contrib3efc.through

class ApplicationTypeOfFloorInline(admin.TabularInline):
    model = Mastercardscholarshipapplication. type_of_floor.through

class ApplicationHouseWallInline(admin.TabularInline):
    model = Mastercardscholarshipapplication.type_of_house_wall.through

class ApplicationRoofingInline(admin.TabularInline):
    model = Mastercardscholarshipapplication.type_of_roofing.through


class MastercardscholarshipapplicationAdmin(VersionAdmin,admin.ModelAdmin):
    inlines = [
        ApplicationAssetsInline,
        ApplicationHouseWallInline,
        ApplicationIcomeContribInline,
        ApplicationRoofingInline,
        ApplicationTypeOfFloorInline
    ]
admin.site.register(Mastercardscholarshipapplication, MastercardscholarshipapplicationAdmin)


class ScholarshipapplicationAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'user',
        'call',
        'submitted',
    ]
    inlines = [
        AdditionalfundingsourceInline,
        CommunityserviceInline,
        CurrentvolunteeringInline,
        EmploymenthistoryInline,
        GroupassociationclubInline,
        HouseholdincomesourceInline,
        MastercardeducationInline,
        MastercardscholarshipapplicationInline,
        OthereducationInline,
        OtherscholarshipapplicationInline,
        ParentInline,
        ReferenceletterInline,
        ScholarshipappreviewInline,
        TranscriptfileInline,
        WorkexperienceInline
    ]
    #exclude = ('participants',)
    '''
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    '''

admin.site.register(Scholarshipapplication, ScholarshipapplicationAdmin)
