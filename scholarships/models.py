# import datetime
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from calls.models import Call
from contacts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from common.choices import COUNTRY_CHOICES, GENDER_CHOICES, YEAR_CHOICES, NA_YES_NO, YES_NO
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
YEARS = list(range(datetime.now().date().year, 1990 - 1, -1))
YEAR_CHOICES = [
    (year, year) for year in YEARS
]


class Typeoffloor(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Typeofhousewall(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Typeofroofingmaterial(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Homeassets(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Incomecontributor(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Scholarshipapplication(models.Model):
    APPLICATION_STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('noncompliant', 'Non Compliant'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('selected_for_funding', 'Selected for Funding')
    )
    STATE_CHOICES = (
        (None, "---please select---"),
        (True, u'Yes'),
        (False, u'No'),
    )
    CALL_SOURCES = (
        (None, "---please select---"),
        ("radio", "Radio"),
        ("newspaper", "Newspaper"),
        ("poster", "Poster"),
        ("ruforum", "RUFORUM staff"),
        ("school", "Former school/university"),
        ("friend", "Friend or word of mouth"),
        ("website", "Website"),
        ("others", "Others (Specify)"),
    )
    user = models.ForeignKey(User, models.DO_NOTHING)
    call = models.ForeignKey(Call, on_delete=models.CASCADE, blank=True, null=True, related_name='applications')
    submitted = models.BooleanField()
    scholarship_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scholarship_manager",
                                            null=True, blank=True)
    state = models.CharField(max_length=20, choices=APPLICATION_STATES, default='submitted')
    polymorphic_ctype = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    selected_for_funding = models.BooleanField(blank=True, null=True)
    selected_for_funding_comments = models.TextField(blank=True, null=True)
    funding_email_sent = models.BooleanField(default=False)
    application_date = models.DateTimeField(default=timezone.now)
    programme_applied_for = models.CharField(max_length=100, help_text='e.g. Bachelor of Science Agriculture',
                                             null=True)
    first_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True)
    other_names = models.CharField(max_length=100, null=True, blank=True)
    passport_photo = models.FileField(blank=True, null=True, help_text='Please attach passport size photograph')
    passport_no = models.CharField(max_length=16, null=True,
                                   help_text='Please include National Identity Card Number/Passport number/Birth certificate number')
    date_of_birth = models.DateField(blank=False, null=True)
    english_in_high_school = models.BooleanField(choices=STATE_CHOICES)
    scholarship_call_source = models.CharField(max_length=32, choices=CALL_SOURCES, null=True)
    compliance_comments = models.TextField(blank=True, null=True)
    validated_academic_document = models.BooleanField(_('Validated Academic Documents'), blank=True, null=True)
    validated_reference_letters = models.BooleanField(blank=True, null=True)
    reviewers = models.ManyToManyField(User, blank=True, related_name="reviewer")
    validators = models.ManyToManyField(User, related_name="scholarshipvalidators", blank=True)

    class Meta:
        unique_together = ['user', 'call']

        permissions = (
            ("assign_scholarship_reviewers", "Can assign scholarship reviewers"),
            ('make_scholarship_permissions', 'Can make scholarship decision'),
            ('validate_scholarship_applications', 'Can validate scholarship Applications'),

        )

    @property
    def is_mastercard(self):
        return self.call.scholarship_type == "mastercard"

    def degree_type(self):
        try:
            return self.otherscholarshipapplication.get_phd_application_display()
        except:
            return ''

    @property
    def compliant(self):
        compliance_fields = [
            'validated_academic_document',
            'validated_reference_letters',
        ]

        for field in compliance_fields:
            if not getattr(self, field):
                return False

        return True

    @property
    def validated(self):
        return self.state == 'validated'

    def is_draft(self):
        return self.state == 'draft'


class Additionalfundingsource(models.Model):
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    already_funded = models.IntegerField()
    source_of_funding = models.CharField(max_length=200)
    amount_already_provided = models.IntegerField(blank=True, null=True)
    scholarship_need = models.IntegerField()
    funding_type = models.CharField(max_length=8)

    class Meta:
        unique_together = (('application', 'funding_type'),)


class Communityservice(models.Model):
    activity = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class Currentvolunteering(models.Model):
    involvement = models.CharField(max_length=100)
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class Employmenthistory(models.Model):
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=150,blank=True,null=True)
    organisation_address= models.TextField(blank=True,null=True)
    professional_responsibilities = models.TextField(blank=True)
    reason_for_leaving = models.TextField(blank=True, null=True)
    employed_from = models.DateField(blank=True, null=True)
    employed_to = models.DateField(blank=True, null=True)


class Groupassociationclub(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class Householdincomesource(models.Model):
    source = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(help_text='Amount of income per year (use local currency)')
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class Leadershipposition(models.Model):
    position = models.CharField(max_length=50, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True, choices=YEAR_CHOICES)
    certificate = models.FileField(blank=True, null=True, help_text='please attach certificates of recognition if any')
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class ResearchAndPublication(models.Model):
    Code = (
        (None, "---please select---"),
        ("bachelor", "Bachelor"),
        ("master", "Master"),
        ("other", "Others"))
    code = models.CharField(max_length=50, choices=Code, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE,
                                    related_name="researchandpublications")

    class Meta:
        unique_together = ('application', 'title')


class Publication(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    published_file = models.FileField(blank=True, null=True)
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE, related_name="publications")

    class Meta:
        unique_together = ('application', 'title')


class Mastercardeducation(models.Model):
    particular = models.CharField(_('Education Level'), max_length=18, blank=False, null=False)
    name_of_school = models.CharField(max_length=50)
    location_of_school = models.CharField(max_length=32, help_text='Location of School (District)')
    school_ownership = models.CharField(max_length=50)
    total_score = models.PositiveSmallIntegerField(blank=True, null=True, help_text='points / aggregate / grade / CGPA')
    year_of_completion = models.PositiveSmallIntegerField(blank=True, null=True, choices=YEAR_CHOICES)
    average_cost_of_fees_per_year = models.PositiveIntegerField(blank=True, null=True)
    certificate = models.FileField(null=True, blank=False, help_text='please attach your certificate')
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('particular', 'application'),)


class Mastercardscholarshipapplication(models.Model):
    TOILET_TYPES = (
        (None, "---please select---"),
        ("flush and pour", "Flush and pour"),
        ("vip", "VIP latrine"),
        ("covered pit", "Covered pit latrine"),
        ("uncovered pit", "Uncovered pit latrine"),
        ("composting", "Composting toilet"),
        ("none", "No facility / bush / field"),
        ("ecosan", "Ecosan"),

    )
    SECTORS = (
        (None, "---please select---"),
        ("education", "Education"),
        ("finance", "Finance and Banking"),
        ("agriculture", "Agriculture"),
        ("engineering", "Engineering"),
        ("medicine", "Medicine and Healthcare services"),
        ("telecoms", "Telecommunications"),
        ("religious", "Religious and social services"),
        ("public", "Public service and Government"),
        ("others", "Others (specify)"),
    )
    STATE_CHOICES = (
        (None, "---please select---"),
        (True, u'Yes'),
        (False, u'No'),
    )
    GRADING_CHOICES = (
        (None, "---please select---"),
        ('cgpa', 'CGPA'),
        ('percentage', 'Percentage'),

    )
    scholarshipapplication_ptr = models.OneToOneField(Scholarshipapplication, on_delete=models.CASCADE,
                                                      primary_key=True)
    held_leadership_position = models.BooleanField(choices=STATE_CHOICES)

    cause_of_arrest = models.CharField(max_length=100, null=True, blank=True, help_text='what was the cause?')
    challenge = models.TextField()
    community_service_participation = models.BooleanField()
    country_of_birth = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    country_of_residence = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    other_names = models.CharField(max_length=100, null=True, blank=True)
    # gender = models.CharField(max_length=6, choices=GENDER_CHOICES,null=True,blank=False)
    currently_volunteering = models.BooleanField()
    degree_program = models.CharField(max_length=50)
    # To DO: include gpa in forms
    gpa = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(100.0)], )
    grading_creteria = models.CharField(choices=GRADING_CHOICES, max_length=40)
    distance_to_the_source = models.PositiveSmallIntegerField()
    district_of_birth = models.CharField(max_length=50, null=True, blank=True)
    district_of_residence = models.CharField(max_length=50, null=True, blank=True)
    electricity = models.BooleanField(choices=STATE_CHOICES)
    employer_support = models.BooleanField(blank=False, choices=NA_YES_NO)

    experience = models.TextField(
        help_text='Make reference to work experience, knowledge,skills, and abilities that you have in these areas',
        null=True)
    guardian_occupation = models.CharField(max_length=100)
    guardian_or_spouse_phone = PhoneNumberField(max_length=20, help_text="Guardian or Spouse's phone contact")
    guardian_relationship = models.CharField(max_length=100,
                                             help_text="If Guardian please indicate Guardian's relationship with you")
    have_been_arrested = models.BooleanField(blank=False, choices=NA_YES_NO, null=True)
    have_history_of_chronic_illness = models.BooleanField(blank=False, choices=NA_YES_NO,
                                                          help_text='Note that you need to provide the true information. Your medical condition does not in any way disadvantage your application.')
    have_physical_disability = models.BooleanField(blank=False, choices=NA_YES_NO)
    history_of_chronic_illness = models.CharField(max_length=200, null=True, blank=True, help_text='please specify')
    how_many_share_toilet = models.PositiveSmallIntegerField()
    income_source_1 = models.CharField(max_length=100)
    income_source_2 = models.CharField(max_length=100, null=True, blank=True)
    income_source_3 = models.CharField(max_length=100, null=True, blank=True)
    income_source_4 = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=50)
    letter_of_endorsement = models.FileField(blank=True, null=True,
                                             help_text='Attach evidence (letter of no objection / endorsement explaining what value add graduate studies will bring to the organisation)')
    member_of_group = models.BooleanField()
    most_significant_contribution = models.TextField()
    name_of_guardian_or_spouse = models.CharField(max_length=100,
                                                  help_text='If you are living with your guardian or spouse please state name of guardian or spouse')
    name_of_university = models.CharField(max_length=50)
    nearest_major_road = models.CharField(max_length=50,
                                          help_text='Name the nearest major road from the nearest trading centre include distance in km.')
    number_of_camels = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_cattle = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_chickens = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_donkeys = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_goats = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_sheep = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_siblings = models.PositiveSmallIntegerField(
        help_text='How many siblings (brothers and sisters) do you currently have?')
    other_call_source = models.CharField(max_length=50, null=True, blank=True, help_text="Please specify")
    other_water_source = models.CharField(max_length=100)
    own_livestock = models.BooleanField(choices=STATE_CHOICES)

    pending_high_school_balances = models.BooleanField(choices=STATE_CHOICES)
    school_balances = models.DecimalField(blank=True, null=True, help_text='Specify amount', decimal_places=2,
                                          max_digits=65)
    people_in_house = models.PositiveSmallIntegerField(blank=False, null=True)
    physical_disability = models.CharField(max_length=100, null=True, blank=True, help_text='please specify')
    primary_certificate = models.FileField(blank=True, null=True, help_text='Attach applicable certificate/pass slip')
    rooms_in_house = models.PositiveSmallIntegerField(blank=False, null=True)
    secondary_certificate = models.FileField(blank=True, null=True,
                                             help_text='Attach applicable certificate/pass slip')
    sector_1 = models.CharField(max_length=50, choices=SECTORS)
    sector_2 = models.CharField(max_length=50, choices=SECTORS)
    sector_3 = models.CharField(max_length=50, choices=SECTORS)
    sketch_map = models.FileField(blank=True, null=True,
                                  help_text='Attach sketch map to allow validation team ease of tracking your home')
    telephone_contacts = PhoneNumberField(max_length=20,
                                          help_text='Include Mobile phone number if available. If not available include for any relative / neighbor / local administrator closest to you')
    telephone_owner = models.CharField(max_length=100, help_text='Name of telephone number owner')
    tertiary_certificate = models.FileField(blank=True, null=True, help_text='Attach applicable certificate/pass slip')
    toilet_type = models.CharField(max_length=14, choices=TOILET_TYPES)
    university_certificate = models.FileField(blank=True, null=True,
                                              help_text='Attach applicable certificate/transcript')
    village_of_birth = models.CharField(max_length=50, null=True, blank=True)
    village_of_residence = models.CharField(max_length=50, null=True, blank=False)
    water_source = models.CharField(max_length=20)
    year_of_completion = models.PositiveSmallIntegerField(blank=True, null=True, choices=YEAR_CHOICES)
    other_assets = models.CharField(max_length=50, null=True, blank=True)
    other_floor = models.CharField(max_length=50, null=True, blank=True)
    other_house_wall = models.CharField(max_length=50, null=True, blank=True)
    other_roofing = models.CharField(max_length=50, null=True, blank=True)
    other_sector_1 = models.CharField(max_length=50, null=True, blank=True,
                                      help_text="Only fill in if you answered 'Others' above")
    other_sector_2 = models.CharField(max_length=50, null=True, blank=True,
                                      help_text="Only fill in if you answered 'Others' above")
    other_sector_3 = models.CharField(max_length=50, null=True, blank=True,
                                      help_text="Only fill in if you answered 'Others' above")

    home_assets = models.ManyToManyField(Homeassets, help_text='tick all applicable')
    income_contrib3efc = models.ManyToManyField(Incomecontributor, help_text='Select up to 3')
    type_of_floor = models.ManyToManyField(Typeoffloor, help_text='tick all applicable')
    type_of_house_wall = models.ManyToManyField(Typeofhousewall, help_text='tick all applicable')
    type_of_roofing = models.ManyToManyField(Typeofroofingmaterial, help_text='select any')

    @property
    def get_income_contrib3efc(self):
        items = [row.text for row in self.income_contrib3efc.all()]
        return ', '.join(items)

    @property
    def get_home_assets(self):
        items = [row.text for row in self.home_assets.all()]
        return ', '.join(items)

    @property
    def get_type_of_floor(self):
        items = [row.text for row in self.type_of_floor.all()]
        return ', '.join(items)

    @property
    def get_type_of_house_wall(self):
        items = [row.text for row in self.type_of_house_wall.all()]
        return ', '.join(items)

    @property
    def get_type_of_roofing(self):
        items = [row.text for row in self.type_of_roofing.all()]
        return ', '.join(items)

    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)


