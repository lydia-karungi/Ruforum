from django import forms

from common.models import Attachments

"""
Forms module for small small hr
"""
from datetime import datetime, time

from django.contrib.auth.models import Group
from django import forms
from django.conf import settings
from contacts.models import User
from common.choices import MONTHS, PAST_YEARS
from django.db.models import Q
from django.utils.translation import ugettext as _

from django.forms import inlineformset_factory
import pytz
from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from .emails import leave_application_email
from .models import (
    Department, TWOPLACES,  LeaveApplication,LeaveType,Leave,
    Role, StaffDocument, StaffProfile, StaffTravel,Month6Appraisal,
    Month6AppraisalActivity,Month6PlannedAppraisalActivity,
    AssetCategory, Asset, Vehicle, Contract, Dependant, AlevelBackground, LeaveAssignment


)


from common.choices import NA_YES_NO
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class DepartmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Department
        exclude = []





class RoleForm(forms.ModelForm):
    """
    Form used when managing Role objects
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = Role
        fields = [
            'name',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'role-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('description',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-primary'),
            )
        )

class LeaveTypeForm(forms.ModelForm):
    """
    Form used when managing Leave objects
    """
    # start = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    #                                 required=True)
    # end = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    #                                 required=True)
    class Meta:  # pylint:
        """
        Class meta options
        """
        model = LeaveType
        exclude = []
     

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        


class LeaveAssignmentForm(forms.ModelForm):
    """
    Form used when managing Leave Assignments objects
    """
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=True)
   
    class Meta: 
        """
        Class meta options
        """
        model = LeaveAssignment
        exclude = ['staff']
     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leave_type'].empty_label = '--please select--'
        self.fields['year'].empty_label = None
        

class EditLeaveAssignmentForm(forms.ModelForm):
    """
    Form used when managing Leave Assignments objects
    """
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=True)
   
    class Meta: 
        """
        Class meta options
        """
        model = LeaveAssignment
        exclude = []
     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leave_type'].empty_label = '--please select--'
        self.fields['year'].empty_label = None
        

class LeaveApplicationForm(forms.ModelForm):
    """
    Form used when managing Leave objects
    """
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                     required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                     required=True)

    contact_person_phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True,
        initial='+256'
        )
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = LeaveApplication
        exclude = ['application_date','extra_requested_days','human_resource_comment','hr_comment_date','supervisor_recommendation','supervisor','recommendation_date','approval','staff']
     

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        staff = StaffProfile.objects.filter(user=self.request.user).values('id')
        current_year = datetime.now().year
        self.fields['leave_assignment'].queryset = LeaveAssignment.objects.filter(staff__id__in=staff,year=current_year)
        self.fields['leave_assignment'].empty_label = '--please select--'
        self.fields['leave_assignment'].label ='Leave'


    def clean(self):
        """
        Custom clean method
        """
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_assignment')
        staff = cleaned_data.get('staff')
        end = cleaned_data.get('end_date')
        start = cleaned_data.get('from_date')
        status = cleaned_data.get('status')

        if all([staff, leave_type, start, end]):
            # end year and start year must be the same
            if end.year != start.year:
                msg = _('start and end must be from the same year')
                self.add_error('start', msg)
                self.add_error('end', msg)

            # end must be later than start
            if end < start:
                self.add_error('end', _("end must be greater than start"))

            # must not overlap unless it is being rejected
            # pylint: disable=no-member
            overlap_qs = LeaveApplication.objects.filter(
                staff=staff,
                status=LeaveApplication.APPROVED,
                leave_type=leave_type).filter(
                    Q(start__gte=start) & Q(end__lte=end))

            if self.instance is not None:
                overlap_qs = overlap_qs.exclude(id=self.instance.id)

            if overlap_qs.exists() and status != LeaveApplication.REJECTED:
                msg = _('you cannot have overlapping leave days')
                self.add_error('start', msg)
                self.add_error('end', msg)




class StaffDocumentForm(forms.ModelForm):
    """
    Form used when managing StaffDocument objects
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = StaffDocument
        fields = [
            'staff',
            'name',
            'description',
            'public',
            'file',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.file:
            self.fields['file'].required = False
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'staffdocument-form'
        self.helper.layout = Layout(
            Field('staff',),
            Field('name',),
            Field('description',),
            Field('file',),
            Field('public',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-primary'),
            )
        )


class UserStaffDocumentForm(forms.ModelForm):
    """
    Form used when managing one's own StaffDocument objects
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = StaffDocument
        fields = [
            'staff',
            'name',
            'description',
            'file',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            # pylint: disable=no-member
            try:
                self.request.user.staffprofile
            except StaffProfile.DoesNotExist:
                pass
            else:
                self.fields['staff'].queryset = StaffProfile.objects.filter(
                    id=self.request.user.staffprofile.id)
        if self.instance and self.instance.file:
            self.fields['file'].required = False
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'staffdocument-form'
        self.helper.layout = Layout(
            Field('staff', type="hidden"),
            Field('name',),
            Field('description',),
            Field('file',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-primary'),
            )
        )





class StaffProfileAdminCreateForm(forms.ModelForm):
    """
    Form used when creating new Staff Profiles
    """
    user = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select user'}),
         queryset=User.objects.filter(staffprofile=None))

    id_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='Staff Number')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    physical_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 4, 'cols': 30}),
                                       required=True, label='Physical Home / residence address')
    staff_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True,
        initial='+256'
        )
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    district_of_residence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    county = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='County')
    sub_county = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Sub-county')
    parish = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    marital_status = forms.ChoiceField(choices=StaffProfile.MaritalStatus, widget=forms.Select(attrs=
                                                                            {'class': 'form-control'}), required=False)
    religion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    religious_conflicts = forms.ChoiceField(choices = NA_YES_NO,
                              widget=forms.Select(attrs={'class': 'form-control'}), required=True,
                                            label='Is there any concerns of your religion/beliefs that conflicts or '
                                                  'doesn’t agree with the Secretariat policies/rules and regulations ')

    Conflict = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),label='Please State it', required=False)
    name_of_spouse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    next_of_kin_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # next_of_kin_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    next_of_kin_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True,
        initial='+256'
        )
    next_of_kin_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),
                               required=True, label='Next of Kin Address')
    have_eye_defect = forms.ChoiceField(choices=NA_YES_NO,
                                         widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    state_eye_defect = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    state_back_problem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    have_allergy = forms.ChoiceField(choices=NA_YES_NO,
                                     widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    state_allergy = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    reason_for_leaving = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),
                                       required=True)
    department = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Department'}),
                                      queryset=Department.objects.all())
    pursuing_any_study = forms.ChoiceField(choices=NA_YES_NO, widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=True, label='Pursuing any study that may require time off from executing duty?')

    duration_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    duration_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    sponsored_by = forms.ChoiceField(choices = StaffProfile.sponsor,
                          initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    employed_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    employed_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    offence_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    offence_explanation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    action_taken = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    role = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Role'}),
                                      queryset=Role.objects.all(), required=True)
    nssf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
    nhif = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    work_permit_ID=forms.CharField(
        label=_('Work Permit ID'), required=False)
    work_permit_expiry_Date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    criminal_record = forms.ChoiceField(choices = NA_YES_NO,
                          initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    state_criminal_offense = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    any_other_information = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                                         'cols': 30}))
    Account_name = forms. CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    Bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    Account_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    currency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    laptop_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    modem_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    others = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = StaffProfile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(StaffProfileAdminCreateForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.fields['user'].empty_label = '--please select--'
        super().__init__(*args, **kwargs)


# edit staff form
class StaffProfileEditForm(forms.ModelForm):
    """
    Form used when creating new Staff Profiles
    """
    user = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select user'}),
         queryset=User.objects.all())

    id_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='Staff Number')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    physical_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 4, 'cols': 30}),
                                       required=True, label='Physical Home / residence address')
    staff_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True,
        initial='+256'
        )
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    district_of_residence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    county = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='County')
    sub_county = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Sub-county')
    parish = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    marital_status = forms.ChoiceField(choices=StaffProfile.MaritalStatus, widget=forms.Select(attrs=
                                                                            {'class': 'form-control'}), required=False)
    religion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    religious_conflicts = forms.ChoiceField(choices = NA_YES_NO,
                              widget=forms.Select(attrs={'class': 'form-control'}), required=True,
                                            label='Is there any concerns of your religion/beliefs that conflicts or '
                                                  'doesn’t agree with the Secretariat policies/rules and regulations ')

    Conflict = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),label='Please State it', required=False)
    name_of_spouse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    next_of_kin_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # next_of_kin_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    next_of_kin_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'style': 'width:50%; display:inline-block;'}),
        required=True,
        initial='+256'
        )
    next_of_kin_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),
                               required=True, label='Next of Kin Address')
    have_eye_defect = forms.ChoiceField(choices=NA_YES_NO,
                                         widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    state_eye_defect = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    state_back_problem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    have_allergy = forms.ChoiceField(choices=NA_YES_NO,
                                     widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    state_allergy = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    reason_for_leaving = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}),
                                       required=True)
    department = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Department'}),
                                      queryset=Department.objects.all())
    pursuing_any_study = forms.ChoiceField(choices=NA_YES_NO, widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=True, label='Pursuing any study that may require time off from executing duty?')

    duration_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    duration_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    sponsored_by = forms.ChoiceField(choices = StaffProfile.sponsor,
                          initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    employed_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    employed_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    offence_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    offence_explanation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    action_taken = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}), required=False)
    role = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Role'}),
                                      queryset=Role.objects.all(), required=True)
    nssf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
    nhif = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    work_permit_ID=forms.CharField(
        label=_('Work Permit ID'), required=False)
    work_permit_expiry_Date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    criminal_record = forms.ChoiceField(choices = NA_YES_NO,
                          initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    state_criminal_offense = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    any_other_information = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                                         'cols': 30}))
    Account_name = forms. CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    Bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    Account_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    currency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    laptop_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    modem_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    others = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30}))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = StaffProfile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(StaffProfileEditForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.fields['user'].empty_label = '--please select--'
        super().__init__(*args, **kwargs)


class StaffTravelForm(forms.ModelForm):
    TRUE_FALSE_CHOICES=(
        (None, '--please select--'),
        (True, 'Yes'),
        (False, 'No')
    )

    attach_travel_report = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control' }), choices=TRUE_FALSE_CHOICES)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    back_to_office_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 5, 'cols': 30}),required=False)

    def __init__(self, *args, **kwargs):
        super(StaffTravelForm, self).__init__(*args, **kwargs)
        self.fields['staff'].empty_label = None
        self.fields['travel_mode'].empty_label=None
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'stafftravel-form'

    class Meta:
        model = StaffTravel
        exclude = []


class AssetCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetCategoryForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = AssetCategory
        exclude = []


class AssetForm(forms.ModelForm):
    insurance_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    insurance_company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    insurance_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    insurance_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    warranty_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    working = forms.ChoiceField(choices = Asset.WORKING_CONDITION,
                         widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    repairable = forms.ChoiceField(choices = Asset.REPAIRABLE,
                         widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    engravement_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Department'}),
                                      queryset=AssetCategory.objects.all())

    asset_model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    asset_value = forms.DecimalField(widget = forms.NumberInput(attrs={'class': 'form-control'}))
    asset_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    invoice_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 5, 'cols': 30}),required=False)
    image = forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*','type': 'file'})
    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'asset-form'

    class Meta:
        model = Asset
        exclude = ['assigned_to']


class AssignAssetForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Department'}),
                                      queryset=StaffProfile.objects.all())
    class Meta:
        model = Asset
        fields = [
            'assigned_to'
        ]
    def __init__(self, *args, **kwargs):
        super(AssignAssetForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].empty_label = None

class VehicleForm(forms.ModelForm):
    date_of_purchase = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    insurance_valid_upto = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    insurance_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    waranty_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    waranty_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    photo= forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*',
                                      'type': 'file'}),required=False)

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.fields['depreciation_cost'].required = False


    class Meta:
        model = Vehicle
        exclude = []


class ContractForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    new_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    new_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control", "type": "date"}
                continue
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Contract
        exclude = []



class TravelAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'travel')


class DependantsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    required=False)
    class Meta:
        model = Dependant
        exclude = ['staff', ]


DependantsFormSet = inlineformset_factory(StaffProfile, Dependant,
                                                  form=DependantsForm, extra=0, max_num=3,min_num=1, can_delete=True)


class AlevelBackgroundForm(forms.ModelForm):
    name_of_school = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     required=True, label='University/School')
    qualification = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = AlevelBackground
        exclude = ['staff' ]


AlevelBackgroundFormSet = inlineformset_factory(StaffProfile, AlevelBackground,
                                                  form=AlevelBackgroundForm, extra=0, max_num=5,min_num=1, can_delete=True)



class LeaveHRConfirmationForm(forms.ModelForm):
    
    human_resource_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 4, 'cols': 30}),required=False)
    class Meta:
        model = LeaveApplication
        fields = ['human_resource_comment']

    def __init__(self, *args, **kwargs):

        super(LeaveHRConfirmationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

class LeaveSupervisorRecommendationForm(forms.ModelForm):
    
    supervisor_comment= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',  'rows': 4, 'cols': 30}),required=False)
    class Meta:
        model = LeaveApplication
        fields = ['supervisor_comment','supervisor_recommendation']

    def __init__(self, *args, **kwargs):

        super(LeaveSupervisorRecommendationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

class LeaveAppApprovalForm(forms.ModelForm):
    
    approval = forms.CharField(widget=forms.Select(choices=LeaveApplication.APPROVAL, attrs={'class':'form-control'}),required=True, label='Approve')
    start = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    end = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    leave_days = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False, label='Leave Days Approved')
    class Meta:
        model = Leave
        fields = ['approval','start','end','leave_days']

    def __init__(self, *args, **kwargs):

        super(LeaveAppApprovalForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[:2]

# month 6 performance appraisal form
class Month6AppraisalForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        super(Month6AppraisalForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if 'date' in name:
                field.widget.attrs = {"class": "form-control", "type": "date"}
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['implementation_activites'].widget.attrs.update({'rows': '2'})
        self.fields['implementation_activites2'].widget.attrs.update({'rows': '2'})
        self.fields['planned_activities'].widget.attrs.update({'rows': '2'})
      

    class Meta:
        model = Month6Appraisal
        exclude = ['supervisor','staff_comment','supervisor_comment','deputy_executive_comment']


class Month6AppraisalActivityForm(forms.ModelForm):
   
    class Meta:
        model = Month6AppraisalActivity
        exclude = ['appraisal']
    
    def __init__(self, *args, **kwargs):
        super(Month6AppraisalActivityForm, self).__init__(*args, **kwargs)
        self.fields['achievement'].widget.attrs.update({'rows': '2'})
        self.fields['supervisor_remarks'].widget.attrs.update({'rows': '2'})
        self.fields['staff_remarks'].widget.attrs.update({'rows': '2'})
    


Month6AppraisalActivityFormSet = inlineformset_factory(Month6Appraisal, Month6AppraisalActivity,
                                                  form=Month6AppraisalActivityForm, extra=0, max_num=10,min_num=1, can_delete=True)


class Month6PlannedAppraisalActivityForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=True)
   
    class Meta:
        model = Month6PlannedAppraisalActivity
        exclude = ['appraisal']
    
    


Month6PlannedAppraisalActivityFormSet = inlineformset_factory(Month6Appraisal, Month6PlannedAppraisalActivity,
                                                  form=Month6PlannedAppraisalActivityForm, extra=0, max_num=10,min_num=1, can_delete=True)
