import re

from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import DevicespoolAdminForm
from .forms import InterfacesAdminForm
from .forms import SwitchportsAdminForm

from .models import Devicespool
from .models import Interfaces
from .models import Switchports
from .models import Association
from .models import Aion

admin.site.site_header = "自动化中台管理系统"
admin.site.site_title = "自动化中台资源库"
admin.site.index_title = "自动化中台资源库"

class InterfacesAddInline(admin.TabularInline):
    model = Interfaces
    form = InterfacesAdminForm
    extra = 2
    can_delete = False
    fields = ("deviceid", "device_port","port_rate")
    verbose_name = "设备端口信息"
    verbose_name_plural = "添加设备端口信息（设备型号非交换机时填写）"

    """ Override this method. Return blank queryset and only use it to add data, not display data """

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.none()

class SwitchportsAddInline(admin.TabularInline):
    model = Switchports
    form = SwitchportsAdminForm
    extra = 2
    can_delete = False
    fields = ("deviceid", "switch_port")

    verbose_name = "交换机端口信息"
    verbose_name_plural = "添加交换机端口信息（设备型号为交换机时填写）"

    """ Override this method. Return blank queryset and only use it to add data, not display data """

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.none()

@admin.register(Devicespool)

class LrmDeviceAdmin(ImportExportModelAdmin):
    model = Devicespool
    form = DevicespoolAdminForm
    list_display = (
        "id",
        "device_name",
        "owner",
        "status",
        "model",
        "domain",
        "mgt_address",
        "mgt_port",
        "user",
        "device_tag",
        "created_at",
        "updated_at",
    )
    list_filter = ("model","domain", "status", "updated_at")
    search_fields = (
        "device_name",
        "domain",
        "model",
        "mgt_address",
        "id",
        "user",
        "device_tag",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "owner__email",
    )
    list_display_links = ("id", "device_name")
    actions_on_bottom = True
    list_editable = [
        "status",
        "owner",
        "device_tag",
        "model",
        "domain",
        "mgt_address",
        "mgt_port",
        "user",
    ]
    date_hierarchy = "updated_at"
    ordering = ["-id"]
    list_per_page = 10
    autocomplete_fields = ["owner"]
    fieldsets = (
        (
            "必填信息",
            {
                "fields": [
                    ("device_name", "model", "connect", "mgt_port"),
                    "mgt_address",
                    "domain",
                    ("username", "password", "priv_cmd", "priv_passwd"),
                ]
            },
        ),
        (
            "选填信息",
            {
                "fields": [
                    ("slot", "status", "testbedid", "board_num", "ports_num_total"),
                    "user",
                    ("com_address", "com_port", "maintain"),
                    ("device_tag", "board_tag", "board_type"),
                ]
            },
        ),
    )
    inlines = [
        InterfacesAddInline,
        SwitchportsAddInline,
    ]

    def get_queryset(self, request):
        qs = super(LrmDeviceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        name_userid = "%s" % request.user
        userid = name_userid.split("_")[1]
        return qs.filter(Q(owner__username=userid) | Q(owner__username="regress"))

    def save_model(self, request, obj, form, change):
        switch_list = ["vswitch", "calient", "polatis", "ctn9k", "zx9k"]
        test_tools_list = [
        "testcenter",
        "vtcqemu",
        "ixnetwork",
        "vtester",
        "tdm",
        "mts5800",
        "syncone",
        "linux",
    ]
        if obj.model in switch_list:
            if not Devicespool.objects.filter(Q(mgt_address__exact=obj.mgt_address)):
                if change:
                    if request.user.is_superuser:
                        obj.save()
                    else:
                        owner_id = obj.id
                        if Devicespool.objects.get(id=owner_id).owner == request.user:
                            self.message_user(
                                request,
                                "%s成功修改%s的数据"
                                % (request.user, Devicespool.objects.get(id=owner_id).owner),
                            )
                            messages.set_level(request, messages.ERROR)
                            obj.save()
                        else:
                            messages.error(
                                request,
                                "%s无法修改%s的数据"
                                % (request.user, Devicespool.objects.get(id=owner_id).owner),
                            )
                            messages.set_level(request, messages.ERROR)
                else:
                    obj.owner = request.user
                    obj.save() 
            else:   
                if Devicespool.objects.filter(Q(mgt_address__exact=obj.mgt_address))[0].device_name!=obj.device_name:
                    messages.error(
                                    request,
                                    "交换机%s的管理IP地址%s与已有设备冲突"
                                    % (obj.device_name, obj.mgt_address),
                                )
                    messages.set_level(request, messages.ERROR)
                else:
                    if change:
                        if request.user.is_superuser:
                            obj.save()
                        else:
                            owner_id = obj.id
                            if Devicespool.objects.get(id=owner_id).owner == request.user:
                                self.message_user(
                                    request,
                                    "%s成功修改%s的数据"
                                    % (request.user, Devicespool.objects.get(id=owner_id).owner),
                                )
                                messages.set_level(request, messages.ERROR)
                                obj.save()
                            else:
                                messages.error(
                                    request,
                                    "%s无法修改%s的数据"
                                    % (request.user, Devicespool.objects.get(id=owner_id).owner),
                                )
                                messages.set_level(request, messages.ERROR)
                    else:
                        obj.owner = request.user
                        obj.save()
                
        elif obj.model in test_tools_list:
            if not Devicespool.objects.filter(Q(mgt_address__exact=obj.mgt_address)):
                if change:
                    if request.user.is_superuser:
                        obj.save()
                    else:
                        owner_id = obj.id
                        if Devicespool.objects.get(id=owner_id).owner == request.user:
                            self.message_user(
                                request,
                                "%s成功修改%s的数据"
                                % (request.user, Devicespool.objects.get(id=owner_id).owner),
                            )
                            messages.set_level(request, messages.ERROR)
                            obj.save()
                        else:
                            messages.error(
                                request,
                                "%s无法修改%s的数据"
                                % (request.user, Devicespool.objects.get(id=owner_id).owner),
                            )
                            messages.set_level(request, messages.ERROR)
                else:
                    obj.owner = request.user
                    obj.save()
            else:
                if Devicespool.objects.filter(Q(mgt_address__exact=obj.mgt_address))[0].device_name!=obj.device_name:
                    messages.error(
                                    request,
                                    "测试仪%s的管理IP地址%s与已有设备冲突"
                                    % (obj.device_name, obj.mgt_address),
                                )
                    messages.set_level(request, messages.ERROR)
                else:
                    if change:
                        if request.user.is_superuser:
                            obj.save()
                        else:
                            owner_id = obj.id
                            if Devicespool.objects.get(id=owner_id).owner == request.user:
                                self.message_user(
                                    request,
                                    "%s成功修改%s的数据"
                                    % (request.user, Devicespool.objects.get(id=owner_id).owner),
                                )
                                messages.set_level(request, messages.ERROR)
                                obj.save()
                            else:
                                messages.error(
                                    request,
                                    "%s无法修改%s的数据"
                                    % (request.user, Devicespool.objects.get(id=owner_id).owner),
                                )
                                messages.set_level(request, messages.ERROR)
                    else:
                        obj.owner = request.user
                        obj.save()
        else:
            if change:
                if request.user.is_superuser:
                    obj.save()
                else:
                    owner_id = obj.id
                    if Devicespool.objects.get(id=owner_id).owner == request.user:
                        self.message_user(
                            request,
                            "%s成功修改%s的数据"
                            % (request.user, Devicespool.objects.get(id=owner_id).owner),
                        )
                        messages.set_level(request, messages.ERROR)
                        obj.save()
                    else:
                        messages.error(
                            request,
                            "%s无法修改%s的数据"
                            % (request.user, Devicespool.objects.get(id=owner_id).owner),
                        )
                        messages.set_level(request, messages.ERROR)
            else:
                obj.owner = request.user
                obj.save()

    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.owner = request.user
            instance.model = request.POST.get("model")
            instance.domain = request.POST.get("domain")
            instance.save()
            formset.save()

    def delete_selected(self, request, obj):
        if request.user.is_superuser:
            i = 0
            for object_item in obj.all():
                i = i + 1
                obj.delete()
            self.message_user(request, "超级管理员成功删除%s条数据" % i)
            messages.set_level(request, messages.ERROR)
        else:
            i = 0
            i_all = 0
            for object_item in obj.all():
                i_all = i_all + 1
                if object_item.owner == request.user:
                    i = i + 1
                    object_item.delete()
            if i == 0:
                messages.error(request, "%s无法删除其他用户的数据" % request.user)
                messages.set_level(request, messages.ERROR)
            elif i < i_all:
                self.message_user(
                    request,
                    "成功删除%s条%s的数据,无法删除%s条其他用户的数据" % (i, request.user, i_all - i),
                )
                messages.set_level(request, messages.ERROR)
            else:
                self.message_user(request, "成功删除%s条%s的数据" % (i, request.user))
                messages.set_level(request, messages.ERROR)

    def update_status(self, request, queryset):
        for devicespool in queryset:
            if devicespool.status == "IDLE":
                devicespool.status = "INUSE"
            else:
                devicespool.status = "IDLE"
            devicespool.save()

        row_updated = len(queryset)
        if row_updated == 1:
            message_bit = "1台设备的状态"
        else:
            message_bit = "%s台设备的状态" % row_updated
        self.message_user(request, "总共 %s 被变更成功" % message_bit)

    update_status.short_description = "变更选中设备状态"
    actions = [delete_selected, update_status]

    update_status.style = "background-color:pink;color:green"
    update_status.icon = "fas fa-audio-description"
    update_status.type = "danger"

@admin.register(Switchports)
class LrmSwitchportAdmin(ImportExportModelAdmin):
    model = Switchports
    form = SwitchportsAdminForm
    list_display = (
        "id",
        "deviceid",
        "owner",
        "switch_port",
        "status",
        "vmname",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("deviceid__device_name", "deviceid__id", "switch_port","owner__username","owner__email","owner__first_name","owner__last_name")
    date_hierarchy = "updated_at"
    ordering = ["-id"]
    autocomplete_fields = ["deviceid","owner"]
    list_editable = ["status", "owner", "vmname", "switch_port"]
    list_per_page = 10
    fieldsets = (
        ("必填信息", {"fields": ["deviceid", "switch_port", "status"]}),
        ("选填信息", {"fields": [("vmname")]}),
    )

    def get_queryset(self, request):
        qs = super(LrmSwitchportAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        name_userid = "%s" % request.user
        userid = name_userid.split("_")[1]
        return qs.filter(Q(owner__username=userid) | Q(owner__username="regress"))

    def save_model(self, request, obj, form, change):
        if not Switchports.objects.filter(Q(deviceid__id__exact=obj.deviceid.id) & Q(switch_port__exact=obj.switch_port)):
            if change:
                obj.save()
            else:
                obj.owner = request.user
                obj.save()
        else:
            if Switchports.objects.filter(Q(deviceid__id__exact=obj.deviceid.id) & Q(switch_port__exact=obj.switch_port))[0].id!=obj.id:
                messages.error(
                                request,
                                "交换机%s的端口%s已存在"
                                % (obj.deviceid.device_name, obj.switch_port),
                            )
                messages.set_level(request, messages.ERROR)
            else:
                if change:
                    obj.save()
                else:
                    obj.owner = request.user
                    obj.save()

    def update_status(self, request, queryset):
        for devicespool in queryset:
            if devicespool.status == "IDLE":
                devicespool.status = "INUSE"
            else:
                devicespool.status = "IDLE"
            devicespool.save()

        row_updated = len(queryset)
        if row_updated == 1:
            message_bit = "1台设备的状态"
        else:
            message_bit = "%s台设备的状态" % row_updated
        self.message_user(request, "总共 %s 被变更成功" % message_bit)

    update_status.short_description = "变更选中设备状态"
    actions = [update_status]

    update_status.style = "background-color:pink;color:green"
    update_status.icon = "fas fa-audio-description"
    update_status.type = "danger"

@admin.register(Interfaces)
class LrmInterfaceAdmin(ImportExportModelAdmin):
    model = Interfaces
    form = InterfacesAdminForm
    list_display = (
        "id",
        "deviceid",
        "owner",
        "status",
        "model",
        "domain",
        "port_rate",
        "device_port",
        "user",
        "peerid",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "domain","updated_at", "port_rate")
    search_fields = ("deviceid__device_name", "deviceid__id", "device_port","user","owner__username","model","domain","owner__email","owner__first_name","owner__last_name")
    date_hierarchy = "updated_at"
    autocomplete_fields = ["deviceid", "peerid","owner"]
    ordering = ["-id"]
    list_editable = [
        "status",
        "owner",
        "model",
        "domain",
        "port_rate",
        "device_port",
        "user",
        "peerid",
    ]
    list_per_page = 10
    fieldsets = (
        (
            "必填信息",
            {"fields": ["deviceid", "device_port", ("port_rate", "model", "status")]},
        ),
        (
            "选填信息",
            {
                "fields": [
                    "domain",
                    "peerid",
                    ("mediatype", "group"),
                    ("link", "slot"),
                    ("board_type", "testbedid"),
                ]
            },
        ),
    )

    def get_queryset(self, request):
        qs = super(LrmInterfaceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        name_userid = "%s" % request.user
        userid = name_userid.split("_")[1]
        return qs.filter(Q(owner__username=userid) | Q(owner__username="regress"))

    def save_model(self, request, obj, form, change):
        if not Interfaces.objects.filter(Q(deviceid__id__exact=obj.deviceid.id) & Q(device_port__exact=obj.device_port)):
            if change:
                obj.save()
            else:
                obj.owner = request.user
                obj.save()
        else:
            if Interfaces.objects.filter(Q(deviceid__id__exact=obj.deviceid.id) & Q(device_port__exact=obj.device_port))[0].id!=obj.id:
                messages.error(
                                request,
                                "设备%s的端口%s已存在"
                                % (obj.deviceid.device_name, obj.device_port),
                            )
                messages.set_level(request, messages.ERROR)
            else:
                if change:
                    obj.save()
                else:
                    obj.owner = request.user
                    obj.save()

    def update_status(self, request, queryset):
        for devicespool in queryset:
            if devicespool.status == "IDLE":
                devicespool.status = "INUSE"
            else:
                devicespool.status = "IDLE"
            devicespool.save()

        row_updated = len(queryset)
        if row_updated == 1:
            message_bit = "1台设备的状态"
        else:
            message_bit = "%s台设备的状态" % row_updated
        self.message_user(request, "总共 %s 被变更成功" % message_bit)

    update_status.short_description = "变更选中设备状态"
    actions = [update_status]

    update_status.style = "background-color:pink;color:green"
    update_status.icon = "fas fa-audio-description"
    update_status.type = "danger"

@admin.register(Association)
class LrmAssociationAdmin(ImportExportModelAdmin):
    model = Association
    list_display = (
        "id",
        "interface",
        "switchport",
        "owner",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = ["-id"]
    list_editable = ["owner"]
    search_fields = (
        "id",
        "interface__deviceid__device_name",
        "interface__deviceid__id",
        "interface__device_port",
        "interface__port_rate",
        "switchport__deviceid__device_name",
        "switchport__switch_port",
        "switchport__deviceid__id",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "owner__email",
    )
    autocomplete_fields = ["interface", "switchport","owner"]
    list_per_page = 10
    fieldsets = (("必填信息", {"fields": [("interface", "switchport")]}),)

    def get_queryset(self, request):
        qs = super(LrmAssociationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        name_userid = "%s" % request.user
        userid = name_userid.split("_")[1]
        return qs.filter(Q(owner__username=userid) | Q(owner__username="regress"))

    def save_model(self, request, obj, form, change):
        if change:
            obj.save()
        else:
            obj.owner = request.user
            obj.save()


@admin.register(Aion)
class LrmAionAdmin(ImportExportModelAdmin):
    model = Aion
    list_display = (
        "id",
        "deviceid",
        "portal",
        "username",
        "owner",
        "password",
        "workspace",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = ["-id"]
    list_display_links = ("id", "deviceid")
    list_editable = ["owner","portal","username","password","workspace"]
    search_fields = (
        "deviceid__id",
        "deviceid__device_name",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "owner__email",
    )
    autocomplete_fields = ["deviceid","owner"]
    list_per_page = 10
    fieldsets = (("必填信息", {"fields": [("deviceid","portal", "username")]}), ("选填信息", {"fields": [("password","workspace")]}),)

    def get_queryset(self, request):
        qs = super(LrmAionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        name_userid = "%s" % request.user
        userid = name_userid.split("_")[1]
        return qs.filter(Q(owner__username=userid) | Q(owner__username="regress"))

    def save_model(self, request, obj, form, change):
        if change:
            obj.save()
        else:
            obj.owner = request.user
            obj.save()

@admin.register(admin.models.LogEntry)
class LogEntryAdmin(ImportExportModelAdmin):
#class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["action_time", "user", "content_type", "__str__"]
    list_display_links = ["action_time"]
    list_filter = ["action_time", "content_type", "user"]
    list_per_page = 15
    readonly_fields = [
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    ]
