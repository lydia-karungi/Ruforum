from django.db import models

from calls.models import GrantCall
from contacts.models import User
from common.choices import COUNTRY_CHOICES,GENDER_CHOICES
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Grantapplication(models.Model):
    APPLICATION_STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('noncompliant', 'Non Compliant'),
        ('rejected', 'Rejected'),
        ('selected_for_funding', 'Selected for Funding')
    )
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='applications')
    call = models.ForeignKey(GrantCall, models.DO_NOTHING, blank=True, null=True, related_name="grant_applications")
    proposal = models.CharField(max_length=200)
    title = models.CharField(max_length=32)
    grant_manager = models.ForeignKey(User, on_delete=models.CASCADE,related_name="grants_manager",null=True,blank=True)
    proposal_title = models.TextField(help_text="please do not exceed 250 words")
    total_budget = models.IntegerField(blank=False, null=True)
    dean_contact = models.TextField()
    cv = models.FileField()
    email = models.EmailField(max_length=200, blank=False, null=True)
    nationality = models.CharField(max_length=64, choices=COUNTRY_CHOICES, null = True)
    business_address = models.TextField(blank=False,null= True)
    duration_months = models.IntegerField(blank=True, null=True)
    students_to_train = models.IntegerField(blank=True, null=True)
    non_university_partners = models.TextField(blank=True)
    other_departments = models.TextField(blank= True)
    other_universities = models.TextField(blank= True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATES, default='draft', blank=True,null=True)
    last_modified = models.DateField(auto_now_add=True)
    application_form = models.FileField(blank=True, null=True)
    supporting_letter_from_university = models.FileField()
    project_budget = models.FileField()
    title = models.CharField(max_length=32)
    last_name = models.CharField(max_length=50)
    area_of_specialisation = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=50,null=True)
    institution = models.CharField(max_length=128)
    business_tel = PhoneNumberField(null=True)
    mobile = PhoneNumberField(null= True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,null = True)
    department = models.CharField(max_length=128)
    country =models.CharField(max_length=64, choices=COUNTRY_CHOICES)
    highest_qualification = models.CharField(max_length=128)
    ref_number = models.CharField(max_length=25)
    compliance_comments = models.TextField(blank=True, null=True)
    validated_phd = models.BooleanField(blank=True, null=True)
    validated_total_budget = models.BooleanField(blank=True, null=True)
    validated_member_university = models.BooleanField(blank=True, null=True)
    validated_university_letter = models.BooleanField(blank=True, null=True)
    validated_uploaded_templates = models.BooleanField(blank=True, null=True)
    validated_main_proposal = models.BooleanField(blank=True, null=True)
    selected_for_funding = models.BooleanField(blank=True, null=True)
    selected_for_funding_comments = models.TextField(blank=True, null=True)
    funding_email_sent = models.BooleanField()
    reviewers = models.ManyToManyField(User, unique=False)
    validators = models.ManyToManyField(User, related_name="validators", blank=True)

    class Meta:
        unique_together=['call', 'user', 'proposal']
        permissions = (
            ("assign_grant_application_validators", "Can assign grant application Validators"),
            ("assign_grant_application_reviewers", "Can assign grant application reviewers"),
        )

    @property
    def compliant(self):
        compliance_fields = [
            'validated_phd',
            'validated_total_budget',
            'validated_member_university',
            'validated_university_letter',
            'validated_uploaded_templates',
            'validated_main_proposal',
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

    def __str__(self):
         return  '{} -- {}'.format(self.proposal,self.user)


class Collaborator(models.Model):
    application = models.ForeignKey(Grantapplication, on_delete=models.CASCADE)
    cv = models.FileField()


class Grantappreview(models.Model):
    RECOMMENDATIONS = (
        (None,'--please select--'),
        ('major', 'Major Revision'),
        ('minor', 'Minor Revision'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )
    application = models.ForeignKey(Grantapplication, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, models.DO_NOTHING)
    comments = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    score = models.IntegerField()
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATIONS)
    review_form = models.FileField(max_length=300)
    application_form = models.FileField(null=True, blank=True, max_length=300)

    class Meta:
        unique_together = (('application', 'reviewer'),)

    @property
    def get_total_marks(self):
        return int(self.score
        )
    @property
    def get_percent_mark(self):
        return int((self.get_total_marks/45)*100)

    def __str__(self):
        return str(self.get_total_marks)


class Supportingletter(models.Model):
    letter = models.FileField()
    application = models.ForeignKey(Grantapplication, on_delete=models.CASCADE)

class ProjectBudget(models.Model):
    """file for the project budget."""
    project_budget = models.FileField()
    application = models.ForeignKey(Grantapplication, on_delete=models.CASCADE)
