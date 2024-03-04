from django.shortcuts import render,get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache

import re

import time
from srm.models import KeywordPost
from srm.models import KeywordList
from srm.models import ScriptPost
from srm.models import ScriptList
from srm.models import KeywordSearch
from srm.models import KeywordDoc

from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect
import json
import socket
from itertools import zip_longest
from django.db.models import Q
from functools import reduce
import operator

from pygments import highlight
from pygments.lexers import RobotFrameworkLexer
from pygments.formatters import HtmlFormatter
import os
from datetime import date
from datetime import datetime
from collections import Counter
import random
import requests
import sys
sys.path.append('/AutoCenter/lib') 
#from ztesw.misc.ConfigTransformers.main import ConfigTrans

def chat_knowledge_for_keyword_doc(query, knowledge_base, top_k=1, raw_data=False):
    url = 'http://10.227.153.211:8960/chat/knowledge_base_chat'  # 这里需要改成langchain服务的地址
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    query = query
    knowledge_base = knowledge_base
    data = {
        "knowledge_base_name": f"{knowledge_base}",
        "top_k": top_k,
        "query": f"{query}",
        "history": [
            {
                "role": "user",
                "content": "根据已知信息，输出关键字,只使用已知信息中的词汇"
            },
            {
                "role": "assistant",
                "content": ""
            }
        ],
        "stream": False,
        "local_doc_url": False,
        "score_threshold": 1,
        "model_name": "Qwen_14B_Chat",
        #"prompt_template": "<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 </指令>\n\n<已知信息>{{ context }}</已知信息>\n\n<问题>{{ question }}</问题>"
        "prompt_template": "只回答**知道了**"
    }
    response = requests.post(url, headers=headers,
                             data=json.dumps(data), stream=True)
    print(f"向量匹配参数：{data}")
    if response.status_code == 200:
        content = ''
        start_time = time.time()
        for line in response.iter_content(decode_unicode=True):
            content = content+line
        try:
            # print(f'this is {content}')
            content = json.loads(content.lstrip('data: '))
        except Exception as e:
            print(e)
        end_time = time.time()
        execution_time = round(end_time - start_time, 1)
        print(f"查询的耗时是：{execution_time}")
        if content.get('code', None) == 404:
            raise Exception(content['msg'])
        else:
            if not raw_data:
                keyword_name_list = []
                #print(content['docs'])
                for item in content['docs']:
                    match = re.search(r'关键字名称: (.*)\n', item)
                    #if match.group(1) not in value_list:
                    keyword_name_list.append(match.group(1))
                return (keyword_name_list, execution_time)
                #return keyword_name_list
            else:
                result = content['docs']
                print(result, type(result))
                return (result, execution_time)
    else:
        print("Error:", response.status_code)

def get_keyword(content):
    text = content
    keyword = "keyword:"

    # 找到关键词的位置
    start_index = text.find(keyword)

    if start_index != -1:
        # 提取关键词后面的信息
        extracted_info = text[start_index + len(keyword):].strip()
        # print("提取的信息:", extracted_info)

        return f'{extracted_info}'
    else:
        return f'{""}'

def chat_knowledge(query, knowledge_base):
    url = 'http://10.227.153.211:8960/chat/knowledge_base_chat'  # 这里需要改成langchain服务的地址
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    query = query
    knowledge_base = knowledge_base
    data = {
        "query": f"{query}",
        "knowledge_base_name": f"{knowledge_base}",
        "top_k": 5,
        "history": [
            {
            "role": "user",
            "content": "根据已知信息，输出关键字,只使用已知信息中的词汇"
            },
            {
            "role": "assistant",
            "content": "配置interface"
            }
        ],
        "stream": False,
        "local_doc_url": False,
        "score_threshold": 1,
        "model_name": "Baichuan2-13B-Chat",
        #"prompt_template": "<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 </指令>\n\n<已知信息>{{ context }}</已知信息>\n\n<问题>{{ question }}</问题>"
        "prompt_template": "只回答**知道了**"
        }
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    return response

# def split_config(configtext):
#     configtrans = ConfigTrans(configtext)
#     config_list = configtrans._export_config_split_list()
#     for x in config_list:
#         print(x)
#     return config_list

# def get_keyword(content):
#     text = content
#     keyword = "keyword:"
#     start_index = text.find(keyword)
#     if start_index != -1:
#         extracted_info = text[start_index + len(keyword):].strip()
#         return f'{extracted_info}'
#     else:
#         print("未找到关键词")

# def chat_knowledge(query, knowledge_base):
#     url = 'http://10.227.153.211:8946/chat/knowledge_base_chat'  # 这里需要改成langchain服务的地址
#     headers = {
#         'accept': 'application/json',
#         'Content-Type': 'application/json',
#     }
#     query = query
#     knowledge_base = knowledge_base
#     data = {
#         "query": f"{query}",
#         "knowledge_base_name": f"{knowledge_base}",
#         "top_k": 2,
#         "history": [
#             {
#             "role": "user",
#             "content": "根据已知信息，输出关键字,只使用已知信息中的词汇"
#             },
#             {
#             "role": "assistant",
#             "content": "配置interface"
#             }
#         ],
#         "stream": False,
#         "local_doc_url": False,
#         "score_threshold": 1,
#         "model_name": "Baichuan2-13B-Chat",
#         "prompt_template": "<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 </指令>\n\n<已知信息>{{ context }}</已知信息>\n\n<问题>{{ question }}</问题>"
#         }
#     response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
#     if response.status_code == 200:
#         content = ''
#         content = response.json()
#         if content.get('code',None) == 404:
#             raise Exception(content['msg'])
#         else:
#             key = get_keyword(content['docs'][0])
#             return key
#     else:
#         print("Error:", response.status_code)

# def get_keywords(text, **kwargs):
#     query = text
#     config_list = split_config(query)
#     result = {}
#     if config_list != []:
#         for x in config_list:
#             result[x] = chat_knowledge(x.replace('<','[').replace('>',']'), 'h9-15')
#     keywords=[]
#     for k, v in result.items():
#         keywords.append(v)
#     return keywords

def generate_random_dict(original_dict, num_elements): 
    keys = list(original_dict.keys()) 
    random.shuffle(keys) 
    new_dict = {} 
    for i in range(num_elements): 
        key = keys[i] 
        new_dict[key] = original_dict[key] 
    return new_dict

