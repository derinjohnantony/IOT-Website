# Generated by Django 4.2.1 on 2023-05-24 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0003_rename_thing_groupdivinfo_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupdivinfo',
            old_name='num',
            new_name='index',
        ),
        migrations.RemoveField(
            model_name='groupdivinfo',
            name='name',
        ),
    ]