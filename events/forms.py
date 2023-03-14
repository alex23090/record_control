from django.forms import ModelForm
from .models import Event
from .widgets import DatePickerInput, TimePickerInput
from django import forms
import datetime


class ClientEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['worker', 'date', 'start_time']
        widgets = {
            'date': DatePickerInput(attrs={'min': datetime.date.today()}),
            'start_time': TimePickerInput(attrs={'type': 'time', 'min': '08:00', 'max': '17:00'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClientEventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


class WorkerEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['client', 'date', 'start_time']
        widgets = {
            'date': DatePickerInput(attrs={'min': datetime.date.today()}),
            'start_time': TimePickerInput(attrs={'type': 'time', 'min': '08:00', 'max': '17:00'}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkerEventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


class DateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}), label='', label_suffix='', required=False)

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control me-2', 'name': 'date'})