def get_sorted_search_keys():
    target_date = datetime.now().date()
    search_counter_today = len(KeywordSearch.objects.filter(created_at__date=target_date))
    results = KeywordSearch.objects.all()
    search_counter_all = len(results)
    keyword_list = []
    user_ip_list = []
    pattern = r'^命令行配置\[.*\]'
    for item in results:
        if item.keyword_search_item!='':
            if not re.search(pattern, item.keyword_search_item):
                keyword_list.append(item.keyword_search_item)
        if item.user_ip!='':
            if item.user_ip not in user_ip_list:
                user_ip_list.append(item.user_ip)
    counter = Counter(keyword_list)
    keyword_dict = dict(counter)
    sorted_items = sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_keys = [item[0].replace('\t', ' ') if '\t' in item[0] else item[0] for item in sorted_items]
    user_ip_counter = len(user_ip_list)
    return sorted_keys, search_counter_today, search_counter_all, user_ip_counter
    
    


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip

def index_keywordinfo(request):
    context = {}
    context["ip"] = get_ip_address()
    return render(request, "keywordinfo.html", context)


def query_data(keyword,keyword_search_range,ai_enable):
    keyword_list = []
    if ai_enable=='ai-enable':
        response = chat_knowledge(keyword, 'h9-15')
        if response.status_code == 200:
            content = response.json()
            for i in range(len(content['docs'])):
                if get_keyword(content['docs'][i]) not in keyword_list:
                    keyword_list.append(get_keyword(content['docs'][i]))
            keyword_list = ["加" + item if item.startswith("配置") else item for item in keyword_list] 
        # keyword_list = get_keywords(keyword)
        # keyword_list = ["加" + item if item.startswith("配置") else item for item in keyword_list]
    else:
        #keyword_list = []
        query_list = []
        if keyword_search_range=='yes':
            if '|' in keyword: 
                query_list = ["(Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s'))" % (element.strip(),element.strip()) for element in keyword.split('|')]
                q_item = '|'.join(query_list)
            elif '&' in keyword:
                query_list = ["(Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s'))" % (element.strip(),element.strip()) for element in keyword.split('&')]
                q_item = '&'.join(query_list)
            else:
                q_item = "Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s')" % (keyword.strip(),keyword.strip())
        elif keyword_search_range=='no':
            if '|' in keyword: 
                query_list = ["Q(keyword_name__icontains='%s')" % element.strip() for element in keyword.split('|')]
                q_item = '|'.join(query_list)
            elif '&' in keyword:
                query_list = ["Q(keyword_name__icontains='%s')" % element.strip() for element in keyword.split('&')]
                q_item = '&'.join(query_list)
            else:
                q_item = "Q(keyword_name__icontains='%s')" % (keyword.strip())
        q_object = eval(q_item)
        results = (
            KeywordDoc.objects.filter(q_object)
            .distinct()
            .order_by("keyword_name")
            )
        for item in results:
            keyword_list.append(item.keyword_name)
    return keyword_list

def query_data_obj(keyword,keyword_search_range):
    keyword_list = []
    query_list = []
    if keyword_search_range=='yes':
        if '|' in keyword: 
            query_list = ["(Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s'))" % (element.strip(),element.strip()) for element in keyword.split('|')]
            q_item = '|'.join(query_list)
        elif '&' in keyword:
            query_list = ["(Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s'))" % (element.strip(),element.strip()) for element in keyword.split('&')]
            q_item = '&'.join(query_list)
        else:
            q_item = "Q(keyword_name__icontains='%s')|Q(keyword_doc_html__icontains='%s')" % (keyword.strip(),keyword.strip())
    elif keyword_search_range=='no':
        if '|' in keyword: 
            query_list = ["Q(keyword_name__icontains='%s')" % element.strip() for element in keyword.split('|')]
            q_item = '|'.join(query_list)
        elif '&' in keyword:
            query_list = ["Q(keyword_name__icontains='%s')" % element.strip() for element in keyword.split('&')]
            q_item = '&'.join(query_list)
        else:
            q_item = "Q(keyword_name__icontains='%s')" % (keyword.strip())
    q_object = eval(q_item)
    results = (
        KeywordDoc.objects.filter(q_object)
        .distinct()
        .order_by("keyword_name")
        )
    return results

#@cache_page(60 * 15)
def search_view(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', None)
        db_name = request.GET.getlist('db_name[]')
        keyword_type = request.GET.get('keyword_type')
        keyword_search_range = request.GET.get('keyword_search_range')
        # cache_key = f'search_view_{keyword}_{db_name}_{keyword_type}_{keyword_search_range}'
        # cached_data = cache.get(cache_key)
        # if cached_data:
        #     matches=cached_data
        #     return JsonResponse(matches, safe=False)
        # else:
        matches=[]
        keyword_dict={}
        results = query_data_obj(keyword,keyword_search_range)
        if results:
            for result in results:
                keyword_dict['%s' % result.keyword_name]=int(result.keyword_example_num)
            sorted_keyword_dict = sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)
            matches = ['关键字速查列表（搜索到%s个RF关键字）:' % len(sorted_keyword_dict)] + [item[0] for item in sorted_keyword_dict]
        else:
            matches=['没有匹配的关键字']
        #cache.set(cache_key, matches)
        return JsonResponse(matches, safe=False)
            

