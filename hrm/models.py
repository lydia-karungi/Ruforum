from django.db import models

from common.choices import COUNTRY_CHOICES, NA_YES_NO

"""
Models module for small_small_hr
"""
from datetime import datetime, timedelta
from decimal import Decimal
from dateutil import relativedelta

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _
from contacts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from private_storage.fields import PrivateFileField
from sorl.thumbnail import ImageField

from .managers import LeaveManager

USER = settings.AUTH_USER_MODEL
TWOPLACES = Decimal(10) ** -2
YEARS = list(range(datetime.now().date().year, 1990 - 1, -1))
YEAR_CHOICES = [
    (year, year) for year in YEARS
]


class TimeStampedModel(models.Model):
    """
    Abstract model class that includes timestamp fields
    """
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True)
    modified = models.DateTimeField(
        verbose_name=_('Modified'),
        auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TimeStampedModel
        """
        abstract = True


class Role(TimeStampedModel, models.Model):
    """
    Model class for staff member role
    """
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, default='')

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for StaffDocument
        """
        abstract = False
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name', 'created']

    def __str__(self):
        # pylint: disable=no-member
        return self.name


class Department(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # pylint: disable=no-member
        return self.name


class StaffProfile(TimeStampedModel, models.Model):
    """
    StaffProfile model class
    Extends auth.User and adds more fields
    """

    # sex choices
    # according to https://en.wikipedia.org/wiki/ISO/IEC_5218
    NOT_KNOWN = '0'
    MALE = '1'
    FEMALE = '2'
    NOT_APPLICABLE = '9'
    MaritalStatus = (
        (None, '--please select--'),
        ('Married', 'Married'),
        ('Single', 'Single'),
    )

    problem = (
        (None, '--please select--'),
        ('True', 'True'),
        ('False', 'False'),
    )

    sponsor = (
        (None, '--please select--'),
        ('ruforum', 'RUFORUM'),
        ('self', 'SELF'),

    )

    user = models.OneToOneField(
        USER, verbose_name=_('User'), on_delete=models.CASCADE, unique=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    image = ImageField(max_length=255, verbose_name=_("Profile Image"), help_text=_("passport size photo"), blank=True)
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    other_name = models.CharField(null=True, blank=True, max_length=50)
    physical_address = models.TextField(null=True)
    staff_email = models.EmailField(null=True, max_length=50)
    mobile = PhoneNumberField(null=True)
    district_of_residence = models.CharField(null=True, max_length=50)
    county = models.CharField(null=True, max_length=50)
    sub_county = models.CharField(null=True, max_length=50)
    parish = models.CharField(null=True, max_length=50)
    marital_status = models.CharField(blank=True, max_length=50, choices=MaritalStatus)
    sub_county = models.CharField(null=True, max_length=50)
    parish = models.CharField(null=True, max_length=50)
    marital_status = models.CharField(blank=True, max_length=50, choices=MaritalStatus)
    religion = models.CharField(null=True, max_length=50)
    religious_conflicts = models.BooleanField(default=False, blank=False)
    Conflict = models.TextField(null=True,blank=True)
    name_of_spouse = models.CharField(null=True, blank=True, max_length=50)
    next_of_kin_name = models.CharField(null=True, max_length=50)
    next_of_kin_phone = PhoneNumberField(null=True)
    next_of_kin_address = models.TextField()
    have_eye_defect = models.BooleanField(blank=False, choices=NA_YES_NO, null=True)
    state_eye_defect = models.TextField(null=True, blank=True, help_text='Specify the eye problem')
    eye_medical_letter = models.FileField(blank=True, null=True)
    have_back_problem = models.BooleanField(blank=False, choices=NA_YES_NO, null=True)
    state_back_problem = models.TextField(null=True, blank=True, help_text='Specify the back problem')
    back_problem_medical_letter = models.FileField(blank=True, null=True)
    have_allergy = models.BooleanField(blank=True, choices=NA_YES_NO, null=True)
    state_allergy = models.TextField(null=True, blank=True, help_text='Specify the allergy')
    allergy_medical_letter = models.FileField(blank=True, null=True)
    pursuing_any_study = models.BooleanField(null=True, choices=NA_YES_NO)
    duration_from = models.DateField(
        _('Start Date'), null=True, default=None, blank=True,
        help_text=_('The start date of studies'))
    duration_to = models.DateField(
        _('End Date'), null=True, default=None, blank=True,
        help_text=_('End date of studies'))
    sponsored_by = models.CharField(max_length=10, choices=sponsor, null=True)
    #sponsor_attachment = models.FileField(_('Attachment'), null=True, help_text='provide document to support this', required=True)
    # former employer
    organisation = models.CharField(max_length=150, blank=False, null=True)
    job_title = models.CharField(blank=False, null=True, max_length=50)
    former_department = models.CharField(_('Department'), max_length=150, blank=False, null=True)
    supervisor_name = models.CharField(blank=False, null=True, max_length=50)
    supervisor_title = models.CharField(blank=False, null=True, max_length=50)
    no_of_staff_supervised_by_you = models.IntegerField(_('No of staffs supervised by the Staff if any'), blank=True, null=True)
    employed_from = models.DateField(blank=False, null=True)
    employed_to = models.DateField(blank=False, null=True)
    reason_for_leaving = models.TextField(null=True)
    criminal_record = models.BooleanField(_('Have you been subjected to any disciplinary action in the last two years'),
                                          default=False, blank=False, choices=NA_YES_NO)
    state_criminal_offense = models.CharField(_('Case Committed'), null=True, max_length=50,blank=True)
    offence_date = models.DateField(null=True, blank=True)
    offence_explanation = models.TextField(null=True, blank=True)
    action_taken = models.TextField(null=True, blank=True)
    any_other_information = models.TextField(_('ANY OTHER INFORMATION RELATED TO EMPLOYMENT'), null=True, blank=True)
    # end of former employment
    # Account details
    account_name = models.CharField(null=True, max_length=50, blank=False)
    bank_name = models.CharField(null=True, max_length=50, blank=False)
    account_no = models.CharField(_('Bank Account No:'), null=True, max_length=50, blank=False)
    branch = models.CharField(null=True, max_length=50, blank=False)
    currency = models.CharField(null=True, max_length=50, blank=False)
    nssf = models.CharField(_('Staff NSSF No:'), null=True, blank=False, max_length=50)
    tin_no = models.CharField(_('URA Tax Identification Number (TIN)'), max_length=50, null=True, blank=False)
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True,
                             default=None, null=True,
                             on_delete=models.SET_NULL)
    birthday = models.DateField(_('Birthday'), blank=True, default=None,
                                null=True)

    overtime_allowed = models.BooleanField(
        _('Overtime allowed'), blank=True, default=False)
    start_date = models.DateField(
        _('Start Date'), null=True, default=None, blank=True,
        help_text=_('The start date of employment'))
    end_date = models.DateField(
        _('End Date'), null=True, default=None, blank=True,
        help_text=_('The end date of employment'))
    department = models.ForeignKey(Department, null=True, on_delete=models.PROTECT)
    nhif = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    #emergency_contact_relationship = models.CharField(max_length=50)
    # pursuing_farther studies
    #emergency_contact_number = PhoneNumberField(null=True, required=True)
    work_permit_ID = models.CharField(null=True, max_length=50)
    work_permit_expiry_Date = models.DateField(
        _('Expiry Date'), null=True, default=None, blank=True,
        help_text=_('The expiry date of the work permit'))

    good_working_condition_laptop = models.BooleanField(null=True, blank=False,choices=NA_YES_NO)
    laptop_type = models.CharField(max_length=50, null=True, blank=False)
    good_working_condition_modem = models.BooleanField(choices=NA_YES_NO, null=True, blank=True)
    modem_type = models.CharField(max_length=50, null=True, blank=True)
    others = models.TextField(null=True, blank=True, help_text='please specify')

    # marital_status = models.CharField(nu)
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for StaffProfile
        """
        abstract = False
        verbose_name = _('Staff Profile')
        verbose_name_plural = _('Staff Profiles')
        ordering = ['user__first_name', 'user__last_name', 'user__username',
                    'created']
    @property
    def get_name(self):
        """
        Returns the staff member's name
        """
        # pylint: disable=no-member
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class StaffDocument(TimeStampedModel, models.Model):
    """
    StaffDocument model class
    """
    staff = models.ForeignKey(
        StaffProfile, verbose_name=_('Staff Member'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, default='')
    file = PrivateFileField(
        _('File'), upload_to='staff-documents/',
        help_text=_("Upload staff member document"),
        content_types=[
            'application/pdf',
            'application/msword',
            'application/vnd.oasis.opendocument.text',
            'image/jpeg',
            'image/png'
        ],
        max_file_size=10485760
    )
    public = models.BooleanField(
        _('Public'),
        help_text=_('If public, it will be available to everyone.'),
        blank=True, default=False)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for StaffDocument
        """
        abstract = False
        verbose_name = _('Staff Document')
        verbose_name_plural = _('Staff Documents')
        ordering = ['staff', 'name', '-created']

    def __str__(self):
        # pylint: disable=no-member
        return f'{self.staff.get_name()} - {self.name}'


class BaseStaffRequest(TimeStampedModel, models.Model):
    """
    Abstract model class for Leave & Overtime tracking
    """
    APPROVED = '1'
    REJECTED = '2'
    PENDING = '3'
    PROBATION = '4'

    STATUS_CHOICES = (
        (None, "---please select---"),
        (APPROVED, _('Approved')),
        (PENDING, _('Pending')),
        (REJECTED, _('Rejected')),
        (PROBATION, _('Still on Probation')),
    )

    staff = models.ForeignKey(
        StaffProfile, verbose_name=_('Staff Member'), on_delete=models.CASCADE)
    start = models.DateField(_('Start Date'))
    end = models.DateField(_('End Date'))
    department = models.CharField(blank=True, max_length=50)
    reason = models.TextField(_('Reason'), blank=True, default='')
    status = models.CharField(
        _('Status'), max_length=1, choices=STATUS_CHOICES, default=PENDING,
        blank=True, db_index=True)

    emergency_contact_name = models.TextField( blank=True, default='')
    emergency_contact_number = PhoneNumberField(null=True)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for StaffDocument
        """
        abstract = True


class LeaveType(models.Model):
    ELIGIBLE_GROUPS =(
        (None,'--please select--'),
        (0, 'All'),
        (1, 'Male'),
        (2,'Female')
    )
    leave_name = models.CharField(max_length=100, null=False, blank=False)
    paid_leave = models.BooleanField(default=False, choices=NA_YES_NO)
    count_holidays = models.BooleanField(default=False, choices=NA_YES_NO)
    leave_days = models.PositiveIntegerField(null=True, blank=False)
    eligible_groups =models.IntegerField(choices=ELIGIBLE_GROUPS)

    def __str__(self):
        return self.leave_name


class LeaveAssignment(models.Model):
    """
    Leave block model class
    This model is used for leave configurations
    """
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(StaffProfile, related_name='leave_assignments', on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True, blank=True)
    leave_days = models.PositiveIntegerField(null=True, blank=False)
    year = models.IntegerField(null=True, blank=False, choices=YEAR_CHOICES)


    def __str__(self):
        # pylint: disable=no-member
        return _(f'{self.leave_type}: {self.leave_days}')
    
    @property
    def get_leave_type(self):
       
        # pylint: disable=no-member
        return f'{self.leave_type.leave_name}'


class LeaveApplication(models.Model):
    RECOMMENDATION =(
        (None, '--please select--'),
        ('recommended','Leave Recommended'),
        ('not_recommended','Not Recommended')
    )
    APPROVAL =(
        (None,'--please select--'), 
        ('pending','Pending Approval'),
        ('approved','Leave Approved'),
        ('not_approved', 'Not Approved')
    )

  
    leave_assignment = models.ForeignKey(LeaveAssignment, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE,null=True)
    from_date = models.DateField(_('From'),null=True, blank=False)
    end_date = models.DateField(_('To'),null=True,blank=False)
    leave_days_requested = models.PositiveIntegerField(null=True, blank=False)
    remarks = models.TextField(_('Remarks/Reasons by the Applicant (Applies to Only Compassionate & Study Leave)'),null=True, blank=False)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_person_phone = PhoneNumberField(null=True)
    contact_person_email = models.EmailField(null=True, blank=True)
    application_date = models.DateField(auto_now=True, null=False)
    extra_requested_days = models.IntegerField(null=True, blank=True)
    #CONFIRMATION BY HUMAN RESOURCE OFFICER
    human_resource_officer = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='leave_human_hr',null=True,blank=True)
    human_resource_comment = models.TextField(null=True, blank=False)
    hr_comment_date = models.DateField(null=True, blank=True)
    # RECOMMENDATION [TO BE COMPLETED BY THE SUPERVISOR/UNIT MANAGER OF THE EMPLOYEE]
    supervisor_recommendation = models.CharField(max_length=20, choices=RECOMMENDATION, null=True, blank=False)
    supervisor = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="staff_supervisor", null=True)
    recommendation_date = models.DateField(null=True, blank=True)
    supervisor_comment = models.TextField(null=True, blank=True)
    # AUTHORISATION / APPROVAL [ES/DES-PRM&M TO APPROVE LEAVE FOR ALL STAFF]
    approval = models.CharField(max_length=15, choices=APPROVAL,default='pending', null=True, blank=True)
    date_approved = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='leave_approver',null=True,blank=True)

    def __str__(self):
        # pylint: disable=no-member
        return _(f'{self.staff}: {self.from_date} to {self.end_date}')

    class Meta:
       
        permissions = (
            ("comment_on_leave", "Can Comment on Leave Applications"),
            ("recommend_on_leave", "Can Recommend on Leave Applications"),
            ("can_approve_leave", "Can Approve Leave Applications"),
           
        )

    


class Leave(models.Model):
    """
    Leave block model class
    This model is used for leave configurations
    """
    leave_application = models.OneToOneField(LeaveApplication, on_delete=models.CASCADE, null=True, unique=True)
    start = models.DateField(null=True, blank=False)
    end = models.DateField(null=True,blank=False)
    leave_days = models.PositiveIntegerField(_('Leave Days Approved'),null=True, blank=False)

    def __str__(self):
        # pylint: disable=no-member
        return _(f'{self.leave_application}: {self.start} to {self.end}')
    @property
    def get_staff(self):
        return _(f'{self.leave_application.staff.get_name}')
    
    @property
    def get_leave_name(self):
         return _(f'{self.leave_application.leave_assignment.leave_type.leave_name}')

        

class Hrcomments(models.Model):
        """
        Abstract model class for Leave & Overtime tracking
        """
        APPROVED = '1'
        REJECTED = '2'
        PENDING = '3'
        PROBATION = '4'

        STATUS_CHOICES = (
            (None, "---please select---"),
            (APPROVED, _('Approved')),
            (PENDING, _('Pending')),
            (REJECTED, _('Rejected')),
            (PROBATION, _('Still on Probation')),
        )
        comments = models.TextField(_('Comments'), blank=True, default='')



class FreeDay(models.Model):
    """Model definition for FreeDay."""
    name = models.CharField(_("Name"), max_length=255)
    date = models.DateField(_('Date'), unique=True)

    class Meta:
        """Meta definition for FreeDay."""
        ordering = ['-date']
        verbose_name = _('Free Day')
        verbose_name_plural = _('Free Days')

    def __str__(self):
        """Unicode representation of FreeDay."""
        return f"{self.date.year} - {self.name}"


def get_days(start: object, end: object):
    """
    Yield the days between two datetime objects
    """
    current_tz = timezone.get_current_timezone()
    local_start = current_tz.normalize(start)
    local_end = current_tz.normalize(end)
    span = local_end.date() - local_start.date()
    for i in range(span.days + 1):
        yield local_start.date() + timedelta(days=i)



''' Travel funder(staff travel funder'''


class Funder(models.Model):
    name = models.CharField(max_length=59, blank=False, null=True)

    def __str__(self):
        return self.name


class StaffTravel(TimeStampedModel, models.Model):
    TRAVEL_MODE_CHOICES = (
        (None, "---please select---"),
        ('train', 'By Train'),
        ('plane', 'By Plane'),
        ('vehicle', 'By Vehicle'),
    )
    DESTINATION = (
        (None, '--please select--'),
        ('local', 'Local'),
        ('internation', 'International')
    )
    VISA_ASSURANCE = (
        (None, '--please select--'),
        ('required', 'Required'),
        ('not_required', 'Not Required')
    )
    staff = models.ManyToManyField(StaffProfile, related_name="travellingstaff")
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    purpose_of_visit = models.TextField()
    place_of_visit = models.CharField(max_length=15, choices=DESTINATION)
    country_of_visit = models.CharField(max_length=64, choices=COUNTRY_CHOICES, null=True, blank=True)
    district_of_visit = models.CharField(max_length=100, null=True, blank=True)
    funder = models.ManyToManyField(Funder, related_name='travel_fund')
    back_to_office_date = models.DateField(null=True)
    travel_mode = models.CharField(max_length=20, choices=TRAVEL_MODE_CHOICES)
    airline = models.CharField(max_length=80, blank=True, null=True)
    visa_assurance = models.CharField(max_length=15,null=True,blank=True,choices=VISA_ASSURANCE)
    comment = models.TextField(null=True)
    attach_travel_report = models.BooleanField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='travel_creater', blank=True, null=True, on_delete=models.SET_NULL)


class AssetCategory(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # pylint: disable=no-member
        return self.name


class Asset(TimeStampedModel, models.Model):
    WORKING_CONDITION = (
        (None, '--please select--'),
        ('good', 'Good Status'),
        ('not_good', 'Not In Good Status'),
        ('lost', 'Lost')
    )
    REPAIRABLE = (
        (None, '--please select--'),
        ('repairable', 'Repairable'),
        ('dispose_off', 'Dispose off')
    )
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    asset_code = models.CharField(max_length=100)
    working = models.CharField(max_length=30, choices=WORKING_CONDITION)
    repairable = models.CharField(max_length=30, choices=REPAIRABLE, null=True)
    purchase_date = models.DateField()
    asset_value = models.DecimalField(max_digits=20, default=0, decimal_places=3, blank=False)
    invoice_number = models.CharField(max_length=100)
    engravement_number = models.CharField(max_length=100, null=True, blank=True)
    warranty_end_date = models.DateField(null=True)
    image = models.ImageField(null=True, blank=True)
    note = models.TextField(null=True)
    asset_model = models.CharField(max_length=100, null=True, blank=True)
    insurance_no = models.CharField(max_length=60, null=True, blank=True)
    insurance_company = models.CharField(max_length=100, null=True, blank=True)
    insurance_start_date = models.DateField(null=True, blank=True)
    insurance_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    VEHICLE_STATUS_CHOICES = (
        ('W', 'Working'),
        ('N', 'Not Working'),
    )
    INSURANCE_STATUS_CHOICES = (
        ('U', 'Updated'),
        ('NU', 'Not Updated'),
    )
    VEHICLE_TYPE_CHOICES = (
        ('P', 'Passenger'),
        ('T', 'Truck'),
        ('C', 'Construction'),
    )
    FUEL_TYPE_CHOICES = (
        ('P', 'Petrol'),
        ('D', 'Diesel'),
    )
    assigned_to = models.ForeignKey(StaffProfile, null=True, on_delete=models.CASCADE)
    depreciation_cost = models.DecimalField(max_digits=20, default="0", decimal_places=3, blank=False)
    registration_plate = models.CharField(max_length=200)
    date_of_purchase = models.DateField()
    insurance_company = models.CharField(max_length=100, null=True)
    fuel_type = models.CharField(max_length=1, default='P', choices=FUEL_TYPE_CHOICES)
    mileage = models.DecimalField(max_digits=20, default=0, decimal_places=0)
    vehicle_type = models.CharField(max_length=1, default='P', choices=VEHICLE_TYPE_CHOICES)
    color = models.CharField(max_length=32)
    make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    chassis_number = models.CharField(max_length=100, null=True)
    engine_number = models.CharField(max_length=100, null=True)
    insurance_number = models.CharField(max_length=100, unique=True)
    insurance_valid_upto = models.DateField(null=True)
    insurance_start_date = models.DateField(null=True)
    registration_card = models.FileField(null=True)
    insurance = models.FileField(null=True)
    photo = models.ImageField(null=True)
    waranty = models.CharField(max_length=100, null=True)
    waranty_start_date = models.DateField(default=timezone.now)
    waranty_end_date = models.DateField(null=True)

    def __str__(self):
        return self.registration_plate


class Contract(TimeStampedModel, models.Model):
    CONTRACT_TYPE = (
        (None, '--please select--'),
        ('services', 'Services'),
        ('consultancy', 'Consultancy'),
        ('non-consultancy', 'Non-Consultancy')
    )
    CONTRACT_STATUS = (
        (None, '--please select--'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On hold')
    )
    contract_name = models.CharField(max_length=100)
    services_offered = models.CharField(max_length=100, null=True, blank=True)
    contract_type = models.CharField(max_length=100, choices=CONTRACT_TYPE)
    contract_amount = models.DecimalField(max_digits=20, default=0, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()
    new_start_date = models.DateField(null=True, blank=True)
    new_end_date = models.DateField(null=True, blank=True)
    # duration = models.DurationField(null=True)
    contract_status = models.CharField(max_length=100, choices=CONTRACT_STATUS)
    installment_paid = models.CharField(max_length=100, null=True)
    payment_details = models.TextField(null=True)
    contract_manager = models.CharField(max_length=100, null=True)
    funder = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.contract_name

    @property
    def compute_duration(self):
        start_date = self.start_date
        end_date = self.end_date
        new_start_date = self.new_start_date
        new_end_date = self.new_end_date
        span = end_date - start_date
        if start_date is not None and end_date is not None and new_start_date is None and new_end_date is None:
            span = end_date - start_date
            return span.days
        elif new_start_date is not None and new_end_date is not None:
            span = new_end_date - new_start_date
            return span.days
        elif start_date is not None and new_end_date is not None and new_start_date is None:
            span = new_end_date - start_date
            return span.days
        else:
            return 0


class Dependant(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)


class AlevelBackground(models.Model):
    LEVEL_CHOICES = (
        (None, '--please select--'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('higher_institutes', 'University/professional Institute')
    )
    name_of_school = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    level = models.CharField(max_length=20, null=True,choices=LEVEL_CHOICES)
    year = models.PositiveSmallIntegerField(blank=True, null=True, choices=YEAR_CHOICES)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return self.name_of_school

class Competency(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class LeadershipCompetency(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    text = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}'.format(self.text)


class Month6Appraisal(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='month6appraisal_staff')
    current_job_title = models.CharField(max_length=50, null=True, blank=False)
    supervisor = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, null=True, blank=True,related_name='month6appraisal_supervisor')
    implementation_activites = models.TextField(_('Implemented activities'),null=True, blank=True)
    implementation_activites2 = models.TextField(_('Lessons from implementation'),null=True, blank=True)
    planned_activities = models.TextField(null=True, blank=True)
    supervisor_comment = models.TextField(null=True, blank=True)
    staff_comment = models.TextField(null=True, blank=True)
    submission_date = models.DateField(auto_now=True)
    deputy_executive_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.staff.first_name)

class Month6AppraisalActivity(models.Model):
    appraisal = models.ForeignKey(Month6Appraisal, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('Activity'),null= False, blank=False, max_length=100)
    achievement = models.TextField(null=False, blank=False)
    staff_remarks = models.TextField(null=False, blank=False)
    supervisor_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Month6PlannedAppraisalActivity(models.Model):
    appraisal = models.ForeignKey(Month6Appraisal, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null= False, blank=False, max_length=100)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name