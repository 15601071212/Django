from django.db import models
from django.contrib.auth.models import User
from django.forms import widgets

MODEL_CHOICES = (
            ('ssp', 'zxrufp::ssp'),
            ('ufp', 'zxrufp::ufp'),
            ('ufp-070', 'zxrufp::ufp-070'),
            ('ufp-59x', 'zxrufp::ufp-59x'),
            ('ufp-61', 'zxrufp::ufp-61'),
            ('ufp-99x', 'zxrufp::ufp-99x'),
            ('ufp-c89e', 'zxrufp::ufp-c89e'),
            ('ufp-99x-ssp4', 'zxrufp::ufp-99x-ssp4'),
            ('9900', 'zxr99::9900'),
            ('9904', 'zxr99::9904'),
            ('9908', 'zxr99::9908'),
            ('9900x', 'zxr99::9900x'),
            ('9904x', 'zxr99::9904x'),
            ('9908x', 'zxr99::9908x'),
            ('9900x-v1', 'zxr99::9900x-v1'),
            ('9900x-v2', 'zxr99::9900x-v2'),
            ('9900x-box', 'zxr99::9900x-box'),
            ('9900x-boxvsc', 'zxr99::9900x-boxvsc'),
            ('9900x-v1vsc', 'zxr99::9900x-v1vsc'),
            ('9900x-v2vsc', 'zxr99::9900x-v2vsc'),
            ('5960x', 'zxr59x::5960x'),
            ('5960-56qu-hf', 'zxr59x::5960-56qu-hf'),
            ('5960x-56qu-hf', 'zxr59x::5960x-56qu-hf'),
            ('5960-54du-hc', 'zxr59x::5960-54du-hc'),
            ('5960x-54du-hf', 'zxr59x::5960x-54du-hf'),
            ('5960x-54dl-hf', 'zxr59x::5960x-54dl-hf'),
            ('5960m', 'zxr59m::5960m'),
            ('5960m-4m-hi', 'zxr59m::5960m-4m-hi'),
            ('5960m-8m-hi', 'zxr59m::5960m-8m-hi'),
            ('6120h', 'zxr61::6120h'),
            ('6120hs', 'zxr61::6120hs'),
            ('6170h', 'zxr61::6170h'),
            ('6180h', 'zxr61::6180h'),
            ('6190h', 'zxr61::6190h'),
            ('6120', 'zxr61::6120'),
            ('6170', 'zxr61::6170'),
            ('6180', 'zxr61:6180'),
            ('6190', 'zxr61::6190'),
            ('9000', 'zxr61::9000'),
            ('m6000', 'zxr61::m6000'),
            ('6700-32', 'zxr67::6700-32'),
            ('6700-12', 'zxr67::6700-12'),
            ('6700-24', 'zxr67::6700-24'),
            ('zx15k', 'zxr15k::zx15k'),
            ('t8k', 'zxr15k::t8k'),
            ('c89e', 'zxrc89e::c89e'),
            ('c89e-3', 'zxrc89e::c89e-3'),
            ('c89e-4', 'zxrc89e::c89e-4'),
            ('c89e-8', 'zxrc89e::c89e-8'),
            ('c89e-12', 'zxrc89e::c89e-12'),
            ('testcenter', 'test_tools:testcenter'),
            ('vtcqemu', 'test_tools::vtcqemu'),
            ('ixnetwork', 'test_tools::ixnetwork'),
            ('vtester', 'test_tools::vtester'),
            ('tdm', 'test_tools::tdm'),
            ('mts5800', 'test_tools::mts5800'),
            ('syncone', 'test_tools::syncone'),
            ('xinertel', 'test_tools::xinertel'),
            ('linux', 'test_tools:linux'),
            ('vswitch', 'switch:vswitch'),
            ('calient', 'switch:calient'),
            ('polatis', 'switch:polatis'),
            ('ctn9k', 'switch:ctn9k'),
            ('zx9k', 'switch:zx9k'),
    )