def keywordinfo(request):  # ajax的url
    data_list = []
    peizhi_keyword_dict = {}
    jiancha_keyword_dict = {}
    baowenjiexi_keyword_dict = {}
    ceshiyi_keyword_dict = {}
    for keyword_item in KeywordList.objects.all():
        keyword_item_lower=keyword_item.keyword_name.lower()
        keyword_type = '配置'
        if (re.match('^加%s' % keyword_type, keyword_item_lower)) or (re.match('^删%s' % keyword_type , keyword_item_lower)) or (re.match('^%s' % keyword_type , keyword_item_lower)):
            if keyword_item.keyword_name not in peizhi_keyword_dict:
                peizhi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
        keyword_type = '检查'
        if keyword_item.keyword_loc:
            if (re.search('/%s' % keyword_type, keyword_item.keyword_loc)):
                if keyword_item.keyword_name not in jiancha_keyword_dict:
                    jiancha_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
        keyword_type = '报文解析'
        if keyword_item.keyword_loc:
            if (re.search('/%s' % keyword_type, keyword_item.keyword_loc)) or (re.search('/CheckPacket', keyword_item.keyword_loc)):
                if keyword_item.keyword_name not in baowenjiexi_keyword_dict:
                    baowenjiexi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
        keyword_type = '测试仪'
        if re.match('^%s' % keyword_type , keyword_item_lower):
            if keyword_item.keyword_name not in ceshiyi_keyword_dict:
                ceshiyi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)   
                 
    lengths=[len(d) for d in (peizhi_keyword_dict,jiancha_keyword_dict,baowenjiexi_keyword_dict,ceshiyi_keyword_dict)]
    #min_length=min(lengths)
    min_length=100
    id_list = list(range(1,101))
    sorted_peizhi_keyword_list = sorted(peizhi_keyword_dict.items(), key=lambda x: x[1], reverse=True)[:min_length]
    sorted_jiancha_keyword_list = sorted(jiancha_keyword_dict.items(), key=lambda x: x[1], reverse=True)[:min_length]
    sorted_baowenjiexi_keyword_list = sorted(baowenjiexi_keyword_dict.items(), key=lambda x: x[1], reverse=True)[:min_length]
    sorted_ceshiyi_keyword_list = sorted(ceshiyi_keyword_dict.items(), key=lambda x: x[1], reverse=True)[:min_length]
    
    for i in range(min_length):
            data_list.append(
                {
                    "id" : "%s" % id_list[i],
                    "peizhi": "%s" % sorted_peizhi_keyword_list[i][0],
                    "jiancha":"%s" %  sorted_jiancha_keyword_list[i][0],
                    "baowenjiexi": "%s" % sorted_baowenjiexi_keyword_list[i][0],
                    "ceshiyi": "%s" % sorted_ceshiyi_keyword_list[i][0],         
                }
            )
    data_dic = {}
    data_dic["rows"] = data_list  # 格式一定要符合官网的json格式，否则会出现一系列错误
    data_dic["total"] = str(len(data_list))
    data_dic["totalNotFiltered"] = str(len(data_list))
    return HttpResponse(json.dumps(data_dic))

def keywordinfo_all(request):  # ajax的url
    # data_list = []
    # peizhi_keyword_dict = {}
    # jiancha_keyword_dict = {}
    # baowenjiexi_keyword_dict = {}
    # ceshiyi_keyword_dict = {}
    # response_cache_key = f'keywordinfo_all'
    # for keyword_item in KeywordList.objects.all():
        
    #     if int(keyword_item.keyword_example_num)!=0:
    #         keyword_item_lower=keyword_item.keyword_name.lower()
    #         keyword_type = '配置'
    #         if (re.match('^加%s' % keyword_type, keyword_item_lower)) or (re.match('^删%s' % keyword_type , keyword_item_lower)) or (re.match('^%s' % keyword_type , keyword_item_lower)):
    #             if keyword_item.keyword_name not in peizhi_keyword_dict:
    #                 peizhi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
    #         keyword_type = '检查'
    #         if keyword_item.keyword_loc:
    #             if (re.search('/%s' % keyword_type, keyword_item.keyword_loc)):
    #                 if keyword_item.keyword_name not in jiancha_keyword_dict:
    #                     jiancha_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
    #         keyword_type = '报文解析'
    #         if keyword_item.keyword_loc:
    #             if (re.search('/%s' % keyword_type, keyword_item.keyword_loc)) or (re.search('/CheckPacket', keyword_item.keyword_loc)):
    #                 if keyword_item.keyword_name not in baowenjiexi_keyword_dict:
    #                     baowenjiexi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)
    #         keyword_type = '测试仪'
    #         if re.match('^%s' % keyword_type , keyword_item_lower):
    #             if keyword_item.keyword_name not in ceshiyi_keyword_dict:
    #                 ceshiyi_keyword_dict['%s' % keyword_item.keyword_name]=int(keyword_item.keyword_example_num)   
                 
    # lengths=[len(d) for d in (peizhi_keyword_dict,jiancha_keyword_dict,baowenjiexi_keyword_dict,ceshiyi_keyword_dict)]
    # max_length=max(lengths)
    # #min_length=100
    # id_list = list(range(1,max_length+1))
    
    # sorted_peizhi_keyword_list = sorted(peizhi_keyword_dict.items(), key=lambda x: x[1], reverse=True)
    # sorted_jiancha_keyword_list = sorted(jiancha_keyword_dict.items(), key=lambda x: x[1], reverse=True)
    # sorted_baowenjiexi_keyword_list = sorted(baowenjiexi_keyword_dict.items(), key=lambda x: x[1], reverse=True)
    # sorted_ceshiyi_keyword_list = sorted(ceshiyi_keyword_dict.items(), key=lambda x: x[1], reverse=True)

    # result = [[elem if elem is not None else '' for elem in arr] for arr in zip_longest(sorted_peizhi_keyword_list, sorted_jiancha_keyword_list, sorted_baowenjiexi_keyword_list, sorted_ceshiyi_keyword_list, fillvalue=['',''])]
    # for i in range(max_length):
    #         data_list.append(
    #             {
    #                 "id" : "%s" % id_list[i],
    #                 "peizhi": "%s" % result[i][0][0],
    #                 "jiancha":"%s" %  result[i][1][0],
    #                 "baowenjiexi": "%s" % result[i][2][0],
    #                 "ceshiyi": "%s" % result[i][3][0],         
    #             }
    #         )
    # data_dic = {}
    # data_dic["rows"] = data_list  # 格式一定要符合官网的json格式，否则会出现一系列错误
    # data_dic["total"] = str(len(data_list))
    # data_dic["totalNotFiltered"] = str(len(data_list))
    # #cache.set('response_cache_key', json.dumps(data_dic)) 
    # with open("/var/www/LRM/srm/templates/data_dic.json", "w") as file: 
    #     json.dump(data_dic, file) 

    with open("/var/www/LRM/srm/templates/data_dic_new.json", "r") as file:
        data_dic = json.load(file) 
        
    return HttpResponse(json.dumps(data_dic))

