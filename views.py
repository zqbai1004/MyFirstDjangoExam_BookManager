from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.views import generic

from .models import Book,BorrowRecord

class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'most_borrow_list'

    def get_queryset(self):
        return Book.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(
            borrow_times=models.Count('borrowrecord',filter=models.Q(borrowrecord__borrow_date__lte=timezone.now()))
        ).order_by('-borrow_times')[:15]
        # 方法不能直接引用

class BookDetailView(generic.DetailView):
