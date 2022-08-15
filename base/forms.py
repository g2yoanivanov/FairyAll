from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Tale, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        labels = {'name': 'Име', 'username': 'Потребителско Име',
                  'password1': 'Парола', 'password2': 'Потвърди паролата'}


class TaleForm(ModelForm):
    class Meta:
        model = Tale
        fields = '__all__'
        labels = {'title': 'Заглавие', 'author': 'Автор',
                  'body': 'Съдържание', 'cover': 'Корица'}


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['picture', 'name', 'username', 'email', 'bio']
        labels = {'picture': 'Снимка', 'name': 'Име',
                  'username': 'Потребителско име', 'email': 'Email', 'bio': 'Нещо за вас'}
