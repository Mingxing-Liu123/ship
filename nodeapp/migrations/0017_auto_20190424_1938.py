# Generated by Django 2.1.7 on 2019-04-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0016_auto_20190424_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node_attribute',
            name='Node_ID',
            field=models.IntegerField(default=0, help_text='Node ID'),
        ),
    ]
