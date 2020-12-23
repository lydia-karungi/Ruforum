import datetime

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from grants.models import Grant

from .models import (FirstReport, FirstStudentReport, Month12Report, Studentmonth12Report, Technology,
                     Month18Report, Studentmonth18Report, Month24Report, Month30Report, Month36Report, Month42Report,
                     Month48Report, Month54Report, Month60Report, Month66Report, Month72Report, Month78Report,
                     Month84Report, Month90Report, Month96Report, Month102Report, Month108Report,
                     Studentmonth24Report, LastReport, LastStudentReport, Studentmonth30Report, Studentmonth36Report,Studentmonth30Report,
                     Studentmonth42Report, Studentmonth48Report, Studentmonth54Report, Studentmonth60Report,
                     Studentmonth66Report, Studentmonth72Report, Studentmonth78Report, Studentmonth84Report,
                     Studentmonth90Report, Studentmonth96Report, Studentmonth102Report, Studentmonth108Report,
                     StudentPublication, PIPublications, RelevantPictures12, RelevantPictures18, RelevantPictures24,
                     RelevantPictures30, RelevantPictures36, RelevantPictures42, RelevantPictures48,
                     RelevantPictures54, RelevantPictures60, RelevantPictures66, RelevantPictures72,
                     RelevantPictures78, RelevantPictures84, RelevantPictures90, RelevantPictures96,
                     RelevantPictures102, RelevantPictures108, Linkage12, Linkage18, Linkage24, Linkage30, Linkage36,
                     Linkage42, Linkage48, Linkage54, Linkage60, Linkage66, Linkage72, Linkage78, Linkage84, Linkage90,
                     Linkage96, Linkage102, Linkage108, Course )


