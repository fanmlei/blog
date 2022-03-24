---
title: Python实现支付宝转账接口
date: 2018-07-31 02:21:08
categories: 
- Python
tags:
- 支付
---
<p>由于工作需要使用python开发一个自动转账接口，记录一下开发过程。</p>

<p>首先需要在蚂蚁金服上申请开通开发者账户，有了开发者账户就可以使用沙箱进行开发了。<br />
在开发之前我们需要在沙箱应用中填写密钥，密钥的获取可以使用阿里提供的工具包自动生成。<br /><img alt="" class="has" height="201" src="https://img-blog.csdn.net/20180731144831401?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="581" /></p>

<p>前期准备工作完成了，接下来是编写代码部分。主要用到了python-alipay-sdk库，使用pip安装即可，如果安装的过程中遇到问题推荐使用Anaconda（crypto这个库安装了我好久没成功，最后换成Anaconda环境了）</p>

<pre class="has">
<code class="language-python">from datetime import datetime
from alipay import AliPay


class Payment():
    def __init__(self, appid, url):
        '''
        支付接口初始化
        :param appid: 商户appid
        :param url: 支付宝接口url
        '''
        self.app_private_key_string = open("app_private_key.txt").read()  # 应用私钥（默认从两个TXT文件中读取）
        self.alipay_public_key_string = open("alipay_public_key.txt").read()  # 支付宝公钥
        self.alipay = AliPay(
            appid=appid,
            app_notify_url=url,
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type="RSA2",
            debug=True
        )</code></pre>

<p>初始化的时候需要用到appid、应用私钥以及支付宝公钥，appid和支付宝公钥可在沙箱应用中看到，应用私钥则需要在刚刚生成密钥工具包的目录下查看<br /><img alt="" class="has" height="239" src="https://img-blog.csdn.net/20180731145729605?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="663" /><br />
获取两个密钥之后可以单独写入到两个TXT文件中然后读取文件内容来获取，以便以后的更改，在写入TXT文件的过程中不能只是单纯的将密钥复制过去，需要再第一行和最后一行加入</p>

<pre class="has">
<code>-----BEGIN PUBLIC KEY-----
你的密钥
-----END PUBLIC KEY-----</code></pre>

<p>要不然会出现这个错误<br /><img alt="" class="has" height="134" src="https://img-blog.csdn.net/20180731150110977?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="884" /><br />
第一次接触这玩意，不知道具体的格式，找了好久的问题，最后在源码的这个地方发现了问题，必须以这个开头<br /><img alt="" class="has" height="471" src="https://img-blog.csdn.net/20180731150457627?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="690" /></p>

<p>公共请求参数部分至此就完成了，接下来就是请求参数了，按照开发文档上有四个是必须的：out_biz_no、payee_type、payee_account、amount  对应的意思分别是：商户转账唯一订单号、收款方账户类型、收款方账户、转账金额。还有部分参数是可选的，在下面的代码中交代了。</p>

<pre class="has">
<code class="language-python">    def pay(self, payee_account, amount, payee_real_name=None, remark=None, payer_show_name=None,
            payee_type="ALIPAY_LOGONID"):
        '''
        发起转账
        :param payee_account: 收款方账户
        :param amount: 转账金额
        :param payee_real_name:
        :param remark: 收款方姓名
        :param payer_show_name: 转账备注
        :param payee_type: 付款方姓名
        :return:
        '''
        result = self.alipay.api_alipay_fund_trans_toaccount_transfer(
            datetime.now().strftime("%Y%m%d%H%M%S"),
            payee_type=payee_type,  # 收款方账户类型
            payee_account=payee_account,  # 收款方账户
            amount=amount,  # 转账金额
            payee_real_name=payee_real_name,  # 收款方姓名（可选，若不匹配则转账失败）
            remark=remark,  # 转账备注
            payer_show_name=payer_show_name  # 付款方姓名

        )
        # result={'code':'10000','msg':'Success','order_id': '','out_biz_no': '',  'pay_date': '2017-06-26 14:36:25'}
        # 接口文档：https://docs.open.alipay.com/api_28/alipay.fund.trans.toaccount.transfer

        if result['code'] == '10000':
            if result['msg'] == "Success":
                print("转账成功" + "  交易单号：" + result["order_id"])

        else:
            print(result)
            print(result['sub_msg'])</code></pre>

<p>到这这个代码的基础部分就此完成：</p>

<p><img alt="" class="has" height="65" src="https://img-blog.csdn.net/20180731151105400?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="477" /></p>
