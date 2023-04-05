from django import forms
from django.forms import ModelForm
from .models import User, Client, Worker
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


class ClientSignUpForm(CustomUserCreationForm):

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user)
        client.name = self.cleaned_data.get('first_name')
        client.username = self.cleaned_data.get('username')
        client.email = self.cleaned_data.get('email')
        client.save()
        return user

    def __init__(self, *args, **kwargs):
        super(ClientSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


class WorkerSignUpForm(CustomUserCreationForm):

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_worker = True
        user.save()
        worker = Worker.objects.create(user=user)
        worker.name = self.cleaned_data.get('first_name')
        worker.username = self.cleaned_data.get('username')
        worker.email = self.cleaned_data.get('email')
        worker.location = self.cleaned_data.get('location')
        worker.save()
        return user

    def __init__(self, *args, **kwargs):
        super(WorkerSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


class ClientAccountForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'username', 'email', 'profile_image']
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'username': forms.TextInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(ClientAccountForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


class WorkerAccountForm(ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'username', 'email', 'profile_image', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'username': forms.TextInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkerAccountForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'
