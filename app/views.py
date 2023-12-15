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
            'title':'�������� ��������',
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
            'title':'��������',
            #'message':'���� �������� ���������',
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
            'title':'� �����',
            #'message':'�������� � ��������� ������ ����������',
            'year':datetime.now().year,
        }
    )
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': '�������', '2': '�������', '3': '������'}
    evaluation = {'1': '1', '2': '2', '3': '3','4': '4', '5': '5'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['username'] = form.cleaned_data['username']
            data['gender'] = gender[form.cleaned_data['gender']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = '��'
            else: 
                  data['notice'] = '���'
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
    if request.method == "POST":  # ����� �������� �����
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  
            reg_f = regform.save(commit=False) 
            reg_f.is_staff = False  # �������� ���� � ���������������� ������
            reg_f.is_active = True  # �������� ������������
            reg_f.is_superuser = False  # �� �������� ������������������
            reg_f.date_joined = datetime.now()  # ���� �����������
            reg_f.last_login = datetime.now()  # ���� ��������� �����������
            reg_f.save()  # ��������� ��������� ����� ���������� ������
            return redirect('home')  # ������������� �� ������� �������� ����� �����������
    else:
        regform = UserCreationForm()  # �������� ������� ����� ��� ����� ������ ������ ������������
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # �������� ����� � ������ ���-��������
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()  # ������ �� ����� ���� ������ ����� �� ������

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'C�����.navbar-nav',
            'posts': posts,  # �������� ������ ������ � ������ ���-��������
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_1 = Blog.objects.get(id=parametr)  # ������ �� ����� ���������� ������ �� ���������
    comments = Comment.objects.filter(post=parametr)
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # ����� �������� ������ ����� �� ������ ������� POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()  # ��������� � ������ ����������� (Comment) ������� ����
            comment_f.post = Blog.objects.get(
                id=parametr)  # ��������� � ������ ����������� (Comment) ������, ��� ������� ������ �����������
            comment_f.save()  # ��������� ��������� ����� ���������� �����
            return redirect('blogpost', parametr=post_1.id)  # ������������� �� �� �� �������� ������ ����� �������� �����������
    else:
        form = CommentForm()  # �������� ����� ��� ����� �����������

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # �������� ���������� ������ � ������ ���-��������
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
            'title': '�������� ������ �����',
            'year': datetime.now().year
        }
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': '�����-������',
            'year': datetime.now().year,
        }
    )