def detail_view(request): 
    script_id=int(request.GET.get('id'))
    keyword_name=request.GET.get('keyword_name')
    #obj = get_object_or_404(ScriptPost, id=id) 
    obj = ScriptPost.objects.get(id=script_id) 
    pageview_num = int(obj.pageview)
    
    # content = obj.script
    # content = content.replace('\t', '    ') 
    # html_content = highlight(content, RobotFrameworkLexer(), HtmlFormatter(full=True))
    html_content = '测试用例robot文件路径：' + obj.script_location + obj.script_html
    html_content = html_content.replace('>%s' % keyword_name, f"><span class='highlight_keyword'>{keyword_name}</span>") 

    html_style='pre { line-height: 125%; }'
    html_style_new='.highlight_keyword { background-color: yellow; }\npre { line-height: 125%; }'
    
    html_content = html_content.replace(html_style, f"{html_style_new}") 
    
    with open('/var/www/LRM/srm/templates/script_%s.html' % script_id, 'w') as file:
        file.write(html_content)
    #script = obj.script.split('\n')
    #context = { 'object': obj , 'content': script} 
    #return render(request, 'detail.html', context) 
    #ScriptPost.objects.update(pageview=0)
    pageview_num = pageview_num + 1
    obj.pageview = pageview_num
    obj.save()
    return render(request, 'script_%s.html' % script_id) 

def testcase_view(request): 
    testcase_id=int(request.GET.get('id'))
    obj = ScriptList.objects.get(id=testcase_id) 
    pageview_num = int(obj.pageview)
    #content = '测试用例名称：%s' % obj.testcase_name + '\n\n' + '测试用例文件路径：%s' % obj.testcase_loc + '\n\n'+ '测试用例文档：' + '\n\n' + obj.testcase_doc + '\n\n' + '测试用例内容：' + '\n\n' + obj.testcase
    #content = content.replace('\t', '    ') 
    #html_content = highlight(content, RobotFrameworkLexer(), HtmlFormatter(full=True))
    html_content = obj.testcase_html
    with open('/var/www/LRM/srm/templates/testcase_%s.html' % testcase_id, 'w') as file:
        file.write(html_content)
    pageview_num = pageview_num + 1
    obj.pageview = pageview_num
    obj.save()
    return render(request, 'testcase_%s.html' % testcase_id) 

def doc_info(request):
    ip = '10.57.170.40'
    keyword_name=request.GET.get('keyword_name')
    results=[]
    rows=[]
    queryset = KeywordDoc.objects.filter(keyword_name='%s' % keyword_name)
    if len(queryset)>=1:
        if queryset[0].keyword_doc_html:
            lines = queryset[0].keyword_doc_html.split('\n')
            rows.append(keyword_name)
            rows.append(lines)
            results.append(rows)
    else:
        lines = ''
        rows.append('')
        rows.append(lines)
        results.append(rows)
    
    return render(request, 'keyword_doc.html', {'results': results, 'ip': ip, 'keyword_name': keyword_name,})

def keyword_doc_view(request): 
    keyword_name=request.GET.get('keyword')
    obj = KeywordList.objects.filter(keyword_name='%s' % keyword_name) 
    #doc = obj.keyword_doc_html.split('\n')
    if obj[0].keyword_example:
        example_dict = eval(obj[0].keyword_example)
        id_list=[]
        example_dict_no_dup={}
        index=0
        for key,value in example_dict.items():
            if value[1] not in id_list:
                index=index+1
                example_dict_no_dup[index]=value
                id_list.append(value[1])
        if len(example_dict_no_dup)>100:
            example_dict_no_dup_100 = generate_random_dict(example_dict_no_dup,100)
        else: 
            example_dict_no_dup_100 = example_dict_no_dup     
            
        # for key,value in example_dict.items():
        #     html_content = highlight('\n'.join(value[2]), RobotFrameworkLexer(), HtmlFormatter(full=True))
        #     value[2] = html_content.split('\n')[98:109]
        
    # if obj.testcase_example:
    #     example_dict = eval(obj.testcase_example)
    else:
        example_dict_no_dup = {}
        example_dict_no_dup_100 = {}
    #context = { 'object': obj , 'content': doc, 'content_example' : example_dict, 'keyword': keyword_name} 
    #ip = get_ip_address()
    ip = '10.57.170.40'
    context = { 'object': obj[0], 'content_example' : example_dict_no_dup_100, 'keyword': keyword_name, 'total_number': len(example_dict_no_dup), 'ip': ip} 
    #context = {'keyword': keyword_name} 
    return render(request, 'doc.html', context) 

def case_all_view(request): 
    keyword_name=request.GET.get('keyword','')
    testcase_db_name=request.GET.get('testcase_db_name','')
    testcase_db_name = eval(testcase_db_name)
    db_name = '、'.join(testcase_db_name)
    obj = KeywordList.objects.filter(keyword_name='%s' % keyword_name) 
    if obj[0].testcase_example:
        example_dict = eval(obj[0].testcase_example)
        id_list=[]
        example_dict_no_dup={}
        index=1
        for key,value in example_dict.items():
            match = re.search(r'测试用例文件路径：/root/script/(.*?)/', value[0])
            if match.group(1) in testcase_db_name:
                if value[1] not in id_list:
                    example_dict_no_dup[index]=value
                    id_list.append(value[1])
                    index=index+1
        if len(example_dict_no_dup)>100:
            example_dict_no_dup_100 = generate_random_dict(example_dict_no_dup,100)  
        else: 
            example_dict_no_dup_100 = example_dict_no_dup
            
        # for key,value in example_dict.items():
        #     html_content = highlight('\n'.join(value[2]), RobotFrameworkLexer(), HtmlFormatter(full=True))
        #     value[2] = html_content.split('\n')[98:109]
        
    # if obj.testcase_example:
    #     example_dict = eval(obj.testcase_example)
    else:
        example_dict_no_dup = {}
        example_dict_no_dup_100 = {}
    #context = { 'object': obj , 'content': doc, 'content_example' : example_dict, 'keyword': keyword_name} 
    #ip = get_ip_address()
    ip = '10.57.170.40'
    context = { 'object': obj[0], 'content_example' : example_dict_no_dup_100, 'keyword': keyword_name, 'total_number': len(example_dict_no_dup), 'ip': ip, 'db_name': db_name} 
    #context = {'keyword': keyword_name} 
    return render(request, 'doc_testcase.html', context) 

def replace_quotes(string):
    pattern = r'``([^``]*)``'
    replacement = r'<code>\1</code>'
    result = re.sub(pattern, replacement, string)
    return result

