from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
from django.views import generic

from .models import *


def index(request):
    return render(request, 'books/index.html')

# def book_search(request):
#     query = request.GET.get('q')
#     if query:
#         results = Book.objects.filter(
#             Q(id__icontains=query) | Q(name__icontains=query),
#             pub_date__lte=timezone.now()
#         )
#     else:
#         results = Book.objects.none()
#
#     return render(request, 'books/book_search.html', {'results': results})
# 基于函数的视图，也可以用，更加简单直观，但是失去了类的继承性和灵活性

def student_index(request):
    all_student = Student.objects.all()
    no_all_return_student = Student.objects.filter(is_all_return_db=False) # 冗余优化后的筛选，底层用SQL实现
    all_return_student = Student.objects.filter(is_all_return_db=True)
    all_return_student_ordered_by_borrow_time = sorted(all_return_student, key=lambda student: student.is_all_return())
    # 未冗余优化，只能以python实现
    context = {'all_return_student_ordered_by_borrow_time':all_return_student_ordered_by_borrow_time,
               'no_all_return_student':no_all_return_student}

    return render(request,'books/student_index.html',context)

def student_search(request):
    search_str = request.GET.get('q')
    if search_str:
        student_search_results = Student.objects.filter(
            Q(stu_id__icontains=search_str) | Q(name__icontains=search_str)
        )
    else:
        student_search_results = Student.objects.none()
    context = {'search_str':search_str,'student_search_results':student_search_results}

    return render(request,'books/student_search.html',context)




class BookIndexView(generic.ListView):
    model = Book
    template_name = 'books/book_index.html'
    context_object_name = 'most_borrow_list'
    def get_queryset(self):
        return Book.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-borrow_times')
    # 冗余优化带来的便利，相比StudentIndexView


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_books'] = Book.objects.all()
        return context

class BookSearchView(generic.ListView):
    model = Book
    template_name = 'books/book_search.html'
    context_object_name = 'book_search_results'  # 在模板中使用的变量名

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(id__icontains=query) | Q(name__icontains=query),
                pub_date__lte=timezone.now()
            )
        else:
            return Book.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_str'] = self.request.GET.get('q')
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'