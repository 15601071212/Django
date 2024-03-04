from django.urls import re_path as url

from . import views

from django.urls import path

urlpatterns =[
     url(r'^$', views.keyword_search, name='doc_backup'),
     url('search/', views.search_view, name='search'),
     url('keyword_info_all', views.keywordinfo_all, name='keywordinfo_all'),
     url('keyword_info', views.keywordinfo, name='keywordinfo'),
     url("index_keywordinfo", views.index_keywordinfo, name="index_keywordinfo"), 
     url('doc_info', views.doc_info, name='doc_info'),
     url('doc', views.keyword_search, name='doc'),
     #url('keyword_search', views.keyword_search, name='keyword_search'),
     url('detail', views.detail_view, name='detail'),
     url('testcase', views.testcase_view, name='testcase'),
     url('example', views.keyword_doc_view, name='example'),
     url('case_all', views.case_all_view, name='case_all'),
        ]
