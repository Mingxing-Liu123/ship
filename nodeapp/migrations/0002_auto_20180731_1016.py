# Generated by Django 2.0.7 on 2018-07-31 02:16

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic=False
    dependencies = [
        ('nodeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodeip',
            name='number',
            field=models.IntegerField(default=0, help_text='the number of node.'),
        ),
        migrations.RemoveField(
            model_name='nodeip',
            name='nodeaddress',
        ),
        migrations.AddField(
            model_name='nodeip',
            name='nodeaddress',
            field=models.ManyToManyField(help_text='Select a address for this nodeIp', to='nodeapp.NodeAddress'),
        ),
    ]
    