STATUS_CHOICES = (
        ('IDLE', 'IDLE'),
        ('INUSE', 'INUSE'),
        ('NotAccess', 'NotAccess'),
    )
PORT_RATE_CHOICES = (
        ('1G', '1G'),
        ('10G', '10G'),
        ('25G', '25G'),
        ('40G', '40G'),
        ('50G', '50G'),
        ('100G', '100G'),
        ('400G', '400G'),
    )       
MGT_PORT_CHOICES = (
        ('22', 'SSH:22'),
        ('23', 'Telnet:23'),
        ('3082', 'Telnet:3082'),
        ('3083', 'Telnet:3083'),
    )   
CONNECT_CHOICES = (
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
    )       

class Devicespool(models.Model):
    testbedid = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备型号",choices=MODEL_CHOICES,help_text='参数文件中"model"的值')
    device_name = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备名称",help_text='参数文件中"device_name"的值')
    domain = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备域名",help_text='参数文件中"domain"的值')
    status = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备状态",choices=STATUS_CHOICES,default='IDLE')
    user = models.CharField(max_length=50, blank=True, null=True,verbose_name="执行机用户名")
    connect = models.CharField(max_length=50, blank=False, null=True,verbose_name="连接方式",choices=CONNECT_CHOICES,default='ssh',help_text='参数文件中"fv-connect"的值')
    mgt_address = models.GenericIPAddressField(blank=False, null=True,verbose_name="连接地址",help_text='参数文件中"fv-mgt_addr"的值')
    mgt_port = models.CharField(max_length=50, blank=False, null=True,verbose_name="连接端口",choices=MGT_PORT_CHOICES,default='22',help_text='参数文件中"fv-mgt_port"的值')
    com_address = models.CharField(max_length=50, blank=True, null=True)
    com_port = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=False, null=True,verbose_name="登录用户名",help_text='参数文件中"fv-username"的值')
    password = models.CharField(max_length=50, blank=False, null=True,verbose_name="登录密码",help_text='参数文件中"fv-password"的值')
    ports_num_total = models.IntegerField(blank=True, null=True)
    device_tag = models.CharField(max_length=250, blank=True, null=True)
    board_tag = models.CharField(max_length=250, blank=True, null=True)
    board_type = models.CharField(max_length=250, blank=True, null=True)
    slot = models.CharField(max_length=100, blank=True, null=True)
    board_num = models.IntegerField(blank=True, null=True)
    priv_cmd = models.CharField(max_length=50, blank=False, null=True,verbose_name="提权命令",default='enable',help_text='参数文件中"fv-privileged_command"的值')
    priv_passwd = models.CharField(max_length=50, blank=False, null=True,verbose_name="提权密码",default= 'zxr10',help_text='参数文件中"fv-privileged_password"的值')
    maintain = models.CharField(max_length=50, blank=True, null=True,default='9999')
    rfassets = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")

    class Meta:
        db_table = 'DevicesPool'
        unique_together = (('device_name', 'domain', 'mgt_address'),)
        verbose_name = "设备资源"  
        verbose_name_plural = "设备资源" 
        
    def __str__(self):
        return "%s::%s" % (self.id, self.device_name)

class Interfaces(models.Model):
    deviceid = models.ForeignKey(Devicespool, on_delete = models.CASCADE, db_column='deviceid', blank=False, null=True,verbose_name="设备名称",help_text='参数文件中“device_name”的值')
    model = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备型号",choices=MODEL_CHOICES,help_text='参数文件中“model”的值')
    domain = models.CharField(max_length=50, blank=True, null=True,verbose_name="设备域名",help_text='参数文件中“domain”的值')
    user = models.CharField(max_length=50, blank=True, null=True,verbose_name="执行机用户名")
    status = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备状态",choices=STATUS_CHOICES,default='IDLE',help_text='参数文件中“status”的值')
    port_rate = models.CharField(max_length=50, blank=False, null=True,verbose_name="端口速率",choices=PORT_RATE_CHOICES,default='10G',help_text='参数文件中"port_rate"的值')
    device_port = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备端口号",help_text='参数文件中"device_port"的值')
    mediatype = models.CharField(max_length=50, blank=True, null=True)
    peerid = models.ForeignKey('self', models.DO_NOTHING, db_column='peerid', blank=True, null=True,related_name='linkinfo',verbose_name="对端设备端口号",help_text='设备端口不经过交换机直接连接时必须填写“对端设备端口号”')
    link = models.CharField(max_length=200, blank=True, null=True)
    group = models.IntegerField(blank=True, null=True)
    slot = models.IntegerField(blank=True, null=True)
    board_type = models.CharField(max_length=250, blank=True, null=True)
    testbedid = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")

    class Meta:
        db_table = 'Interfaces'
        unique_together = (('deviceid', 'device_port'),)
        verbose_name = "设备端口资源"
        verbose_name_plural = "设备端口资源"
    def __str__(self):
        return "%s::%s::%s" % (self.deviceid,self.device_port,self.port_rate)

