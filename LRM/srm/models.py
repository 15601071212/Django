from django.db import models

class ScriptPost(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True,verbose_name="测试用例名称")
    script_location = models.CharField(max_length=500,blank=True, null=True,verbose_name="脚本文件路径")
    script_name = models.CharField(max_length=500,blank=True, null=True,verbose_name="脚本文件名")
    author = models.CharField(max_length=50,blank=True, null=True,verbose_name="脚本作者")
    script = models.TextField(blank=True, null=True,verbose_name="脚本内容")
    pageview = models.CharField(max_length=50,blank=True, null=True,verbose_name="访问次数")
    script_html = models.TextField(blank=True, null=True,verbose_name="脚本内容HTML")
    

    class Meta:
        ordering = ('-id',)
        verbose_name = "测试脚本库"  
        verbose_name_plural = "测试脚本库" 

class ScriptList(models.Model):
    testcase_loc = models.CharField(max_length=500,blank=True, null=True,verbose_name="测试用例路径")
    testcase_name = models.CharField(max_length=500,blank=True, null=True,verbose_name="测试用例名称")
    testcase_doc = models.TextField(blank=True, null=True,verbose_name="测试用例文档")
    testcase = models.TextField(blank=True, null=True,verbose_name="测试用例内容")
    pageview = models.CharField(max_length=50,blank=True, null=True,verbose_name="访问次数")
    testcase_html = models.TextField(blank=True, null=True,verbose_name="测试用例内容HTML")

    

    class Meta:
        ordering = ('-id',)
        verbose_name = "测试用例库"  
        verbose_name_plural = "测试用例库"

class KeywordPost(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True,verbose_name="关键字名称")
    keyword_location = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字文件路径")
    keyword_name = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字文件名")
    author = models.CharField(max_length=50,blank=True, null=True,verbose_name="关键字作者")
    keyword = models.TextField(blank=True, null=True,verbose_name="关键字内容")
    

    class Meta:
        ordering = ('-id',)
        verbose_name = "关键字库"  
        verbose_name_plural = "关键字库" 

class KeywordList(models.Model):
    keyword_name = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字名")
    keyword_doc = models.TextField(blank=True, null=True,verbose_name="关键字说明")
    keyword_doc_html = models.TextField(blank=True, null=True,verbose_name="关键字说明HTML")
    keyword_loc = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字文件路径")
    keyword_example = models.TextField(blank=True, null=True,verbose_name="关键字示例")
    #keyword_example_html = models.TextField(blank=True, null=True,verbose_name="关键字示例HTML")
    keyword_example_num =  models.CharField(max_length=100,blank=True, null=True,verbose_name="关键字示例数量")
    testcase_example = models.TextField(blank=True, null=True,verbose_name="测试用例示例")
    #testcase_example_html = models.TextField(blank=True, null=True,verbose_name="测试用例示例HTML")
    testcase_example_num =  models.CharField(max_length=100,blank=True, null=True,verbose_name="测试用例示例数量")
    
    class Meta:
        ordering = ('-id',)
        verbose_name = "关键字名称库"  
        verbose_name_plural = "关键字名称库" 

class KeywordSearch(models.Model):
    keyword_search_item = models.CharField(max_length=10000,blank=True, null=True,verbose_name="关键字搜索记录")
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    user_ip = models.CharField(max_length=50,blank=True, null=True,verbose_name="访问用户IP")

    class Meta:
        ordering = ('-id',)
        verbose_name = "关键字搜索记录库"  
        verbose_name_plural = "关键字搜索记录库" 

class KeywordDoc(models.Model):
    keyword_name = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字名")
    keyword_doc_html = models.TextField(blank=True, null=True,verbose_name="关键字文档HTML")
    keyword_loc = models.CharField(max_length=500,blank=True, null=True,verbose_name="关键字文件路径")
    keyword_example_num =  models.CharField(max_length=100,blank=True, null=True,verbose_name="关键字示例数量")
    keyword_example = models.TextField(blank=True, null=True,verbose_name="关键字示例")
    class Meta:
        ordering = ('-id',)
        verbose_name = "关键字文档库"  
        verbose_name_plural = "关键字文档库" 
