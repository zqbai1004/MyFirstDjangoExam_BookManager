from django.contrib import admin

# Register your models here.
from .models import *


class BorrowRecordsInline(admin.TabularInline):
    model = BorrowRecord
    extra = 1


class ReturnRecordsInline(admin.TabularInline):
    model = ReturnRecord
    extra = 0

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

class BookCategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name','book_quantity','book_count']


class BookAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'cover_image', 'total_quantity', 'offered_by', 'pub_date']
    list_display = ('name','cover_image','available_quantity', 'borrow_times', 'was_borrowed_recently')
    inlines = [BorrowRecordsInline]

    search_fields = ['book_inf']


class BorrowRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Borrow_Information', {'fields': ['student', 'book', 'borrow_date']})
    ]
    inlines = [ReturnRecordsInline]
    list_display = ('student', 'book', 'borrow_date','isreturn')
    search_fields = ['book__name','student__name']




class ReturnRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Return_Information',{'fields': ['borrowrecord__student__name', 'borrowrecord__book', 'borrowrecord__borrow_date']})
    ]
    search_fields = ['borrowrecord__book__name','borrowrecord__student__name']


class StudentAdmin(admin.ModelAdmin):
    fields = ['stu_id', 'name', 'sex', 'school', 'major', 'grade']
    list_display = ['stu_id', 'name','is_all_return','borrow_quantity']


class SchoolAdmin(admin.ModelAdmin):
    fields = ['name','location']
    list_display = ['name','offer_book_count','offer_total_quantity','borrow_quantity']

class MajorAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name','borrow_quantity']


admin.site.register(Book, BookAdmin)
admin.site.register(BorrowRecord, BorrowRecordAdmin)
admin.site.register(ReturnRecord)
admin.site.register(BookCategory,BookCategoryAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Major, MajorAdmin)
