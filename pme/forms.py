from django import forms
"""
Forms module for small small hr
"""
from datetime import datetime, time
from common.choices import YES_NO

from django.contrib.auth.models import Group
from django import forms
from django.conf import settings
from contacts.models import User
from django.db.models import Q
from django.utils.translation import ugettext as _

import pytz
from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from .models import (
    Unit, Sourceoffunding, Resultarea, FinancialYear, Workplan,
    Activity, Expectedoutput, Task, Indicator,ActivityOutput,TaskReport,Framework,
    FrameWorkUnit,FrameworkResult
)

class UnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = None 
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Unit
        exclude = ['created_by', 'created_at', 'updated_at']


class SourceoffundingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SourceoffundingForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Sourceoffunding
        exclude = ['created_by', 'created_at', 'updated_at']


class ResultareaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResultareaForm, self).__init__(*args, **kwargs)
        self.fields['result_area'].label = "Flagship" 
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            


    class Meta:
        model = Resultarea
        exclude = ['created_by', 'created_at', 'updated_at']


class FinancialYearForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    quarter_one_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    quarter_one_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_two_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_two_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_three_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_three_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_four_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))
    quarter_four_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-contro', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(FinancialYearForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = FinancialYear
        exclude = ['created_by', 'created_at', 'updated_at']


class WorkplanForm(forms.ModelForm):
    workplan_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    #description= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
     
    def __init__(self, *args, **kwargs):
        super(WorkplanForm, self).__init__(*args, **kwargs)
        self.fields['financial_year'].empty_label = None 
        self.fields['department'].empty_label = None 
        self.fields['unit'].empty_label = None 
        for name, field in self.fields.items():
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
            if 'date' in name:
                field.widget.attrs = {"class": "form-control date"}
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Workplan
        exclude = ['created_by', 'created_at', 'updated_at']


class ActivityForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['workplan'].empty_label = '--please select--'
        self.fields['sourceoffunding'].empty_label = '--please select--'
        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control"}
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Activity
        exclude = ['created_by', 'created_at', 'updated_at']


class ExpectedoutputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpectedoutputForm, self).__init__(*args, **kwargs)
        self.fields['activity'].empty_label = None
        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control date"}
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Expectedoutput
        exclude = ['created_by', 'created_at', 'updated_at']


class TaskForm(forms.ModelForm):
    lead = forms.ModelChoiceField(
        queryset=User.objects.filter(
            groups__name__in=['Staff', 'Administrative/HR', 'Planning, Monitoring & Evaluation']
        )
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control date', 'type': 'date'}),required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control date', 'type': 'date'}),required=True)
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['activity'].empty_label = None
        self.fields['lead'].empty_label = None
        self.fields['unit'].empty_label = None
        for name, field in self.fields.items():
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Task
        exclude = ['created_by', 'created_at', 'updated_at']

class TaskReportForm(forms.ModelForm):
    has_file = forms.ChoiceField(choices = YES_NO, 
        initial='', widget=forms.Select(attrs={'class':'form-control'}), required=True)
    task_file =forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)
    task = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=Task.objects.all())
    
    status = forms.CharField(widget=forms.Select(choices=TaskReport.Status, attrs={'class': 'form-control','required':True}))
    def __init__(self,*args,**kwargs):
        super(TaskReportForm,self).__init__(*args,**kwargs)
       # self.fields['task'].empty_label=None
        for name, field in self.fields.items():
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices =field.choices[1:]
         

    class Meta:
        model = TaskReport
        exclude=['reported_on']


class IndicatorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.fields['activity'].empty_label = None
        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control date"}
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Indicator
        exclude = ['created_by', 'created_at', 'updated_at']


class ActivityOutputForm(forms.ModelForm):
    activity = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=Activity.objects.all())
    output = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}))
    activity.empty_label=None

    class Meta:
        model = ActivityOutput
        exclude = ['created_by']

class FrameworkForm(forms.ModelForm):
    particular= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}))

    class Meta:
        model =Framework
        exclude = []


class FrameWorkUnitForm(forms.ModelForm):


    class Meta:
        model =FrameWorkUnit
        exclude = []

    def __init__(self, *args, **kwargs):
        super(FrameWorkUnitForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control date"}
                continue
            field.widget.attrs = {"class": "form-control"}


class FrameworkResultForm(forms.ModelForm):


    class Meta:
        model =FrameworkResult
        exclude = []

    def __init__(self, *args, **kwargs):
        super(FrameworkResultForm, self).__init__(*args, **kwargs)
        self.fields['framework'].empty_label=None
        self.fields['unit_of_measure'].empty_label=None
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]

