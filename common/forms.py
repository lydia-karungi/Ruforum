import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Group
from contacts.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from .models import Document
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class SignUpForm(UserCreationForm):
    #title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    business_email = forms.EmailField(max_length=254, help_text='Required. Insert a valid email address.')
    home_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}))
    #nationality = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'multiple':''}),
                                   #  queryset=Country.objects.order_by('country_name').all())
    #country = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'multiple':''}),
                                    # queryset=Country.objects.order_by('country_name').all())
    mobile=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: none;'}),
                required=True,
                initial='+256'
                            )
    business_tel=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width: auto; display: inline-block;'}),
                required=True,
                initial='+256'
                            )
    class Meta:
        model = User
        exclude = []
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = None
        self.fields['nationality'].empty_label = None
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
        self.fields['mobile'].widget.attrs.update({'class':'form-control','style': 'width: 50%; display: inline-block;'})
        self.fields['business_tel'].widget.attrs.update({'class':'form-control','style': 'width: 50%; display: inline-block;'})


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    business_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  #  groups = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'multiple':
                                     #                            ''}),
                                    #  queryset=Group.objects.all())
    # sales = forms.BooleanField(required=False)
    # marketing = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['business_email', 'first_name', 'last_name', 'groups','picture'
                    
                ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['groups'].empty_label = None
        self.fields['first_name'].required = True
        if not self.instance.pk:
            self.fields['password'].required = True

        # self.fields['password'].required = True

    # def __init__(self, args: object, kwargs: object) -> object:
    #     super(UserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['first_name'].required = True
    #     self.fields['username'].required = True
    #     self.fields['email'].required = True
    #
        # if not self.instance.pk:
        #     self.fields['password'].required = True


    def clean(self):
       cleaned_data = super(UserForm, self).clean()
       password = cleaned_data.get("password")
       confirm_password = cleaned_data.get("confirm_password")

       if password != confirm_password:
           self.add_error('confirm_password', "Password does not match")

       return cleaned_data

    def clean_password(self):
         password = self.cleaned_data.get('password')

         if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
            return password

    def clean_has_sales_access(self):
        sales = self.cleaned_data.get('has_sales_access', False)
        user_role = self.cleaned_data.get('role')
        if user_role == 'ADMIN':
            is_admin = True
        else:
            is_admin = False
        if self.request_user.role == 'ADMIN' or self.request_user.is_superuser:
            if not is_admin:
                marketing = self.data.get('has_marketing_access', False)
                if not sales and not marketing:
                    raise forms.ValidationError('Select atleast one option.')
            # if not (self.instance.role == 'ADMIN' or self.instance.is_superuser):
            #     marketing = self.data.get('has_marketing_access', False)
            #     if not sales and not marketing:
            #         raise forms.ValidationError('Select atleast one option.')
        if self.request_user.role == 'USER':
            sales = self.instance.has_sales_access
        return sales

    def clean_has_marketing_access(self):
        marketing = self.cleaned_data.get('has_marketing_access', False)
        if self.request_user.role == 'USER':
            marketing = self.instance.has_marketing_access
        return marketing

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.id:
            if self.instance.email != email:
                if not User.objects.filter(
                        email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
                raise forms.ValidationError('Email already exists')
            else:
                return self.cleaned_data.get("email")
        else:
            if not User.objects.filter(
                    email=self.cleaned_data.get("email")).exists():
                return self.cleaned_data.get("email")
            raise forms.ValidationError('User already exists with this email')


class UserProfileForm(forms.ModelForm):


    class Meta:
        model = User
        fields = [
            'title',
            'business_email',
            'first_name',
            'last_name',
            'personal_email',
            'home_address',
            'business_address',
            'country',
            'nationality',
            'gender',
            'contact_type',
            'passport_no',
            'job_title',
            'institution',
            'area_of_specialisation',
            'home_tel',
            'business_tel',
            'mobile',
            'fax',
            'skype_id',
            'yahoo_messenger',
            'msn_id',
            'notes',
            'picture',
            'cv'

        ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True



class LoginForm(forms.ModelForm):
    business_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['business_email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
        return password

    def clean(self):
        business_email = self.cleaned_data.get("business_email")
        password = self.cleaned_data.get("password")


        if business_email and password:
            self.user = authenticate(username=business_email, password=password)
            if self.user:
                if not self.user.is_active:
                    pass
                    # raise forms.ValidationError("User is Inactive")
            else:
                pass
                # raise forms.ValidationError("Invalid email and password")
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    # CurrentPassword = forms.CharField(max_length=100)
    Newpassword = forms.CharField(max_length=100)
    confirm = forms.CharField(max_length=100)
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_confirm(self):
        # if len(self.data.get('confirm')) < 4:
        #     raise forms.ValidationError(
        #         'Password must be at least 4 characters long!')
        if self.data.get('confirm') != self.cleaned_data.get('Newpassword'):
            raise forms.ValidationError(
                'Confirm password do not match with new password')
        password_validation.validate_password(
            self.cleaned_data.get('Newpassword'), user=self.user)
        return self.data.get('confirm')


class PasswordResetEmailForm(PasswordResetForm):

    def clean_email(self):
        business_email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=business_email,
                                   is_active=True).exists():
            raise forms.ValidationError("User doesn't exist with this Email")
        return business_email




def find_urls(string):
    # website_regex = "^((http|https)://)?([A-Za-z0-9.-]+\.[A-Za-z]{2,63})?$"  # (http(s)://)google.com or google.com
    # website_regex = "^https?://([A-Za-z0-9.-]+\.[A-Za-z]{2,63})?$"  # (http(s)://)google.com
    # http(s)://google.com
    website_regex = "^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$"
    # http(s)://google.com:8000
    website_regex_port = "^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,63}:[0-9]{2,4}$"
    url = re.findall(website_regex, string)
    url_port = re.findall(website_regex_port, string)
    if url and url[0] != '':
        return url
    return url_port


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        exclude = []


class DocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        users = kwargs.pop('users', [])
        super(DocumentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['status'].choices = [
            (each[0], each[1]) for each in Document.DOCUMENT_STATUS_CHOICE]
        self.fields['status'].required = False
        self.fields['title'].required = True
        if users:
            self.fields['shared_to'].queryset = users
        self.fields['shared_to'].required = False
        #self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in Teams.objects.all().values('id', 'name')]
        #self.fields["teams"].required = False

    class Meta:
        model = Document
        fields = ['title', 'document_file', 'status', 'shared_to']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not self.instance:
            if Document.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    'Document with this Title already exists')
                return title
        if Document.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Document with this Title already exists')
            return title
        return title