class Othereducation(models.Model):
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=50, blank=False, null=True)
    institution = models.CharField(max_length=50, null=True, blank=False)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, null=True, blank=False)
    date_from = models.DateField(blank=False, null=True)
    date_to = models.DateField(blank=False, null=True)
    total_score = models.DecimalField(blank=False, null=True, help_text='points / aggregate / grade / CGPA',
                                      decimal_places=2, max_digits=65)
    major = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(blank=False, null=True)


class Otherscholarshipapplication(models.Model):
    MARITAL_STATUSES = (
        (None, "---please select---"),
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    )
    ACCOMMODATION_CHOICES = (
        ('single', 'Single'),
        ('apartment', 'Single self contained apartment'),
        ('none', 'No accommodation required'),
    )
    APPLICATION_TYPES = (
        (0, 'Masters Degree'),
        (1, 'Phd')
    )
    FUNDING_TYPE = (
        (None, '--please select--'),
        ('research', 'Research'),
        ('tuition', 'Tuition')
    )

    scholarshipapplication_ptr = models.OneToOneField(Scholarshipapplication, on_delete=models.CASCADE,
                                                      primary_key=True)
    # bio data
    marital_status = models.CharField(max_length=8, choices=MARITAL_STATUSES)
    place_of_birth = models.CharField(max_length=100, null=True)
    country_of_residence = models.CharField(max_length=3, choices=COUNTRY_CHOICES, null=True, blank=False)
    residence_contact_address = models.TextField(null=True)
    contact_email = models.EmailField(null=True)
    telephone_contacts = PhoneNumberField(max_length=20,
                                          help_text='Include Mobile phone number if available. If not available include for any relative / neighbor / local administrator closest to you',
                                          null=True)

    experience = models.TextField(
        help_text='Using concrete examples, briefly describe your experience (Make reference to work experience, knowledge, skills, and abilities that you have)',
        null=True, blank=True)
    # research interest
    research_experience = models.TextField()
    research_location = models.CharField(max_length=4, choices=COUNTRY_CHOICES, null=True)
    research_location_reason = models.TextField()

    name_of_university = models.CharField(max_length=50, null=True)
    research_concept_note = models.FileField(blank=True, null=True)
    # employer support
    employer_support = models.BooleanField(default=True)
    support_evidence = models.FileField(null=True)
    # Additional funding
    have_additional_funding = models.BooleanField(default=False)
    # if True specify
    specify_funding_type = models.TextField(null=True, blank=True)
    funding_type = models.CharField(max_length=200, null=True, blank=True, choices=FUNDING_TYPE)
    already_funded = models.BooleanField(null=True)
    # amount in us dollar
    amount_provided = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=65)
    # Other Information
    other_call_source = models.CharField(max_length=50, null=True, blank=True,
                                         help_text="Please specify if you selected 'others' above")


