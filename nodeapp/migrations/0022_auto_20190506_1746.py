# Generated by Django 2.1.7 on 2019-05-06 09:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nodeapp', '0021_auto_20190428_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raw_Node',
            fields=[
                ('RawNode_ID', models.IntegerField(help_text='节点逻辑序号,从1开始计数', primary_key=True, serialize=False)),
                ('MAC_Address', models.CharField(default='', help_text='原始节点的物理地址', max_length=18)),
                ('Geo_Address', models.ForeignKey(blank=True, help_text='原生节点地理位置', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.Geography_Attribute')),
            ],
        ),
        migrations.RemoveField(
            model_name='node_attribute',
            name='Node_MAC',
        ),
        migrations.AddField(
            model_name='time_node',
            name='IP_Address',
            field=models.ForeignKey(blank=True, help_text='IP地址', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.Net_Attribute'),
        ),
        migrations.AddField(
            model_name='time_node',
            name='Note_PH',
            field=models.ForeignKey(blank=True, help_text='PH value', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.MSG_PH_Attribute'),
        ),
        migrations.AddField(
            model_name='time_node',
            name='Note_PS',
            field=models.ForeignKey(blank=True, help_text='Pressure,(KPa)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.MSG_Press_Attrubute'),
        ),
        migrations.AddField(
            model_name='time_node',
            name='Note_TP',
            field=models.ForeignKey(blank=True, help_text='temperature,(centidegree) ', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.MSG_Temperature_Attribute'),
        ),
        migrations.AddField(
            model_name='time_node',
            name='Note_Time',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 6, 9, 46, 36, 701514, tzinfo=utc), help_text='记录时间'),
        ),
        migrations.DeleteModel(
            name='MAC_Attribute',
        ),
        migrations.AddField(
            model_name='time_node',
            name='Note_Node',
            field=models.ForeignKey(blank=True, help_text='原始节点', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodeapp.Raw_Node'),
        ),
        migrations.RemoveField(
            model_name='time_node',
            name='Collect_Node',
        ),
        migrations.RemoveField(
            model_name='time_node',
            name='Collect_Time',
        ),
        migrations.RemoveField(
            model_name='time_node',
            name='status',
        ),
        migrations.AlterUniqueTogether(
            name='time_node',
            unique_together={('Note_Time', 'Note_Node')},
        ),
    ]
