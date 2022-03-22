---
title: Django支付宝自动转账功能（一）
date: 2018-08-11 10:20:45
categories: 
- Django
tags:
- 支付
---
首先说明一下最终实现的效果：===》用户上传excel文件====》网页端显示读取文件并显示预览效果====》上传文件至服务器，服务器后台开始调用接口自动转账===》所有转账信息存储到数据库中，失败信息返回到网页上。

上一篇已经大致将支付接口实现了，这一篇将介绍如何和Django后台连接起来使用，在项目中使用的是excel文件储存转账信息的，所以我们首先需要了解如何读取Excel文件，然后才是进行转账操作，django则是提供网页服务，接收用户上传excel文件，保存交易信息等等。

1.网页端的预览：选择上传文件后需要将文件内容读取并显示出来，方便确认信息是否有误后在上传，这里主要是通过JS读取文件内容，然后再把数据以表格的形式展现出来。这里用到了一个一个xlsx插件
```javascript
//文件读取
<script src="http://oss.sheetjs.com/js-xlsx/xlsx.full.min.js"></script>
<script>
    /*
    FileReader共有4种读取方法：
    1.readAsArrayBuffer(file)：将文件读取为ArrayBuffer。
    2.readAsBinaryString(file)：将文件读取为二进制字符串
    3.readAsDataURL(file)：将文件读取为Data URL
    4.readAsText(file, [encoding])：将文件读取为文本，encoding缺省值为'UTF-8'
    */
    var wb;//读取完成的数据
    var rABS = false; //是否将文件读取为二进制字符串
 
    function importf(obj) {//导入
        if (!obj.files) {
            return;
        }
        var f = obj.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            var data = e.target.result;
            if (rABS) {
                wb = XLSX.read(btoa(fixdata(data)), {//手动转化
                    type: 'base64'
                });
            } else {
                wb = XLSX.read(data, {
                    type: 'binary'
                });
            }
            //wb.SheetNames[0]是获取Sheets中第一个Sheet的名字
            //wb.Sheets[Sheet名]获取第一个Sheet的数据
            document.getElementById("preview").innerHTML = XLSX.utils.sheet_to_html(wb.Sheets[wb.SheetNames[0]]);
 
        };
        if (rABS) {
            reader.readAsArrayBuffer(f);
        } else {
            reader.readAsBinaryString(f);
        }
    }
 
    function fixdata(data) { //文件流转BinaryString
        var o = "",
            l = 0,
            w = 10240;
        for (; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
        return o;
    }
</script>
```
HTML部分
```html
<form method="post" action="" id="upload_form" enctype="multipart/form-data">
  <div style="height: 40px;">
  <input id="uploadFile" type="file" onchange="importf(this)" style="display: inline-block;"name="payment"/>
   <button id="upload" style="height: 32px">上传文件</button>
  </div>
  <div style="border: 1px solid #3b8fc5;border-radius: 5px;height: 500px;position: relative;overflow: auto;text-align:center;vertical-align: middle;"id="preview">
     <p style="color: #c1c1c1">文件预览</p>
   </div>
</form>
```
最终效果
![](1.png)

2.Excel文件上传和保存：通过Ajax提交form表单数据到后台，Ajax操作没什么可说的了，需要注意的是form 的enctype属性值，来看一下W3C上面的介绍
![](2.png)
![](3.png)

因此我们在上传文件的时候要用enctype="multipart/form-data"
前端发送文件了接下来就是后端接收文件了，文件数据会包含在request.FILES里面（注意，只有当request方法为POST并且form 的enctype属性值为multipart/form-data的时候request.FILES才会有数据
request.FILES中包含下面几个属性：name(文件名)、size(文件大小)、content_type(文件类型)、read()读取整个文件、chunks()返回一个生成器对象
```python
file = request.FILES.get('payment', None)
f = open(file.name, 'wb')
for chunck in file.chunks():
    f.write(chunck)
f.close()
```
至此文件就保存下来了，文件名就是上传的文件名，路径默认为根路径
