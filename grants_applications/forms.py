import datetime

from django import forms
from django.forms.models import inlineformset_factory

from .models import Grantapplication, Collaborator, Supportingletter, Grantappreview,ProjectBudget
from contacts.models import User
from calls.models import GrantCall
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from .custom_layout_object import *

class ProfileForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
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


class GrantProfileForm(forms.ModelForm):
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
        super(GrantProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
        self.fields['mobile'].empty_label = None
        self.fields['business_address'].widget.attrs.update({'rows': '2'})
        self.fields['cv'].widget.attrs.update({'class':'form-control-file'},required = True)


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




class GrantapplicationForm(forms.ModelForm):

    call = forms.ModelChoiceField(
        queryset=GrantCall.objects.filter(
            submission_deadline__gte=datetime.date.today(),
            grant_type__isnull=False),
    )
    business_tel=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}),
                required=True,
                initial='+256'
                            )
    mobile=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}),
                required=True,
                initial='+256'
                            )

    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
        super(GrantapplicationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['call'].empty_label = None
        self.fields['country'].empty_label = None
        self.fields['non_university_partners'].widget.attrs.update({'rows': '2'})
        self.fields['other_departments'].widget.attrs.update({'rows': '2'})
        self.fields['other_universities'].widget.attrs.update({'rows': '2'})
        self.fields['application_form'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['project_budget'].widget.attrs.update({'class': 'form-control-file'})
        #self.fields['results_framework'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['total_budget'].widget.attrs.update({'class': 'form-control'},required = True)
        self.fields['supporting_letter_from_university'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['cv'].widget.attrs.update({'class':'form-control-file'},required = True)

    class Meta:
        model = Grantapplication
        exclude = [
            'user',
            'status',
            'last_modified',
            'ref_number',
            'reviewers',
            
       ]

class GrantapplicationUpdateForm(forms.ModelForm):

    call = forms.ModelChoiceField(
        queryset=GrantCall.objects.filter(
            submission_deadline__gte=datetime.date.today(),
            grant_type__isnull=False),
    )
    business_tel=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}),
                required=True,
                initial='+256'
                            )
    mobile=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}),
                required=True,
                initial='+256'
                            )

    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
        super(GrantapplicationUpdateForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['call'].empty_label = None
        self.fields['country'].empty_label = None
        self.fields['non_university_partners'].widget.attrs.update({'rows': '2'},required = False)
        self.fields['other_departments'].widget.attrs.update({'rows': '2'}, required = True)
        self.fields['other_universities'].widget.attrs.update({'rows': '2'}, required = True)

    class Meta:
        model = Grantapplication
        exclude = [
            'user',
            'state',
            'last_modified',
            'ref_number',
            'reviewers','title','last_name','institution','highest_qualification'
            
       ]

class GrantappreviewForm(forms.ModelForm):
    
    comments= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    class Meta:
        model = Grantappreview
        exclude = ['date',  'reviewer']

    def __init__(self, *args, **kwargs):

        super(GrantappreviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            #self.fields['recommendation'].empty_label = None

#GrantCarpappreviewForm
class GrantCarpappreviewForm(forms.ModelForm):
    comments= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    strength_and_opportunity= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)
    major_improvements= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=False)


    class Meta:
        model = Grantappreview
        exclude = ['date', 'application', 'reviewer',]

    def __init__(self, *args, **kwargs):

        super(GrantCarpappreviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            self.fields['review_form'].widget.attrs.update({'class': 'form-control-file'})
            self.fields['application_form'].widget.attrs.update({'class':'form-cotrol-file'})
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]

class GrantapplicationValidateForm(forms.ModelForm):
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
    validated_university_letter=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_main_proposal = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_uploaded_templates = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_phd = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_total_budget = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    validated_member_university = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }),choices=TRUE_FALSE_CHOICES,initial="Unknown")
    class Meta:
        model = Grantapplication
        fields = [
            'compliance_comments',
            'validated_phd',
            'validated_total_budget',
            'validated_member_university',
            'validated_university_letter',
            'validated_uploaded_templates',
            'validated_main_proposal'
        ]
    

class GrantapplicationReviewersForm(forms.ModelForm):
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='review_grant_applications'
        ).distinct()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(GrantapplicationReviewersForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Grantapplication
        fields = [
            'reviewers'
        ]


class GrantapplicationValidatorsForm(forms.ModelForm):
    validators = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='can_validate_grant_application'
            
        ).distinct()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(GrantapplicationValidatorsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Grantapplication
        fields = [
            'validators', 'grant_manager'
        ]

class GrantapplicationRejectForm(forms.ModelForm):
    
    class Meta:
        model = Grantapplication
        fields = [
            'selected_for_funding'
        ]

class CollaboratorForm(forms.ModelForm):
    cv = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'type': 'file'}),required=False)

    class Meta:
        model = Collaborator
        exclude = ['application']


CollaboratorFormSet = inlineformset_factory(
    Grantapplication, Collaborator, form=CollaboratorForm,
    fields=['cv'], extra=1, can_delete=True
    )

class SupportingletterForm(forms.ModelForm):
    letter = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'type': 'file'}),required=True)


    class Meta:
        model = Supportingletter
        exclude = ['application']

SupportingletterFormSet = inlineformset_factory(
    Grantapplication, Supportingletter, form=SupportingletterForm,
    fields=['letter'], extra=1, can_delete=True
    )

class ProjectBudgetForm(forms.ModelForm):
    project_budget=forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'type': 'file'}),required=True)

    class Meta:
        model = ProjectBudget
        exclude = ['application']


ProjectBudgetFormSet = inlineformset_factory(
    Grantapplication, ProjectBudget, form=ProjectBudgetForm,
    fields=['project_budget'], extra=1, can_delete=True
    )


#Select Grant call form
class SelectCallForm(forms.ModelForm):
    call = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control','placeholder':'Select' }),
        queryset=GrantCall.objects.filter(
             grant_type__isnull=False,
            submission_deadline__gte=datetime.date.today()
        )
    )

    class Meta:
        model = Grantapplication
        fields = ['call']

    def __init__(self, *args, **kwargs):
        super(SelectCallForm, self).__init__(*args, **kwargs)
        self.fields['call'].empty_label = None