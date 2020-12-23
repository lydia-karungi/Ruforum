import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from calls.models import Call
from common.choices import MONTHS, PAST_YEARS
from common.choices import NA_YES_NO
from contacts.models import User
from .models import (
    Scholarshipapplication, Otherscholarshipapplication, Othereducation,
    Employmenthistory, Referenceletter, Transcriptfile,
    Mastercardscholarshipapplication, Scholarshipappreview, Parent,
    Mastercardeducation, Typeoffloor, Typeofhousewall,
    Typeofroofingmaterial, Householdincomesource,
    Leadershipposition, Workexperience, ResearchAndPublication, Publication, Scholarship
)


# from .custom_layout_object import *


class SelectCallForm(forms.ModelForm):
    call = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
                                  queryset=Call.objects.filter(
                                      scholarship_type__isnull=False,
                                      submission_deadline__gte=datetime.date.today()
                                  )
                                  )

    class Meta:
        model = Scholarshipapplication
        fields = ['call']

    def __init__(self, *args, **kwargs):
        super(SelectCallForm, self).__init__(*args, **kwargs)
        self.fields['call'].empty_label = "---please select---"


class ScholarshipForm(forms.ModelForm):
    call = forms.ModelChoiceField(
        queryset=Call.objects.filter(
            scholarship_type__isnull=False,
            submission_deadline__gte=datetime.date.today()
        )
    )
    date_of_birth = forms.DateField(
        required=True,

        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS, attrs={'class': 'form-control, input-group'}))

    def __init__(self, *args, **kwargs):
        super(ScholarshipForm, self).__init__(*args, **kwargs)
        self.fields['call'].empty_label = None
        self.fields['call'].attrs = {'readonly': True}
        self.fields['gender'].attrs = {'required': True}
        self.fields['english_in_high_school'].label = 'Was English your language of instruction in High school?'
        self.fields['scholarship_call_source'].label = "How did you learn about this scholarship call?"
        self.fields[
            'passport_no'].help_text = 'Please include National Identity Card Number/Passport number/Birth certificate number'
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

        # self.fields['other_universities'].widget.attrs.update({'rows': '8'})

    # file size validation function
    def clean_content(self):
        content = self.cleaned_data['content']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content

    class Meta:
        model = Scholarshipapplication
        exclude = ['user', 'application_date','state']


