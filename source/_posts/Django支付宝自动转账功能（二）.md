---
title: Django支付宝自动转账功能（二）
date: 2018-08-12 10:20:45
categories: 
- Django
tags:
- 支付
---

接着上一篇的介绍，这部分将介绍如何读取上传的文件并调用转账接口实现转账功能。
具体步骤  ===》打开文件  ===》读取每一行的数据 ===》调用支付宝单笔转账接口

1.Excel文件的读取
python读取excel文件需要用到xlrd这个库，这个库的具体用法这里就不说了，主要介绍一下读取excel文件的步骤：
1. 使用xlrd.open_workbook(path)打开文件
2. 遍历文件中所有的sheet，并且读取所有行数据
```python
for sheet in ExcelFile.sheet_names():
    data = ExcelFile.sheet_by_name(sheet)
    i = 0
    while i &lt; (data.nrows):
        yield data.row_values(i)
        i += 1
```
为了防止文件过大占有太多内存，没有一次将所有数据都读取出来，而是使用生成器返回一个迭代对象，每次调用这个迭代对象来取出数据。

```
f = read_excel('../files/2018.7.30(1).xls')
for i in f:
    print(i)
```
运行结果：
![](1.png)

2.调用转账接口：
接口部分我们之前已经说过了，现在只需要将excel中的数据传递进去就能够实现转账功能了，为了不单单只是在后台打印交易信息，对之前的pay方法做一些调整
```python
data = {'payee_account': None, 'amount': None, 'payee_real_name': None, 'remark': None, 'order_id': None,
        'out_biz_no': None, 'pay_date': None, 'status': None}
if result['code'] == '10000':
    if result['msg'] == "Success":
        print(payee_account + "  转账成功" + "  交易单号：" + result["out_biz_no"])
    data['payee_account'] = payee_account
    data['amount'] = amount
    data['payee_real_name'] = payee_real_name
    data['order_id'] = result['order_id']
    data['out_biz_no'] = result['out_biz_no']
    data['pay_date'] = result['pay_date']
    data['status'] = '转账成功'
    return data
else:
    print(payee_account, amount, result['sub_msg'], result["out_biz_no"])
    data['payee_account'] = payee_account
    data['amount'] = amount
    data['payee_real_name'] = payee_real_name
    data['out_biz_no'] = result['out_biz_no']
    data['status'] = result['sub_msg']
    # error = [payee_account, amount, payee_real_name, result['sub_msg'], result['out_biz_no']]
    return data
```
方便起见将excel文件读取和转账接口封装到一个函数里面了，现在只需要传递文件路径就能直接转账了，数据库写入就不详细说了。
```python
def run(path):
    file = read_excel(path)
    pay = Payment(*******)
    data = []
    error = []
    for item in file:
        res = pay.pay(item[1], item[0], item[3], item[2])
        res['remark'] = item[4]
        data.append(res)
        if res['status'] != '转账成功':
            error.append([res['payee_account'], res['amount'], res['payee_real_name'], res['remark'], res['status'],
                          res['out_biz_no']])
            # except Exception as e:
            #     pass
    write(data)  # 写入数据库
    return error  # 网页返回错误信息
```

3.网页显示失败信息：
这一步没什么好说的了，我是直接使用django的render函数将错误信息渲染完成之后返回了一个新的页面。其实用Ajax接收数据然后js来渲染页面这种做法要好一些。
