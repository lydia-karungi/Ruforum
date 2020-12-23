import datetime

from django import forms
from .models import Granttype

from grant_types.models import Granttype


class GranttypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GranttypeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name.startswith('require'):
                continue
            field.widget.attrs = {"class": "form-control"}
            self.fields['instructions'].widget.attrs.update({'class': 'form-control-file'})
            self.fields['template'].widget.attrs.update({'class': 'form-control-file'})
            self.fields['project_budget_template'].widget.attrs.update({'class': 'form-control-file'})
            self.fields['review_form_template'].widget.attrs.update({'class': 'form-control-file'})

    class Meta:
        model = Granttype
        exclude = []