class MastercardscholarshipapplicationForm(forms.ModelForm):
    type_of_floor = forms.ModelChoiceField(
        queryset=Typeoffloor.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    type_of_house_wall = forms.ModelChoiceField(
        queryset=Typeofhousewall.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    type_of_roofing = forms.ModelChoiceField(
        queryset=Typeofroofingmaterial.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'roof_type'}),
        required=True
    )
    village_of_residence = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    district_of_residence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    sketch_map = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file clearablefileinput',
                                                               'type': 'file'}), required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Applicant Expression of Study Interest',

                'name_of_university',
                css_id='study-interest',
                css_class='form-fieldset-group'
            ),
            Fieldset(
                'Applicant Biodata (as applicable in your National Registration Documents)',

                HTML('<h4>Place of birth</h4>'),
                'village_of_birth',
                'district_of_birth',
                'country_of_birth',
                HTML('<h5>Residence contact address</h5>'),
                'village_of_residence',
                'district_of_residence',
                'country_of_residence',
                'nearest_major_road',
                'sketch_map',
                'telephone_contacts',
                'telephone_owner',
                css_id='biodata',
                css_class='form-control'
            ),
            Fieldset(
                'Family Background and History',
                'name_of_guardian_or_spouse',
                'guardian_or_spouse_phone',
                'guardian_relationship',
                'guardian_occupation',
                'number_of_siblings',
                css_id='background',
                css_class='form-fieldset-group'
            ),
            Fieldset(
                "Applicant's Education Background",
                'primary_certificate',
                'secondary_certificate',
                'tertiary_certificate',
                'university_certificate',
                css_id='education-background',
                css_class='form-fieldset-group'
            ),
            Fieldset(
                'Family associated Information',
                'income_contrib3efc',
                'own_livestock',
                'number_of_donkeys',
                'number_of_camels',
                'number_of_chickens',
                'number_of_cattle',
                'number_of_goats',
                'number_of_sheep',
                'electricity',
                'toilet_type',
                'how_many_share_toilet',
                'water_source',
                'other_water_source',
                'distance_to_the_source',
                'type_of_roofing',
                'other_roofing',
                'type_of_house_wall',
                'other_house_wall',
                'type_of_floor',
                'other_floor',
                'home_assets',
                'other_assets',
                'income_source_1',
                'income_source_2',
                'income_source_3',
                'income_source_4',
                'rooms_in_house',
                'people_in_house',
                'pending_high_school_balances',
                css_id='family',
                css_class='form-fieldset-group'

            ),
            Fieldset(
                'Leadership experience and participation in community activities',
                'held_leadership_position'
                'community_service_participation',
                'currently_volunteering',
                'experience',
                'challenge',

                'sector_1',
                'other_sector_1',
                'sector_2',
                'other_sector_2',
                'sector_3',
                'other_sector_3',
            ),
            Fieldset(
                'Work Experience (to be filled by Postgraduate and Masters Applicants Only)',
                'degree_program',
                'gpa'
                'institution',
                'year_of_completion',
                'most_significant_contribution',
                'employer_support',
                'letter_of_endorsement',
                css_id='work-experience',
                css_class='form-fieldset-group'
            ),
            Fieldset(
                'Other information',
                'have_physical_disability',
                'physical_disability',
                'have_history_of_chronic_illness',
                'history_of_chronic_illness',
                'have_been_arrested',
                'cause_of_arrest',
                'english_in_high_school',
                'scholarship_call_source',
                'other_call_source',
                css_id='other-info',
                css_class='form-control'
            ),
            Fieldset(
                'Sworn Statements',
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn btn-lg btn-success')
                ),
                css_id='statements',
                css_class='form-fieldset-group'
            )
        )
        super(MastercardscholarshipapplicationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields['type_of_roofing'].empty_label = None
            self.fields['type_of_house_wall'].empty_label = None
            self.fields['type_of_floor'].empty_label = None
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices = field.choices[0:]

    class Meta:
        model = Mastercardscholarshipapplication
        exclude = ['scholarshipapplication_ptr']
        labels = {
            'passport_no': 'Passport / ID Number',
            'primary_certificate': 'Primary level',
            'secondary_certificate': 'Secondary level',
            'tertiary_certificate': 'Tertiary level (TVET or Technical college)',
            'university_certificate': 'University (only for those applying for Masters)',
            'name_of_guarian_or_spouse': 'Guardian / spouse',
            'guardian_or_spouse_phone': 'Guardian / spouse phone',
            'guardian_occupation': "Guardian or Spouse's occupation",
            'income_contrib3efc': 'Who among the following contribute the most to the household income?',
            'own_livestock': 'Does your household own livestock?',
            'electricity': 'Is your family house connected to electricity?',
            'toilet_type': 'What type of toilet do you have?',
            'how_many_share_toilet': 'How many people share this toilet?',
            'water_source': 'What is your major water source for household use?',
            'distance_to_the_source': 'Distance to the source (km)',
            'type_of_roofing': 'Type of Roofing material for your house',
            'home_assets': 'Which of the following assets do you have in your home?',
            'rooms_in_house': 'Number of rooms in the house',
            'people_in_house': 'Number of people living in the house',
            'pending_high_school_balances': 'After high school, did you ever have any pending school fees balances?',
            'held_leadership_position': 'Have you held any leadership position in your life time?',
            'experience': 'Using concrete examples, briefly describe your experience in relation to agriculture, livestock, and natural resources.',
            'challenge': 'What is the most important challenge or problem that you have faced in your life, and how did you overcome or solve it?',
            'most_significant_contribution': 'Describe your most significant contribution to each of the organizations you have listed above',
            'employer_support': 'Do you have full support of your current employer to undertake graduate studies through full release?',
            'have_physical_disability': 'Do you have any physical disability?',
            'have_history_of_chronic_illness': 'Do you have any past medical history of chronic illness',
            'have_been_arrested': 'Have you ever been arrested and/or convicted by a court of Law (apart from a traffic offense)',

            'scholarship_call_source': 'How did you learn about this scholarship call?',
            'gpa': 'Grade'
        }
        widgets = {
            'income_contrib3efc': forms.CheckboxSelectMultiple,
            'home_assets': forms.CheckboxSelectMultiple,
            'pending_high_school_balances': forms.Select(attrs={'class': 'form-control'}),
            'held_leadership_position': forms.Select(attrs={'class': 'form-control'}),
            'employer_support': forms.Select(attrs={'class': 'form-control'}),
            'have_physical_disability': forms.Select(attrs={'class': 'form-control'}),
            'have_history_of_chronic_illness': forms.Select(attrs={'class': 'form-control'}),
            'have_been_arrested': forms.Select(attrs={'class': 'form-control'}),
            'english_in_high_school': forms.RadioSelect,
            'own_livestock': forms.Select(attrs={'class': 'form-control'}),
            'electricity': forms.Select(attrs={'class': 'form-control'}),
            'telephone_contacts': PhoneNumberPrefixWidget(
                attrs={'class': 'form-control', 'style': 'width: 50%; display: inline-block;'}),
            'guardian_or_spouse_phone': PhoneNumberPrefixWidget(
                attrs={'class': 'form-control', 'style': 'width: 50%; display: inline-block;'}),
            'name_of_university': forms.TextInput(attrs={'class': 'form-control'}),
            'village_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_birth': forms.Select(attrs={'class': 'form-control'}),
            'country_of_residence': forms.Select(attrs={'class': 'form-control'}),
            'nearest_major_road': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_owner': forms.TextInput(attrs={'class': 'form-control'}),
            'income_source_1': forms.TextInput(attrs={'class': 'form-control'}),
            'toilet_type': forms.Select(attrs={'class': 'form-control'}),
            'name_of_guardian_or_spouse': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_siblings': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            # 'village_of_residence':forms.TextInput(attrs={'class':'form-control'},required = True),

        }


class FormsetMixin():
    def __init__(self, *args, **kwargs):
        super(FormsetMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class HouseholdincomesourceForm(FormsetMixin, forms.ModelForm):
    source = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Householdincomesource
        exclude = ['application']


HouseholdincomesourceFormSet = inlineformset_factory(Scholarshipapplication, Householdincomesource,
                                                     form=HouseholdincomesourceForm, extra=1, max_num=5, can_delete=True)


class LeadershippositionForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Leadershipposition
        exclude = ['application', ]


LeadershippositionFormSet = inlineformset_factory(Scholarshipapplication, Leadershipposition,
                                                  form=LeadershippositionForm, extra=1, max_num=10, can_delete=True)


class WorkexperienceForm(FormsetMixin, forms.ModelForm):
    organisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    employed_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    employed_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                  required=False)

    class Meta:
        model = Workexperience
        exclude = ['application', ]


WorkexperienceFormSet = inlineformset_factory(Scholarshipapplication, Workexperience,
                                              form=WorkexperienceForm, extra=1, max_num=10, can_delete=True)


class ParentForm(FormsetMixin, forms.ModelForm):
    date_of_death = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS, attrs={'class': 'form-control'}))
    disability = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                 required=False)
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    status = forms.ChoiceField(choices=Parent.PARENT_STATUSES,
                               widget=forms.Select(attrs={'class': 'form-control parent_status'}), required=True)
    occupation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    organisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    gross_annual_income = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]

    class Meta:
        model = Parent
        exclude = ['application', 'relationship']


