from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.utils import timezone

from django.views import generic

from .models import Book,BorrowRecord

class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'latest_borrowed_list'

    def get_queryset(self):
        return Book.objects.filter(
            borrowrecord__borrow_date=timezone.now()
        ).order_by('borrowrecord__borrow_date').distinct()[10]
