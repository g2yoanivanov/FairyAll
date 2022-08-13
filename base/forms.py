from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Tale, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        labels = {'name': 'Име', 'username': 'Потребителско Име', 'password1': 'Парола', 'password2': 'Потвърди паролата'}