ParentFormSet = inlineformset_factory(Scholarshipapplication, Parent,
                                      form=ParentForm, extra=2, max_num=2, can_delete=False)


class MastercardeducationForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Mastercardeducation
        exclude = ['application']


MastercardeducationFormSet = inlineformset_factory(Scholarshipapplication, Mastercardeducation,
                                                   form=MastercardeducationForm, extra=1, max_num=10, can_delete=False)


class ScholarshipappreviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                              required=True)

    class Meta:
        model = Scholarshipappreview
        exclude = ['reviewed_on', 'application', 'reviewer', ]

    def __init__(self, *args, **kwargs):
        super(ScholarshipappreviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            self.fields['review_form'].widget.attrs.update({'class': 'form-control-file'})
            self.fields['concept_note'].widget.attrs.update({'class': 'form-control-file'})


class OtherForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS, attrs={'class': 'form-control'}))
    telephone_contacts = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: none;'}),
        required=True,
        initial='+256'
        )
    employer_support = forms.ChoiceField(choices=NA_YES_NO,
                                         initial='', widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=True)
    support_evidence = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file',
                                                                     'type': 'file'}), required=False)
    have_additional_funding = forms.ChoiceField(choices=NA_YES_NO,
                                                initial='', widget=forms.Select(attrs={'class': 'form-control'}),
                                                required=True)

    already_funded = forms.ChoiceField(choices=NA_YES_NO,
                                       initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        # account_view = kwargs.pop('account', False)
        # request_user = kwargs.pop('request_user', None)
        super(OtherForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]
        # self.fields['other_skills'].widget.attrs.update({'rows': '2'})
        self.fields['support_evidence'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['research_concept_note'].widget.attrs.update({'class': 'form-control-file'})
        # self.fields['non_university_partners'].widget.attrs.update({'rows': '8'})
        # self.fields['other_departments'].widget.attrs.update({'rows': '8'})
        # self.fields['other_universities'].widget.attrs.update({'rows': '8'})

    class Meta:
        model = Otherscholarshipapplication
        exclude = ['scholarshipapplication_ptr']


class EducationForm(forms.ModelForm):
    qualification = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    major = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # country = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}),required=True)
    total_score = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    date_from = forms.DateField(required=False,
                                widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS,
                                                              attrs={'class': 'form-control',
                                                                     'style': 'display: inline-block; width: auto;'}))
    date_to = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS,
                                      attrs={'class': 'form-control', 'style': 'display: inline-block; width: auto;'}))

    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'type': 'file'}), required=True)

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'required': True})

    class Meta:
        model = Othereducation
        exclude = ['application']


