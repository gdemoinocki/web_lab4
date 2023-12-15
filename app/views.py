# coding=windows-1251
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm, BlogForm 
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from .models import Blog
from .models import Comment
from .forms import CommentForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            #'message':'Ваша страница контактов',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О сайте',
            #'message':'Страница с описанием вашего приложения',
            'year':datetime.now().year,
        }
    )
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина', '3': 'Другой'}
    evaluation = {'1': '1', '2': '2', '3': '3','4': '4', '5': '5'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['username'] = form.cleaned_data['username']
            data['gender'] = gender[form.cleaned_data['gender']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else: 
                  data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email'] 
            data['suggestion'] = form.cleaned_data['suggestion'] 
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data': data
        }
        )
def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  
            reg_f = regform.save(commit=False) 
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            return redirect('home')  # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()  # запрос на выбор всех статей блога из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Cтатьи.navbar-nav',
            'posts': posts,  # передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_1 = Blog.objects.get(id=parametr)  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()  # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(
                id=parametr)  # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save()  # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id)  # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm()  # создание формы для ввода комментария

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # передача конкретной статьи в шаблон веб-страницы
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f: Blog = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year
        }
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео-ролики',
            'year': datetime.now().year,
        }
    )

