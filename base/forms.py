from wsgiref.validate import validator
from django import forms
from django.contrib.auth import password_validation
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Tale, User


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Парола"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Потвърдете паролата"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Въведете същата парола!"),
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        labels = {'name': 'Име', 'username': 'Потребителско Име'}


class TaleForm(ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Tale
        fields = '__all__'
        labels = {'title': 'Заглавие', 'author': 'Автор',
                  'body': 'Съдържание', 'cover': 'Корица'}


class AuthorForm(ModelForm):
    bio = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Author
        fields = '__all__'
        labels = {'name': 'Име', 'nationality': 'Националност',
                  'bio': 'Биография', 'picture': 'Снимка'}


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['picture', 'name', 'username',
                  'email', 'favourite_tale', 'bio']
        labels = {'picture': 'Снимка', 'name': 'Име',
                  'username': 'Потребителско име', 'email': 'Email', 'bio': 'Нещо за вас', 'favourite_tale': 'Любима приказка'}
