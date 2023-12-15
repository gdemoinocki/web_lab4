# coding=windows-1251
"""
Definition of urls for web_lab4.
"""
from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
admin.autodiscover()



urlpatterns = [
    path('anketa/', views.anketa, name='anketa'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('videopost/', views.videopost, name='videopost'),
    re_path(r'^(?P<parametr>\d+)/$', views.blogpost, name='blogpost'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

