# Generated by Django 3.0.6 on 2020-05-20 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20200520_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='file',
            new_name='file1',
        ),
    ]