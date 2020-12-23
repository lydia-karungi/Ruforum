from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_comments.models import Comment

from contacts.models import User, Student
from custom_comments.models import Ruforumcomment
from grants.models import Grant


class ReportMixin:
    def status(self):
        if self.accepted_on:
            _status = 'Accepted'
        elif self.last_submitted:
            _status = 'Submitted'
        else:
            _status = 'Draft'
        return _status

    def css_class(self):
        classes = {
            'Accepted': 'ok',
            'Submitted': 'warning',
            'Draft': 'error'
        }
        status = self.status()
        return classes[status]

    def get_comments(self):
        site_id = getattr(settings, "SITE_ID", None)
        # if not site_id and ('request' in context):
        #    site_id = get_current_site(context['request']).pk
        ctype = ContentType.objects.get_for_model(self)
        comments = Ruforumcomment.objects.filter(
            comment_ptr__content_type=ctype,
            comment_ptr__object_pk=self.pk,
            comment_ptr__site__pk=site_id,
        )
        return comments


UNKNOWN_YES_NO = (
    (None, "--please select--"),
    (2, "Yes"),
    (3, "No"),
)


class Beneficiary(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class FirstReport(ReportMixin, models.Model):
    APPLICATION_STATES = (
        ('Accepted', 'Accepted'),
        ('Submitted', 'Submitted'),
        ('Draft', 'Draft')
    )
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, models.CASCADE, unique=True)
    recruitment_criteria_and_process = models.TextField(null=True)
    recruitment_criteria_and_process_upload = models.FileField(blank=True, upload_to='', max_length=300, null=True)
    project_activities_upload = models.FileField(max_length=500, blank=True, upload_to='', null=True,
                                                 help_text='File size limit: 200KB')
    planned_activities_upload = models.FileField(max_length=500, blank=True, upload_to='', null=True)
    progress_against_objectives = models.TextField(
        help_text='Please use 70 words for each objective (max 3 objectives)')
    teamwork_and_mentoring = models.TextField(null=True)
    problems_and_challenges = models.TextField()
    modifications = models.TextField(null=True)
    skills_gap = models.TextField(null=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField()
    month = models.PositiveIntegerField(default =6, null=False, blank=True)

    def __str__(self):
        return str(self.grant)


class Month12Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=False,null=True )
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True, blank=False)
    teamwork_mentoring = models.TextField(null=True, blank=False)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    participants = models.FileField(null=True, blank=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=False, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=False)
    month = models.PositiveIntegerField(default =12, null=False, blank=True)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures12(models.Model):
    grant_report = models.ForeignKey(Month12Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)
 

class Linkage12(models.Model):
    grant_report = models.ForeignKey(Month12Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)




