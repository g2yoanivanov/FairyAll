from email import contentmanager, message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, AuthorForm, TaleForm, UserForm
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
        Q(title__icontains=q.lower())
    )[0:3]

    authors = Author.objects.all()[0:4]
    user_messages = Message.objects.all()[0:7]

    all_tales = Tale.objects.all()
    tales_count = all_tales.count()

    context = {'tales': tales, 'authors': authors,
               'user_messages': user_messages, 'tales_count': tales_count}
    return render(request, 'base/home.html', context)


def author_profile(request, pk):
    author = Author.objects.get(id=pk)
    authors = Author.objects.all()[0:10]
    user_messages = Message.objects.all()[0:7]

    all_tales = Tale.objects.all()
    tales_count = all_tales.count()

    context = {'author': author, 'authors': authors,
               'user_messages': user_messages, 'tales_count': tales_count}
    return render(request, 'base/author.html', context)


def tale(request, pk):
    tale = Tale.objects.get(id=pk)
    tales = Tale.objects.all()[0:7]

    context = {'tale': tale, 'tales': tales}
    return render(request, 'base/tale.html', context)


def all_tales(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    tales = Tale.objects.filter(
        Q(author__name__icontains=q) |
        Q(title__icontains=q.lower())
    )

    context={'tales': tales}
    return render(request, 'base/all_tales.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    user_messages = user.message_set.all()[0:3]
    authors = Author.objects.all()

    all_tales = Tale.objects.all()
    tales_count = all_tales.count()

    context = {'user': user, 'user_messages': user_messages, 'authors': authors, 'tales_count': tales_count}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/creation-form.html', {'form': form})


@login_required(login_url='login')
def forum(request):
    user_messages = Message.objects.all()[0:100]

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            body=request.POST.get('body')
        )
        return redirect('forum')

    context = {'user_messages': user_messages}
    return render(request, 'base/forum.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Нямате достъп до тази страница')

    if request.method == 'POST':
        message.delete()
        return redirect('forum')
    return render(request, 'base/delete.html', {'obj': message})


# TODO: add a view for a staff members page

@staff_member_required
def create_tale(request):
    title = 'tale-create'
    form = TaleForm()

    if request.method == 'POST':
        form = TaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # TODO: redirect to a page for the staff members
            return redirect('home')
        else:
            messages.error(request, 'Неуспешно създаване на приказка')

    context = {'form': form, 'title': title}
    return render(request, 'base/creation-form.html', context)


@staff_member_required
def update_tale(request, pk):
    title = 'tale-update'
    tale = Tale.objects.get(id=pk)
    form = TaleForm(instance=tale)

    if not request.user.is_staff:
        return HttpResponse('Нямате достъп до тази страница!')

    if request.method == 'POST':
        form = TaleForm(request.POST, request.FILES, instance=tale)
        if form.is_valid():
            form.save()
            # TODO: redirect to a page for the staff members
            return redirect('home')

    context = {'form': form, 'title': title}
    return render(request, 'base/creation-form.html', context)


@staff_member_required
def delete_tale(request, pk):
    tale = Tale.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse('Нямате достъп до тази страница!')

    if request.method == 'POST':
        tale.delete()
        return redirect('home')

    context = {'obj': tale}
    return render(request, 'base/delete.html', context)


@staff_member_required
def create_author(request):
    title = 'author-create'
    form = AuthorForm()

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # TODO: redirect to a page for the staff members
            return redirect('home')
        else:
            messages.error(request, 'Неуспешно създаване на автор')

    context = {'form': form, 'title': title}
    return render(request, 'base/creation-form.html', context)


@staff_member_required
def update_author(request, pk):
    title = 'author-update'
    author = Author.objects.get(id=pk)
    form = AuthorForm(instance=author)

    if not request.user.is_staff:
        return HttpResponse('Нямате достъп до тази страница!')

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=tale)
        if form.is_valid():
            form.save()
            # TODO: redirect to a page for the staff members
            return redirect('home')

    context = {'form': form, 'title': title}
    return render(request, 'base/creation-form.html', context)


@staff_member_required
def delete_author(request, pk):
    author = Author.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse('Нямате достъп до тази страница!')

    if request.method == 'POST':
        author.delete()
        return redirect('home')

    context = {'obj': author}
    return render(request, 'base/delete.html', context)


def all_authors(request):
    authors = Author.objects.all()
    all_tales = Tale.objects.all()
    tales_count = all_tales.count()

    context={'authors': authors, 'tales_count': tales_count}
    return render(request, 'base/all_authors.html', context)

