from django.db import models
from datetime import datetime
from contacts.models import User
from hrm.models import Department
from django.utils import timezone


class Unit(models.Model):
    department = models.ForeignKey(Department, models.DO_NOTHING)
    unit_name = models.CharField(max_length=191)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.unit_name


class Resultarea(models.Model):
    result_area = models.CharField(max_length=191)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.result_area


class Sourceoffunding(models.Model):
    fund_name = models.CharField(max_length=191)
    created_by = models.ForeignKey(User, models.DO_NOTHING,  blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.fund_name


class Indicatorcategory(models.Model):
    category = models.CharField(max_length=191)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class FinancialYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    quarter_one_start_date = models.DateField()
    quarter_one_end_date = models.DateField()
    quarter_two_start_date = models.DateField()
    quarter_two_end_date = models.DateField()
    quarter_three_start_date = models.DateField()
    quarter_three_end_date = models.DateField()
    quarter_four_start_date = models.DateField()
    quarter_four_end_date = models.DateField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.start_date, self.end_date)


class Workplan(models.Model):
    workplan_name = models.CharField(max_length=500)
    # remove work plan type as work plan is the secretariat and activities are individual work plans
    financial_year = models.ForeignKey(FinancialYear, models.DO_NOTHING)
    department = models.ForeignKey(Resultarea, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.financial_year, self.department, self.unit)


class Activity(models.Model):
    workplan = models.ForeignKey(Workplan, models.DO_NOTHING)
    activity_name = models.CharField(max_length=191)
    from_date = models.DateTimeField(blank=False, null=True)
    to_date = models.DateTimeField(blank=False, null=True)
    budget = models.FloatField(blank=True, null=True)
    sourceoffunding = models.ForeignKey('Sourceoffunding', models.DO_NOTHING)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    @property
    def getduration(self):
        return int((self.to_date - self.from_date).days)

    def __str__(self):
        return self.activity_name

class Expectedoutput(models.Model):
    activity = models.ForeignKey(Activity,models.CASCADE)
    output = models.FloatField()
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.output)

class ActivityOutput(models.Model):
    activity = models.ForeignKey(Activity, models.DO_NOTHING)
    output = models.FloatField(blank=False, null=False)
    description= models.TextField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return str(self.output)+ ' ' + str(self.activity)

class Indicator(models.Model):
    activity = models.ForeignKey(Activity, models.DO_NOTHING)
    indicator = models.CharField(max_length=191)
    target_output = models.CharField(max_length=191)
    unit_of_measure = models.FloatField()
    means_of_verification = models.TextField()
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Task(models.Model):
    PRIORITY_CHOICES = (
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low')
    )
    task_name = models.CharField(max_length=191)
    activity = models.ForeignKey(Activity,models.CASCADE)
    task_description = models.TextField()
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    expectedoutput = models.PositiveIntegerField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    lead = models.ForeignKey(User, models.DO_NOTHING, related_name='leading_tasks')
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    @property
    def getduration(self):
        return int((self.end_date - self.start_date).days)

    @property
    def running_days(self):
        return int((datetime.now().date() - self.start_date).days)
    
    @property
    def calculate_percentage(self):
        return ((self.running_days/self.getduration)*100)

    def __str__(self):
        return self.task_name


class TaskReport(models.Model):
    Status = (
        ('not_started', 'Not started'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('failed','Failed'))
    task = models.ForeignKey(Task, models.CASCADE,related_name='task')
    status =models.CharField(choices=Status,max_length=50)
    has_file=models.BooleanField()
    task_file = models.FileField(null=True, blank=True)
    reported_on = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.status


class TaskUser(models.Model):
    task = models.ForeignKey(Task, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='tasks')
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Milestone(models.Model):
    milestone = models.CharField(max_length=191)
    milestone_date = models.DateField()
    task = models.ForeignKey(Task, models.DO_NOTHING)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Taskreporting(models.Model):
    report_title = models.CharField(max_length=191)
    reporting_date = models.DateField()
    quarter = models.CharField(max_length=191)
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING)
    task = models.ForeignKey(Task, models.DO_NOTHING)
    output_target = models.CharField(max_length=191)
    status = models.IntegerField()
    percentage_progress = models.CharField(max_length=191)
    target_met = models.IntegerField()
    target_numbers = models.CharField(max_length=191)
    description_of_achievement = models.CharField(max_length=191)
    attachment = models.FileField()
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='reports')
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Framework(models.Model):
    particular=models.TextField()

    def __str__(self):
        return self.particular

class FrameWorkUnit(models.Model):
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.unit


class FrameworkResult(models.Model):
    NKNOWN_YES_NO = (
    (True, "Yes"),
    (False, "No"),
)
    framework=models.ForeignKey(Framework,on_delete=models.CASCADE)
    result=models.TextField()
    key_performance_indicator=models.CharField(max_length=300)
    is_core=models.BooleanField(choices=NKNOWN_YES_NO)
    unit_of_measure=models.ForeignKey(FrameWorkUnit,on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    baseline=models.CharField(max_length=300)
    target = models.CharField(max_length=200)
    actual=models.CharField(max_length=200,blank=True,null=True)
    data_source = models.CharField(max_length=200)
    collection_method=models.CharField(max_length=200)
    rating_scale_methodology=models.TextField()
    responsible_staff=models.CharField(max_length=100)
    collection_frequency=models.CharField(max_length=50)

    def __str__(self):
        return self.framework