class Month18Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=False, null=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True, blank=False)
    teamwork_mentoring = models.TextField(null=True, blank=False)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True, blank=False)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True, blank=False)
    ensure_sustainability_strategies = models.TextField(null=True, blank=False)
    uptake_pathway = models.TextField(null=True, blank=False)
    unexpected_spillover = models.TextField(null=True, blank=False)
    field_days_organized = models.IntegerField(blank=False, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=False)
    month = models.PositiveIntegerField(default =18, null=False, blank=True)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures18(models.Model):
    grant_report = models.ForeignKey(Month18Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage18(models.Model):
    grant_report = models.ForeignKey(Month18Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")

    def __str__(self):
        return str(self.grant_report)


class Month24Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=False, null=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True, blank=False)
    teamwork_mentoring = models.TextField(null=True, blank=False)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True, blank=False)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True, blank=False)
    ensure_sustainability_strategies = models.TextField(null=True, blank=False)
    uptake_pathway = models.TextField(null=True, blank=False)
    unexpected_spillover = models.TextField(null=True, blank=False)
    field_days_organized = models.IntegerField(blank=False, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=False)
    month = models.PositiveIntegerField(default =24, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures24(models.Model):
    grant_report = models.ForeignKey(Month24Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage24(models.Model):
    grant_report = models.ForeignKey(Month24Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")

    def __str__(self):
        return str(self.grant_report)



class Month30Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
   
    summary_progress = models.TextField(blank=False, null=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True, blank=False)
    teamwork_mentoring = models.TextField(null=True, blank=False)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True, blank=False)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True, blank=False)
    ensure_sustainability_strategies = models.TextField(null=True, blank=False)
    uptake_pathway = models.TextField(null=True, blank=False)
    unexpected_spillover = models.TextField(null=True, blank=False)
    field_days_organized = models.IntegerField(blank=False, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=False)
    month = models.PositiveIntegerField(default =30, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures30(models.Model):
    grant_report = models.ForeignKey(Month30Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage30(models.Model):
    grant_report = models.ForeignKey(Month30Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)



class Month36Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =36, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures36(models.Model):
    grant_report = models.ForeignKey(Month36Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage36(models.Model):
    grant_report = models.ForeignKey(Month36Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month42Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =42, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures42(models.Model):
    grant_report = models.ForeignKey(Month42Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage42(models.Model):
    grant_report = models.ForeignKey(Month42Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month48Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True,null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =48, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures48(models.Model):
    grant_report = models.ForeignKey(Month48Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage48(models.Model):
    grant_report = models.ForeignKey(Month48Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month54Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =54, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures54(models.Model):
    grant_report = models.ForeignKey(Month54Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage54(models.Model):
    grant_report = models.ForeignKey(Month54Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month60Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =60, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures60(models.Model):
    grant_report = models.ForeignKey(Month60Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage60(models.Model):
    grant_report = models.ForeignKey(Month60Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month66Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =66, null=False)
    any_other_upload = models.FileField(null=True, blank=True)

class RelevantPictures66(models.Model):
    grant_report = models.ForeignKey(Month66Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage66(models.Model):
    grant_report = models.ForeignKey(Month66Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month72Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =72, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures72(models.Model):
    grant_report = models.ForeignKey(Month72Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage72(models.Model):
    grant_report = models.ForeignKey(Month72Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month78Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =78, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures78(models.Model):
    grant_report = models.ForeignKey(Month78Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage78(models.Model):
    grant_report = models.ForeignKey(Month78Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month84Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =84, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures84(models.Model):
    grant_report = models.ForeignKey(Month84Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage84(models.Model):
    grant_report = models.ForeignKey(Month84Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month90Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =90, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures90(models.Model):
    grant_report = models.ForeignKey(Month90Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage90(models.Model):
    grant_report = models.ForeignKey(Month90Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)



class Month96Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =96, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures96(models.Model):
    grant_report = models.ForeignKey(Month96Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage96(models.Model):
    grant_report = models.ForeignKey(Month96Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month102Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=False)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =102, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures102(models.Model):
    grant_report = models.ForeignKey(Month102Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage102(models.Model):
    grant_report = models.ForeignKey(Month102Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class Month108Report(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    how_student_objectives_link_to_research_objectives = models.TextField(blank=False)
    project_progress = models.TextField(null=True, blank=True)
    student_progress = models.TextField(null=True, blank=False)
    summary_progress = models.TextField(blank=True)
    linkages_for_next_12_months = models.TextField(blank=True, null=True)
    student_capacity_gaps = models.TextField(null=True)
    teamwork_mentoring = models.TextField(null=True)
    # project beneficiaries
    beneficary_group = models.ManyToManyField(Beneficiary, help_text='Check all that are applicable', blank=True)
    male_participants = models.PositiveIntegerField(null=True, blank=True)
    female_participants = models.PositiveIntegerField(null=True, blank=True)
    how_engaged_beneficiaries = models.IntegerField(blank=True, null=True)
    participants = models.FileField(null=True, blank=True)
    direct_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    indirect_beneficiaries = models.PositiveIntegerField(blank = True, null=True)
    problems_and_challenges = models.TextField(null=True)
    problems_and_challenges_solution = models.TextField(null=True)
    changes_made = models.TextField(null=True, blank=True)
    have_engaged_beneficiaries = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_required = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    no_cost_extension_explained = models.TextField(null=True, blank=True)
    on_schedule = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    not_on_schedule_explanation = models.TextField(blank=True)
    request_for_funds_for_year2 = models.FileField(upload_to='', max_length=300, null=True)
    audited_12_month_financial_report = models.FileField(upload_to='', max_length=300, null=True)
    flyers_brochures = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    flyers_brochures_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    policy_briefs = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    policy_briefs_upload = models.FileField(upload_to='', max_length=300, null=True, blank=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField(null=True)
    linkages_established = models.TextField(null=True)
    ensure_sustainability_strategies = models.TextField(null=True)
    uptake_pathway = models.TextField(null=True)
    unexpected_spillover = models.TextField(null=True)
    field_days_organized = models.IntegerField(blank=True, null=True)
    research_to_students_field_attachment = models.TextField(null=True, blank=True)
    month = models.PositiveIntegerField(default =108, null=False)
    any_other_upload = models.FileField(null=True, blank=True)


class RelevantPictures108(models.Model):
    grant_report = models.ForeignKey(Month108Report, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.grant_report)


class Linkage108(models.Model):
    grant_report = models.ForeignKey(Month108Report, on_delete=models.CASCADE)
    organisations = models.TextField(blank=False, null=True)
    partners = models.TextField(blank=False, null=True)
    linkage = models.FileField(blank=False, null=True, help_text="Attach document with linkages")
    
    def __str__(self):
        return str(self.grant_report)


class LastReport(ReportMixin, models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
    objectives_achieved = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    update_on_objectives = models.TextField(null=True)
    objective_challenges = models.TextField(null=True)
    key_achievements = models.TextField(null=True)
    research_outcomes = models.TextField(null=True)
    significant_individual_change = models.TextField(null=True)
    significant_student_change = models.TextField(null=True)
    benefited_university = models.TextField(null=True)
    benefited_stakeholders = models.TextField(null=True)
    lessons_learned = models.TextField(null=True)
    challenges_encountered_resolved = models.TextField(null=True)
    papers_published = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    student_papers_published = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    won_new_grants = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    new_grant_value = models.IntegerField(blank=True, null=True)
    new_grant_funder = models.TextField(null=True, blank=True)
    recognized_for_outstanding_research = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    invitation_to_continue_working = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    cases_of_uptake = models.TextField(null=True)
    accepted_on = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    started = models.IntegerField()
    month = models.PositiveIntegerField(default =114, null=True, blank=True)
  
class Technology(models.Model):
    grant_report = models.ForeignKey(LastReport, on_delete=models.CASCADE)
    method_used = models.CharField(max_length=200, null=True, blank=False)
    description = models.TextField()
    attach_photo_1 = models.ImageField(null=True, blank=True)
    attach_photo_2 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.method_used


class StudentPublication(models.Model):
    grant_report = models.ForeignKey(LastReport, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=False)
    Journal = models.CharField(max_length=200, null=True, blank=False)
    paper = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title


class PIPublications(models.Model):
    grant_report = models.ForeignKey(LastReport, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=False)
    Journal = models.CharField(max_length=200, null=True, blank=False)
    paper = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title


class FirstStudentReport(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month_6_report = models.ForeignKey(FirstReport, on_delete=models.CASCADE)
    registered = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    tuition_paid = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    tuition_paid_upload = models.FileField(blank=True, null=True, upload_to='', max_length=300)
    allocated_supervisors = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    num_of_courses = models.PositiveIntegerField(null=True, blank=False)
   
   
    class Meta:
        unique_together = (('month_6_report', 'student'),)

class Course(models.Model):
    COURSE_YEARS = (
        (None, '--please select--'),
        (1,'1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    )
    COURSE_SEMESTER = (
        (None, '--please select--'),
        (1,'1'),
        (2, '2'),

    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    month_6_report = models.ForeignKey(FirstReport, on_delete=models.CASCADE, null=True)
    course_code = models.CharField(max_length=100, null=True, blank=False)
    name = models.CharField(max_length=100, null=True, blank=False)
    year = models.PositiveIntegerField( null=True, blank=False, choices=COURSE_YEARS)
    semester = models.PositiveIntegerField(null=True, blank=False, choices=COURSE_SEMESTER)

    def __str__(self):
        self.course_code

class Studentmonth12Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month_12_report = models.ForeignKey(Month12Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_12_report', 'student'),)


class Studentmonth18Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_18_report = models.ForeignKey(Month18Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_18_report', 'student'),)


class Studentmonth24Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_24_report = models.ForeignKey(Month24Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_24_report', 'student'),)


class Studentmonth30Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_30_report = models.ForeignKey(Month30Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_30_report', 'student'),)


class Studentmonth36Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_36_report = models.ForeignKey(Month36Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_36_report', 'student'),)


class Studentmonth42Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_42_report = models.ForeignKey(Month42Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_42_report', 'student'),)


class Studentmonth48Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_48_report = models.ForeignKey(Month48Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_48_report', 'student'),)


class Studentmonth54Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_54_report = models.ForeignKey(Month54Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=True, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_54_report', 'student'),)


class Studentmonth60Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_60_report = models.ForeignKey(Month60Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_60_report', 'student'),)


class Studentmonth66Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_66_report = models.ForeignKey(Month66Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_66_report', 'student'),)


class Studentmonth72Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_72_report = models.ForeignKey(Month72Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_72_report', 'student'),)


class Studentmonth78Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_78_report = models.ForeignKey(Month78Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_78_report', 'student'),)


class Studentmonth84Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_84_report = models.ForeignKey(Month84Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_84_report', 'student'),)


class Studentmonth90Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_90_report = models.ForeignKey(Month90Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_90_report', 'student'),)


class Studentmonth96Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_96_report = models.ForeignKey(Month96Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_96_report', 'student'),)


class Studentmonth102Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_102_report = models.ForeignKey(Month102Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True)
    research_objectives = models.TextField(blank=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_102_report', 'student'),)


class Studentmonth108Report(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_108_report = models.ForeignKey(Month108Report, on_delete=models.CASCADE)
    passed_second_courses = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    done_academic_requirements = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    number_of_retakes = models.IntegerField(blank=True, null=True)
    retakes_registration_date = models.DateField(blank=True, null=True)
    defended_proposal = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    defended_proposal_delay_explanation = models.TextField(blank=True, null=True)
    research_objectives = models.TextField(blank=True, null=True)
    progress_as_planned = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    research_progress = models.TextField(blank=True, null=True)
    thesis_submission_external = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_defense = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    thesis_submission = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    submission_delay_explanation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('month_108_report', 'student'),)


class LastStudentReport(models.Model):
    last_submitted = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    month_30_report = models.ForeignKey(LastReport, on_delete=models.CASCADE)
    student_graduated = models.IntegerField(blank=False, null=True, choices=UNKNOWN_YES_NO)
    not_graduated_explanation = models.TextField(null=True, blank=True)
    steps_to_graduation = models.TextField(null=True, blank=True)
    expected_graduation_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('month_30_report', 'student'),)


class TempReport(ReportMixin, models.Model):
    id = models.BigIntegerField(primary_key=True, unique=False)
    pi = models.IntegerField()
    month = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grant_id = models.CharField(max_length=50)
    grant_title = models.CharField(max_length=256)
    reporting_period = models.IntegerField()
    accepted_on = models.DateTimeField()
    last_submitted = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "grant_reports"