# Generated by Django 2.0.7 on 2020-09-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0038_auto_20200901_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship_msg',
            name='alt',
            field=models.FloatField(blank=True, help_text='高度7', null=True),
        ),
        migrations.AddField(
            model_name='ship_msg',
            name='pitch',
            field=models.FloatField(blank=True, help_text='俯仰角3', null=True),
        ),
        migrations.AddField(
            model_name='ship_msg',
            name='roll',
            field=models.FloatField(blank=True, help_text='横滚角4', null=True),
        ),
        migrations.AddField(
            model_name='ship_msg',
            name='ve',
            field=models.FloatField(blank=True, help_text='东向速度11', null=True),
        ),
        migrations.AddField(
            model_name='ship_msg',
            name='vn',
            field=models.FloatField(blank=True, help_text='北向速度12', null=True),
        ),
        migrations.AddField(
            model_name='ship_msg',
            name='vu',
            field=models.FloatField(blank=True, help_text='天向速度13', null=True),
        ),
        migrations.AlterField(
            model_name='ship_msg',
            name='poi_lat',
            field=models.FloatField(blank=True, help_text='维度5', null=True),
        ),
        migrations.AlterField(
            model_name='ship_msg',
            name='poi_lng',
            field=models.FloatField(blank=True, help_text='经度6', null=True),
        ),
    ]
