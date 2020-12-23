import datetime

from django.db import models

from contacts.models import User
from common.choices import COUNTRY_CHOICES

from dateutil.rrule import rrule, DAILY, WEEKLY, HOURLY
from dateutil.relativedelta import relativedelta, MO, SU

class APPROVAL_CHOICES:
    APPROVED = 'approved'
    NOT_APPROVED = 'not_approved'
    CHOICES = (
        (APPROVED, 'Approved'),
        (NOT_APPROVED, 'Not Approved')
    )

class Fellowship(models.Model):
    
    title = models.CharField(max_length=256)
    summary = models.TextField()
    budget = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    new_end_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=0, help_text='''To be computed from Start and End Date''')
    pi = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='fellowships', help_text='''Principal Investigator''')
    approval_status = models.CharField(max_length=30, choices=APPROVAL_CHOICES.CHOICES, default=APPROVAL_CHOICES.NOT_APPROVED)
    approved_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='fellowship_approvals')
    fellowship_id = models.CharField(max_length=30, blank=True, null=True)
    students = models.ManyToManyField(User, through='FellowshipStudentMembership', blank=True)
    is_expired = models.BooleanField(default=False)

    def effective_end_date(self):
        return self.new_end_date if self.new_end_date else self.end_date #in case a fellowship extension was set, use the extension deadline as end-date

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
        super(Fellowship,self).save(*args, **kwargs)

    def is_active(self):
        '''
        @JWL: Isaac indicates the RIMS spec considers a fellowship "active" when it's approval_status is "approved"
        '''
        return True if self.approval_status == APPROVAL_CHOICES.APPROVED else False

    @staticmethod
    def count_all_active():
        '''returns the total number of all active fellowships'''
        return Fellowship.objects.filter(approval_status=APPROVAL_CHOICES.APPROVED).count()

    def pi_reports(self):
        reports = []

        #try:
        reports.append({'month': 6, 'report': self.month6report})
        reports.append({'month': 12, 'report': self.month12report})
        reports.append({'month': 18, 'report': self.month18report})
        reports.append({'month': 24, 'report': self.month24report})
        reports.append({'month': 30, 'report': self.month30report})
        #except:
        #    pass

        return reports

    def month6_due_date(self):
        return self.start_date + relativedelta(months=6)


class FellowshipComment(models.Model):
    fellowship = models.ForeignKey(Fellowship, models.DO_NOTHING, related_name='fellowship_comments')
    comment = models.TextField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='fellowship_comments')


class FellowshipStudentmembership(models.Model):
    fellowship = models.ForeignKey(Fellowship, models.DO_NOTHING)
    student = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        unique_together = (('student', 'fellowship'),)