class Parent(models.Model):
    PARENT_STATUSES = (
        (None, "---please select---"),
        ('alive', 'Alive'),
        ('deceased', 'Deceased')
    )
    PARENT_RELATIONSHIPS = (
        ('father', 'Father'),
        ('mother', 'Mother')
    )
    full_name = models.CharField(max_length=100)
    status = models.CharField(max_length=16, choices=PARENT_STATUSES)
    date_of_death = models.DateField(blank=True, null=True, help_text='If deceased, give date of death')
    death_certificate = models.FileField(blank=True, null=True,
                                         help_text='upload death certificate or letter from a reliable authority')
    disability = models.TextField(null=True, blank=True,
                                  help_text='Does this parent have any disability? If YES please indicate the type of disability')
    occupation = models.CharField(max_length=100, help_text='Occupation / Job Title either now or previously')
    organisation = models.CharField(max_length=150, help_text='Organization or Place of Work', null=True, blank=True)
    gross_annual_income = models.IntegerField(blank=True, null=True,
                                              help_text='Gross Annual Income (if parent not in formal employment, compute together the income from various sources)')
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=6, choices=PARENT_RELATIONSHIPS)

    class Meta:
        unique_together = (('relationship', 'application'),)


class Referenceletter(models.Model):
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    referee_names = models.CharField(max_length=300, null=True, blank=False)
    referee_address = models.TextField(null=True, blank=False)
    contact_details = models.TextField(null=True, blank=False)
    file = models.FileField(blank=False, null=True)


