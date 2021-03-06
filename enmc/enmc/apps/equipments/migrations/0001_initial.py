# Generated by Django 2.0.5 on 2018-05-09 12:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('cabinetid', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='机柜ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='机柜名称')),
                ('network', models.CharField(blank=True, max_length=20, null=True, verbose_name='网络线路')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='合约开始时间')),
                ('stop_time', models.DateTimeField(blank=True, null=True, verbose_name='合约结束时间')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '机柜信息表',
                'verbose_name_plural': '机柜信息表',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('countryid', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='地区ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='国家地区')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '国家地区表',
                'verbose_name_plural': '国家地区表',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('equipmentid', models.CharField(max_length=18, primary_key=True, serialize=False, verbose_name='设备ID')),
                ('relatedid', models.CharField(blank=True, max_length=100, null=True, verbose_name='交换机设备关联ID')),
                ('relatedport', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联交换机端口')),
                ('mother', models.GenericIPAddressField(blank=True, null=True, verbose_name='宿主ID')),
                ('sn', models.CharField(blank=True, max_length=20, null=True, verbose_name='设备SN码')),
                ('hostname', models.CharField(blank=True, max_length=20, null=True, verbose_name='主机名')),
                ('system', models.CharField(blank=True, max_length=30, null=True, verbose_name='操作系统')),
                ('cpu', models.CharField(blank=True, max_length=6, null=True, verbose_name='CPU核数')),
                ('memory', models.CharField(blank=True, max_length=10, null=True, verbose_name='内存大小')),
                ('disk', models.CharField(blank=True, max_length=10, null=True, verbose_name='磁盘大小')),
                ('ssh_port', models.CharField(blank=True, max_length=5, null=True, verbose_name='SSH端口')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='Ip地址')),
                ('ip1', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址1')),
                ('ip2', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址2')),
                ('ip3', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址3')),
                ('ip4', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址4')),
                ('ip5', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址5')),
                ('ip6', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址6')),
                ('ip7', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址7')),
                ('ip8', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址8')),
                ('ip9', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip地址9')),
                ('addtime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('updatetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Cabinet', verbose_name='机柜ID')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Country', verbose_name='地区ID')),
            ],
            options={
                'verbose_name': '设备信息表',
                'verbose_name_plural': '设备信息表',
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('equipment_typeid', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='类型ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='类型名称')),
            ],
            options={
                'verbose_name': '设备类型表',
                'verbose_name_plural': '设备类型表',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomid', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='机房ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='机房名称')),
                ('roomaddress', models.CharField(blank=True, max_length=100, null=True, verbose_name='机房地址')),
                ('isp', models.CharField(blank=True, max_length=100, null=True, verbose_name='托管商')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Country', verbose_name='地区ID')),
            ],
            options={
                'verbose_name': '机房信息表',
                'verbose_name_plural': '机房信息表',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('serviceid', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='服务ID')),
                ('name', models.CharField(max_length=20, verbose_name='服务名称')),
                ('install', models.CharField(blank=True, max_length=100, null=True, verbose_name='安装路径')),
                ('config', models.CharField(blank=True, max_length=200, null=True, verbose_name='配置文件')),
                ('start', models.CharField(blank=True, max_length=100, null=True, verbose_name='启动文件')),
                ('version', models.CharField(blank=True, max_length=50, null=True, verbose_name='软件版本')),
                ('port', models.CharField(blank=True, max_length=5, null=True, verbose_name='端口号')),
                ('protocol', models.CharField(blank=True, choices=[('tcp', 'TCP'), ('udp', 'UDP')], default='tcp', max_length=3, null=True, verbose_name='协议类型')),
                ('user', models.CharField(blank=True, max_length=20, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='密码')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Equipment', verbose_name='设备ID')),
            ],
            options={
                'verbose_name': '服务信息表',
                'verbose_name_plural': '服务信息表',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('zaiyong', '在用'), ('kongxian', '空闲'), ('weixiu', '维修')], default='kongxian', max_length=8, verbose_name='设备状态')),
            ],
            options={
                'verbose_name': '状态表',
                'verbose_name_plural': '状态表',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='equipment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.EquipmentType', verbose_name='设备类型'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Room', verbose_name='机房ID'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Status', verbose_name='设备状态'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Country', verbose_name='地区ID'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.Room', verbose_name='机房ID'),
        ),
    ]
