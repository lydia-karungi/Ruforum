from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'has_reports':
                continue
            field.widget.attrs = {"class": "form-control"}
       # self.fields['start_date'].widget.attrs = {"class": "form-control"}
       # self.fields['end_date'].widget.attrs = {"class": "form-control"}

    class Meta:
        model = Event
        exclude = []