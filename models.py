# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib import admin

import datetime

TIMEOUTLIMIT = timezone.now() - datetime.timedelta(days=30)


class School(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def offer_book_count(self):
        return Book.objects.filter(
            offered_by=self,
            pub_date__lte=timezone.now()
        ).count()

    def offer_total_quantity(self):
        return Book.objects.filter(
            offered_by=self,
            pub_date__lte=timezone.now()
        ).aggregate(models.Sum('total_quantity'))['total_quantity__sum']

    def borrow_quantity(self):
        return BorrowRecord.objects.filter(
            student__school=self,
            borrow_date__lte=timezone.now()
        ).count()


class Major(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def borrow_quantity(self):
        return BorrowRecord.objects.filter(
            student__major=self,
            borrow_date__lte=timezone.now()
        ).count()


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    YEAR_CHOICES = [(r, r) for r in range(1980, datetime.date.today().year + 2)]
    stu_id = models.CharField(max_length=8)
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    grade = models.IntegerField(choices=YEAR_CHOICES)
    # borrow_time = models.IntegerField(default=0)  这里不跟books用同一种存储方法，这里不用冗余优化
    is_all_return_db = models.BooleanField(default=True) # 冗余优化
    borrow_times_db = models.IntegerField(default=0)  #还是用冗余优化吧，太慢了

    def __str__(self):
        return f"{self.stu_id}-{self.name}"

    def borrow_times(self):
        return BorrowRecord.objects.filter(
            student=self,
            borrow_date__lte=timezone.now()
        ).count()
    # 非冗余方法,好慢好慢，

    def return_times(self):
        borrow_records = BorrowRecord.objects.filter(
            student=self,
            borrow_date__lte=timezone.now()
        )
        return ReturnRecord.objects.filter(
            borrowrecord__in=borrow_records,
            borrowrecord__borrow_date__lte=timezone.now()
        ).count()

    def is_all_return(self):
        return self.return_times() == self.borrow_times_db

    def timeout_records(self):
        if self.is_all_return():
            return None
        else:
            borrow_records = BorrowRecord.objects.filter(
                student=self,
                borrow_date__lte=timezone.now(),
            )
            # 借走的记录
            return_records = ReturnRecord.objects.filter(
                borrowrecord__in=borrow_records,
                borrowrecord__borrow_date__lte=timezone.now()
            )
            # 归还的记录
            not_return_records = borrow_records.exclude(
                id__in=return_records.values_list('borrowrecord_id', flat=True)
            )
            # 借走中未归还的记录

            return not_return_records.order_by('borrow_date')

    def latest_borrow_date(self):
        latest_borrow_record = BorrowRecord.objects.filter(
            student=self,
            borrow_date__lte=timezone.now()
        ).order_by('-borrow_date').first()
        if latest_borrow_record:
            return latest_borrow_record.borrow_date
        else:
            return None

    def latest_return_date(self):
        latest_return_record = ReturnRecord.objects.filter(
            borrowrecord__student=self,
            borrowrecord__borrow_date__lte=timezone.now()
        ).order_by('-return_date').first()

        if latest_return_record:
            return latest_return_record.return_date
        else:
            return None

    def save(self, *args, **kwargs):
        self.borrow_times_db = self.borrow_times()
        self.is_all_return_db = self.is_all_return()
        super().save(*args, **kwargs)

    # for s in Student.objects.all():
    # ...     s.save()
    #刚加入时有小bug，用该语句“刷新”2023.7.11



class BookCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def book_quantity(self):
        return Book.objects.filter(
            category=self,
            pub_date__lte=timezone.now()
        ).aggregate(models.Sum('total_quantity'))['total_quantity__sum']

    def book_count(self):
        return Book.objects.filter(
            category=self,
            pub_date__lte=timezone.now()
        ).count()


class Book(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    pub_date = models.DateTimeField('data published')
    total_quantity = models.IntegerField(default=1, null=False)
    offered_by = models.ForeignKey(School, on_delete=models.PROTECT)
    cover_image = models.ImageField(upload_to='books/cover_images', null=True, blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT)
    borrow_times_db = models.IntegerField(default=0)  # 冗余优化

    def __str__(self):
        return f"{self.id}-{self.name}"

    def latest_borrow_date(self):
        latest_borrow_record =  BorrowRecord.objects.filter(
            book=self,
            borrow_date__lte=timezone.now()
        ).order_by('-borrow_date').first()
        if latest_borrow_record:
            return latest_borrow_record.borrow_date
        else:
            return None

    def was_borrowed_recently(self):
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        recent_borrow_records = BorrowRecord.objects.filter(
            book=self,
            borrow_date__gte=one_day_ago,
            borrow_date__lte=timezone.now()
        )

        return recent_borrow_records.exists()

    def available_quantity(self):
        borrow_records = BorrowRecord.objects.filter(
            book=self,
            borrow_date__lte=timezone.now()
        )
        return_records = ReturnRecord.objects.filter(
            borrowrecord__in=borrow_records,
            return_date__lte=timezone.now()
        )
        return self.total_quantity - borrow_records.count() + return_records.count()

    def borrow_times(self):
        return BorrowRecord.objects.filter(
            book=self,
            borrow_date__lte=timezone.now()
        ).count()

    def save(self, *args, **kwargs):
        self.borrow_times_db = self.borrow_times()
        super().save(*args, **kwargs)



class BorrowRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrow_date = models.DateTimeField()
    isreturned = models.BooleanField(default=False)  # 逻辑优化（修正）

    # def isreturn(self):
    #     return ReturnRecord.objects.exists(
    #         return_date__lte=timezone.now(),
    #         borrowrecord = self
    #     )
    # 循环依赖
    def __str__(self):
        return f"borrow：{self.student.name} - {self.book.name}"

    def save(self, *args, **kwargs):
        self.book.save()
        self.student.save()
        super().save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        self.book.save()
        self.student.save()
        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     self.book.borrow_times += 1
    #     self.book.save()
    #     super().save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     self.book.borrow_times -= 1
    #     self.book.save()
    #     super().delete(*args, **kwargs)
    #  这个逻辑无法成立，因为bookrecord不仅仅在创建时会使用save方法


class ReturnRecord(models.Model):
    return_date = models.DateTimeField()
    borrowrecord = models.ForeignKey(BorrowRecord, on_delete=models.CASCADE)

    def __str__(self):
        return f"return:{self.borrowrecord.student.name}-{self.borrowrecord.book.name}"

    def save(self, *args, **kwargs):
        self.borrowrecord.isreturned = True
        self.borrowrecord.save()
        super().save(*args, **kwargs)
        # 该逻辑是可以成立的

    def delete(self, *args, **kwargs):
        self.borrowrecord.isreturned = False
        self.borrowrecord.save()
        super().delete(*args, **kwargs)
