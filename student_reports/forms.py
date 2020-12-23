from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import (
    Studentreport, Otherstudentreport, Milestone, Publicationattachment,Products,AdditionInformation,
    Briefsattachment, Manuscript, SupervisorDetails, ResearchInformation,SkillsImprovement
)
from contacts.models import User, Student

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit



class StudentreportForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentreportForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4

        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Studentreport
        exclude = ['student', 'period', 'state', 'submitted_on']


class FormsetMixin():
    def __init__(self, *args, **kwargs):
        super(FormsetMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class MilestoneForm(FormsetMixin, forms.ModelForm):

    due_date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    completed_date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    completed = forms.CharField(widget=forms.Select(choices=Milestone.YES_NO, attrs={'class': 'form-control','required':True}))
    
    def __init__(self, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4
                field.widget.attrs['required']=True

    class Meta:
        model = Milestone
        exclude = ['report', 'milestone_type']

MilestoneFormSet = inlineformset_factory(Studentreport, Milestone,
                                            form=MilestoneForm, extra=len(Milestone.MILESTONE_TYPES), can_delete=False)


class PublicationForm(FormsetMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            #print(type(field.widget))
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4

    class Meta:
        model = Publicationattachment
        exclude = ['report']

PublicationFormSet = inlineformset_factory(Studentreport, Publicationattachment,
                                            form=PublicationForm, extra=1, can_delete=False)


class BriefForm(FormsetMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BriefForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            #print(type(field.widget))
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4

    class Meta:
        model = Briefsattachment
        exclude = ['report']

BriefFormSet = inlineformset_factory(Studentreport, Briefsattachment,
                                            form=BriefForm, extra=1, can_delete=False)


class ManuscriptForm(FormsetMixin, forms.ModelForm):
    publication_date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control date', 'type': 'date'}),required=False)

    def __init__(self, *args, **kwargs):
        super(ManuscriptForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control",'required':'false'}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
            #print(type(field.widget))
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4




    class Meta:
        model = Manuscript
        exclude = ['report']

ManuscriptFormSet = inlineformset_factory(Studentreport, Manuscript,
                                            form=ManuscriptForm, extra=1, can_delete=False)


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
               'Personal Information',
               HTML('<h6>This information will be saved in your profile. Changing it will affect future applications </h6>'),
               Div('title',css_class='col-md-8'),
               Div('first_name',css_class='col-md-8'),
               Div('last_name',css_class='col-md-8'),
               Div('gender',css_class='col-md-8'),
               Div('contact_type',css_class='col-md-8'),
               Div('passport_no',css_class='col-md-8'),
               Div('home_address',css_class='col-md-8'),
               Div('business_address',css_class='col-md-8'),
               Div('business_email',css_class='col-md-8'),
               Div('country',css_class='col-md-8'),
               Div('nationality',css_class='col-md-8'),
               Div('job_title',css_class='col-md-8'),
               Div('institution',css_class='col-md-8'),
               Div('department',css_class='col-md-8'),
               Div('highest_qualification',css_class='col-md-8'),
               Div('area_of_specialisation',css_class='col-md-8'),
               Div('personal_email',css_class='col-md-8'),
               Div('skype_id',css_class='col-md-8'),
               Div('yahoo_messenger',css_class='col-md-8'),
               Div('msn_id',css_class='col-md-8'),
               Div('home_tel',css_class='col-md-8'),
               Div('business_tel',css_class='col-md-8'),
               Div('mobile',css_class='col-md-8'),
               Div('fax',css_class='col-md-8'),
               Div('notes',css_class='col-md-12'),
                css_id = 'study-interest',
                css_class='row'
            )
        )
        self.helper.form_tag = False
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            if type(field.widget) == forms.Textarea:
                 field.widget.attrs['rows'] = 4

    class Meta:
        model = User
        fields = [
            'title',
            'first_name',
            'last_name',
            'gender',
            'contact_type',
            'passport_no',
            'home_address',
            'business_address',
            'business_email',
            'country',
            'nationality',
            'job_title',
            'institution',
            'department',
            'highest_qualification',
            'area_of_specialisation',
            'personal_email',
            'skype_id',
            'yahoo_messenger',
            'msn_id',
            'home_tel',
            'business_tel',
            'mobile',
            'fax',
            'notes',

        ]


class StudentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
      
        self.helper.layout = Layout(
            Fieldset(
                'Student Information',
                Div('year_of_birth',css_class='col-md-8'),
                Div('university',css_class='col-md-8'),
                Div('university_department',css_class='col-md-8'),
                Div('university_reg_no',css_class='col-md-8'),
                Div('degree_program_level',css_class='col-md-8'),
                Div('degree_program_name',css_class='col-md-8'),
                Div('intake_year',css_class='col-md-8'),
                Div('grad_expected',css_class='col-md-8'),
                Div('grad_actual',css_class='col-md-8'),
                Div('thesis_title',css_class='col-md-8'),
                Div('cohort',css_class='col-md-8'),
                Div('supervisor1',css_class='col-md-8'),
                Div('supervisor2',css_class='col-md-8'),
                Div('supervisor3',css_class='col-md-8'),
                Div('grant_type',css_class='col-md-8'),
                Div('student_type',css_class='col-md-8'),
                Div('research_abstract',css_class='col-md-12'),
                 css_class='row'
            )
        )
        self.helper.form_tag = False
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['supervisor3'].required= False

    class Meta:
        model = Student
        exclude = ['user']

class SupervisorDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Student Support',
                Div('name',css_class='col-md-8'),
                Div('title',css_class='col-md-8'),
                Div('area_of_mentorship',css_class='col-md-8'),
                Div('areas_of_achievement',css_class='col-md-8'),
                Div('areas_required_more_attention_and_support',css_class='col-md-8'),
                Div('address',css_class='col-md-8'),
                 css_class='row'
            )
        )
        
        self.helper.form_tag = False
        super(SupervisorDetailsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SupervisorDetails
        fields = [
            'name',
            'title',
            'area_of_mentorship',
            'areas_of_achievement',
            'areas_required_more_attention_and_support',
            'address',
            ]

class ResearchInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Research Information',
                Div('research_summary',css_class='col-md-8'),
                Div('location',css_class='col-md-8'),
                Div('number_of_stakeholders',css_class='col-md-8'),
                Div('type_of_farming_communities',css_class='col-md-8'),
                Div('number_of_actors_that_are_non_farmers',css_class='col-md-8'),
                Div('Your_champion_technology',css_class='col-md-8'),
                Div('activities_executed',css_class='col-md-8'),
                Div('scientists_in_your_institution',css_class='col-md-8'),
                Div('technicians_in_your_institution',css_class='col-md-8'),
                Div('fellow_students',css_class='col-md-8'),
                Div('others',css_class='col-md-8'),
                Div('benefits_for_institution',css_class='col-md-8'),
                Div('critical_issues',css_class='col-md-8'),
                Div('skills_required',css_class='col-md-8'),
                Div('challenges_encountered',css_class='col-md-8'),
                Div('plan_during_the_next_reporting_period',css_class='col-md-8'),
                 css_class='row'
            )
        )
        
        self.helper.form_tag = False
        super(ResearchInformationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ResearchInformation
        fields = [
            'research_summary',
            'location',
            'number_of_stakeholders',
            'type_of_farming_communities',
            'number_of_actors_that_are_non_farmers',
            'Your_champion_technology',
            'activities_executed',
            'scientists_in_your_institution',
            'technicians_in_your_institution',
            'fellow_students',
            'others',
            'benefits_for_institution',
            'critical_issues',
            'skills_required',
            'challenges_encountered',
            'plan_during_the_next_reporting_period',
            ]



class SkillsImprovementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Skills Improvement',
                Div('brief_farm_description',css_class='col-md-8'),
                Div('short_courses_attended',css_class='col-md-8'),
                Div('courses_objectives',css_class='col-md-8'),
                Div('evaluate_the_course_delivery',css_class='col-md-8'),
                Div('self_evaluation',css_class='col-md-8'),
                Div('areas_of_improvement',css_class='col-md-8'),
                 css_class='row'
            )
        )
        
        self.helper.form_tag = False
        super(SkillsImprovementForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SkillsImprovement
        fields = [
            'brief_farm_description',
            'short_courses_attended',
            'courses_objectives',
            'evaluate_the_course_delivery',
            'self_evaluation',
            'areas_of_improvement',
            ]


class ProductsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Products',
                Div('innovation_produced',css_class='col-md-8'),
                Div('publications',css_class='col-md-8'),
                Div('conference_papers',css_class='col-md-8'),
                Div('presentations',css_class='col-md-8'),
                Div('funding_from_other_sources',css_class='col-md-8'),
                 css_class='row'
            )
        )
        
        self.helper.form_tag = False
        super(ProductsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Products
        fields = [
            'innovation_produced',
            'publications',
            'conference_papers',
            'presentations',
            'funding_from_other_sources',
            ]


class AdditionInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'AdditionInformation',
                Div('futureplans_or_feedback',css_class='col-md-8'),
                 css_class='row'
            )
        )
        
        self.helper.form_tag = False
        super(AdditionInformationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AdditionInformation
        fields = [
            'futureplans_or_feedback',
            ]



class OtherstudentreportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Project Information',
                'challenges',
                'benefited_count',
                'new_technology',
                'technology_use',
                'trainings',
                'skills_use',
                'spillovers',
                'significant_change',
                'accomplishments',
                'workplace',
                'other_info',
            )
        )
        self.helper.form_tag = False
        super(OtherstudentreportForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            #print(type(field.widget))
            if type(field.widget) == forms.Textarea:
                field.widget.attrs['rows'] = 4

    class Meta:
        model = Otherstudentreport
        exclude = ['studentreport_ptr']
        labels = {
            'challenges': 'What challenges, issues or difficulties are you encountering?',
            'benefited_count': 'How many farmers / target beneficiaries have you shared your technology / new approach with? 0-1000',
            'new_technology': 'Provide a brief description of the technology or new approach that you have developed.',
            'technology_use': 'How will this technology or new approach be used to improve current farmer problems or agricultural problems?',

            'trainings': 'What skill enhancement trainings have you attended?',
            'skills_use': 'How are you using the skills gained from the skills enhancement trainings?',
            'spillovers': 'Are there any spillover effects as a result of your MSc / PhD research e.g Linkages with other organizations or researchers of grants',
            'significant_change': 'What is the Most Significant Change of the training and research on you',
            'accomplishments': 'If you graduated what have you been able to accomplish so far in your career',
            'workplace': 'Where are you working now that you have graduated',
            'other_info': 'Please provide any other relevant information',
        }
