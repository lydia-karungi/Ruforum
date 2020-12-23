from django.db import models
from django.contrib import auth
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from common.choices import COUNTRY_CHOICES, GENDER_CHOICES
from phonenumber_field.modelfields import PhoneNumberField
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime

from grant_types.models import Granttype

API_KEY = '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'


class Student(models.Model):
    DEGREE_PROGRAM_LEVELS = (
        ('msc', 'Msc'),
        ('phd', 'PhD'),
        ('mphil', 'MPhil'),
        ('bachelor', 'Bachelor'),
    )
    STUDENT_TYPE = (
        ('other', 'OTHER'),
        ('regional_programs', 'Regional Programs'),
        ('competitive_grants', 'Competitive Grants'),
    )
    YEAR_CHOICES = (
        (year, year) for year in range(datetime.date.today().year, 1990 - 1, -1)
    )

    user = models.OneToOneField('User', models.DO_NOTHING)
    student_no = models.CharField(max_length=64, unique=True, null=True, editable=False)
    year_of_birth = models.CharField(max_length=4)
    university = models.CharField(max_length=100)
    university_department = models.CharField(max_length=64)
    university_reg_no = models.CharField(max_length=20)
    degree_program_level = models.CharField(max_length=8, choices=DEGREE_PROGRAM_LEVELS)
    degree_program_name = models.CharField(max_length=64)
    intake_year = models.CharField(max_length=4)
    grad_expected = models.DateField(blank=True, null=True)
    grad_actual = models.DateField(blank=True, null=True)
    thesis_title = models.CharField(max_length=256)
    cohort = models.IntegerField(blank=True, null=True)
    supervisor1 = models.CharField(max_length=128)
    supervisor2 = models.CharField(max_length=128)
    supervisor3 = models.CharField(max_length=128)
    research_abstract = models.TextField()
    funder = models.CharField(max_length=100, null=True, blank=True)
    grant_type = models.ForeignKey(Granttype, models.DO_NOTHING, null=True)
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPE, default='other')
    graduated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


class Studentfundingsource(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    funder = models.TextField()
    items = models.CharField(max_length=60)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(str(self.student), self.funder)


class MyUserManager(BaseUserManager):
    def create_user(self, business_email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not business_email:
            raise ValueError('Users must have an email address')

        user = self.model(
            business_email=self.normalize_email(business_email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, business_email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            business_email=business_email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    TITLE_CHOICES =(
        ('mr', 'Mr'),
        ('ms','Mrs'),
        ('miss','Miss'),
        ('dr','Dr'),
        ('prof','Prof')

    )
    '''
    This model represents the application user, the business email is used as the
    user name during login'''
    password = models.CharField(max_length=128, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    business_email = models.CharField(unique=True, max_length=254)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(choices=TITLE_CHOICES, max_length=32)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    contact_type = models.CharField(max_length=32, blank=True)
    passport_no = models.CharField(_('Passport Number'),max_length=16, blank=True)
    home_address = models.TextField()
    business_address = models.TextField(blank=True)
    country = models.CharField(max_length=64, choices=COUNTRY_CHOICES)
    nationality = models.CharField(max_length=64, choices=COUNTRY_CHOICES)
    job_title = models.CharField(max_length=64, blank=True)
    institution = models.CharField(max_length=128)
    area_of_specialisation = models.CharField(max_length=128)
    personal_email = models.CharField(max_length=254, blank=True)
    skype_id = models.CharField(max_length=32, blank=True)
    yahoo_messenger = models.CharField(max_length=32, blank=True)
    msn_id = models.CharField(max_length=32, blank=True)
    home_tel = models.CharField(max_length=20, blank=True)
    business_tel = PhoneNumberField()
    mobile = PhoneNumberField()
    fax = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    picture = models.FileField(blank=True, null=True)
    cv = models.FileField(blank=True, null=True)
    department = models.CharField(max_length=128, blank=True)
    highest_qualification = models.CharField(max_length=128)
    email_confirmed = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'business_email'
    EMAIL_FIELD = 'business_email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = (
            ("can_validate_grant_application", "Can validate grant application"),
            ("can_validate_fellowship", "can Validate Fellowship"),
            ("can_view_contacts", "Can view contacts"),
            ("can_edit_contacts", "can edit contacts"),
            ("can_delete_contacts", "can delete contacts"),
        )

    def __str__(self):
        return self.get_full_name()

    '''
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    '''

    def has_perm(user, perm, obj=None):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, 'has_perm'):
                continue
            try:
                if backend.has_perm(user, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_module_perms(user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, 'has_module_perms'):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False

    '''
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True
    '''
    
    def get_full_name(self):
        return str(self.first_name) +' '+str(self.last_name)+ ' ('+str(self.business_email)+')'

    @property
    def role(self):
        roles = [group.name for group in self.groups.all()]
        return ', '.join(roles)

    def email_user(self, subject, message):
        message = Mail(
            from_email='nonereply@ruforum.org',
            to_emails=self.business_email,
            subject=subject,
            html_content=message)
        try:
            sg = SendGridAPIClient(API_KEY)  # os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
