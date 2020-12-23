import datetime

from django import forms
from django.forms.models import inlineformset_factory

from .models import Fellowshipapplication, Fellowshipappreview
from contacts.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from calls.models import FellowshipCall

class ProfileForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Please select country'
        self.fields['gender'].empty_label = [('', 'please select gender')]+ GENDER_CHOICES
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['business_address'].widget.attrs.update({'rows': '2'})

    class Meta:
        model = User
        exclude = []


class FellowshipProfileForm(forms.ModelForm):
    mobile=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: none;'}),
                required=True,
                initial='+256'
                            )
    business_tel= PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: none;'}),
                required=True,
                initial='+256'
                            )
    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
        super(FellowshipProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
        self.fields['mobile'].empty_label = None
        self.fields['business_address'].widget.attrs.update({'rows': '2'})
        self.fields['cv'].widget.attrs.update({'class':'form-control-file'})


    class Meta:
        model = User
        fields = [
            'title',
            'first_name',
            'last_name',
            'gender',
            'country',
            'nationality',
            'mobile',
            'business_tel',
            'business_address',
            'institution',
            'highest_qualification',
            'area_of_specialisation',
            'cv',
        ]


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from .custom_layout_object import *



class FellowshipapplicationForm(forms.ModelForm):
    call = forms.ModelChoiceField(
        queryset=FellowshipCall.objects.filter(
            submission_deadline__gte=datetime.date.today()),
    )
    telephone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: none;'}),
                required=False,
                initial='+256'
                            )
    proposed_begining = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    proposed_end = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
        super(FellowshipapplicationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['country'].empty_label = None
        self.fields['call'].empty_label = None
        self.fields['letter_of_release'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['address'].widget.attrs.update({'rows': '2'})
        self.fields['cv'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['proposed_value'].widget.attrs.update({'rows': '2'})
        self.fields['other_activities'].widget.attrs.update({'rows': '2'})
        self.fields['motivation'].widget.attrs.update({'rows': '12'})
        self.fields['comment'].widget.attrs.update({'rows': '2'})


    class Meta:
        model = Fellowshipapplication
        exclude = [
            'user',
            'state',
            'last_modified',
            'ref_number',
            'reviewers'
       ]


class FellowshipappreviewForm(forms.ModelForm):

    comments= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    class Meta:
        model = Fellowshipappreview
        exclude = ['date', 'application', 'reviewer',]

    def __init__(self, *args, **kwargs):

        super(FellowshipappreviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            self.fields['review_form'].widget.attrs.update({'class': 'form-control-file'})

            #field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]

#FellowshipCarpappreviewForm
class FellowshipCarpappreviewForm(forms.ModelForm):
    qn1_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn2_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn3_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn4_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn5_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn6_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn7_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn8_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn9_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn10_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn11_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn12_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn13_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn14_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn15_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn16_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn17_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    qn18_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    comments= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    strength_and_opportunity= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    major_improvements= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)


    class Meta:
        model = Fellowshipappreview
        exclude = ['date', 'application', 'reviewer']

    def __init__(self, *args, **kwargs):

        super(FellowshipCarpappreviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

class FellowshipapplicationReviewersForm(forms.ModelForm):
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='change_fellowshipappreview'
        ).distinct()
    )

    class Meta:
        model = Fellowshipapplication
        fields = [
            'reviewers'
        ]
#Select Fellowship call form
class SelectCallForm(forms.ModelForm):
    call = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control','placeholder':'Select' }),
        queryset=FellowshipCall.objects.filter(
            submission_deadline__gte=datetime.date.today()
        )
    )

    class Meta:
        model = Fellowshipapplication
        fields = ['call']

    def __init__(self, *args, **kwargs):
        super(SelectCallForm, self).__init__(*args, **kwargs)
        self.fields['call'].empty_label = None


class FellowshipapplicationValidatorsForm(forms.ModelForm):
    validators = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='can_validate_fellowship'
            
        ).distinct()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(FellowshipapplicationValidatorsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fellowshipapplication
        fields = [
            'validators'
        ]

class FellowshipapplicationValidateForm(forms.ModelForm):
    COMPLIANCE_CHOICES = (
        ('c', 'Compliant'),
        ('nc', 'Non compliant')
    )
    TRUE_FALSE_CHOICES=(
        (None, '--please select--'),
        (True, 'Yes'),
        (False, 'No')
    )
    compliance_comments= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    compliant = forms.ChoiceField(choices=COMPLIANCE_CHOICES, widget=forms.RadioSelect())
    validated_home_institute=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_host_institute = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_letter_of_release = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_cv = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    
    class Meta:
        model = Fellowshipapplication
        fields = [
            'compliance_comments',
            'validated_home_institute',
            'validated_host_institute',
            'validated_letter_of_release',
            'validated_cv',
         
        ]