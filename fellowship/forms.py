import datetime

from django import forms
from .models import Fellowship, FellowshipComment
from contacts.models import User
from calls.models import FellowshipType
'''
from common.models import Comment, Attachments, User
from leads.models import Lead
from contacts.models import Contact
from django.db.models import Q
'''



class FellowshipForm(forms.ModelForm):
    #teams_queryset = []
    pi = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='PIs').order_by('first_name', 'last_name')
    )

    '''
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Students').order_by('first_name', 'last_name')
    )
    '''

    def __init__(self, *args, **kwargs):
        #account_view = kwargs.pop('account', False)
        #request_user = kwargs.pop('request_user', None)
        super(FellowshipForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['summary'].widget.attrs.update({'rows': '2'})
        self.fields['start_date'].widget.attrs = {"class": "form-control date"}
        self.fields['end_date'].widget.attrs = {"class": "form-control date"}
        self.fields['new_end_date'].widget.attrs={'class':'form-control date'}

        self.fields['approval_status'].required = True if self.instance else False # initially, we have a default
        self.fields['approval_status'].readonly = False if self.instance else True

       
    class Meta:
        model = Fellowship
        exclude = []

class FellowshipCommentForm(forms.ModelForm):
    fellowship = forms.IntegerField()
    created_by = forms.IntegerField()
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = FellowshipComment
        fields = ('fellowship','created_by','comment')

class FellowshipTypeForm(forms.ModelForm):

  

    def __init__(self, *args, **kwargs):

        super(FellowshipTypeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
        self.fields['name'].widget.attrs = {"class": "form-control"}
        self.fields['instructions'].widget.attrs = {"class": "form-control-file"}
        self.fields['review_form'].widget.attrs={'class':'form-control-file'}
       
    class Meta:
        model = FellowshipType
        exclude = []
