# coding=windows-1251
"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.contrib import admin
from django.urls import reverse

class Blog(models.Model):
    #id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="���������")
    description = models.TextField(verbose_name="������� ����������")
    content = models.TextField(verbose_name="������ ����������")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="������������")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="�����")
    image = models.FileField(default="temp.jpg", verbose_name="���� � ��������")
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["posted"]
        verbose_name = "������ �����"
        verbose_name_plural = "������ �����"

class Comment(models.Model):
    text = models.TextField(verbose_name="�����������")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="����")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="�����")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="������")

    def __str__(self):
        return f"����������� {self.author} � ������ \"{self}\""

    class Meta:
        db_table = "Comments"
        verbose_name = "�����������"
        verbose_name_plural = "����������� � ������� �����"
        ordering = ["-date"]


admin.site.register(Blog)
admin.site.register(Comment)