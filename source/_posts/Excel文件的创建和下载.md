---
title: Excel文件的创建和下载
date: 2018-08-07 19:42:49
categories: 
- Python
tags:
- 文件处理
- Django
- Excel
---

简述：利用xlwt和django将table内的数据转换为excel文件下载到本地保存

### 生成Excel文件
使用了 xlwt 库，xlwt库可以将数据和格式信息写入到Excel文件中，具体步骤如下
1. 创建Excel文件首先需要实例化 Workbook 对象
```
class   <code>xlwt.Workbook.</code><code>Workbook(</code>encoding ='ascii'，style_compression = 0 )
#有两个参数 encoding→文件编码格式    style_compression → 是否压缩 ，一般情况下使用默认参数即可。
```
2. 通过Workbook的add_sheet方法创建工作表
```
add_sheet (sheetname, cell_overwrite_ok=False)
sheetname→工作表名称   cell_overwrite_ok 重复写入同一个单元格是否覆盖原有内容，通过源码中发现当我们调用这个  方法的时候实际上得到的返回结果为一个Worksheet实例化对象
```
```python
def add_sheet(self, sheetname, cell_overwrite_ok=False):
    """
    This method is used to create Worksheets in a Workbook.

    :param sheetname:

      The name to use for this sheet, as it will appear in the
      tabs at the bottom of the Excel application.

    :param cell_overwrite_ok:

      If ``True``, cells in the added worksheet will not raise an
      exception if written to more than once.

    :return:

      The :class:`~xlwt.Worksheet.Worksheet` that was added.

    """
    from . import Utils
    from .Worksheet import Worksheet
    if not isinstance(sheetname, unicode_type):
        sheetname = sheetname.decode(self.encoding)
    if not Utils.valid_sheet_name(sheetname):
        raise Exception("invalid worksheet name %r" % sheetname)
    lower_name = sheetname.lower()
    if lower_name in self.__worksheet_idx_from_name:
        raise Exception("duplicate worksheet name %r" % sheetname)
    self.__worksheet_idx_from_name[lower_name] = len(self.__worksheets)
    self.__worksheets.append(Worksheet(sheetname, self, cell_overwrite_ok))
    return `self.__worksheets[-1]
```
3. 往单元格里面写入数据
通过Worksheet 的write方法写入数据write（r，c，label =''，style = <xlwt.Style.XFStyle object> ） r 、c参数为单元格的行列数  label需要写入的数据  style指定单元格的内容格式 通过xlwt.Style.easyxf()方法创建格式对象，包含字体、大小、颜色等
4. 保存
使用Workbook中的save方法保存，save方法提供两种保存方式：1.写入到本地磁盘  2.具有</code>write方法的流对象</p>

### Excel文件下载

Django提供有自带的文件下载功能，直接导入引用就可以了
```python
from django.http import FileResponse
file = open(name, 'rb')
response = FileResponse(file)
response['Content-Type'] = 'application/octet-stream'
response['Content-Disposition'] = 'attachment;filename=' + datetime.now().strftime("%Y-%m-%d") + name
return response
```

示例
```python
import xlwt


def write(data, name):
    wbx = xlwt.Workbook()
    sheet = wbx.add_sheet('Sheet1', cell_overwrite_ok=True)
    for row, i in enumerate(data):
        col = 0
        for j in i:
            sheet.write(row, col, i[j])
            col += 1
    wbx.save(name)
```