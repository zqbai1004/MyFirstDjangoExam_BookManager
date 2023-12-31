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
    path('index/', views.index, name='index'),

    path('index/book/', views.BookIndexView.as_view(), name='book_index'),
    path('index/student/', views.student_index, name='student_index'),

    path('detail/book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('detail/student/<int:pk>', views.student_detail, name="student_detail"),

    path('search/book', views.BookSearchView.as_view(), name='book_search'),
    path('search/student', views.student_search, name='student_search'),

    path('run/book/<int:book_id>/<int:student_id>', views.book_run, name='book_run'),
    path('run/student/<int:book_id>/<int:student_id>',views.stu_run, name='student_run'),

    path('index/category/', views.category_index,name='category_index'),
    path('index/school/', views.school_index, name='school_index'),
    path('index/major/', views.major_index, name='major_index'),

    path('detail/school/<int:pk>',views.school_detail,name="school_detail"),
    path('detail/major/<int:pk>', views.major_detail, name="major_detail"),
    path('detail/category/<int:pk>', views.category_detail, name="category_detail")

]
