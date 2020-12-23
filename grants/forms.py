import datetime

from django import forms
from .models import Grant, GrantComment

from calls.models import Call
from contacts.models import User,Student
from common.choices import NA_YES_NO



class GrantForm(forms.ModelForm):
    #teams_queryset = []

    pi = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='PIs').order_by('first_name', 'last_name')
    )

    
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all().order_by('user__first_name', 'user__last_name'),required=False
    )
    
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    new_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    has_reports = forms.ChoiceField(choices = NA_YES_NO,
                              initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)


    def __init__(self, *args, **kwargs):
     
        super(GrantForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[0:3]
        self.fields['project_objectives'].widget.attrs.update({'rows': '2'})
        self.fields['summary'].widget.attrs.update({'rows': '2'})
        self.fields['theme'].widget.attrs.update({'rows': '2'})
        self.fields['value_chain'].widget.attrs.update({'rows': '2'})
        self.fields['collaborators'].widget.attrs.update({'rows': '2'})
        self.fields['collaborators'].required=False
        self.fields['approval_status'].required = True if self.instance else False # initially, we have a default
        self.fields['approval_status'].readonly = False if self.instance else True
       # self.fields['grant_application'].empty_label = None
        self.fields['pi'].empty_label = None
            

        if not self.instance:
            self.fields['call'].queryset = Call.objects.filter(end_date__gte=datetime.date.today())

      
        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+91-123-456-7890"
            else:
                value.widget.attrs['placeholder'] = value.label
        
    class Meta:
        model = Grant
        exclude = ['grant_year','generated_number']

class GrantCommentForm(forms.ModelForm):
    grant = forms.IntegerField()
    created_by = forms.IntegerField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),required=False)
    class Meta:
        model = GrantComment
        fields = ('grant','created_by','comment')

class GrantApprovalForm(forms.ModelForm):
    #teams_queryset = []

    
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all().order_by('user__first_name', 'user__last_name'),required=False
    )
    
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    #new_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    has_reports = forms.ChoiceField(choices = NA_YES_NO,
                              initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)


    def __init__(self, *args, **kwargs):
     
        super(GrantApprovalForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[0:3]
        self.fields['project_objectives'].widget.attrs.update({'rows': '2'})
        #self.fields['summary'].widget.attrs.update({'rows': '2'})
        #self.fields['theme'].widget.attrs.update({'rows': '2'})
        #self.fields['value_chain'].widget.attrs.update({'rows': '2'})
        self.fields['collaborators'].widget.attrs.update({'rows': '2'})
        self.fields['collaborators'].required=False
      
            
        
    class Meta:
        model = Grant
        exclude = ['grant_application','title','summary','theme','pi','approval_status','approved_by','grant_id','is_expired','new_end_date','duration','value_chain','report_number','grant_year','generated_number']