# Generated by Django 2.1.7 on 2019-05-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0027_message_board_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='Content',
            field=models.TextField(help_text='talk about', max_length=250),
        ),
    ]