def convert_to_html(text): 
    html = "<p><b>参数介绍：</b></p>\n" 
    if '配置参数介绍' in text:
        option_params = text[text.index("*参数介绍：*") + 7:text.index("*配置参数介绍：*")].strip().split("\n")
    else:
        option_params = text[text.index("*参数介绍：*") + 7:text.index("*作者：*")].strip().split("\n")
        
    option_params_html=replace_quotes(option_params[0])
    option_params_list=option_params_html.split('...')
    for option in option_params_list:
            if '<code>' in option:
                html += "<p>" + option.split('</code>')[0] + "</code>  " + option.split('</code>')[1] + "</p>\n"
            
    html += "<p><b>配置参数介绍：</b></p>\n" 
    html += "<table>\n" 
    html += "<tr><td><b>参数名称</b></td><td><b>参数说明</b></td><td><b>value</b></td><td><b>对应配置或命令</b></td></tr>\n" 
    config_params = text[text.index("*配置参数介绍：*") + 9:text.index("*示例：*")].strip().split("\n") 
    for param in config_params: 
        param = param.strip("|").strip() 
        #print(param)
        if param!="...":
            if "参数名称" not in param:
                html += "<tr>" 
                for i in range(len(param.split("|"))):
                    if param.split("|")[i].strip()!="...":
                        string = replace_quotes(param.split("|")[i].strip())
                        html += "<td>" + string + "</td>" 
            
                html += "</tr>\n" 
    html += "</table>\n" 
    html += "<p><b>示例：</b></p>\n" 
    html += "<table>\n" 
    examples = text[text.index("*示例：*") + 5:text.index("*作者：*")].strip().split("\n") 
    for example in examples: 
        print(example)
        example = example.strip("|").strip() 
        if example!="...":
            html += "<tr>" 
            for i in range(len(example.split("|"))):
                if example.split("|")[i].strip()!="...":
                    html += "<td>" + example.split("|")[i].strip() + "</td>" 
            
            html += "</tr>\n" 
    html += "</table>\n" # 作者和时间部分 
    html += "<p><b>作者：</b>" + text[text.index("*作者：*") + 5:text.index("*创建时间：*")].strip().split('\n')[0] + "</p>\n"
    html += "<p><b>创建时间：</b>" + text[text.index("*创建时间：*") + 7:text.index("*最后修改时间：*")].strip().split('\n')[0] + "</p>\n"
    html += "<p><b>最后修改时间：</b>"  + text[text.index("*最后修改时间：*") + 9:].strip().split('\n')[0] + "</p>\n"
    
    return html

