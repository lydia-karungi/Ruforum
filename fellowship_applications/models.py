from django.db import models
from contacts.models import User
from common.choices import COUNTRY_CHOICES
from phonenumber_field.modelfields import PhoneNumberField
from calls.models import FellowshipCall


class Fellowshipapplication(models.Model):
    APPLICATION_STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('noncompliant', 'Non Compliant'),
        ('rejected', 'Rejected'),
        ('selected_for_funding', 'Selected for Funding')
    )
    Service = (
        ('research_collaboration', 'Research collaboration'),
        ('lectures', 'Lectures'),
        ('graduate_supervision ', 'Graduate Supervision')
    )

    user = models.ForeignKey(User, models.DO_NOTHING, related_name='fellowship_applications')
    call = models.ForeignKey(FellowshipCall, models.DO_NOTHING, blank=True, null=True, related_name='applications')
    # Home Institution
    home_institute_name = models.CharField(max_length=200)
    home_institute_place = models.CharField(max_length=200)
    home_institute_faculty = models.CharField(max_length=150)
    home_institute_department = models.CharField(max_length=150)
    letter_of_release = models.FileField()
    # Host Institution
    host_institute_name = models.CharField(max_length=200)
    host_institute_place = models.CharField(max_length=200)
    host_institute_faculty = models.CharField(max_length=150)
    host_institute_department = models.CharField(max_length=150)
    # Exchange Fellow
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=64, blank=True)
    position = models.CharField(max_length=100, blank=True)
    area_of_specialization = models.CharField(max_length=100, blank=True)
    area_of_interest=models.CharField(max_length=200, blank=True)
    address = models.TextField()
    email_1 = models.EmailField(verbose_name='Email 1',max_length=255)
    email_2 = models.EmailField(verbose_name='Email 1',max_length=255)
    telephone = PhoneNumberField()
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=64, choices=COUNTRY_CHOICES)
    cv = models.FileField()
    subject_area = models.CharField(max_length=500, blank=True)
    proposed_begining = models.DateField()
    proposed_end = models.DateField()
    duration = models.IntegerField(blank=True, null=True)
    form_of_service=models.CharField(max_length=50, choices=Service)
    proposed_value = models.TextField()
    other_activities = models.TextField()
    comment = models.TextField()
    motivation = models.TextField()
    reviewers = models.ManyToManyField(User)
    fellowship_manager = models.ForeignKey(User, on_delete=models.CASCADE,related_name="fellowship_manager",null=True,blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATES, default='Submitted')
    validators = models.ManyToManyField(User, related_name="validator", blank=True)
    compliance_comments = models.TextField(blank=True, null=True)
    validated_home_institute = models.BooleanField(blank=True, null=True)
    validated_host_institute = models.BooleanField(blank=True, null=True)
    validated_letter_of_release = models.BooleanField(blank=True, null=True)
    validated_cv = models.BooleanField(blank=True, null=True)
   
    class Meta:
        unique_together=['call','user']
        permissions = (
            ("assign_fellowship_validators", "Can assign Fellowship Validators"),
            ("assign_fellowship_reviewers", "Can assign Fellowship reviewers"),
            ("can_validate_fellowship_app", "Can Validate Fellowship Application"),
            
        )

    @property
    def compliant(self):
        compliance_fields = [
            'validated_home_institute',
            'validated_host_institute',
            'validated_letter_of_release',
            'validated_cv',
            
        ]

        for field in compliance_fields:
            if not getattr(self, field):
                return False

        return True

    @property
    def validated(self):
        return self.status == 'validated'

    def is_draft(self):
        return self.status == 'draft'


class Fellowshipappreview(models.Model):
    RECOMMENDATIONS = (
        ('major', 'Major Revision'),
        ('minor', 'Minor Revision'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )
    application = models.ForeignKey(Fellowshipapplication, models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, models.DO_NOTHING)
    comments = models.TextField()
    date = models.DateTimeField()
    score = models.IntegerField()
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATIONS)
    review_form = models.FileField()

    class Meta:
        unique_together = (('application', 'reviewer'),)
