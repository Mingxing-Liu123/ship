# Generated by Django 2.1.7 on 2019-05-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0028_auto_20190511_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='Reviewer_MSG',
        ),
        migrations.AddField(
            model_name='topic',
            name='Reviewer_MSG',
            field=models.ManyToManyField(blank=True, help_text='留言', null=True, to='nodeapp.Message_Board'),
        ),
    ]
