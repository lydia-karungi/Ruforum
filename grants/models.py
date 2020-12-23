import datetime

from django.db import models

from calls.models import Call
from contacts.models import User

from dateutil.rrule import rrule, DAILY, WEEKLY, HOURLY
from dateutil.relativedelta import relativedelta, MO, SU
from grants_applications.models import Grantapplication
from django.utils import timezone
from contacts.models import Student

class APPROVAL_CHOICES:
    APPROVED = 'approved'
    NOT_APPROVED = 'not_approved'
    CHOICES = (
        (APPROVED, 'Approved'),
        (NOT_APPROVED, 'Not Approved')
    )


class Grant(models.Model):
    PERIOD_CHOICES = (
        (None,'--please select'),
        (3, '3 Months'),
        (6, '6 Months'),
        (9, '9 Months'),
        (12, '12 Months'),
        (15, '15 Months'),
        (18, '18 Months'),
        (21, '21 Months'),
    )
    PERIOD_CHOICES6 = (
        (3, '6 Months'),
        (6, '12 Months'),
        (9, '18 Months'),
        (12, '24 Months'),
        (15, '30 Months'),
    )
    grant_application = models.ForeignKey(Grantapplication, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=256)
    summary = models.TextField()
    budget = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    new_end_date = models.DateField(blank=True, null=True)
    theme = models.TextField(null=True, blank=True)
    value_chain = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, help_text='''To be computed from Start and End Date''')
    pi = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='grants', help_text='''Principal Investigator''')
    approval_status = models.CharField(max_length=30, choices=APPROVAL_CHOICES.CHOICES, default=APPROVAL_CHOICES.NOT_APPROVED)
    approved_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='approvals')
    grant_id = models.CharField(max_length=50, blank=True, null=True)
    project_objectives = models.TextField()
    collaborators = models.TextField()
    #keywords = models.CharField(max_length=150)
    grant_year = models.CharField(max_length=20)
    generated_number = models.IntegerField(null=True,default=1)
    has_reports = models.BooleanField()
    reporting_period = models.PositiveIntegerField( choices=PERIOD_CHOICES,blank=True,null=True)
    report_number = models.PositiveIntegerField(blank=True,null=True)
    students = models.ManyToManyField(Student, through='StudentMembership', blank=True)
    is_expired = models.BooleanField(default=False)

    def effective_end_date(self):
        return self.new_end_date if self.new_end_date else self.end_date #in case a grant extension was set, use the extension deadline as end-date

    def compute_duration(self):
        start_date = self.start_date
        end_date = self.effective_end_date()
        if start_date is not None and end_date is not None:
            span = end_date - start_date
            return span.days
        else:
            return 0 #where 0 means, "invalid/problematic"

    def compute_days_past(self):
        if self.start_date is not None:
            start_date = self.start_date
            end_date = datetime.date.today()
            span = end_date - start_date
            return span.days
        else:
            return 0

    def update_duration(self, commit=False):
        self.duration = self.compute_duration()

        #since expiry depends on duration, we can as well update it here...
        if self.start_date is not None:
            self.is_expired = self.compute_days_past() > self.duration if self.duration > 0 else False

        if commit:
            self.save()



    def show_maturity(self):
        age = self.compute_days_past()
        dur = self.compute_duration()
        left = dur - age
        end_date = self.effective_end_date()
        if left >= 0:
            return '''%(status)s<br/>Days: %(age)s/%(dur)s : %(left)s left''' % {'status':'ACTIVE', 'age': age, 'dur':dur, 'left': left}
        else:
            return '''%(status)s<br/>since %(exp)s''' % {'status':'EXPIRED', 'exp': end_date}

    def save(self, *args, **kwargs):
        # ensure we update duration to correct val...
        self.update_duration()
        super(Grant,self).save(*args, **kwargs)

    def is_active(self):
        '''
        @JWL: Isaac indicates the RIMS spec considers a grant "active" when it's approval_status is "approved"
        '''
        return True if self.approval_status == APPROVAL_CHOICES.APPROVED else False

    @staticmethod
    def count_all_active():
        '''returns the total number of all active grants'''
        return Grant.objects.filter(approval_status=APPROVAL_CHOICES.APPROVED).count()

    def pi_reports(self):
        reports = []
        reports.append({'month': self.reporting_period, 'report': self.firstreport})
        reports.append({'month': self.reporting_period*2, 'report': self.month12report})
        reports.append({'month': self.reporting_period*3, 'report': self.month18report})
        reports.append({'month': self.reporting_period*4, 'report': self.month24report})
        reports.append({'month': self.reporting_period*5, 'report': self.month30report})
        reports.append({'month': self.reporting_period * 6, 'report': self.month36report})
        reports.append({'month': self.reporting_period*7, 'report': self.lastreport})

        return reports

    def month6_due_date(self):
        return self.start_date + relativedelta(months=6)

    def __str__(self):
         return  str(self.grant_id)



class GrantComment(models.Model):
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name='grant_comments')
    comment = models.TextField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='grant_comments')


class Studentmembership(models.Model):
    Years=(
        ('first','First'),
        ('second','Second'),
        ('third','Third'),
        ('fourth','Fourth'),
        ('fifth','Fifth'),
        ('sixth','Sixth'),
        ('seventh','Seventh'),
                              )
    Support = (
        ('research_only', 'Research only'),
        ('research_and_tuition', 'Research and Tuition'),
        ('tution_only', 'Tuition only'),)
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    study_year = models.CharField(max_length=20, choices=Years,default='first')
    Support_type = models.CharField(max_length=20, choices=Support,default='research_and_tuition')
    enrollment_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('student', 'grant'),)

    def __str__(self):
         return  '{} {} {}'.format(self.grant,self.student,self.Support_type)
