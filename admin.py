from django.contrib import admin

# Register your models here.
from .models import Book,BorrowRecord

class RecordsInline(admin.TabularInline):
    model = BorrowRecord
    extra = 1

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields':['book_inf','pub_date','cover_image']}),
        ('Status',   {'fields':['borrow_times','available_quantity','total_quantity']})
    ]
    list_display = ('book_inf','available_quantity','was_borrowed_recently')
    inlines = [RecordsInline]

    list_filter = ['pub_date']
    search_fields = ['book_inf']

admin.site.register(Book,BookAdmin)
admin.site.register(BorrowRecord)