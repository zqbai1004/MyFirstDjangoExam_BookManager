# Generated by Django 4.1 on 2023-07-10 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Major_inf',
            new_name='Major',
        ),
        migrations.RenameModel(
            old_name='School_inf',
            new_name='School',
        ),
        migrations.RenameModel(
            old_name='Student_inf',
            new_name='Student',
        ),
    ]
