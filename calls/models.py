from django.db import models

from grant_types.models import Granttype
from contacts.models import User
#from scholarships.models import Scholarshipappreview

class Commodityfocus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subtheme(models.Model):
    name = models.CharField(max_length=100)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FellowshipType(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.FileField(blank=True, null=True)
    review_form = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class Call(models.Model):
    SCHOLARSHIP_TYPES = (
        ('mastercard', 'Mastercard'),
        ('RI', 'Research and Innovation'),
        ('GTA', 'GTA'),
        )
    title = models.CharField(max_length=256)
    call_id = models.CharField(max_length=100)
    submission_deadline = models.DateField()
    text = models.FileField(blank=True, null=True)
    review_form = models.FileField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    call_year = models.CharField(max_length=20)
    generated_number = models.IntegerField(null=True)
    #removed grants from scholarship
    scholarship_type = models.CharField(max_length=32, blank=True, null=True, choices=SCHOLARSHIP_TYPES)

    def xreview_count(self):
        return self.reviews().count()

    def __str__(self):
        return '{}'.format(self.call_id)

    class Meta:
        ordering = ['submission_deadline']

    @staticmethod
    def get_scholarship_calls():
        return Call.objects.filter(scholarship_type__isnull=False)



# Grant calls
class GrantCall(models.Model):
    QUALIFICATIONS = (
        (None,'--please select--'),
         ('bac', 'BAC'),
        ('msc', 'MSC'),
        ('phd','PHD'),
       
    )
    title = models.CharField(max_length=256)
    call_id = models.CharField(max_length=100)
    submission_deadline = models.DateField()
    text = models.FileField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    call_year = models.CharField(max_length=20)
    generated_number = models.IntegerField(null=True)
    grant_type = models.ForeignKey(Granttype, models.DO_NOTHING, blank=False, null=True)
    commodity_focus = models.ForeignKey(Commodityfocus, models.DO_NOTHING, blank=True, null=True)
    proposal_theme = models.ForeignKey(Theme, models.DO_NOTHING, blank=True, null=True)
    proposal_sub_theme = models.ForeignKey(Subtheme, models.DO_NOTHING, blank=True, null=True)
    minimum_qualification = models.CharField(choices=QUALIFICATIONS,max_length=10, null=True, blank=False)

    def xreviews(self):
        return Scholarshipappreview.objects.filter(application__call=self)

    def xreview_count(self):
        return self.reviews().count()

    @staticmethod
    def get_grant_calls():
        return GrantCall.objects.filter(grant_type__isnull=False)


    def __str__(self):
        return '{}'.format(self.call_id)

    class Meta:
        ordering = ['-submission_deadline','-id']


# Fellowship  calls
class FellowshipCall(models.Model):
    title = models.CharField(max_length=256)
    call_id = models.CharField(max_length=250)
    submission_deadline = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=250)
    member_university = models.TextField()
    home_institute_obligations=models.TextField()
    host_institute=models.TextField()
    goal = models.CharField(max_length=500)
    objectives = models.TextField()
    who_can_apply = models.TextField()
    financial_support = models.TextField()
    institute_obligations = models.TextField()
    call_year = models.CharField(max_length=20)
    generated_number = models.IntegerField(null=True)
    fellowship_type = models.ForeignKey(FellowshipType, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return '{}'.format(self.call_id)

    class Meta:
        ordering = ['submission_deadline']
