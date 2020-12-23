from django import forms

from hrm.models import StaffProfile
from tasks.models import Task
from contacts.models import User
from common.models import Attachments, Comment
from django.db.models import Q
from teams.models import Teams


class TaskForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)
    due_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=StaffProfile.objects.all().order_by('user__first_name', 'user__last_name'), required=False
    )
    new_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
            self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in Teams.objects.all().values('id', 'name')]

        self.fields["teams"].required = False
        self.fields['assigned_to'].required = False
        self.fields['title'].required = True
        self.fields['status'].required = True
        self.fields['priority'].required = True
        self.fields['due_date'].required = False


    class Meta:
        model = Task
        fields = (
            'title', 'status', 'priority', 'assigned_to',
            'due_date', 'from_date'
        )


class TaskCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'task', 'commented_by')


class TaskAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'task')
