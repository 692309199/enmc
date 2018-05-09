# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models


class Country(models.Model):
    # 地区ID，以"g"开头，后面跟3位数字。如：g001
    countryid = models.CharField(primary_key=True, max_length=4, verbose_name=u'地区ID')
    name = models.CharField(unique=True, max_length=50, verbose_name=u'国家地区')
    remark = models.TextField(null=True, blank=True, verbose_name=u'备注')

    class Meta:
        verbose_name = u'国家地区表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Room(models.Model):
    # 机房ID，以"地区ID"开头，再连接"r"开头，后面跟3位数字。如：g001r001
    roomid = models.CharField(primary_key=True, max_length=8, verbose_name=u'机房ID')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=u'地区ID')
    name = models.CharField(unique=True, max_length=100, null=False, blank=False, verbose_name=u'机房名称')
    roomaddress = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'机房地址')
    isp = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'托管商')
    remark = models.TextField(null=True, blank=True, verbose_name=u'备注')

    class Meta:
        verbose_name = u'机房信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    # 机柜ID，以"地区ID机房ID"开头，再连接"j"开头，后面跟3位数字。如：g001r001j001
    cabinetid = models.CharField(primary_key=True, max_length=12, verbose_name=u'机柜ID')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=u'地区ID')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=u'机房ID')
    name = models.CharField(unique=True, max_length=10, verbose_name=u'机柜名称')
    network = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'网络线路')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=u'合约开始时间')
    stop_time = models.DateTimeField(null=True, blank=True, verbose_name=u'合约结束时间')
    remark = models.TextField(null=True, blank=True, verbose_name=u'备注')

    class Meta:
        verbose_name = u'机柜信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    equipment_typeid = models.CharField(primary_key=True, max_length=3, verbose_name=u'类型ID')
    name = models.CharField(unique=True, max_length=20, verbose_name=u'类型名称')

    class Meta:
        verbose_name = u'设备类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=8, choices=(('zaiyong', u'在用'), ('kongxian', u'空闲'), ('weixiu', u'维修')),
                              default='kongxian', verbose_name=u'设备状态')

    class Meta:
        verbose_name = u'状态表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.status


class Equipment(models.Model):
    # 主键
    # 设备ID，以"地区ID机房ID机柜ID"开头，再连接"e"开头，后面跟5位数字。如：g001r001j001e00001
    equipmentid = models.CharField(primary_key=True, max_length=18, verbose_name=u'设备ID')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=u'地区ID')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=u'机房ID')
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, verbose_name=u'机柜ID')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=u'设备状态')
    relatedid = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'交换机设备关联ID')
    relatedport = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'关联交换机端口')
    # 设备类型，对应设备类型表
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name=u'设备类型')
    mother = models.GenericIPAddressField(max_length=18, null=True, blank=True, verbose_name=u'宿主ID')
    sn = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'设备SN码')
    hostname = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'主机名')
    system = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'操作系统')
    cpu = models.CharField(max_length=6, null=True, blank=True, verbose_name=u'CPU核数')
    memory = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'内存大小')
    disk = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'磁盘大小')
    ssh_port = models.CharField(null=True, blank=True, max_length=5, verbose_name=u'SSH端口')
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'Ip地址')
    ip1 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址1')
    ip2 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址2')
    ip3 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址3')
    ip4 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址4')
    ip5 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址5')
    ip6 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址6')
    ip7 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址7')
    ip8 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址8')
    ip9 = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'Ip地址9')
    addtime = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    updatetime = models.DateTimeField(default=datetime.now, verbose_name=u'更新时间')
    remark = models.TextField(null=True, blank=True, verbose_name=u'备注')

    class Meta:
        verbose_name = u'设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

class Service(models.Model):
    # 服务ID，以"s"开头，后面跟3位数字。如：s001
    serviceid = models.CharField(primary_key=True, max_length=4, verbose_name=u'服务ID')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name=u'设备ID')
    name = models.CharField(max_length=20, verbose_name=u'服务名称')
    install = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'安装路径')
    config = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'配置文件')
    start = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'启动文件')
    version = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'软件版本')
    port = models.CharField(max_length=5, null=True, blank=True, verbose_name=u'端口号')
    protocol = models.CharField(max_length=3, null=True, blank=True, choices=(('tcp', u'TCP'), ('udp', u'UDP')),
                            default='tcp', verbose_name=u'协议类型')
    user = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'用户名')
    password = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'密码')
    remark = models.TextField(null=True, blank=True,verbose_name=u'备注')

    class Meta:
        verbose_name = u'服务信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name