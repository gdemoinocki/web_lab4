# coding=windows-1251
"""
Definition of forms.
"""

from os import name
#from tokenize import Comment
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from app.models import Comment
from app.models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class AnketaForm(forms.Form):
    name=forms.CharField(label='Ваше Имя', min_length=2, max_length=50)
    username=forms.CharField(label='Имя пользователя', min_length=2, max_length=50)
    gender=forms.ChoiceField(label='Ваш пол', choices=[('1', 'Мужской'),('2', 'Женский'),('3', 'Другой')], widget=forms.RadioSelect, initial=1)
    evaluation=forms.ChoiceField(label='Оцените работу сайта по шкале от 1 до 5', choices=[('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')], 
                            widget=forms.RadioSelect, initial=1)
    notice=forms.BooleanField(label='Получать новости о сайте на e-mail?', 
                                required=False)
    email=forms.EmailField(label='Ваш e-mail',min_length=8, required=False)
    suggestion=forms.CharField(label='Жалобы и пожелания', widget=forms.Textarea(attrs={'row':12, 'cols':20}), required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # используемая модель
        fields = ('text',)  # требуется заполнить только поле text
        labels = {'text': "Комментарий"}  # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинки"}    