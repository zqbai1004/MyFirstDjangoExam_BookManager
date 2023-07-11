# -*- coding: utf-8 -*-

"""
Author: zqbai
Created Time: 2023/7/7 20:42
"""
from django.urls import path, include
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/',views.index,name='index'),
    path('index/book/', views.BookIndexView.as_view(), name='book_index'),
    path('index/student/', views.student_index, name='student_index'),
    path('detail/book/<int:pk>',views.BookDetailView.as_view(),name='book_detail'),
    path('search/book', views.BookSearchView.as_view(),name='book_search'),
    path('search/student', views.student_search, name='student_search')

]
