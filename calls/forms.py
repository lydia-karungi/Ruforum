import datetime

from django import forms
from .models import GrantCall, Call,Subtheme,FellowshipCall,Commodityfocus,Theme,Subtheme
from contacts.models import User


class CallForm(forms.ModelForm):
    submission_deadline = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}


        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+91-123-456-7890"
            else:
                value.widget.attrs['placeholder'] = value.label
        self.fields['commodity_focus'].empty_label = None
        self.fields['grant_type'].empty_label = None
        self.fields['proposal_theme'].empty_label = '--select--'
        #self.fields['proposal_sub_theme'].queryset = Subtheme.objects.none()

        if 'proposal_theme' in self.data:
            try:
                theme_id = int(self.data.get('proposal_theme'))
                self.fields['proposal_sub_theme'].queryset = Subtheme.objects.filter(theme_id=theme_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to emptyqueryset
        elif self.instance.pk:
            self.fields['proposal_theme'].initial = self.instance.proposal_theme
            self.fields['proposal_sub_theme'].initial = self.instance.proposal_sub_theme

    class Meta:
        model = GrantCall
        exclude = ['call_id','call_year','generated_number']

class CallReviewersForm(forms.ModelForm):

    class Meta:
        model = GrantCall
        fields = [
        ]

class CommodityfocusForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)

    class Meta:
        model = Commodityfocus
        fields = ['name'
        ]

class ThemeForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)

    class Meta:
        model = Theme
        fields = ['name'
        ]

class SubthemeForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    theme = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=Theme.objects.all())

    class Meta:
        model = Subtheme
        fields = ['name','theme'
        ]

# form for the scholarship call
class ScholarshipCallForm(forms.ModelForm):
    submission_deadline = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    review_form = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'type': 'file'}),required=False)

    def __init__(self, *args, **kwargs):
        super(ScholarshipCallForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]


    class Meta:
        model = Call
        exclude = ['call_id','call_year','generated_number']
# form for the scholarship call
class FellowshipCallForm(forms.ModelForm):
    submission_deadline = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(FellowshipCallForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}


        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+91-123-456-7890"
            else:
                value.widget.attrs['placeholder'] = value.label

    class Meta:
        model = FellowshipCall
        exclude = ['call_id','call_year','generated_number']
