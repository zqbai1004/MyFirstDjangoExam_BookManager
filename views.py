# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.db.models import Q
from django.views import generic
from django.core.paginator import Paginator
from django.contrib import messages

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
    no_all_return_student = Student.objects.filter(is_all_return_db=False)  # 冗余优化后的筛选，底层用SQL实现
    all_return_student = Student.objects.filter(is_all_return_db=True)
    all_return_student_ordered_by_borrow_time = Student.objects.filter(
        is_all_return_db=True
    ).order_by('-borrow_times_db')
    no_all_return_student_pages = Paginator(no_all_return_student, 20)
    all_return_student_ordered_by_borrow_time_pages = Paginator(all_return_student_ordered_by_borrow_time, 20)
    # 分页器
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    page_obj1 = no_all_return_student_pages.get_page(page1)
    page_obj2 = all_return_student_ordered_by_borrow_time_pages.get_page(page2)

    # 未冗余优化，只能以python实现
    context = {'all_return_student_ordered_by_borrow_time_pages': page_obj2,
               'no_all_return_student_pages': page_obj1,
               'page1': page1,
               'page2': page2
               }

    return render(request, 'books/student_index.html', context)


def student_search(request):
    search_str = request.GET.get('q')
    if search_str:
        student_search_results = Student.objects.filter(
            Q(stu_id__icontains=search_str) | Q(name__icontains=search_str)
        )
    else:
        student_search_results = Student.objects.none()
    context = {'search_str': search_str, 'student_search_results': student_search_results}

    return render(request, 'books/student_search.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    book_inf = request.GET('book_inf')

    no_results = not Book.objects.filter(
        id=book_inf
    ).exists()
    context = {'student': student, 'no_results': no_results}

    return render(request, 'books/student_detail.html', context)


class BookIndexView(generic.ListView):
    model = Book
    template_name = 'books/book_index.html'
    context_object_name = 'most_borrow_list'

    def get_queryset(self):
        return Book.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-borrow_times_db')

    # 冗余优化带来的便利，相比使用临时声明排序borrow_times方法返回值
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
            ).order_by('-borrow_times_db')
        else:
            return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_str'] = self.request.GET.get('q')
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stu_inf = self.request.GET.get('stu_inf', '')
        no_results = not Student.objects.filter(
            stu_id=stu_inf
        ).exists() if stu_inf else True
        context['no_results'] = no_results
        context['stu_inf'] = stu_inf
        can_borrow = None
        can_return = None
        if not no_results:
            can_borrow = self.object.available_quantity()
            can_return = BorrowRecord.objects.filter(
                borrow_date__lte=timezone.now(),
                book=self.object,
                isreturned=False,
                student__stu_id=stu_inf
            ).exists()
        context['can_borrow'] = can_borrow
        context['can_return'] = can_return

        return context


def run(request, book_id, student_id):
    if request.POST['b_or_r'] == '1':
        new_borrow_record = BorrowRecord(book=get_object_or_404(Book, id=book_id),
                                         student=get_object_or_404(Student, stu_id=student_id),
                                         borrow_date=timezone.now())
        new_borrow_record.save()
    elif request.POST['b_or_r'] == '2':
        related_borrow_record = BorrowRecord.objects.filter(
                                                            student__stu_id=student_id,
                                                            book_id=book_id,
                                                            borrow_date__lte=timezone.now()
                                                            )
        if not related_borrow_record.exists():
            return Http404
        related_borrow_record = related_borrow_record.order_by('borrow_date').first()
        # 选最早借的还
        new_return_record = ReturnRecord(
            borrowrecord=related_borrow_record,
            return_date=timezone.now()
        )
        new_return_record.save()
    else:
        return Http404
    messages.success(request, 'Operation successful!')
    # 成功弹窗还是要用Javascript做？这个好像直接被覆盖掉了
    return


def book_run(request, book_id, student_id):
    run(request, book_id, student_id)
    return HttpResponseRedirect(reverse('books:book_detail', args=(book_id,)) + "?stu_inf=" + str(student_id))


def stu_run(request, book_id, student_id):
    run(request, book_id, student_id)
    return HttpResponse(reverse('books:student_detail', args=(student_id,)))
