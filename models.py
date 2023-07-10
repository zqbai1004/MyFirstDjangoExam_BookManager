from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib import admin

import datetime


class Book(models.Model):
    book_inf = models.CharField(max_length=200,null=False,blank=False)
    pub_date = models.DateField('data published')
    available_quantity = models.IntegerField(default=1,null=False)
    total_quantity = models.IntegerField(default=1,null=False)
    borrow_times = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='books/cover_images', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_quantity = self.total_quantity

    def __str__(self):
        return self.book_inf

    def was_borrowed_recently(self):
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        recent_borrow_records = BorrowRecord.objects.filter(
            book=self,
            borrow_date__gte=one_day_ago,
            borrow_date__lte=timezone.now()
        )

        return recent_borrow_records.exists()




class BorrowRecord(models.Model):
    stu_id = models.CharField(max_length=8)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    reture_date = models.DateField(null=True, blank=True)

    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stu_id} - {self.book}"
