from django import forms

from common.choices import YES_NO
from contacts.models import Student
from grants.models import Studentmembership, Grant
from .models import ProjectEvent


class ProjectEventForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    event_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                        required=False)

    class Meta:
        model = ProjectEvent
        exclude = ['organiser']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectEventForm, self).__init__(*args, **kwargs)
        self.fields['grant'].empty_label = '--please select--'
        self.fields['grant'].queryset = Grant.objects.filter(pi=self.request.user)


class StudentEnrollmentForm(forms.ModelForm):
    Support_type = forms.CharField(required=False, widget=forms.Select(choices=Studentmembership.Support,
                                                                       attrs={'class': 'form-control', 'required': ''}))
    study_year = forms.CharField(required=False, widget=forms.Select(choices=Studentmembership.Years,
                                                                     attrs={'class': 'form-control', 'required': ''}))

    class Meta:
        model = Studentmembership
        exclude = ['enrollment_date', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentEnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['grant'].widget.attrs.update({'class': 'form-control'})
        self.fields['grant'].queryset = Grant.objects.filter(pi=self.request.user)
        self.fields['grant'].empty_label = None


# used a different for cause some fields are supposed not to be required 

class StudentEnrollForm(forms.ModelForm):
    class Meta:
        model = Studentmembership
        exclude = ['enrollment_date', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentEnrollForm, self).__init__(*args, **kwargs)


class ApplicantEnrollmentForm(forms.ModelForm):
    grant = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
                                   queryset=Grant.objects.all())
    Support_type = forms.CharField(required=False, widget=forms.Select(choices=Studentmembership.Support,
                                                                       attrs={'class': 'form-control', 'required': ''}))
    study_year = forms.CharField(required=False, widget=forms.Select(choices=Studentmembership.Years,
                                                                     attrs={'class': 'form-control', 'required': ''}))

    class Meta:
        model = Studentmembership
        exclude = ['pi', 'enrollment_date', 'student']

    def __init__(self, user, *args, **kwargs):
        super(ApplicantEnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['grant'].queryset = Grant.objects.filter(pi=user.id)
