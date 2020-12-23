from django.db import models
from django.contrib.contenttypes.models import ContentType


from contacts.models import User
from common.choices import YES_NO

class Studentreport(models.Model):
    PERIOD_CHOICES = (
        ('03', '3 Months'),
        ('6', '6 Months'),
        ('9', '9 Months'),
        ('12', '12 Months'),
        ('15', '15 Months'),
        ('18', '18 Months'),
        ('21', '21 Months'),
    )
    STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    )
    student = models.ForeignKey(User, models.DO_NOTHING)
    period = models.CharField(max_length=3, choices=PERIOD_CHOICES)
    state = models.CharField(max_length=20, choices=STATES, default='draft')
    submitted_on = models.DateField(blank=True, null=True)
    polymorphic_ctype = models.ForeignKey(ContentType, models.DO_NOTHING, blank=True, null=True)

    '''
    @property
    def student_type(self):
        user_type.get_object_for_this_type(username='Guido')
    '''

class Briefsattachment(models.Model):
    report = models.ForeignKey(Studentreport, models.DO_NOTHING, blank=True, null=True)
    title = models.TextField()
    file = models.FileField(blank=True, null=True)


class Manuscript(models.Model):
    STATUS_CHOICES = (
        ("not_written", "Not yet written"),
        ("written", "Written"),
        ("submitted", "Submitted"),
        ("accepted", "Accepted"),
        ("published", "Published"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    title = models.TextField()
    journal = models.TextField()
    publication_date = models.DateField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    report = models.ForeignKey(Studentreport, models.DO_NOTHING, blank=True, null=True)

class SupervisorDetails(models.Model):
    TITLE =(
        ("mr", "Mr"),
        ("mrs", "Mrs"),
        ("ms", "Ms"),
        ("Dr", "Dr"),
        ("Prof", "Prof")
    )

    name = models.CharField(max_length=25, null=True)
    title = models.CharField(choices=TITLE, max_length=25)
    area_of_mentorship = models.CharField(max_length=50, blank=True)
    areas_of_achievement = models.TextField()
    areas_required_more_attention_and_support = models.TextField()
    address = models.TextField()


class ResearchInformation(models.Model):
    research_summary = models.TextField()
    location = models.TextField()
    number_of_stakeholders = models.FloatField(null=True)
    type_of_farming_communities = models.TextField()
    number_of_actors_that_are_non_farmers = models.TextField()
    Your_champion_technology = models.TextField()
    activities_executed = models.TextField()
    scientists_in_your_institution = models.FloatField(null=True)
    technicians_in_your_institution = models.FloatField(null=True)
    fellow_students = models.FloatField(null=True)
    others = models.FloatField(null=True)
    benefits_for_institution = models.TextField()
    critical_issues = models.TextField()
    skills_required = models.TextField()
    challenges_encountered = models.TextField()
    plan_during_the_next_reporting_period = models.TextField()


class SkillsImprovement(models.Model):
    brief_farm_description = models.TextField()
    short_courses_attended = models.TextField()
    courses_objectives = models.TextField()
    evaluate_the_course_delivery = models.TextField()
    self_evaluation = models.TextField()
    areas_of_improvement = models.TextField()


class Products(models.Model):
    innovation_produced = models.TextField()
    publications = models.TextField()
    conference_papers = models.TextField()
    presentations = models.TextField()
    funding_from_other_sources = models.CharField(choices=YES_NO, max_length=15)


class AdditionInformation(models.Model):
    futureplans_or_feedback = models.TextField()

class Mastercardalumnireport(models.Model):
    id = models.AutoField(primary_key=True)
    studentreport_ptr = models.OneToOneField(Studentreport, models.DO_NOTHING)
    transition_from_university = models.TextField()
    name_of_employer_institution = models.CharField(max_length=255)
    name_of_studying_institution = models.CharField(max_length=255)
    status_of_enterprise = models.CharField(max_length=20)
    activities_of_enterprise = models.TextField()
    community_initiatives = models.TextField()


class Mastercardstudentreport(models.Model):
    id = models.AutoField(primary_key=True)
    studentreport_ptr = models.OneToOneField(Studentreport, models.DO_NOTHING)
    additional_health_needs = models.TextField()
    address = models.TextField()
    approval_by_program_coordinator = models.CharField(max_length=255)
    area_attention_required = models.TextField()
    area_of_achievement = models.TextField()
    areas_to_improve = models.TextField()
    aware_of_guidance = models.IntegerField()
    business_actors = models.PositiveIntegerField(blank=True, null=True)
    business_challenges = models.TextField()
    business_competition = models.TextField()
    business_future = models.TextField()
    business_growth = models.TextField()
    business_innovation = models.TextField()
    career_areas_more_support = models.TextField()
    career_guidance_qos = models.CharField(max_length=1)
    career_key_issues = models.TextField()
    career_mentor_email = models.CharField(max_length=254)
    career_mentor_name = models.CharField(max_length=255)
    career_mentor_phone = models.CharField(max_length=20)
    contact_at_home_email = models.CharField(max_length=254)
    contact_at_home_name = models.CharField(max_length=255)
    contact_at_home_tel = models.CharField(max_length=20)
    course_unit_code = models.CharField(max_length=255)
    course_units_failed = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    degree_type = models.CharField(max_length=1)
    email = models.CharField(max_length=254)
    farmers_engaged = models.PositiveIntegerField(blank=True, null=True)
    farming_activities = models.TextField()
    farming_actors = models.TextField()
    farming_communities = models.TextField()
    farming_issues = models.TextField()
    farming_organisations = models.TextField()
    farming_skills_required = models.TextField()
    farming_tech = models.TextField()
    field_location = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)
    guidance_attendance_count = models.PositiveIntegerField(blank=True, null=True)
    health_insurance_end = models.DateField(blank=True, null=True)
    health_insurance_number = models.CharField(max_length=255)
    health_insurance_provider = models.CharField(max_length=255)
    health_insurance_qos = models.CharField(max_length=1)
    health_insurance_start = models.DateField(blank=True, null=True)
    last_name = models.CharField(max_length=50)
    middle_names = models.CharField(max_length=255)
    name_of_business = models.CharField(max_length=255)
    name_of_course_unit = models.CharField(max_length=255)
    nationality = models.CharField(max_length=64)
    number_of_credit_units = models.PositiveIntegerField(blank=True, null=True)
    passport_no = models.CharField(max_length=16)
    phone = models.CharField(max_length=20)
    program_title = models.CharField(max_length=255)
    quality_of_teaching = models.CharField(max_length=1)
    semester = models.CharField(max_length=1)
    student_number = models.CharField(max_length=255)
    study_period_end = models.DateField(blank=True, null=True)
    study_period_start = models.DateField(blank=True, null=True)
    supervisor_name = models.CharField(max_length=255)
    supervisor_title = models.CharField(max_length=32)
    timeframe = models.CharField(max_length=255)
    title = models.CharField(max_length=32)
    title_of_research_proposal = models.CharField(max_length=255)
    total_marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    type_of_business = models.CharField(max_length=255)
    type_of_mentor = models.CharField(max_length=255)
    volume_of_business = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    area_of_mentorship = models.CharField(max_length=255)


class Milestone(models.Model):
    MILESTONE_TYPES = (
        ('rp_written', 'Research Proposal Written'),
        ('rp_reviewed', 'Research Proposal Reviewed by Supervisor'),
        ('rp_defended', 'Research Proposal successfully Defended at Department Level'),
        ('fieldwork_prep', 'Preparations for field research done'),
        ('fieldwork_done', 'Field Work and Data Collection Done'),
        ('data_analysed', 'Data Analysis Done'),
        ('reported', 'Documenting Findings / Reporting Done'),
        ('activities', 'Activities dissemination done'),
        ('channels', 'Different dissemination channels used'),
        ('documented', 'Implementation process documented'),
        ('papers_written', 'Draft Manuscripts written for peer reviewed journals'),
        ('papers_submitted', 'Submitted Manuscripts to peer reviewed journals'),
        ('papers_accepted', 'Manuscripts accepted by peer reviewed journals'),
        ('posters', 'Posters, fliers, policy briefs, articles submitted in conference proceedings'),
        ('thesis_written', 'Final Thesis Written'),
        ('thesis_submitted', 'Thesis submitted for external examination'),
        ('thesis_corrected', 'Thesis corrected'),
        ('thesis_defended', 'Thesis Defended'),
        ('graduated', 'Student graduated'),
    )
    YES_NO=(
       
        ('no','No'),
         ('yes','Yes')
    )
    report = models.ForeignKey(Studentreport, models.DO_NOTHING, related_name='milestones')
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    due_date = models.DateField()
    completed = models.CharField(max_length=9, choices=YES_NO)
    comments = models.TextField()
    completed_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['due_date']


class Otherstudentreport(models.Model):
    studentreport_ptr = models.OneToOneField(Studentreport, models.DO_NOTHING, primary_key=True)
    accomplishments = models.TextField()
    benefited_count = models.TextField()
    challenges = models.TextField()
    new_technology = models.TextField()
    other_info = models.TextField()
    significant_change = models.TextField()
    skills_use = models.TextField()
    spillovers = models.TextField()
    technology_use = models.TextField()
    trainings = models.TextField()
    workplace = models.TextField()


class Publicationattachment(models.Model):
    report = models.ForeignKey(Studentreport, models.DO_NOTHING, blank=True, null=True)
    title = models.TextField()
    file = models.FileField(blank=True, null=True)


# class Skillenhancement(models.Model):
#     name = models.CharField(max_length=255)
#     objectives = models.TextField()
#     course_evaluation = models.CharField(max_length=1)
#     self_evaluation = models.CharField(max_length=1)
#     improvement = models.TextField()
#     report = models.ForeignKey(Mastercardstudentreport, models.DO_NOTHING)
