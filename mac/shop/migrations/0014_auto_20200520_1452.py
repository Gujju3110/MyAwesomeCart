# Generated by Django 3.0.6 on 2020-05-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20200520_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file1',
            field=models.FileField(upload_to='pdf/'),
        ),
    ]
