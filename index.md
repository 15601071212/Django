### **LRM/lrm/templates/lrm/index.html**
```html
{% load static %}
{% load bootstrap3 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="zh-CN">
    <head>
        
        <meta charset="UTF-8">
        
        {#    核心组件 bootstrap JQuey#}
        <link href="{% static 'bootstrap/css/bootstrap.min.css' %}" rel="stylesheet"/>
        <script src="{% static 'jquery/jquery-3.5.1.min.js' %}"></script>
        <script src="{% static 'bootstrap/js/bootstrap.min.js' %}"></script>
        {#    bootstrap-table 插件#}
        <link href="{% static 'bootstrap-table-master/dist/bootstrap-table.min.css' %}" rel="stylesheet"/>
        <script src="{% static 'bootstrap-table-master/dist/bootstrap-table.min.js' %}"></script>
        <script src="{% static 'bootstrap-table-master/dist/locale/bootstrap-table-zh-CN.min.js' %}"></script>
        <script src="{% static 'bootstrap-table-master/dist/extensions/export/bootstrap-table-export.min.js' %}"></script>
        <script src="{% static 'tableExport/tableExport.min.js' %}"></script>
        <!-- 加载bootstrap-dualllistbox -->
        <link rel="stylesheet" href="{% static 'bootstrap-duallistbox/disc/bootstrap-duallistbox.css' %}" rel="external nofollow"/>
        <script src="{% static 'disc/jquery.bootstrap-duallistbox.js' %}"></script>

        <link rel="stylesheet" href="bootstrap/css/bootstrap.css">
        <link rel="stylesheet" href="bootstrap-duallistbox/disc/bootstrap-duallistbox.css">
        <script src="jquery/jquery-3.5.1.min.js"></script>
        <script src="bootstrap/js/bootstrap.min.js"></script>
  
        <script src="bootstrap-duallistbox/disc/jquery.bootstrap-duallistbox.js"></script>
        
        <link rel="stylesheet" href="https://adminlte.io/themes/AdminLTE/bower_components/bootstrap/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://adminlte.io/themes/AdminLTE/dist/css/AdminLTE.min.css">
        
        <title>自动化测试中台</title>
        
    </head>
    
    <p/>
    <body>
        
        <p/>
        
    <div class="container">
        
    <p/>
    
    <div class="container-fluid">
      <button id="btn_admin" type="button" style="margin-right:27px;width:255px;" class="btn btn-default">
        <span class="glyphicon glyphicon-cloud" aria-hidden="true"></span>    登录自动化中台管理系统      
      </button>
      
        <p/>
        <!-- Small boxes (Stat box) -->
        <div class="row">
          <div class="col-sm-3">
            <!-- small box -->
            <div class="small-box bg-info">
              <div class="inner">
                <h3>{{ user_count }}</h3>

                <p>责任人总数</p>
              </div>
              <div class="icon">
                <i class="ion ion-bag"></i>
              </div>
              <a href="/index_userinfo" class="small-box-footer">更多信息 <i class="fas fa-arrow-circle-right"></i></a>
            </div>
          </div>
          <!-- ./col -->
          <div class="col-sm-3">
            <!-- small box -->
            <div class="small-box bg-success">
              <div class="inner">
                <h3>{{ device_count }}</h3>
                <p>设备总数</p>
              </div>
              <div class="icon">
                <i class="ion ion-stats-bars"></i>
              </div>
              <a href="/demo" class="small-box-footer">更多信息 <i class="fas fa-arrow-circle-right"></i></a>
            </div>
          </div>
          <!-- ./col -->
             <div class="col-sm-3">
            <!-- small box -->
            <div class="small-box bg-info">
              <div class="inner">
                <h3>{{ device_inuse_count }}</h3>

                <p>被占用设备数</p>
              </div>
              <div class="icon">
                <i class="ion ion-bag"></i>
              </div>
              <a href="/admin" class="small-box-footer">更多信息 <i class="fas fa-arrow-circle-right"></i></a>
            </div>
          </div>
          <!-- ./col -->
          <div class="col-sm-3">
            <!-- small box -->
            <div class="small-box bg-success">
              <div class="inner">
                <h3>{{ device_port_count }}</h3>

                <p>设备已连接端口总数</p>
              </div>
              <div class="icon">
                <i class="ion ion-stats-bars"></i>
              </div>
              <a href="/admin" class="small-box-footer">更多信息 <i class="fas fa-arrow-circle-right"></i></a>
            </div>
          </div>
          <!-- ./col -->
        </div>
      </div>
      
      <div style="float:center ; width:100%;">
        
        <!-- 左侧iframe -->
            <div id="monthList"  style=" float:left ; width:28% ;  height:320px; border:2px">
            <iframe frameborder=0 style="position:relative;" height="320"  id="leftFrame"  name="leftFrame" width="100%"  src="http://{{ip}}:8000/gau"></iframe>
            </div>
            <!-- 右侧iframe -->
            <div id="dataDetail"  style=" float:right ; width:72% ;  height:320px; border:2px">
            <iframe frameborder=0 style="position:relative;" height="320"  id="rightFrame"  name="rightFrame" width="100%"  src="http://{{ip}}:8000/demo"></iframe>
            </div>
        </div> 
    
    <h5 align="left">动态拓扑资源数据库查询时间：{{ time_now }}</h5>
    <h3 align="center"><b>动态拓扑设备资源列表</b></h3>
    
    <body>
        
        <div id="toolbar" class="btn-group">
           
            <button id="btn_draw" type="button" class="btn btn-default">
                <span class="glyphicon glyphicon-list" aria-hidden="true"></span>执行机用户责任人列表
            </button>
            <button id="btn_checkinfo" type="button" class="btn btn-default">
              <span class="glyphicon glyphicon-list" aria-hidden="true"></span>测试设备运行状态巡检表
          </button>
        </div>
    
            
        
            <table id="table"></table>
       
        </body>
   
</div>

</body>

<script type="text/javascript">
    $(document).ready(function(){ 
    $("#btn_draw").click(function(){
     location.href="http://{{ip}}:8000/index_userinfo";
     });
    }); 
    </script>
<script type="text/javascript">
  $(document).ready(function(){ 
  $("#btn_checkinfo").click(function(){
   location.href="http://10.229.191.65:8000/index_checkinfo?p1=-1";
   });
  }); 
  </script>
<script type="text/javascript">
    $(document).ready(function(){ 
    $("#btn_add").click(function(){
     location.href="http://{{ip}}:8000/share";
     });
    }); 
    </script>
<script type="text/javascript">
    $(document).ready(function(){ 
    $("#btn_admin").click(function(){
     location.href="http://{{ip}}:8000/admin";
     });
    }); 
    </script>
<script>
    var url = 'http://{{ip}}:8000/deviceinfo';
    var columns = [
        {   field: 'id',
            title: 'ID号',
            sortable:true //设置ID列可以排序
        }, {
            field: 'device_name',
            title: '设备名称',
        }, {
            field: 'status',
            title: '设备状态'
        }, {
            field: 'model',
            title: '设备型号'
        },{
            field: 'domain',
            title: '设备域名'
        },{
            field: 'mgt_address',
            title: '设备管理地址'
        },{
            field: 'user',
            title: '设备用户'
        },{
            field: 'owner',
            title: '责任人'
        },
    ];
    $("#table").bootstrapTable({
        locale: 'zh-CN',
        toolbar: '#toolbar',                //自定义工具按钮
        url: url,                           //请求后台的URL（*）
        method: 'get',                      //请求方式（*）
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 20, 50, 100, 'All'], //可供选择的每页的行数（*）
        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                      //初始化加载第一页，默认第一页
        search: true,                       //是否显示表格搜索
        showColumns: true,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        height: 550,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
        columns: columns,                   //列参数
        detailView: false,                   //是否显示父子表
        sortName: 'id',
        sortable: true,
        sortOrder: 'desc',
        showExport: true,               //显示导出按钮
        exportDataType: 'basic',          //'basic':当前页的数据, 'all':全部的数据, 'selected':选中的数据
        maintainSelected :true,

        //展开行事件
        onExpandRow: function (index, row, $detail) {
            zi_table(index, row, $detail); //回调函数
        },
    });
    
    function getCookie(name) {
    	let cookieValue = null;
    	if (document.cookie && document.cookie !== '') {
        	const cookies = document.cookie.split(';');
        	for (let i = 0; i < cookies.length; i++) {
            	const cookie = cookies[i].trim();
            	// Does this cookie string begin with the name we want?
            	if (cookie.substring(0, name.length + 1) === (name + '=')) {
                	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                	break;
            	}
        	}
    	}
    	return cookieValue;
	}
	const csrftoken = getCookie('csrftoken');

    function getInfo(){
      var rows = $('#table').bootstrapTable('getSelections');
      var html = rows[0].id + rows[1].id;
      location.href="http://{{ip}}:8000/link_add/?id1=" + rows[0].id +"&id2=" + rows[1].id;
      
      
    }

    //定义子表函数
    function zi_table(index, row, $detail) {
        var fzr_table = $detail.html('<table></table>').find('table');
        $(fzr_table).bootstrapTable({
            url: url,
            columns: columns,
        })
    }
</script>

{% if messages %}
    
    <script>
            {% for msg in messages %}
                alert('{{ msg.message }}');
            {% endfor %}
    </script>
    {% endif %}

</html>

```
