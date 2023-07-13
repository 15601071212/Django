import datetime
import operator
import string
import re
import json
import paramiko
import sys
import time
import socket
import pandas as pd
from __future__ import division
from functools import reduce
from django.db.models import Q
from django.shortcuts import render
from .models import Devicespool
from .models import Switchports
from .models import Interfaces
from .models import Association
from .forms import DevicespoolForm
from jinja2 import Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Bar, Gauge, Pie, Page, Funnel, Geo, Scatter3D
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./lrm/templates"))

def user_dict(request):
    user_dict={}
    for item in Devicespool.objects.all():
        if item.user:
            if item.owner:
                user_dict["%s" % item.user]=item.owner.id
    return HttpResponse("执行机用户责任人 = %s" % user_dict)
    

def email_list(request):
    email_list=[]
    for item in Devicespool.objects.all():
        if item.owner:
            if item.owner.email not in email_list:
                email_list.append(item.owner.email)
    return HttpResponse("Owner_Email_List = %s" % email_list)

def gau(request):  # 仪表图
    context = {}
    context["device_count"] = Devicespool.objects.exclude(owner__isnull=True).count()
    context["device_inuse_count"] = (
        Devicespool.objects.filter(status="INUSE").exclude(owner__isnull=True).count()
    )
    context["use_ratio"] = format(
        float(context["device_inuse_count"]) / float(context["device_count"]) * 100,
        ".1f",
    )
    c = (
        Gauge(init_opts=opts.InitOpts(width="300px", height="300px"))
        .add(series_name="设备占用率", data_pair=[["", context["use_ratio"]]])
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_bottom="0", is_show=True),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, formatter="{a} <br/>{b} : {c}%"
            ),
            title_opts=opts.TitleOpts(title="动态拓扑设备实时占用率(%)"),
        )
    )
    return HttpResponse(c.render_embed())

def pyecharts_demo(request):
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
    aut_list = switch_list + test_tools_list
    model_list = []

    switch_num = 0
    test_tools_num = 0
    for obj in Devicespool.objects.exclude(owner__isnull=True):
        if obj.model not in model_list:
            if obj.model not in aut_list:
                if obj.model!='SSP':
                    model_list.append(obj.model)
        if obj.model in switch_list:
            switch_num = switch_num + 1
        if obj.model in test_tools_list:
            test_tools_num = test_tools_num + 1
    device_num = (
        Devicespool.objects.exclude(owner__isnull=True).count()
        - switch_num
        - test_tools_num
    )
    model_num_list = []
    for item in model_list:
        model_num_list.append(
            Devicespool.objects.filter(model=item).exclude(owner__isnull=True).count()
        )
    model_dict = {"model_num": model_num_list}
    df = pd.DataFrame(data=model_dict, index=model_list)
    df_sort = df.sort_values(by="model_num", ascending=False)
    x_list = []
    y_list = []
    for i in range(len(df_sort.index)):
        x_list.append(df_sort.index[i])
        y_list.append(int(df_sort["model_num"][i]))
    y_list = y_list[0:8]
    x_list = x_list[0:8]
    y_list.append(switch_num)
    x_list.append('交换机')
    y_list.append(test_tools_num)
    x_list.append("测试仪")
    bar = (
        Bar(init_opts=opts.InitOpts(width="810px", height="300px"))
        .add_xaxis(x_list)
        .add_yaxis("设备数量", y_list)
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_bottom="0", is_show=True),
            title_opts=opts.TitleOpts(
                title="动态拓扑设备资源分布图（测试设备%s台，连接用交换机%s台，测试仪%s台）" % (device_num, switch_num, test_tools_num),
                subtitle="注：测试设备按设备型号分类排序，显示TOP8",
            ),
        )
    )
    return HttpResponse(bar.render_embed())
   
options_dict_cn = {
    "All": "所有的列",
    "device_name": "设备名称列",
    "status": "设备状态列",
    "model": "设备型号列",
    "user": "设备用户列",
}

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip

