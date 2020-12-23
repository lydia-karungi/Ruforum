from django import forms
from .models import ProjectManagement, LogicalFramework

class ProjectManagementForm(forms.ModelForm):
    project_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    ruforum_grant_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    lead_institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    contact_person_from_lead_institution_if_not_RUFORUM = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    contact_person_at_RUFORUM = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    partners = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    new_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    project_status = forms.ChoiceField(choices=ProjectManagement.PROJECT_STATUS, widget=forms.Select(attrs=
                                                                            {'class': 'form-control'}), required=False)
    project_duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    donor_currency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    total_project_budget_original_currency = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_budget_us = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_budget_received_from_donor_to_ruforum = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    ruforum_secretariat_staff_time = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    annual_budget_available = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    project_goal = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    project_objectives = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    project_proposal = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*',
                                      'type': 'file'}),required=False)
    reporting_frequency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)

    def __init__(self, *args, **kwargs):
        super(ProjectManagementForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control", "type": "date"}
                continue
            field.widget.attrs = {"class": "form-control"}
    class Meta:
        model = ProjectManagement
        exclude = []

class LogicalFrameworkForm(forms.ModelForm):
    overall_objectives = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True)
    broader_objectives_to_which_the_project_will_contribute = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label='What are the overall broader objectives to which the project will contribute?')
    project_objectives = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the key indicators related to the overall objectives?')
    sources_of_information_to_indicators = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the sources of information for these indicators?')
    specific_objective = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What specific objective is the project intended to achieve to contribute to the overall objectives?')
    indicators_that_clearly_show_that_objective_has_been_achieved = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label='What are the indicators that clearly show the objective of the action has been achieved?')
    sources_of_information_that_exist_or_can_be_collected = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label ='What are the sources of information that exist or can be collected? What are the methods required to get this information?')
    necessary_factors_outside_the_beneficiaries_responsibility = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What factors and conditions outside the Beneficiarys responsibility are necessary to achieve that objective?(external conditions) Which risks should be taken into consideration?')
    expected_results = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the expected results, Detail them.(The results are the outputs envisaged to achieve the specific objective)')
    indicators_to_measure_expected_results = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the indicators to measure whether and to what extent the action achieves the expected result?')

    external_conditions_for_expected_results = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What external conditions must be met to obtain the expected results on schedule?')
    key_activities = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True,label ='What are the key activities to be carried out and in what sequence in order to produce the expected results? please list the activities in order' )
    means_required_to_carry_out_activities = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the means required to implement these activities, e.g. personnel, equipment, training, studies, supplies, operational facilities, etc.')
    sources_of_information_about_action_progress = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What are the sources of information about action progress?')
    pre_conditions_required = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What pre-conditions are required before the action starts?')
    conditions_outside_beneficiaries_control = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 2, 'cols': 30}), required=True, label = 'What conditions outside the Beneficiarys direct control have to be met for the implementation of the planned activities?')

    def __init__(self, *args, **kwargs):


        super(LogicalFrameworkForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control", "type": "date"}
                continue
            field.widget.attrs = {"class": "form-control"}
    class Meta:
        model = LogicalFramework
        exclude = []



class SelectProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
                              queryset=ProjectManagement.objects.filter(
                                  project_title__isnull=False,
                              ))

    class Meta:
        model = LogicalFramework
        fields = ['project']

    def __init__(self, *args, **kwargs):
        super(SelectProjectForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = "---please select---"
