import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from .models import User, Country, Author, Tale, Message


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get('email')
        except:
            messages.error(request, 'Потребителят не съществува')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Пощата или паролата са неправилни')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Настъпи някаква грешка! Опитайте отново!')

    context = {'form': form}

    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    tales = Tale.objects.filter(
        Q(author__name__icontains=q) |
        Q(title__icontains=q)
    )[0:3]

    authors = Author.objects.all()[0:5]
    user_messages = Message.objects.all()[0:3]

    tales_count = tales.count()

    context = {'tales': tales, 'authors': authors,
               'user_messages': user_messages, 'tales_count': tales_count}
    return render(request, 'base/home.html', context)


def author_profile(request, pk):
    author = Author.objects.get(id=pk)
    authors = Author.objects.all()[0:5]
    user_messages = Message.objects.all()[0:3]

    context = {'author': author, 'authors': authors,
               'user_messages': user_messages}
    return render(request, 'base/author.html', context)


def tale(request, pk):
    tale = Tale.objects.get(id=pk)

    context = {'tale': tale}
    return render(request, 'base/tale.html', context)