class Scholarshipappreview(models.Model):
    RECOMMENDATIONS = (
        (None, '--please select--'),
        ('major', 'Major Revision'),
        ('minor', 'Minor Revision'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATIONS, null=True)
    review_form = models.FileField(null=True)
    concept_note = models.FileField(null=True, help_text='please add a concept note', blank=True)
    reviewed_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('application', 'reviewer'),)

    @property
    def get_total_marks(self):
        return self.mark

    @property
    def get_percent_mark(self):
        return int((self.get_total) * 100)

    def __str__(self):
        return str(self.get_total_marks)


class Transcriptfile(models.Model):
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)


class Workexperience(models.Model):
    organisation = models.CharField(max_length=300)
    employed_from = models.DateField(blank=True, null=True)
    employed_to = models.DateField(blank=True, null=True)
    average_monthly_salary = models.IntegerField(blank=True)
    reason_for_leaving = models.CharField(max_length=100, blank=True)
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)


class ScholarShipType(models.Model):
    """docstring for ."""
    type_name = models.CharField(max_length=300)

    def __str__(self):
        return self.type_name


class Scholarship(models.Model):
    CHOICES = (
        ('approved', 'Approved'),
        ('not_approved', 'Not Approved')
    )
    PERIOD_CHOICES = (
        (None, '--please select--'),
        (3, '3 Months'),
        (6, '6 Months'),

    )
    application = models.ForeignKey(Scholarshipapplication, on_delete=models.CASCADE)
    scholarship_id = models.CharField(max_length=50, blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    programme_applied_for = models.CharField(max_length=50, blank=False, null=True)
    institution = models.CharField(max_length=50, null=True, blank=False)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    scholarship_year = models.CharField(max_length=20)
    generated_number = models.IntegerField(null=True,default=1)
    reporting_period = models.PositiveIntegerField(choices=PERIOD_CHOICES, blank=True, null=True)
    report_number = models.PositiveIntegerField(blank=True, null=True)
    approval_status = models.CharField(max_length=30, choices=CHOICES, default='approved')
    approved_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='scholarship_approvals')

    def __str__(self):
        return self.student.get_full_name()