EducationFormSet = inlineformset_factory(Scholarshipapplication, Othereducation,
                                         form=EducationForm, min_num=1, extra=0, max_num=10, can_delete=True)


class ResearchAndPublicationsForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Select(choices=ResearchAndPublication.Code, attrs={'class': 'form-control'}),
                           label="Level", required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                  required=False)

    class Meta:
        model = ResearchAndPublication
        exclude = ['application', ]


ResearchFormSet = inlineformset_factory(Scholarshipapplication, ResearchAndPublication,
                                        form=ResearchAndPublicationsForm, min_num=1, max_num=10, extra=0)


class PublicationsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Publication
        exclude = ['application', ]


PublicationsFormSet = inlineformset_factory(Scholarshipapplication, Publication,
                                            form=PublicationsForm, min_num=1, max_num=10, extra=0)


class EmploymenthistoryForm(forms.ModelForm):
    organisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    organisation_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    reason_for_leaving = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),
                                         required=False)
    employed_from = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS,
                                      attrs={'class': 'form-control', 'style': 'display: inline-block; width: auto;'}))
    employed_to = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(months=MONTHS, years=PAST_YEARS,
                                      attrs={'class': 'form-control', 'style': 'display: inline-block; width: auto;'}))
    professional_responsibilities = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)

    class Meta:
        model = Employmenthistory
        exclude = ['major', 'application']


EmploymenthistoryFormSet = inlineformset_factory(Scholarshipapplication, Employmenthistory,
                                                 form=EmploymenthistoryForm, min_num=1,max_num=10, extra=0)


class ReferenceletterForm(forms.ModelForm):
    referee_names = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    referee_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                      required=True)
    contact_details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                      required=True)
    file = forms.FileField(label="reference letter")

    class Meta:
        model = Referenceletter
        exclude = ['application']


ReferenceletterFormSet = inlineformset_factory(
    Scholarshipapplication, Referenceletter, form=ReferenceletterForm, extra=0, min_num=1, max_num=10, can_delete=True
)


class TranscriptfileForm(forms.ModelForm):
    file = forms.FileField(label="Academic Document")

    class Meta:
        model = Transcriptfile
        exclude = ['application']


TranscriptfileFormSet = inlineformset_factory(
    Scholarshipapplication, Transcriptfile, form=TranscriptfileForm,
    extra=0, min_num=1, can_delete=True
)


# scholarship reviewer form


class ScholarshipReviewerForm(forms.ModelForm):
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='mark_scholarship_applications'
        ).distinct()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ScholarshipReviewerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Scholarshipapplication
        fields = [
            'reviewers'
        ]


class ScholarshipApprovalForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    selected_for_funding_comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 5, 'cols': 30}), required=False)

    def __init__(self, *args, **kwargs):

        super(ScholarshipApprovalForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Scholarship
        exclude = ['application', 'student', 'report_number',  'approved_by', 'approval_status', 'scholarship_year',
                   'generated_number']


class ScholarshipApplicationRejectForm(forms.ModelForm):
    selected_for_funding_comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 5, 'cols': 30}), required=False)
    
    class Meta:
        model = Scholarshipapplication
        fields = [
            'selected_for_funding','selected_for_funding_comments'
        ]

    def __init__(self, *args, **kwargs):
        super(ScholarshipApplicationRejectForm, self).__init__(*args, **kwargs)
        self.initial['selected_for_funding_comments'] = 'After double reviewing your application by external reviewers, we regret to inform you that your application did not go through. We however, encourage you to apply for subsequent calls.'


class ScholarshipapplicationValidationForm(forms.ModelForm):
    COMPLIANCE_CHOICES = (
        ('c', 'Compliant'),
        ('nc', 'Non compliant')
    )
    TRUE_FALSE_CHOICES = (
        (None, '--please select--'),
        (True, 'Yes'),
        (False, 'No')
    )
    compliance_comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                          required=False)
    compliant = forms.ChoiceField(choices=COMPLIANCE_CHOICES, widget=forms.RadioSelect())
    validated_academic_document = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                                    choices=TRUE_FALSE_CHOICES, initial="Unknown", label="validated Academic Documents")
    validated_reference_letters = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                                choices=TRUE_FALSE_CHOICES, initial="Unknown")
   
   

    class Meta:
        model = Scholarshipapplication
        fields = [
            'compliance_comments',
            'validated_academic_document',
            'validated_reference_letters'
        ]


class ScholarshipValidatorForm(forms.ModelForm):
    validators = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            groups__permissions__codename='validate_scholarship_applications'
        ).distinct()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ScholarshipValidatorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Scholarshipapplication
        fields = [
            'validators'
        ]

class EditScholarshipForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    class Meta:
        model = Scholarship
        exclude = ['generated_number','scholarship_year','approved_by']