class Switchports(models.Model):
    deviceid = models.ForeignKey(Devicespool, db_column='deviceid', blank=False, null=True, related_name = 'device_name_switch', on_delete = models.CASCADE,verbose_name="设备名称",help_text='参数文件中“device_name”的值')
    status = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备状态",choices=STATUS_CHOICES,default='IDLE',help_text='参数文件中“status”的值')
    switch_port = models.CharField(max_length=50, blank=False, null=True,verbose_name="交换机端口号",help_text='参数文件中"switch_port"的值')
    vmname = models.CharField(max_length=50, blank=True, null=True,help_text='参数文件中“vmname”的值')
    #user = models.CharField(max_length=50, blank=True, null=True,verbose_name="设备用户")
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")

    class Meta:
        #managed = False
        db_table = 'SwitchPorts'
        unique_together = (('deviceid', 'switch_port'),)
        verbose_name = "交换机端口资源"
        verbose_name_plural = "交换机端口资源"
    def __str__(self):
        #return self.switch_port
        return "%s::%s" % (self.deviceid,self.switch_port)

class Association(models.Model):
    interface = models.ForeignKey('Interfaces',db_column='interface_id', unique=True, blank=False, null=True, related_name = 'interface', on_delete = models.CASCADE,verbose_name="设备端口 (interface)")
    switchport = models.ForeignKey('Switchports', db_column='switchport_id', unique=True, blank=False, null=True, related_name = 'switchport', on_delete = models.CASCADE,verbose_name="交换机端口 (switchport)")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")

    class Meta:
        db_table = 'Association'
        unique_together = (('interface', 'switchport'),)
        verbose_name = "端口连接信息"
        verbose_name_plural = "端口连接信息"
    def __str__(self):
        return "%s<-->%s" % (self.interface,self.switchport)

class Aion(models.Model):
    deviceid = models.ForeignKey('Devicespool', on_delete = models.CASCADE, unique=True, db_column='deviceid', blank=False, null=True,verbose_name="设备名称",help_text='参数文件中“device_name”的值')
    portal = models.CharField(max_length=50, blank=False, null=True,verbose_name="虚拟测试仪aion license server地址",help_text='参数文件中"fv-aion_server"的值',default='http://10.229.188.166')
    username = models.CharField(max_length=50, blank=False, null=True,verbose_name="虚拟测试仪aion username",help_text='参数文件中"fv-aion_username"的值')
    password = models.CharField(max_length=50, blank=True, null=True,verbose_name="虚拟测试仪aion password",help_text='参数文件中"fv-aion_password"的值',default='spt_admin')
    workspace = models.CharField(max_length=50, blank=True, null=True,verbose_name="虚拟测试仪aion workspace",help_text='参数文件中"fv-aion_workspace"的值',default='ZTE Corporation')
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")
    
    class Meta:
        db_table = 'Aion'
        unique_together = (('deviceid', 'portal'),)
        verbose_name = "思博伦虚拟测试仪认证服务器信息"
        verbose_name_plural = "思博伦虚拟测试仪认证服务器信息"
    def __str__(self):
        return "%s::%s" % (self.deviceid,self.portal)
