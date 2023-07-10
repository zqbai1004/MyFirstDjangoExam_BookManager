# -*- coding: utf-8 -*-

"""
Author: zqbai
Created Time: 2023/7/7 20:42
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(),name='index')
]