from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class Country(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=128)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    bio = RichTextField()
    picture = models.ImageField(null=True, default='picture.svg')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tale(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = RichTextField()
    cover = models.ImageField(null=True, default='cover.jpg')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['author', 'created']

    def __str__(self):
        return self.title


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = RichTextField(null=True)
    picture = models.ImageField(null=True, default="avatar.svg")

    favourite_tale = models.ForeignKey(
        Tale, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
