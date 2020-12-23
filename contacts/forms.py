import datetime

from crispy_forms.helper import FormHelper
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from common.choices import YEAR_CHOICES
from common.choices import YES_NO
from contacts.models import User, Student
from grant_types.models import Granttype


class ContactForm(forms.ModelForm):
    
    home_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    business_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    job_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    business_tel = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True, initial='+256')
    mobile = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True, initial='+256')
   
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 30}),
                            required=False)
  
    class Meta:
        model = User
        fields = [
            'title',
            'business_email',
            'first_name',
            'last_name',
            'personal_email',
            'home_address',
            'business_address',
            'country',
            'nationality',
            'gender',
            'contact_type',
            'passport_no',
            'job_title',
            'institution',
            'area_of_specialisation',
            'home_tel',
            'business_tel',
            'mobile',
            'fax',
            'skype_id',
            'yahoo_messenger',
            'msn_id',
            'notes',
            'picture',
            'cv'
        ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices = field.choices[1:]


class StudentForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                  queryset=User.objects.filter(groups__name='Applicants'))
    year_of_birth = forms.CharField(required=False, widget=forms.Select(choices=YEAR_CHOICES,
                                                                        attrs={'class': 'form-control'}))
    university = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    university_department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                            label='Department')
    university_reg_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                        label='University Registration No.')
    degree_program_level = forms.CharField(required=False, widget=forms.Select(choices=Student.DEGREE_PROGRAM_LEVELS,
                                                                               attrs={'class': 'form-control'}))
    degree_program_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    intake_year = forms.CharField(required=False, widget=forms.Select(choices=Student.YEAR_CHOICES,
                                                                      attrs={'class': 'form-control'}))
    grad_expected = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    label='Expected Graduation date')
    grad_actual = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                  label='Actual Graduation Date', required=False)
    thesis_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    cohort = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    supervisor1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                  label='Supervisor 1')
    supervisor2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                  label='Supervisor 2')
    supervisor3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                  label='Supervisor 3')
    research_abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),
                                        required=False)
    grant_type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=Granttype.objects.all())
    student_type = forms.CharField(required=False, widget=forms.Select(choices=Student.STUDENT_TYPE,
                                                                       attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        exclude = ['graduated']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['grant_type'].empty_label = '--please select--'
        self.fields['user'].empty_label = '--please select--'
        self.helper = FormHelper()


class UpdateStudentForm(forms.ModelForm):
    YEAR_CHOICES2 = ((year, year) for year in range(datetime.date.today().year, 1980 - 1, -1))
    Intake_year = ((year, year) for year in range(datetime.date.today().year, 1990 - 1, -1))
    user = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                  queryset=User.objects.filter(groups__name='Students'))
    year_of_birth = forms.CharField(required=False,
                                    widget=forms.Select(choices=YEAR_CHOICES2,
                                                        attrs={'class': 'form-control', 'required': ''}))
    university = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': ''}), required=True)
    university_department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
                                            required=True)
    university_reg_no = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
                                        required=True)
    degree_program_level = forms.CharField(required=False,
                                           widget=forms.Select(choices=Student.DEGREE_PROGRAM_LEVELS,
                                                               attrs={'class': 'form-control', 'required': ''}))
    degree_program_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    intake_year = forms.CharField(required=False, widget=forms.Select(choices=Intake_year,
                                                                      attrs={'class': 'form-control', 'required': ''}))
    grad_expected = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    grad_actual = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    thesis_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    cohort = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    supervisor1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    supervisor2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    supervisor3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    research_abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                        required=False)
    grant_type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=Granttype.objects.all())
    student_type = forms.CharField(required=False, widget=forms.Select(choices=Student.STUDENT_TYPE,
                                                                       attrs={'class': 'form-control', 'required': ''}))
    graduated = forms.ChoiceField(choices=YES_NO,
                                  initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Student
        exclude = []

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UpdateStudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
