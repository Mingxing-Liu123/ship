# Generated by Django 2.0.7 on 2020-09-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0039_auto_20200901_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship_msg',
            name='heading',
            field=models.FloatField(blank=True, help_text='偏航角2', null=True),
        ),
    ]