def device_search(request):
    query = request.GET.get("q", "")
    para_dict = request.GET.lists()
    para_list = list(para_dict)
    results_all = []
    results = []
    url_key_list = []
    url_key_and_list = []
    if query:
        url_key_list.append("q=" + query)
        if len(para_list) > 1:
            option_list = para_list[1][1]
            predicates = []
            options_list_cn = []
            for item in option_list:
                # if (item=='user'):
                #    predicates.append(('%s__user__icontains' % item, '%s' % query))
                # else:
                predicates.append(("%s__icontains" % item, "%s" % query))
                options_list_cn.append("%s" % options_dict_cn["%s" % item])
                url_key_list.append("check_box_list=" + item)
            q_list = [Q(x) for x in predicates]
            results = (
                Devicespool.objects.filter(reduce(operator.or_, q_list))
                .distinct()
                .order_by("device_name")
            )
            option = " ; ".join(options_list_cn)

        else:
            option_list = ["device_name", "status", "model", "user"]
            predicates = []
            for item in option_list:
                predicates.append(("%s__icontains" % item, "%s" % query))
                url_key_list.append("check_box_list=" + item)
            q_list = [Q(x) for x in predicates]
            results = (
                Devicespool.objects.filter(reduce(operator.or_, q_list))
                .distinct()
                .order_by("device_name")
            )
            option = "%s" % options_dict_cn["All"]

        page = request.GET.get("page")  # 获取分页数
        paginator = Paginator(results, 30)  # 设置一页显示多少条数据（news为要分页的数据）
        try:
            news = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            news = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            news = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    else:
        option = "All"
        results_all = Devicespool.objects.all().order_by("device_name")
        page = request.GET.get("page")  # 获取分页数
        paginator = Paginator(results_all, 30)  # 设置一页显示多少条数据（news为要分页的数据）
        try:
            news = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            news = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            news = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    results_all = Devicespool.objects.all().order_by("device_name")
    results_len = str(len(results))
    results_all_len = str(len(results_all))
    if url_key_list != []:
        url_key_and_list = "&".join(
            url_key_list_item for url_key_list_item in url_key_list
        )
    return render(request, "lrm/device_search.html", locals())

def device_add(request):
    model_list_set = Devicespool.objects.values_list("model", flat=True)
    model_list = []
    for item in model_list_set:
        if item not in model_list:
            model_list.append(item)
    m = request.method
    if m == "GET":
        return render(request, "lrm/device_add.html", {"model_list": model_list})
    else:
        device_name = request.POST.get("device_name", "")
        model = request.POST.get("model", "")
        mgt_address = request.POST.get("mgt_address", "")
        if device_name and model and mgt_address:
            device = Devicespool(
                device_name=device_name, model=model, mgt_address=mgt_address
            )
            device.save()
            messages.error(request, "设备%s的信息已成功添加" % device_name)
            return HttpResponseRedirect("/index")
        messages.error(request, "请补全相关设备信息")
        return HttpResponseRedirect("/add")

