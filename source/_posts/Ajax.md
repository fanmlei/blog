---
title: Ajax
date: 2018-05-04 12:12:57
categories: 
- 前端
tags:
- jQuery
- 网络请求
---
## Ajax
AJAX即Asynchronous JavaScript and XML (异步的JavaScript和XML)，一种创建交互式网页应用的网页开发技术方案。之前我们在页面进行操作的时候往往会导致整个页面进行刷新，这样的体验往往不是很好，使用ajax发送请求的时候可以在后台处理请求和响应，例如在用户登录的时候提示用户当前输入的用户名是否正确，或者验证密码等等操作。
### 原生Ajax
原生的ajax是基于XmlHttpRequest对象进行操作的，因此要使用原生ajax先来看看XmlHttpRequest对象的主要方法和属性：
- 方法：
``` javascript
   用于创建请求
    
   参数：
       method： 请求方式（字符串类型），如：POST、GET、DELETE...
       url：    要请求的地址（字符串类型）
       async：  是否异步（布尔类型）
 
b. void send(String body)
    用于发送请求
 
    参数：
        body： 要发送的数据（字符串类型）
 
c. void setRequestHeader(String header,String value)
    用于设置请求头
 
    参数：
        header： 请求头的key（字符串类型）
        vlaue：  请求头的value（字符串类型）
 
d. String getAllResponseHeaders()
    获取所有响应头
 
    返回值：
        响应头数据（字符串类型）
 
e. String getResponseHeader(String header)
    获取响应头中指定header的值
 
    参数：
        header： 响应头的key（字符串类型）
 
    返回值：
        响应头中指定的header对应的值
 
f. void abort()
 
    终止请求</pre>
```
- 属性：
``` javascript
   状态值（整数）
 
   详细：
      0-未初始化，尚未调用open()方法；
      1-启动，调用了open()方法，未调用send()方法；
      2-发送，已经调用了send()方法，未接收到响应；
      3-接收，已经接收到部分响应数据；
      4-完成，已经接收到全部响应数据；
 
b. Function onreadystatechange
   当readyState的值改变时自动触发执行其对应的函数（回调函数）
 
c. String responseText
   服务器返回的数据（字符串类型）
 
d. XmlDocument responseXML
   服务器返回的数据（Xml对象）
 
e. Number states
   状态码（整数），如：200、404...
 
f. String statesText
   状态文本（字符串），如：OK、NotFound...
```

有了上面的知识我们来实现一个最简单的原生ajax请求

ajax_test.html:
``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <input type="button" value="test" onclick="ajax_test();">
    <script>
        function ajax_test() {
            var xhr = new XMLHttpRequest();
            xhr.open("POST",'/ajax_receive/',true);
            //设置请求头
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset-UTF-8');
            xhr.send("name=root;password=123");
        }
    </script>
</body>
</html>
```
ajax_receive处理函数：
``` python
def ajax_receive(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("l")
```
点击按钮后台运行结果：
```
[04/May/2018 15:20:21] "GET /ajax_receive/?t=1 HTTP/1.1" 200 2
<QueryDict: {'name': ['root'], 'password': ['123']}>
```

需要注意的是，使用原生ajax发送数据的时候必须要设置请求头，否则无法正常接收解析发送过来的数据

### JQuery的ajax
jquery的ajax也是基于XmlHttpRequest或者ActiveXObject的
- 常用参数及作用:
```
url：请求地址
type：请求方式，GET、POST（1.9.0之后用method）
headers：请求头
data：要发送的数据
contentType：即将发送信息至服务器的内容编码类型(默认: "application/x-www-form-urlencoded; charset=UTF-8")
async：是否异步
timeout：设置请求超时时间（毫秒）
beforeSend：发送请求前执行的函数(全局)
complete：完成之后执行的回调函数(全局)
success：成功之后执行的回调函数(全局)
error：失败之后执行的回调函数(全局)


accepts：通过请求头发送给服务器，告诉服务器当前客户端课接受的数据类型
dataType：将服务器端返回的数据转换成指定类型
    "xml": 将服务器端返回的内容转换成xml&#26684;式
    "text": 将服务器端返回的内容转换成普通文本&#26684;式
    "html": 将服务器端返回的内容转换成普通文本&#26684;式，在插入DOM中时，如果包含JavaScript标签，则会尝试去执行。
    "script": 尝试将返回值当作JavaScript去执行，然后再将服务器端返回的内容转换成普通文本&#26684;式
    "json": 将服务器端返回的内容转换成相应的JavaScript对象
    "jsonp": JSONP &#26684;式 使用 JSONP 形式调用函数时，如 "myurl?callback=?" jQuery 将自动替换 ? 为正确的函数名，以执行回调函数

converters： 转换器，将服务器端的内容根据指定的dataType转换类型，并传值给success回调函数
```
- 示例
``` html
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>

    <p>
        <input type="button" onclick="JqSendRequest();" value='Ajax请求' />
    </p>
    <script type="text/javascript" src="../static/js/jquery-1.11.0.min.js"></script>
    <script>

        function JqSendRequest(){
            $.ajax({
                url: "/ajax_receive/",
                type: 'GET',
                dataType: 'text',
                data:{"name":"root"},
                success: function(data){
                    alert(data)
                }
            })
        }
    </script>
</body>
</html>
``` 
接收函数
``` python
def ajax_receive(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("POST")
    if request.method == 'GET':
        print(request.GET)
        return HttpResponse("GET")
```

### 使用Ajax提交Form表单实现注册功能实例：

首先需要对form表单做一下调整：
``` html
<form id="register_form" onsubmit="return false">
    <h6>用户名</h6>
    <input type="text" placeholder="用户名" name="username" required="">
    <h6>邮箱</h6>
    <input type="text" class="email" placeholder="邮箱" name="Email">
    <h6>密码</h6>
    <input type="password" placeholder="密码" name="password">
    <h6>确认密码</h6>
    <input type="password" placeholder="确认密码" name="password">
    <div class="login-bottom">
        <input type="submit" value="注 册" onclick="login()">
        <div class="clear"></div>
    </div>
</form>
```
为了防止点击submit按钮的时候发生跳转，需要在form中添加 onsubmit="return false"参数，再去掉常用的action，method参数，最后再给submit按钮绑定点击事件，至此form表单完成
接下来就是js部分：
``` html
<script src="../../static/js/jquery-1.11.0.min.js"></script>
    <script type="text/javascript">
        function login() {
            $.ajax({
                //几个参数需要注意一下
                type: "POST",//方法类型
                dataType: "json",//预期服务器返回的数据类型
                url: "/iot/register",//url
                data: $('#register_form').serialize(),
                success: function (data) {
                    if (data['error'] == "OK"){
                        alert("注册成功")
                    }
                    else {
                        alert(data['error']);
                    }
                }

            });
        }
    </script>
```
data: 将form表单内容序列化一下，通过post方法发送请求，在回调函数里面显示提示信息。

view函数：
``` python
def register(request):
    res = {'error':None}
    if request.method == "POST":
        name = request.POST.get("username")
        email= request.POST.get("Email")
        password =request.POST.getlist("password")
        print(password)
        if password[0] != password[1]:
            res['error'] = "两次密码不同，请重新填写"
        else:
            res['error'] = 'OK'
        return HttpResponse(json.dumps(res),content_type="application/json")
```
通过getlist方法获取列表多个值，判断两个密码是否相同，并把结果一json格式发送给前端。
