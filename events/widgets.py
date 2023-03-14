from django.forms.widgets import TimeInput, DateInput


class DatePickerInput(DateInput):
    input_type = 'date'


class TimePickerInput(TimeInput):
    input_type = 'time'