#@cache_page(60 * 15)
def keyword_search(request): 
    start_time = time.time()
    if request.method == 'POST': 
        keyword = request.POST.get('keyword')
        db_name = request.POST.getlist('db_name')
        testcase_db_name = request.POST.getlist('testcase_db_name')
        choice = request.POST.get('choice')
        output_number = request.POST.get('output_number')
        keyword_type = request.POST.get('keyword_type')
        keyword_search_range = request.POST.get('keyword_search_range')
        #ai_enable = request.POST.get('ai_enable')
        ai_enable = 'ai-disable'
        user_ip = request.META.get('REMOTE_ADDR')
        db_list= '、'.join(db_name) 
        db_name_list=[]
        if choice=='yes':
            link_type='example'
        elif choice=='no':
            link_type='case_all'
        #cache_key = f'keyword_search_{keyword}_{db_name}_{choice}_{output_number}_{keyword_type}_{keyword_search_range}_{ai_enable}'
        #cached_data = cache.get(cache_key)
        if ai_enable=='ai-enable':
            keyword_search_obj = KeywordSearch(keyword_search_item="命令行配置[%s]" % keyword, user_ip=user_ip)
        else:
            keyword_search_obj = KeywordSearch(keyword_search_item=keyword, user_ip=user_ip)
        keyword_search_obj.save()
        # if cached_data:
        #     if choice=='yes':
        #         return render(request, 'search_results_without_example.html', cached_data)
        #     elif choice=='no':
        #         return render(request, 'search_results_without_example_all.html', cached_data)

        # else:
        for db_name_item in db_name:
            if db_name_item.split('关键字库')[0]=='中台':
                db_name_list.append('keywords')
                db_name_list.append('lib')
            elif db_name_item.split('关键字库')[0]=='15K':
                #db_name_list.append('keywords_9k')
                db_name_list.append('zxr15k')
            elif db_name_item.split('关键字库')[0]=='C89E':
                db_name_list.append('keywords_c89e')
            elif db_name_item.split('关键字库')[0]=='UFP':
                db_name_list.append('keywords_ufp')
                db_name_list.append('zxrUFP')
            elif db_name_item.split('关键字库')[0]=='DC':
                db_name_list.append('keywords_dc')
                db_name_list.append('zxrdc')
                db_name_list.append('keywords_9k')
            elif db_name_item.split('关键字库')[0]=='智家':
                db_name_list.append('zhijia')
            elif db_name_item.split('关键字库')[0]=='无线':
                db_name_list.append('wuxian')
            else:
                db_name_list.append('keywords_%s' % db_name_item.split('关键字库')[0].lower())
        matches=[]
        query_list = []
        if '|' in keyword: 
            query_list = [keyword.strip() for keyword in keyword.split('|')]
        elif '&' in keyword:
            query_list = [keyword.strip() for keyword in keyword.split('&')]
        else:
            query_list = [keyword.strip()]
        #lines_html = """<p><b>参数介绍：</b></p>"""
        #lines_html = convert_to_html(line_text)
        keyword_list=[]
        keyword_lower=keyword.lower()
        results=[]
        results_example_counter=0
        script_results=[]
        script_results_all=[]
        sample_number = 0
        # for keyword_item in KeywordList.objects.all():
        #     keyword_item_lower=keyword_item.keyword_name.lower()
        #     if keyword_type == 'all':
        #         if keyword_lower in keyword_item_lower:
        #             if keyword_item.keyword_name not in keyword_list:
        #                 keyword_list.append(keyword_item.keyword_name)
        #     elif keyword_type == '配置':
        #         if (keyword_lower in keyword_item_lower) and ((re.match('^加%s' % keyword_type , keyword_item_lower)) or (re.match('^删%s' % keyword_type , keyword_item_lower)) or (re.match('^%s' % keyword_type , keyword_item_lower))):
        #             if keyword_item.keyword_name not in keyword_list:
        #                 keyword_list.append(keyword_item.keyword_name)
        #     else:
        #         if (keyword_lower in keyword_item_lower) and (re.match('^%s' % keyword_type , keyword_item_lower)):
        #             if keyword_item.keyword_name not in keyword_list:
        #                 keyword_list.append(keyword_item.keyword_name)
        keyword_list_query = query_data(keyword_lower,keyword_search_range,ai_enable)
        for keyword_item in keyword_list_query:
            keyword_item_lower=keyword_item.lower()
            if keyword_type == 'all':
                keyword_list.append(keyword_item)
            elif keyword_type == '配置':
                if (re.match('^加%s' % keyword_type , keyword_item_lower)) or (re.match('^删%s' % keyword_type , keyword_item_lower)) or (re.match('^%s' % keyword_type , keyword_item_lower)):
                    keyword_list.append(keyword_item)
            elif keyword_type == '检查':
                if (re.match('^%s' % keyword_type , keyword_item_lower)) or (re.match('^获取' , keyword_item_lower)) or (re.match('^重复%s' % keyword_type, keyword_item_lower)):
                    keyword_list.append(keyword_item)
            else:
                if (re.match('^%s' % keyword_type , keyword_item_lower)):
                    keyword_list.append(keyword_item)
        keyword_list_sorted = sorted(keyword_list, key=len, reverse=True)
        
        for keyword_name in keyword_list_sorted:
            #pattern = r'%s\n(.*?)\[Arguments\]' % keyword_name
            #for item in KeywordPost.objects.all():
            lines=''
            example_lines=''
            rows=[]
            #line_text = item.keyword
            #result = re.findall(pattern, item.keyword, re.DOTALL)
                
                #if result:
            queryset = KeywordDoc.objects.filter(keyword_name='%s' % keyword_name)
            if queryset[0].keyword_loc:
                if queryset[0].keyword_loc.split('/')[3].lower() in db_name_list:
                    #line_text = result[0]
                    #lines = result[0].split('...')
                    queryset = KeywordDoc.objects.filter(keyword_name='%s' % keyword_name)
                    #if queryset[0].keyword_doc:
                    if queryset[0].keyword_doc_html:
                        #replace_str = '&lt;mark&gt;%s&lt;/mark&gt' % keyword
                        #highlighted_keyword_doc = queryset[0].keyword_doc.replace(keyword, replace_str)
                        #lines = highlighted_keyword_doc.split('...')
                        #lines = queryset[0].keyword_doc.split('...')
                        highlighted_lines=queryset[0].keyword_doc_html
                        for query_item in query_list: 
                            pattern = query_item
                            match = re.search(pattern, highlighted_lines, flags=re.IGNORECASE) 
                            if match: 
                                matched_string = match.group()
                                highlighted_lines = highlighted_lines.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                            else:
                                highlighted_lines = highlighted_lines.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                    
                           
                        # pattern = keyword.strip()
                        # match = re.search(pattern, queryset[0].keyword_doc_html, flags=re.IGNORECASE) 
                        # if match: 
                        #     matched_string = match.group()
                        #     highlighted_lines = queryset[0].keyword_doc_html.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                        # else:
                        #     highlighted_lines = queryset[0].keyword_doc_html.replace(keyword, f"<span class='highlight'>{keyword}</span>")

                        #highlighted_lines = queryset[0].keyword_doc_html.replace(keyword, f"<span class='highlight'>{keyword}</span>")
                        lines = highlighted_lines.split('\n')
                        #lines = queryset[0].keyword_doc_html.split('\n')
                    #line_text = '###\n'.join(lines)
                    #lines_html = convert_to_html(lines)
                    
                    #script_name_list=[]
                    if queryset[0].keyword_example: 
                        highlighted_lines='\n'.join(eval(queryset[0].keyword_example)[2])
                        highlighted_lines=highlighted_lines.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
                        for query_item in query_list: 
                            pattern = query_item
                            match = re.search(pattern, highlighted_lines, flags=re.IGNORECASE) 
                            if match: 
                                matched_string = match.group()
                                highlighted_lines = highlighted_lines.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                            else:
                                highlighted_lines = highlighted_lines.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                        example_lines = highlighted_lines.split('\n')
                        
                    for query_item in query_list:
                        
                        pattern = query_item
                        match = re.search(pattern, keyword_name, flags=re.IGNORECASE) 
                        if match: 
                            matched_string = match.group()
                            keyword_name_highlight = keyword_name.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                            
                        else:
                            keyword_name_highlight = keyword_name.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                    script_results_all=[]
                    rows.append(keyword_name_highlight)
                    rows.append(lines)
                    rows.append(keyword_name)
                    rows.append(example_lines)
                    # obj=KeywordList.objects.filter(keyword_name=keyword_name)
                    # if len(obj)>=1:
                    #     if obj[0].keyword_example:
                    #         example_dict = eval(obj[0].keyword_example)
                    #         rows.append(example_dict[1][2])
                    results.append(rows)
                    results_example_counter=results_example_counter+len(example_lines)
                    # if choice=='yes':
                    #     for script_item in ScriptPost.objects.all():
                    #         script_item_list = script_item.script.split('\n')
                    #         #for line in script_item_list:
                            
                    #         if script_item.script_location+script_item.script_name not in script_name_list:
                    #             script_name_list.append(script_item.script_location+script_item.script_name)
                    #             for i in range(len(script_item_list)):   
                    #                 #if  keyword_name.lower() in line.lower():
                    #                 if ' %s ' % keyword_name.lower() in script_item_list[i].lower():
                                        
                    #                         if script_item_list[i] not in script_results:
                    #                             #script_results.append('%s [示例索引：%s/%s.robot]' % (line,script_item.script_location,script_item.script_name))
                    #                             script_with_title=[]
                    #                             script_results.append(script_item_list[i])
                                                
                    #                             script_with_title.append('[示例索引号 %s ：%s/%s.robot]' % (script_item.id,script_item.script_location,script_item.script_name))
                    #                             script_with_title.append(script_item.id)
                    #                             script_with_title.append(script_item_list[i-5:i+6])
                    #                             script_results_all.append(script_with_title)
                    # if choice=='yes':
                    #     if queryset[0].keyword_example:
                    #         # example_content = queryset[0].keyword_example.replace('\t', '    ')
                    #         # example_dic = eval(example_content)
                    #         example_dic = eval(queryset[0].keyword_example)
                    
                    #     #id_list=[]
                    #         for key,value in example_dic.items():
                    #             script_with_title=[]
                    #             new_string_list=[]
                    #             #if value[1] not in id_list:
                    #             html_content = highlight('\n'.join(value[2]), RobotFrameworkLexer(), HtmlFormatter(full=True))
                    #             html_content_list = html_content.split('\n')[98:109]
                    #             for item in html_content_list:
                    #             #for item in value[2]:
                    #                 item = re.sub(r'^\t', '    ', item)
                    #                 for query_item in query_list: 
                    #                     pattern = query_item
                    #                     match = re.search(pattern, item, flags=re.IGNORECASE) 
                    #                     if match: 
                    #                         matched_string = match.group()
                    #                         item = item.replace(matched_string, f"<span class='highlight'>{matched_string}</span>")
                    #                         #item = item.replace(item, f"<span class='highlight'>{item}</span>")
                    #                     else:
                    #                         item = item.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                                            
                    #                 new_string_list.append(item)
                                
                    #             script_with_title.append(value[0])
                    #             script_with_title.append(value[1])
                    #             script_with_title.append(new_string_list)
                    #             #script_with_title.append(value[2])
                    #             script_results_all.append(script_with_title)
                    #             #id_list.append(value[1])
                    # elif choice=='no':
                    #     if queryset[0].testcase_example:
                    #         example_dic = eval(queryset[0].testcase_example)
                    #     #else:
                    #     #    example_dic = {}
                    #         id_list=[]
                    #         for key,value in example_dic.items():
                    #             script_with_title=[]
                    #             new_string_list=[]
                    #             if value[1] not in id_list:
                    #                 for item in value[2]:
                    #                     item = re.sub(r'^\t', '    ', item)
                    #                     for query_item in query_list: 
                    #                         pattern = query_item
                    #                         match = re.search(pattern, item, flags=re.IGNORECASE) 
                    #                         if match: 
                    #                             matched_string = match.group()
                    #                             item = item.replace(matched_string, f"<span class='highlight'>{matched_string}</span>")
                    #                             #item = item.replace(item, f"<span class='highlight'>{item}</span>")
                    #                         else:
                    #                             item = item.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                                                
                    #                     new_string_list.append(item)
                                    
                    #                 script_with_title.append(value[0])
                    #                 script_with_title.append(value[1])
                    #                 script_with_title.append(new_string_list)
                    #                 #script_with_title.append(value[2])
                    #                 script_results_all.append(script_with_title)
                    #                 id_list.append(value[1])
                                
                    # # for query_item in query_list:  
                    # #     if query_item in keyword_name:
                    # #         highlighted_keyword_name = keyword_name.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                    # #     else:
                    # #         highlighted_keyword_name = keyword_name
                    # #     highlighted_keyword_name = re.sub(re.escape(query_item), f"<span class='highlight'>{query_item}</span>", keyword_name, flags=re.IGNORECASE)
                    # for query_item in query_list:
                        
                    #     pattern = query_item
                    #     match = re.search(pattern, keyword_name, flags=re.IGNORECASE) 
                    #     if match: 
                    #         matched_string = match.group()
                    #         keyword_name_highlight = keyword_name.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                            
                    #     else:
                    #         keyword_name_highlight = keyword_name.replace(query_item, f"<span class='highlight'>{query_item}</span>")
                            
                    
                    # # pattern = keyword.strip()
                    # # match = re.search(pattern, keyword_name, flags=re.IGNORECASE) 
                    # # if match: 
                    # #     matched_string = match.group()
                    # #     highlighted_keyword_name = keyword_name.replace(matched_string, f"<span class='highlight'>{matched_string}</span>") 
                    # # else:
                    # #     highlighted_keyword_name = keyword_name.replace(keyword, f"<span class='highlight'>{keyword}</span>")
                    # #rows.append(highlighted_keyword_name)
                    # rows.append(keyword_name_highlight)
                    # rows.append(lines)
                    # script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all)} 
                    # rows.append(script_results_all_dict)
                    # sample_number = sample_number + len(script_results_all)
                    # rows.append(keyword_name)
                    # results.append(rows)
                    # #         rows.append(script_results_all_dict)
                    # if (choice=='yes') or (choice=='all'):
                    #     #if script_results_all:
                    #     if output_number=='3':
                    #         if len(script_results_all)>=3:
                    #             script_sample=[script_results_all[0],script_results_all[len(script_results_all)//2],script_results_all[-1]]
                    #             script_sample_dict = {index+1: sample for index, sample in enumerate(script_sample)} 
                    #             rows.append(script_sample_dict)
                                
                    #         else:
                    #             script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all)} 
                    #             rows.append(script_results_all_dict)
                            
                    #     elif output_number=='5':
                    #         if len(script_results_all)>=5:
                    #             script_sample=[script_results_all[0],script_results_all[len(script_results_all)//2//2],script_results_all[len(script_results_all)//2],script_results_all[-len(script_results_all)//2//2],script_results_all[-1]]
                    #             script_sample_dict = {index+1: sample for index, sample in enumerate(script_sample)} 
                    #             rows.append(script_sample_dict)
                    #         else:
                    #             script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all)} 
                    #             rows.append(script_results_all_dict)
                    #     elif output_number=='7':
                    #         if len(script_results_all)>=9:
                    #             script_sample=[script_results_all[0],script_results_all[len(script_results_all)//2//2//2],script_results_all[len(script_results_all)//2//2],script_results_all[len(script_results_all)//2],script_results_all[-len(script_results_all)//2//2],script_results_all[-len(script_results_all)//2//2//2],script_results_all[-1]]
                    #             script_sample_dict = {index+1: sample for index, sample in enumerate(script_sample)} 
                    #             rows.append(script_sample_dict)
                    #         else:
                    #             script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all[0:7])}
                    #             rows.append(script_results_all_dict)
                    #     elif output_number=='17':
                    #         if len(script_results_all)>=17:
                    #             script_sample=[script_results_all[0],script_results_all[len(script_results_all)//2//2//2//2],script_results_all[len(script_results_all)//2//2//2],script_results_all[len(script_results_all)//2//2],script_results_all[len(script_results_all)//2],script_results_all[-len(script_results_all)//2//2],script_results_all[-len(script_results_all)//2//2//2],script_results_all[-len(script_results_all)//2//2//2//2],script_results_all[-1]]
                    #             script_sample_dict = {index+1: sample for index, sample in enumerate(script_sample)} 
                    #             rows.append(script_sample_dict)
                    #         else:
                    #             script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all[0:9])}
                    #             rows.append(script_results_all_dict)
                    #     elif output_number=='all':
                    #         script_results_all_dict = {index+1: sample for index, sample in enumerate(script_results_all)} 
                    #         rows.append(script_results_all_dict)
                                
                    #         #results.append(rows)
                    #     #if script_results_all:
                    #     sample_number = sample_number + len(script_results_all)
                    #     rows.append(keyword_name)
                    #     results.append(rows)
                    # else:
                    #     rows.append(keyword_name)
                    #     results.append(rows)   

        total_number = len(results) 
        end_time = time.time()
        run_time = round(end_time - start_time, 1)
        results_invert = results[::-1]
        #ip = get_ip_address()
        ip = '10.57.170.40'
        #cache.set(cache_key, {'results': results_invert, 'total_number': total_number, 'db_list': db_list, 'sample_number': sample_number, 'run_time': run_time})
        if not results:
            output_number=10
            if 'zhijia' in db_name_list:
                keyword_name_list, execution_time = chat_knowledge_for_keyword_doc(keyword,'zhijia_keyword_doc', top_k=output_number)
            elif 'wuxian' in db_name_list:
                keyword_name_list, execution_time = chat_knowledge_for_keyword_doc(keyword,'wuxian_keyword_doc', top_k=output_number)
            else:
                #keyword_name_list, execution_time = chat_knowledge_for_keyword_doc(keyword,'keyword_doc_20231218', top_k=output_number)
                keyword_name_list, execution_time = chat_knowledge_for_keyword_doc(keyword,'keyword_doc_20240130', top_k=output_number)
            if len(keyword_name_list)>10:
                keyword_name_list=keyword_name_list[:10]
            results=[]
            results_example_counter=0
            for i in range(len(keyword_name_list)):
                lines=''
                example_lines=''
                rows=[]
                queryset = KeywordDoc.objects.filter(keyword_name='%s' % keyword_name_list[i])
                if len(queryset)>=1:
                    if queryset[0].keyword_doc_html:
                        lines = queryset[0].keyword_doc_html.split('\n')
                        
                    if queryset[0].keyword_example: 
                        highlighted_lines='\n'.join(eval(queryset[0].keyword_example)[2])
                        highlighted_lines=highlighted_lines.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
                        example_lines = highlighted_lines.split('\n')
                    rows.append(keyword_name_list[i])
                    rows.append(lines)
                    rows.append(example_lines)
                    results.append(rows)
                    results_example_counter=results_example_counter+len(example_lines)
                else:
                    rows.append('')
                    rows.append(lines)
                    rows.append('')
                    results.append(rows)
            total_number=len(results)
            return render(request, 'search_results_for_keyword_doc.html', {'results': results, 'total_number': total_number, 'ip': ip, 'run_time': execution_time, 'keyword_name': keyword, 'results_example_counter': results_example_counter, 'link_type': link_type, 'testcase_db_name': testcase_db_name})
        # if choice=='yes':
                
        #     return render(request, 'search_results.html', {'results': results, 'total_number': total_number, 'db_list': db_list, 'sample_number': sample_number, 'run_time': run_time})

        # elif choice=='all':
            
        #     return render(request, 'search_results_all.html', {'results': results, 'total_number': total_number, 'db_list': db_list, 'sample_number': sample_number, 'run_time': run_time})
        # else:
            
        #     return render(request, 'search_results_without_example.html', {'results': results, 'total_number': total_number, 'db_list': db_list,'sample_number': sample_number, 'run_time': run_time})
        
        
        return render(request, 'search_results_without_example_all.html', {'results': results_invert, 'total_number': total_number, 'db_list': db_list,'sample_number': sample_number, 'run_time': run_time, 'ip': ip, 'results_example_counter': results_example_counter, 'link_type': link_type, 'testcase_db_name': testcase_db_name})

            
            
        
    else: 
        #total_keyword_number = len(KeywordDoc.objects.all())
        # total_keyword_number = len(KeywordList.objects.all())
        #total_file_number = len(KeywordPost.objects.all())
        # total_script_number = len(ScriptPost.objects.all())
        #return render(request, 'search_form.html', {'total_keyword_number': total_keyword_number, 'total_file_number': total_file_number, 'total_script_number': total_script_number}) 
        #sorted_search_keys = get_sorted_search_keys()
        #ip = get_ip_address()
        ip = '10.57.170.40'
        user_ip = request.META.get('REMOTE_ADDR')
        sorted_search_keys, search_counter_today, search_counter_all, user_ip_counter = get_sorted_search_keys()
        #return render(request, 'search_form.html', {'sorted_search_keys': sorted_search_keys[:50]})
        #return render(request, 'search_form.html', {'total_keyword_number': total_keyword_number, 'total_file_number': total_file_number, 'sorted_search_keys': sorted_search_keys[:50], 'search_counter_today': search_counter_today, 'search_counter_all': search_counter_all, 'user_ip': user_ip, 'ip': ip, 'user_ip_counter': user_ip_counter })
        return render(request, 'search_form.html', {'sorted_search_keys': sorted_search_keys[:50], 'search_counter_today': search_counter_today, 'search_counter_all': search_counter_all, 'user_ip': user_ip, 'ip': ip, 'user_ip_counter': user_ip_counter })
        #return render(request, 'search_form.html') 
     
        # keyword_number_list = [0,0,0,0,0]
        # for item in KeywordList.objects.all():
        #     print(item.keyword_loc)
        #     if item.keyword_loc:
        #         if '/root/rfhub/keywords/' in item.keyword_loc:
        #             keyword_number_list[0]=keyword_number_list[0]+1
        #         elif '/root/rfhub/keywords_9k/' in item.keyword_loc:
        #             keyword_number_list[1]=keyword_number_list[1]+1
        #         elif '/root/rfhub/keywords_c89e/' in item.keyword_loc:
        #             keyword_number_list[2]=keyword_number_list[2]+1
        #         elif '/root/rfhub/keywords_UFP/' in item.keyword_loc:
        #             keyword_number_list[3]=keyword_number_list[3]+1
        #     else:
        #         keyword_number_list[4]=keyword_number_list[4]+1
                
        # return render(request, 'search_form.html', {'keyword_number_list': keyword_number_list}) 
        #return render(request, 'search_form.html')


        
