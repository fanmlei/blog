---
title: Django rest framework  认证组件源码分析
date: 2021-05-14 16:30:24
categories: 
- Django
tags:
- 源码
- Django
- DRF
cover: img/covers/rest_framework_auth.png
---
Django rest framework的认证组件是最常用的几个组件之一，内部实现并不复杂，通过源码可以了解Django是如何处理请求的，在认证的过程中组件帮我们实现了哪些功能，以及如何实现我们自己的认证方法。
<!--more-->
### 基础知识

想要弄清楚rest framework的执行过程首先需要明白Django中CBV和FBV执行流程，http请求最最本质的就是一个socket，一个请求过来第一步就是做路由匹配，在FBV中因为视图本身就是一个函数，所以直接调用函数就可以了，但是CBV中视图是一个类而在这个类里面是我们编写的视图函数，所以比FBV多了一步如何找到那个函数并且执行它。

CBV中是基于反射实现请求方式不同执行不同的方法，我们在使用CBV来实现的时候，通常都是在路由中使用as_view方法。<br />
```
url(r'^dashboard$', views.Dashboard.as_view())
```

这个方法存在于我们继承的父类View中，在as_view内部又会调用dispatch方法通过反射去找到对应的函数<br />
![](1.png)
![](2.png)

所以总得来说，在CBV中一个请求过来的具体流程：url  → view → as_view → dispatch
![](3.png)

### 源码分析

有了上面的基础接下来就比较容易理解了

首先在使用rest framework框架的时候 CBV不在是继承django的View了而是 rest framework的APIView，只是这个APIView也是继承django的View的，只不过是在原有的View中增加了很多功能而已，依然还是通过反射来实现的，所以跳过前面的内容直接到dispatch这部分

![](4.png)
![](5.png)

正式进入正题，restframework主要包含认证、解析器、分页和序列化四个大的部分，就对应上图框框内的几个部分，这几个部分流程大致相同，所以就以认证为例来具体说说他的流程

咱们接着上图继续往下一步一步走，首先会获取所有认证类的实例化对象。
![](6.png)

如果自己写的类里面没有认证类，就会到基类中继续寻找，默认使用rest framework的配置文件中的认证类
```
authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
```
拿到了认证所需要的类的对象，就继续返回到dispatch中，这时候request已经是增加内容了的request

返回dispatch之后回调用initial方法，在这个方法里面会执行所有之前我们添加的认证类、解析类
![](7.png)

initial方法里面跳转比较频繁，这里截图就重叠到一起方便看，经过一路的跳转最终是执行了request对象的_authenticate方法
![](8.png)

在_authenticate方法里面，会依次执行所有认证类的authenticate方法（由此我们也能知道如果我们想编写自己的认证类，那么认证部分需要放在authenticate方法里面），同时会将返回值赋值给request的user和auth属性<br />
![](9.png)

所以rest framework的认证流程总得来说就是
![](10.png)