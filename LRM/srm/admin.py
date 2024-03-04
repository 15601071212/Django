from django.contrib import admin
from import_export.admin import ImportExportModelAdmin #导入Excel表格导入导出模块

from .models import ScriptPost
from .models import ScriptList
from .models import KeywordPost
from .models import KeywordList
from .models import KeywordSearch
from .models import KeywordDoc

@admin.register(ScriptPost)

class SrmScriptAdmin(ImportExportModelAdmin):
#class SrmScriptAdmin(admin.ModelAdmin):
    model = ScriptPost
    list_display = (
        "id",
        "script_name",
        "script_location",
        "author",
        "pageview",
        "script_html"
    )
    list_filter = ("author","script_location")
    list_editable = ["author"]
    search_fields = (
        "script_name",
        "script_location",
        "script",
        "author",
        "id",
        "pageview",
        "script_html",
    )
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            keywords = search_term.split()
            q = Q()
            for keyword in keywords:
                q |= Q(script__icontains=keyword) | Q(script__icontains=keyword)
            queryset = queryset.filter(q)
        except:
            pass
        return queryset, use_distinct
@admin.register(KeywordPost)

class SrmKeywordAdmin(ImportExportModelAdmin):
#class SrmKeywordAdmin(admin.ModelAdmin):
    model = KeywordPost
    list_display = (
        "id",
        "keyword_name",
        "keyword_location",
        "author"
    )
    list_filter = ("author","keyword_location")
    list_editable = ["author"]
    search_fields = (
        "keyword_name",
        "keyword_location",
        "keyword",
        "author",
        "id"
    )
@admin.register(KeywordList)

class SrmKeywordListAdmin(ImportExportModelAdmin):
#class SrmKeywordListAdmin(admin.ModelAdmin):
    model = KeywordList
    list_display = (
        "id",
        "keyword_name",
        "keyword_doc",
        "keyword_doc_html",
        "keyword_loc",
        # "keyword_example",
        # "testcase_example",
    )
    search_fields = (
        "keyword_name",
        # "keyword_doc",
        # "keyword_doc_html",
        "keyword_loc",
        # "keyword_example",
        # "testcase_example",
        # "id",
    )
#admin.site.register(ScriptPost)

@admin.register(KeywordSearch)

class SrmKeywordSearchAdmin(ImportExportModelAdmin):
#class SrmKeywordListAdmin(admin.ModelAdmin):
    model = KeywordSearch
    list_display = (
        "id",
        "keyword_search_item",
        "created_at",
        "user_ip",
        
    )
    search_fields = (
        "id",
        "keyword_search_item",
        "created_at",
        "user_ip",
    )

@admin.register(ScriptList)

class SrmScriptListAdmin(ImportExportModelAdmin):
    model = ScriptList
    list_display = (
        "id",
        "testcase_name",
        "testcase_loc",
        "testcase_doc",
        "testcase",  
        "testcase_html",
    )
    search_fields = (
        "id",
        "testcase_name",
        "testcase_loc",
        "testcase_doc",
        "testcase",
        "testcase_html",
    )

@admin.register(KeywordDoc)

class SrmKeywordDocAdmin(ImportExportModelAdmin):
    model = KeywordDoc
    list_display = (
        "id",
        "keyword_name",
        "keyword_doc_html",
        "keyword_loc",
        "keyword_example",
        "keyword_example_num",
    )
    search_fields = (
        "keyword_name",
        "keyword_doc_html",
        "keyword_loc",
        "keyword_example",
        "id",
    )