class Month6ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month6ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = FirstReport
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'recruitment_criteria_and_process': 'What was the criteria for students recruitment?',
            'recruitment_criteria_and_process_upload': 'What process was used for students recruitment?',
            'project_activities_upload': 'Against each project research objective report on: what you had planned to achieve, what you have achieved and any gaps and way forward.',
            'planned_activities_upload': 'Please upload the outline of planned activities for the next Period.',
            'progress_against_objectives': 'Briefly outline progress made towards achieving project research objectives.',
            'teamwork_and_mentoring': 'Teamwork and mentoring: Provide a list of supervisors, co-supervisors and students.',
            'problems_and_challenges': 'Provide any challenges you have encountered at project inception.',
            'modifications': 'What strategies is the PI using to ensure that students achieve deliverables and students are mentored.',
            'skills_gap': "Have you identified any skills gaps (through interactions with the students) that may not be provided through the formal training and curriculum but are critical to the students' success and timely completion of MSc training. Please indicate any plans targeted to address the identified gaps."
        }
        widgets = {
            'recruitment_criteria_and_process': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'progress_against_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_and_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'modifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'skills_gap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class EditMonth6ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditMonth6ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = FirstReport
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started','month']
        labels = {
            'recruitment_criteria_and_process': 'What was the criteria for students recruitment?',
            'recruitment_criteria_and_process_upload': 'What process was used for students recruitment?',
            'project_activities_upload': 'Against each project research objective report on: what you had planned to achieve, what you have achieved and any gaps and way forward.',
            'planned_activities_upload': 'Please upload the outline of planned activities for the next Period.',
            'progress_against_objectives': 'Briefly outline progress made towards achieving project research objectives.',
            'teamwork_and_mentoring': 'Teamwork and mentoring: Provide a list of supervisors, co-supervisors and students.',
            'problems_and_challenges': 'Provide any challenges you have encountered at project inception.',
            'modifications': 'What strategies is the PI using to ensure that students achieve deliverables and students are mentored.',
            'skills_gap': "Have you identified any skills gaps (through interactions with the students) that may not be provided through the formal training and curriculum but are critical to the students' success and timely completion of MSc training. Please indicate any plans targeted to address the identified gaps."
        }
        widgets = {
            'recruitment_criteria_and_process': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'progress_against_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_and_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'modifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'skills_gap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class FormsetMixin():
    def __init__(self, *args, **kwargs):
        super(FormsetMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class Studentmonth6ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = FirstStudentReport
        exclude = ['last_submitted']

        labels = {
            'registered': 'Has the student registered?',
            'tuition_paid': "Has the student's tuition fees been paid?",
            'tuition_paid_upload': 'Please upload the evidence for the Student Tuition Fee payment. File size limit: 300KB',
            'allocated_supervisors': 'Has the student been allocated supervisors?',
            'num_of_courses': 'How many course Units is the student  taking?',
        }
        widgets = {
            'tuition_paid_upload': forms.FileInput(attrs={'class': 'form-control-file', 'type': 'file',
                                                          'accept': 'application/pdf,image/png, image/jpeg,.doc,.docx,application/msword'}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth6ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['tuition_paid_upload'].required = False
        for field_name in self.fields:
            field = self.fields.get(field_name)


Studentmonth6ReportFormSet = inlineformset_factory(FirstReport, FirstStudentReport,
                                                   form=Studentmonth6ReportForm,extra=0, can_delete=False)


class CourseForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['student_report']


    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


CourseFormSet = inlineformset_factory(FirstReport, Course,
                                                   form=CourseForm, extra=1, can_delete=True)


class Month12ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month12ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month12Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please  report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'beneficary_group': 'Please select all beneficies groups engaged',
            'how_engaged_beneficiaries': 'How many have you engaged? ',
            'male_participants': 'How many are male?',
            'female_participants': 'How many are female?',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'participants': 'Download, fill and upload participants\' attendence',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' What are the teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'relevant_pictures_videos_2': 'Upload relevant pictures related to your research activities. (Two)',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research and Research uptake?',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

            'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures12Form(FormsetMixin, forms.ModelForm):
   
    class Meta:
        model = RelevantPictures12
        exclude = ['grant_report', ]


RelevantPictures12FormSet = inlineformset_factory(Month12Report, RelevantPictures12,
                                                  form=RelevantPictures12Form, extra=1, max_num=10, can_delete=True)


class Linkage12Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage12
        exclude = ['grant_report', ]


Linkage12FormSet = inlineformset_factory(Month12Report, Linkage12,
                                                  form=Linkage12Form, extra=1, max_num=10, can_delete=True)


class Month18ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month18ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month18Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'male_participants': 'How many are male?',
            'female_participants': 'How many are female?',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'participants': 'Download, fill and upload participants\' attendance',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

            'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures18Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures18
        exclude = ['grant_report', ]


RelevantPictures18FormSet = inlineformset_factory(Month18Report, RelevantPictures18,
                                                  form=RelevantPictures18Form, extra=1, max_num=10, can_delete=True)


class Linkage18Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage18
        exclude = ['grant_report', ]


Linkage18FormSet = inlineformset_factory(Month18Report, Linkage18,
                                                  form=Linkage18Form, extra=1, max_num=10, can_delete=True)


class Month24ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month24ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month24Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'male_participants': 'How many are male?',
            'female_participants': 'How many are female?',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'participants': 'Download, fill and upload participants\' attendance',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures24Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures24
        exclude = ['grant_report', ]


RelevantPictures24FormSet = inlineformset_factory(Month24Report, RelevantPictures24,
                                                  form=RelevantPictures24Form, extra=1, max_num=10, can_delete=True)


class Linkage24Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage24
        exclude = ['grant_report', ]


Linkage24FormSet = inlineformset_factory(Month24Report, Linkage24,
                                                  form=Linkage24Form, extra=1, max_num=10, can_delete=True)


class Month30ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month30ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month30Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'male_participants': 'How many are male?',
            'female_participants': 'How many are female?',
            'participants': 'Download, fill and upload participants\' attendance',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

            
              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures30Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures30
        exclude = ['grant_report', ]


RelevantPictures30FormSet = inlineformset_factory(Month30Report, RelevantPictures30,
                                                  form=RelevantPictures30Form, extra=1, max_num=10, can_delete=True)



class Linkage30Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage30
        exclude = ['grant_report', ]


Linkage30FormSet = inlineformset_factory(Month30Report, Linkage30,
                                                  form=Linkage30Form, extra=1, max_num=10, can_delete=True)

class Month36ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month36ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month36Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {
              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures36Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures36
        exclude = ['grant_report', ]


RelevantPictures36FormSet = inlineformset_factory(Month36Report, RelevantPictures36,
                                                  form=RelevantPictures36Form, extra=1, max_num=10, can_delete=True)


class Linkage36Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage36
        exclude = ['grant_report', ]


Linkage36FormSet = inlineformset_factory(Month36Report, Linkage36,
                                                  form=Linkage36Form, extra=1, max_num=10, can_delete=True)


class Month42ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month42ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month42Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {
            
              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures42Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures42
        exclude = ['grant_report', ]


RelevantPictures42FormSet = inlineformset_factory(Month42Report, RelevantPictures42,
                                                  form=RelevantPictures42Form, extra=1, max_num=10, can_delete=True)


class Linkage42Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage42
        exclude = ['grant_report', ]


Linkage42FormSet = inlineformset_factory(Month42Report, Linkage42,
                                                  form=Linkage42Form, extra=1, max_num=10, can_delete=True)


class Month48ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month48ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month48Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures48Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures48
        exclude = ['grant_report', ]


RelevantPictures48FormSet = inlineformset_factory(Month48Report, RelevantPictures48,
                                                  form=RelevantPictures48Form, extra=1, max_num=10, can_delete=True)


class Linkage48Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage48
        exclude = ['grant_report', ]


Linkage48FormSet = inlineformset_factory(Month48Report, Linkage48,
                                                  form=Linkage48Form, extra=1, max_num=10, can_delete=True)


class Month54ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month54ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month54Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures54Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures54
        exclude = ['grant_report', ]


RelevantPictures54FormSet = inlineformset_factory(Month54Report, RelevantPictures54,
                                                  form=RelevantPictures54Form, extra=1, max_num=10, can_delete=True)


class Linkage54Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage54
        exclude = ['grant_report', ]


Linkage54FormSet = inlineformset_factory(Month54Report, Linkage54,
                                                  form=Linkage54Form, extra=1, max_num=10, can_delete=True)


class Month60ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month60ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month60Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures60Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures60
        exclude = ['grant_report', ]


RelevantPictures60FormSet = inlineformset_factory(Month60Report, RelevantPictures60,
                             
                                                  form=RelevantPictures60Form, extra=1, max_num=10, can_delete=True)

class Linkage60Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage60
        exclude = ['grant_report', ]


Linkage60FormSet = inlineformset_factory(Month60Report, Linkage60,
                                                  form=Linkage60Form, extra=1, max_num=10, can_delete=True)

class Month66ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month66ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month66Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures66Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures66
        exclude = ['grant_report', ]


RelevantPictures66FormSet = inlineformset_factory(Month66Report, RelevantPictures66,
                                                  form=RelevantPictures66Form, extra=1, max_num=10, can_delete=True)


class Linkage66Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage66
        exclude = ['grant_report', ]


Linkage66FormSet = inlineformset_factory(Month66Report, Linkage66,
                                                  form=Linkage66Form, extra=1, max_num=10, can_delete=True)


class Month72ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month72ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month72Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

            'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures72Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures72
        exclude = ['grant_report', ]


RelevantPictures72FormSet = inlineformset_factory(Month72Report, RelevantPictures72,
                                                  form=RelevantPictures72Form, extra=1, max_num=10, can_delete=True)


class Linkage72Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage72
        exclude = ['grant_report', ]


Linkage72FormSet = inlineformset_factory(Month72Report, Linkage72,
                                                  form=Linkage72Form, extra=1, max_num=10, can_delete=True)

class Month78ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month78ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month78Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures78Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures78
        exclude = ['grant_report', ]


RelevantPictures78FormSet = inlineformset_factory(Month78Report, RelevantPictures78,
                                                  form=RelevantPictures78Form, extra=1, max_num=10, can_delete=True)


class Linkage78Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage78
        exclude = ['grant_report', ]


Linkage78FormSet = inlineformset_factory(Month78Report, Linkage78,
                                                  form=Linkage78Form, extra=1, max_num=10, can_delete=True)


class Month84ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month84ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month84Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation.',
            'problems_and_challenges_solution': 'How were these problems and challenges addressed?',
            'changes_made': 'List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures84Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures84
        exclude = ['grant_report', ]


RelevantPictures84FormSet = inlineformset_factory(Month84Report, RelevantPictures84,
                                                  form=RelevantPictures84Form, extra=1, max_num=10, can_delete=True)


class Linkage84Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage84
        exclude = ['grant_report', ]


Linkage84FormSet = inlineformset_factory(Month84Report, Linkage84,
                                                  form=Linkage84Form, extra=1, max_num=10, can_delete=True)


class Month90ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month90ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month90Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation. How were these problems and challenges addressed? List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
        }


class RelevantPictures90Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures90
        exclude = ['grant_report', ]


RelevantPictures90FormSet = inlineformset_factory(Month90Report, RelevantPictures90,
                                                  form=RelevantPictures90Form, extra=1, max_num=10, can_delete=True)


class Linkage90Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage90
        exclude = ['grant_report', ]


Linkage90FormSet = inlineformset_factory(Month90Report, Linkage90,
                                                  form=Linkage90Form, extra=1, max_num=10, can_delete=True)


class Month96ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month96ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month96Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation. How were these problems and challenges addressed? List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures96Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures96
        exclude = ['grant_report', ]


RelevantPictures96FormSet = inlineformset_factory(Month96Report, RelevantPictures96,
                                                  form=RelevantPictures96Form, extra=1, max_num=10, can_delete=True)


class Linkage96Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage96
        exclude = ['grant_report', ]


Linkage96FormSet = inlineformset_factory(Month96Report, Linkage96,
                                                  form=Linkage96Form, extra=1, max_num=10, can_delete=True)

class Month102ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month102ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month102Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives. ',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation. How were these problems and challenges addressed? List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

           
              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures102Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures102
        exclude = ['grant_report', ]


RelevantPictures102FormSet = inlineformset_factory(Month102Report, RelevantPictures102,
                                                   form=RelevantPictures102Form, extra=1, max_num=10, can_delete=True)


class Linkage102Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage102
        exclude = ['grant_report', ]


Linkage102FormSet = inlineformset_factory(Month102Report, Linkage102,
                                                  form=Linkage102Form, extra=1, max_num=10, can_delete=True)



class Month108ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Month108ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = Month108Report
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'how_student_objectives_link_to_research_objectives': 'Indicate how the students research objectives link to the project research objectives',
            'project_progress': 'Please report on the Overall Project Research Objectives.',
            'student_progress': 'Please report on the Overall Student Progress.',
            'summary_progress': 'Briefly summarize the progress made towards achieving each of your project research objectives.',
            'linkages_for_next_12_months': 'What linkages will you maintain and or initiate as part of the research in the remaining period.',
            'have_engaged_beneficiaries': 'Have you engaged any beneficiaries?',
            'number_beneficiaries': 'How many have you engaged? ',
            'direct_beneficiaries' : 'How many are direct beneficiaries',
            'indirect_beneficiaries' : 'How many are indirect beneficiries',
            'student_capacity_gaps': 'What are the students capacity gaps that need to be addressed to enable them successfully complete their research successfully.',
            'teamwork_mentoring': ' Give examples of teamwork and mentoring among the PI, co-supervisors, collaborators and students? ',
            'problems_and_challenges': 'Highlight the problems and challenges encountered during project implementation. How were these problems and challenges addressed? List the changes made, if any, to the original project implementation plan as a result of the challenges encountered. Note: Any major changes to the initial project plan must be approved by the RUFORUM Grants Manager.',
            'no_cost_extension_required': 'Do you anticipate the need for a “no-cost extension”?',
            'no_cost_extension_explained': 'Provide a justification.',
            'on_schedule': 'Is your project on schedule for completion on time? ',
            'not_on_schedule_explanation': 'Mention challenges that are likely to affect project completion within the remaining period.',
            'request_for_funds_for_year2': 'Upload your Request for funds for the Year. ',
            'audited_12_month_financial_report': 'Upload your Audited annual financial report.',
            'flyers_brochures': 'Have you produced flyers / brochures / posters ?',
            'flyers_brochures_upload': 'Please upload samples of flyers / brochures / posters.',
            'policy_briefs': 'Have you developed policy briefs?',
            'policy_briefs_upload': 'Please upload samples of these policy briefs.',
            'linkages_established': 'Describe any linkages established by the students and your research team to enhance the research.',
            'ensure_sustainability_strategies': 'What strategies will be undertaken in order to ensure sustainability or continuity of the research carried out after the project has ended?',
            'uptake_pathway': 'Explain how the findings of your research have been (or will be) applied along the uptake pathway',
            'unexpected_spillover': 'Describe any spill over benefits of your project to the various beneficiaries.',
            'field_days_organized': 'How many farmer field days/exbitions have you organised?',
            'research_to_students_field_attachment': 'Which aspects of your research can be developed into a plan for the students\' Field Attachment Activities.',
        }
        widgets = {

              'how_student_objectives_link_to_research_objectives': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'summary_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_for_next_12_months': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_capacity_gaps': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'teamwork_mentoring': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'beneficary_group': forms.CheckboxSelectMultiple,
            'project_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'student_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'no_cost_extension_explained': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'problems_and_challenges_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'changes_made': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'not_on_schedule_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'linkages_established': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'ensure_sustainability_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'uptake_pathway': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'unexpected_spillover': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_to_students_field_attachment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class RelevantPictures108Form(FormsetMixin, forms.ModelForm):
    class Meta:
        model = RelevantPictures108
        exclude = ['grant_report', ]


RelevantPictures108FormSet = inlineformset_factory(Month108Report, RelevantPictures108,
                                                  form=RelevantPictures108Form, extra=1, max_num=10, can_delete=True)


class Linkage108Form(FormsetMixin, forms.ModelForm):
    organisations= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    partners = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 3, 'cols': 30}),required=True)
    class Meta:
        model = Linkage108
        exclude = ['grant_report', ]


Linkage108FormSet = inlineformset_factory(Month108Report, Linkage108,
                                                  form=Linkage108Form, extra=1, max_num=10, can_delete=True)

class Studentmonth12ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth12Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s  progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth12ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth12ReportFormSet = inlineformset_factory(Month12Report, Studentmonth12Report,extra=0,
                                                    form=Studentmonth12ReportForm, can_delete=False)




class Studentmonth18ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth18Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth18ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth18ReportFormSet = inlineformset_factory(Month18Report, Studentmonth18Report,extra=0,
                                                    form=Studentmonth18ReportForm, can_delete=False)


class Studentmonth24ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth24Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth24ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth24ReportFormSet = inlineformset_factory(Month24Report, Studentmonth24Report,extra=0,
                                                    form=Studentmonth24ReportForm, can_delete=False)


class Studentmonth30ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth30Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth30ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth30ReportFormSet = inlineformset_factory(Month30Report, Studentmonth30Report,extra=0,
                                                    form=Studentmonth30ReportForm, can_delete=False)


class Studentmonth36ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth36Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth36ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth36ReportFormSet = inlineformset_factory(Month36Report, Studentmonth36Report,extra=0,
                                                    form=Studentmonth36ReportForm, can_delete=False)


class Studentmonth42ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth42Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth42ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
          

Studentmonth42ReportFormSet = inlineformset_factory(Month42Report, Studentmonth42Report,extra=0,
                                                    form=Studentmonth42ReportForm, can_delete=False)


class Studentmonth48ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth48Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth48ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth48ReportFormSet = inlineformset_factory(Month48Report, Studentmonth48Report,extra=0,
                                                    form=Studentmonth48ReportForm, can_delete=False)


class Studentmonth54ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth54Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth54ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth54ReportFormSet = inlineformset_factory(Month54Report, Studentmonth54Report,extra=0,
                                                    form=Studentmonth54ReportForm, can_delete=False)


class Studentmonth60ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth60Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth60ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth60ReportFormSet = inlineformset_factory(Month60Report, Studentmonth60Report,extra=0,
                                                    form=Studentmonth60ReportForm, can_delete=False)


class Studentmonth66ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth66Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth66ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth66ReportFormSet = inlineformset_factory(Month66Report, Studentmonth66Report,extra=0,
                                                    form=Studentmonth66ReportForm, can_delete=False)


class Studentmonth72ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth72Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth72ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth72ReportFormSet = inlineformset_factory(Month72Report, Studentmonth72Report,extra=0,
                                                    form=Studentmonth72ReportForm, can_delete=False)


class Studentmonth78ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth78Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth78ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth78ReportFormSet = inlineformset_factory(Month78Report, Studentmonth78Report,extra=0,
                                                    form=Studentmonth78ReportForm, can_delete=False)


class Studentmonth84ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth84Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth84ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth84ReportFormSet = inlineformset_factory(Month84Report, Studentmonth84Report,extra=0,
                                                    form=Studentmonth84ReportForm, can_delete=False)


class Studentmonth90ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth90Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth90ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth90ReportFormSet = inlineformset_factory(Month90Report, Studentmonth90Report,extra=0,
                                                    form=Studentmonth90ReportForm, can_delete=False)


class Studentmonth96ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth96Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth96ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth96ReportFormSet = inlineformset_factory(Month96Report, Studentmonth96Report,extra=0,
                                                    form=Studentmonth96ReportForm, can_delete=False)


class Studentmonth102ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth102Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth102ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth102ReportFormSet = inlineformset_factory(Month102Report, Studentmonth102Report,extra=0,
                                                    form=Studentmonth102ReportForm, can_delete=False)


class Studentmonth108ReportForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Studentmonth108Report
        exclude = ['last_submitted']

        labels = {
            'passed_second_courses': 'Has the student passed all courses registered for in this semester?',
            'done_academic_requirements': 'Has the student fulfilled the academic requirements for this period?',
            'number_of_retakes': 'If not, how many retakes/additional courses does the student have to do?',
            'retakes_registration_date': 'When will the student register for these retakes / additional courses? ',
            'defended_proposal': 'Has the student developed and defended his/her proposal at department level?',
            'defended_proposal_delay_explanation': 'If not, please indicate what is causing delays.',
            'research_objectives': 'List the student research objectives.',
            'progress_as_planned': 'Are the student\'s research activities on schedule as planned? ',
            'research_progress': 'Briefly describe the student\'s research progress to date against each of his/her objectives.',
            'thesis_submission_external': 'Has student completed his/her thesis submission for external examination?',
            'thesis_defense': 'Has student completed his/her thesis defense?',
            'thesis_submission': 'Has student completed his/her thesis final submission?',
            'submission_delay_explanation': 'If any of the answers to the above questions is "No" please indicate what is causing delays',
        }
        widgets = {
            'retakes_registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defended_proposal_delay_explanation': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'submission_delay_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }

    def __init__(self, *args, **kwargs):
        super(Studentmonth108ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)
            # if field and isinstance(field , forms.TypedChoiceField):
            #     field.choices = field.choices[1:]


Studentmonth108ReportFormSet = inlineformset_factory(Month108Report, Studentmonth108Report,extra=0,
                                                     form=Studentmonth108ReportForm, can_delete=False)


class LastReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LastReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = LastReport
        exclude = ['last_submitted', 'accepted_on', 'accepted_by', 'started']
        labels = {
            'objectives_achieved': 'Have the project research objectives been achieved?',
            'update_on_objectives': 'Give an update on each of the project research objectives',
            'objective_challenges': 'If an objective has not yet been realized indicate the challenges, how these will be addressed and when.',
            'key_achievements': 'In relation to the objectives of your research, what are the key achievements obtained during implementation of this project?',
            'research_outcomes': 'What are the outcomes of your research?',
            'significant_individual_change': 'What is the Most Significant Change of this research grant to your individual career/profession?',
            'significant_student_change': 'What  significant change has this project research had on your students supported by this grant.',
            'benefited_university': 'How has this grant benefited your College/School/Faculty or University as a whole?',
            'benefited_stakeholders': 'What has been the benefit of the research outputs/outcomes on the targeted stakeholders (smallholder farmers, communities, Community Based Organisations (CBOs)?',
            'lessons_learned': 'What lessons have you learnt during the implementation of this project?',
            'challenges_encountered_resolved': 'Outline any challenges that you encountered. How were these challenges resolved to ensure that the project remains on schedule?',
            'papers_published': 'Have you published any papers? ',
            'student_papers_published': 'Have you or the Students published any papers? ',
            'won_new_grants': 'Have you as a PI been able to win any other grant as a result of implementing this project?',
            'new_grant_value': 'What is the value of the grant(s)? (US$)',
            'new_grant_funder': 'Who are/is the funder(s)?',
            'recognized_for_outstanding_research': 'Have you / your team been recognized for outstanding research in any forum?',

            'invitation_to_continue_working': 'Have you / your team received invitations to continue working with your collaborators on other assignments related to your project/research?',
            'cases_of_uptake': 'Please provide a summery of uptake of your research outputs (technology packages)',

        }
        widgets = {
            'expected_graduation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'strategies_for_sustainability': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'cases_of_uptake': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

            'new_grant_funder': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'challenges_encountered_resolved': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'lessons_learned': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'benefited_stakeholders': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'benefited_university': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'significant_student_change': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'significant_individual_change': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'research_outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'key_achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'objective_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'update_on_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


class LastStudentReportForm(FormsetMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LastStudentReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name in self.fields:
            field = self.fields.get(field_name)

    class Meta:
        model = LastStudentReport
        exclude = ['last_submitted']

        labels = {
            'student_graduated': 'Has the student graduated?',
            'not_graduated_explanation': 'If not, give reasons why he/she has not graduated.',
            'steps_to_graduation': 'What steps are being taken to ensure that the student graduates within the next six months',
            'expected_graduation_date': 'What is the expected date of graduation for the student?',

        }
        widgets = {
            'expected_graduation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'not_graduated_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'steps_to_graduation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }


LastStudentReportFormSet = inlineformset_factory(LastReport, LastStudentReport,
                                                 form=LastStudentReportForm, extra=0, can_delete=False)


class TechnologyForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = Technology
        exclude = ['grant_report', ]


TechnologyFormSet = inlineformset_factory(LastReport, Technology,
                                          form=TechnologyForm, extra=0, can_delete=True)


class StudentPublicationForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = StudentPublication
        exclude = ['grant_report', ]


StudentPublicationFormSet = inlineformset_factory(LastReport, StudentPublication,
                                                  form=StudentPublicationForm, extra=1, max_num=10, can_delete=True)


class PIPublicationForm(FormsetMixin, forms.ModelForm):
    class Meta:
        model = PIPublications
        exclude = ['grant_report', ]


PIPublicationFormSet = inlineformset_factory(LastReport, PIPublications,
                                             form=PIPublicationForm, extra=1, max_num=10, can_delete=True)