def index(request):
    context = {}
    context["ip"] = get_ip_address()
    context["user_count"] = User.objects.count() - 7
    context["device_count"] = Devicespool.objects.exclude(owner__isnull=True).count()
    context["device_inuse_count"] = (
        Devicespool.objects.filter(status="INUSE").exclude(owner__isnull=True).count()
    )
    context["device_port_count"] = Association.objects.exclude(
        owner__isnull=True
    ).count()
    context["use_ratio"] = format(
        float(context["device_inuse_count"]) / float(context["device_count"]) * 100,
        ".1f",
    )
    context["time_now"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return render(request, "lrm/index.html", context)

def deviceinfo(request):  # ajax的url
    data_list = []
    query_set = Devicespool.objects.all()
    for data_info in query_set:
        if data_info.owner and data_info.owner.username != "admin":
            data_list.append(
                {
                    "id": data_info.id,
                    "device_name": data_info.device_name,
                    "status": data_info.status,
                    "model": data_info.model,
                    "domain": data_info.domain,
                    "mgt_address": data_info.mgt_address,
                    "user": data_info.user,
                    "owner": "%s%s_%s"
                    % (
                        data_info.owner.last_name,
                        data_info.owner.first_name,
                        data_info.owner.username,
                    ),
                }
            )
    data_dic = {}
    data_dic["rows"] = data_list  # 格式一定要符合官网的json格式，否则会出现一系列错误
    data_dic["total"] = str(len(data_list))
    data_dic["totalNotFiltered"] = str(len(data_list))
    return HttpResponse(json.dumps(data_dic))

def userinfo(request):  # ajax的url
    data_list = []
    user_list = []
    user_count = 0
    id = 0
    query_set = Devicespool.objects.all()
    for data_info in query_set:
        user_count = Devicespool.objects.filter(user=data_info.user).count()
        if data_info.owner:
            if data_info.user not in user_list:
                id = id + 1
                data_list.append(
                    {
                        "id": id,
                        "user": data_info.user,
                        "count": user_count,
                        "owner": "%s%s%s"
                        % (
                            data_info.owner.last_name,
                            data_info.owner.first_name,
                            data_info.owner.username,
                        ),
                        "email": "%s" % data_info.owner.email,
                        "group": "%s" % Group.objects.get(user=data_info.owner.id),
                    }
                )
        user_list.append(data_info.user)
    data_dic = {}
    data_dic["rows"] = data_list  # 格式一定要符合官网的json格式，否则会出现一系列错误
    data_dic["total"] = str(len(data_list))
    data_dic["totalNotFiltered"] = str(len(data_list))
    return HttpResponse(json.dumps(data_dic))


def index_userinfo(request):
    context = {}
    context["ip"] = get_ip_address()
    return render(request, "lrm/userinfo.html", context)

def link_add(request):
    id1 = request.GET.get("id1")
    id2 = request.GET.get("id2")
    switch_port_list_set = (
        Switchports.objects.filter(deviceid=973)
        .order_by("id")
        .values_list("switch_port", flat=True)
    )
    device_port_list_set = (
        Interfaces.objects.filter(deviceid=922)
        .order_by("id")
        .values_list("device_port", flat=True)
    )

    switch_port_list = []
    device_port_list = []
    context = {}
    context["switch_port_list"] = switch_port_list
    context["device_port_list"] = device_port_list
    context["ip"] = get_ip_address()

    for switch_port_item in switch_port_list_set:
        if switch_port_item not in switch_port_list:
            switch_port_list.append(switch_port_item)

    for device_port_item in device_port_list_set:
        if device_port_item not in device_port_list:
            device_port_list.append(device_port_item)

    m = request.method
    if m == "GET":
        return render(request, "lrm/link_add.html", context)
    else:
        device_port_link_list = request.POST.getlist("device_port")
        switch_port_link_list = request.POST.getlist("switch_port")
        context["device_port_link_list"] = device_port_link_list
        context["switch_port_link_list"] = switch_port_link_list
        if device_port_link_list != "":
            return render(request, "lrm/link_add_result.html", context)
        else:
            return render(request, "lrm/link_add.html", context)

@login_required
def device_share(request):
    model_list_set = Devicespool.objects.values_list("model", flat=True)
    model_list = []
    context = {}
    context["model_list"] = model_list
    context["ip"] = get_ip_address()

    for item in model_list_set:
        if item not in model_list:
            model_list.append(item)

    m = request.method
    if m == "GET":
        form_post = DevicespoolForm()
        context["obj"] = form_post
        return render(request, "lrm/share.html", context)
    else:
        device_name = request.POST.get("device_name", "")
        model = request.POST.get("model", "")
        mgt_address = request.POST.get("mgt_address", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        form_post = DevicespoolForm(request.POST or None)

        if form_post.is_valid():
            time_now = time.strftime("%Y-%m-%d %H:%M:%S.000", time.localtime())

            device = Devicespool(
                device_name=device_name,
                model=model,
                mgt_address=mgt_address,
                created_at=time_now,
                updated_at=time_now,
            )
            device.save()
            model_list = ["zx9k"]
            if model in model_list:
                switchport_obj_list = []
                interface_list = get_interface_info(
                    mgt_address=mgt_address,
                    mgt_username=username,
                    mgt_password=password,
                )
                status = "IDLE"
                filter_result = Devicespool.objects.filter(
                    device_name="%s" % device_name
                )
                for switch_port_item in interface_list:
                    switch_port = Switchports(
                        deviceid=filter_result[0],
                        switch_port=switch_port_item,
                        status=status,
                        created_at=time_now,
                        updated_at=time_now,
                    )
                    switchport_obj_list.append(switch_port)
                Switchports.objects.bulk_create(switchport_obj_list)

            messages.error(request, "设备%s的信息已成功添加" % device_name)
            return HttpResponseRedirect("/index")
        else:
            error_msg = form_post.errors
            context["obj"] = form_post
            context["errors"] = error_msg
            context["device_name"] = device_name
            context["model"] = model
            context["mgt_address"] = mgt_address
            context["username"] = username
            context["password"] = password
            return render(request, "lrm/share.html", context)
    return HttpResponseRedirect("/share")

def get_interface_info(mgt_address, mgt_username, mgt_password):
    host = "10.57.170.158"
    username = "liurui"
    password = "zxr10@ZTE"
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    cmd = "python3 /home/liurui/Django/get_interface_info.py --host={mgt_address} --username={mgt_username} --password={mgt_password}".format(
        mgt_address=mgt_address, mgt_username=mgt_username, mgt_password=mgt_password
    )
    try:
        ssh_client.connect(hostname=host, username=username, password=password)
    except Exception as e:
        print("设备%s连接失败" % host)
        print(e)
        sys.exit()
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    stdout_info = stdout.read().decode("utf8")
    stdout_info_list = []
    stdout_info_list = stdout_info.split("\n")
    interface_list = []
    for interface_item in stdout_info_list:
        if interface_item != "":
            interface_list.append(interface_item)
    ssh_client.close()
    return interface_list
