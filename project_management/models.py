from django.db import models
from django.utils import timezone
from datetime import datetime
from pme.models import Resultarea

# Create your models here.
class ProjectManagement(models.Model):

    PROJECT_STATUS = (
        (None, "---please select---"),
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
    )

    project_title = models.CharField(max_length=200, blank = True)
    ruforum_grant_number = models.CharField(max_length=100, blank=True)
    lead_institution =  models.CharField(max_length=200, blank = True)
    contact_person_from_lead_institution_if_not_RUFORUM = models.CharField(max_length=200, blank = True)
    contact_person_at_ruforum = models.CharField(max_length=200, blank = False)
    ruforum_flagship = models.ForeignKey(Resultarea, on_delete=models.CASCADE)
    partners = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    new_end_date = models.DateField(blank=False, null=True)
    project_status = models.CharField(max_length=100, choices = PROJECT_STATUS, db_index=True)
    project_duration = models.IntegerField(blank=True, help_text='enter the project duration in months')
    donor_currency = models. CharField(blank=True, help_text='currency of the donor', max_length=100)
    total_project_budget_original_currency = models. IntegerField(blank=True)
    total_budget_us = models. IntegerField(blank=True)
    total_budget_received_from_Donor_to_RUFORUM = models. IntegerField(blank=True)
    ruforum_secretariat_staff_time = models.DateField(blank=False, null=True)
    annual_budget_available = models. IntegerField(blank=True)
    project_goal = models.TextField(blank=True)
    project_objectives = models.TextField(blank=True)
    project_proposal = models.FileField(null=True,help_text='upload the full project proposal')
    reporting_frequency = models.CharField(blank=True, max_length=100, help_text='monthly, quarterly, biannually, annually, etc')

    def __str__(self):
        return self.project_title



class LogicalFramework(models.Model):
    project = models.ForeignKey(ProjectManagement, on_delete=models.CASCADE , null=True, blank=True)
    overall_objectives = models.TextField(blank=True)
    broader_objectives_to_which_the_project_will_contribute = models.TextField(blank=True)
    project_objectives = models.TextField(blank=True)
    sources_of_information_to_indicators = models.TextField(blank=True)
    specific_objective = models.TextField(blank=True)
    indicators_that_clearly_show_that_objective_has_been_achieved = models.TextField(blank=True)
    sources_of_information_that_exist_or_can_be_collected = models.TextField(blank=True)
    necessary_factors_outside_the_beneficiaries_responsibility = models.TextField(blank=True)
    expected_results = models.TextField(blank=True, help_text='what are the expected results, Detail them')
    indicators_to_measure_expected_results = models.TextField(blank=True)
    external_conditions_for_expected_results = models.TextField(blank=True)
    key_activities = models.TextField(blank=True)
    means_required_to_carry_out_activities = models.TextField(blank=True)
    sources_of_information_about_action_progress = models.TextField(blank=True)
    pre_conditions_required = models.TextField(blank=True)
    conditions_outside_beneficiaries_control = models.TextField(blank=True)
