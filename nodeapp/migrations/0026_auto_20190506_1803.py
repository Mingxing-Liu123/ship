# Generated by Django 2.1.7 on 2019-05-06 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0025_auto_20190506_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_node',
            name='Note_Time',
            field=models.DateTimeField(auto_now_add=True, help_text='记录时间'),
        ),
    ]
