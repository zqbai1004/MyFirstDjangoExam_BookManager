# Generated by Django 4.1 on 2023-07-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_student_is_all_return_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='borrow_times',
            field=models.IntegerField(default=0),
        ),
    ]
