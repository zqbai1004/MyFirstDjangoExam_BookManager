from django.test import TestCase

# Create your tests here.
import random
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import *
import factory

class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker('company')
    location = factory.Faker('address')

class MajorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Major

    name = factory.Faker('job')

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    stu_id = factory.Faker('random_int', min=10000000, max=99999999)
    name = factory.Faker('name')
    school = factory.SubFactory(SchoolFactory)
    sex = factory.Iterator(['M', 'F', 'O'])
    major = factory.SubFactory(MajorFactory)
    grade = factory.Faker('random_int', min=1980, max=timezone.now().year)

class BookCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookCategory

    name = factory.Faker('word')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    name = factory.Faker('sentence', nb_words=4)
    pub_date = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
    total_quantity = factory.Faker('random_int', min=1, max=10)
    offered_by = factory.SubFactory(SchoolFactory)
    cover_image = None
    category = factory.SubFactory(BookCategoryFactory)

class BorrowRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BorrowRecord

    student = factory.SubFactory(StudentFactory)
    book = factory.SubFactory(BookFactory)
    borrow_date = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())

class ReturnRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReturnRecord

    return_date = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
    borrowrecord = factory.SubFactory(BorrowRecordFactory)

# Now we start writing tests

class SchoolModelTest(TestCase):
    def setUp(self):
        self.school = SchoolFactory.create()

    def test_string_representation(self):
        self.assertEqual(str(self.school), self.school.name)

class MajorModelTest(TestCase):
    def setUp(self):
        self.major = MajorFactory.create()

    def test_string_representation(self):
        self.assertEqual(str(self.major), self.major.name)

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = StudentFactory.create()

    def test_string_representation(self):
        self.assertEqual(str(self.student), f"{self.student.stu_id}-{self.student.name}")

# Continue with other models and their methods...

class BorrowAndReturnTest(TestCase):
    def setUp(self):
        # Create 5 students, 10 books and 15 borrow records
        self.students = [StudentFactory.create() for _ in range(5)]
        self.books = [BookFactory.create() for _ in range(20)]
        self.borrow_records = []
        for i in range(15):
            available_books = [book for book in self.books if book.available_quantity > 0]
            if available_books:
                book = random.choice(available_books)
                student = random.choice(self.students)
                borrow_record = BorrowRecordFactory.create(student=student, book=book)
                self.borrow_records.append(borrow_record)

    def test_borrow_and_return(self):
        # Randomly create return records for some borrow records
        return_records = []
        for i in range(10):
            borrow_record = random.choice(self.borrow_records)
            return_record = ReturnRecordFactory.create(borrowrecord=borrow_record)
            return_records.append(return_record)
            self.borrow_records.remove(borrow_record)


        # Test if available_quantity, Borrow_times and is_all_return are correct
        for book in self.books:
            self.assertEqual(book.available_quantity, book.total_quantity - BorrowRecord.objects.filter(book=book, isreturned=False).count())
            self.assertEqual(book.borrow_times_db, BorrowRecord.objects.filter(book=book).count())
        for student in self.students:
            self.assertEqual(student.is_all_return_db, not BorrowRecord.objects.filter(student=student, isreturned=False).exists())
            self.assertEqual(student.borrow_times_db, BorrowRecord.objects.filter(student=student).count())
            self.assertEqual(student.return_times,ReturnRecord.objects.filter(borrowrecord__student=student).count())

    def test_cannot_borrow_when_no_stock(self):
        # Create a book with no stock
        book_no_stock = BookFactory.create(total_quantity=0)
        # Try to create a borrow record for this book
        with self.assertRaises(ValueError):
            BorrowRecordFactory.create(student=random.choice(self.students), book=book_no_stock)

    def test_timeout_records(self):
        timeout_borrow_record_list = []
        student = StudentFactory.create()
        for i in range(random.randint(1,20)):
            timeout_borrow_record = BorrowRecordFactory.create(borrow_date = TIMEOUTLIMIT - datetime.timedelta(minutes=1),student=student)
            timeout_borrow_record_list.append(timeout_borrow_record)
        self.assertEqual(list(student.notreturn_records), timeout_borrow_record_list)

