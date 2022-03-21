<h3 id="EMQ%EF%BC%9A">EMQ：</h3>

<p style="text-indent:50px;">现有的MQTT服务器有很多，例如Mosquitto、Apache-Apollo、EMQ等等，最后呢选择了EMQ毕，国内公司的开源产品，中文资料相对要多一些。EMQ的官网宣称是百万级分布式开源物联网MQTT消息服务器，百不百万倒无所谓，反正是给自用的没有那么多的数据产生。</p>

<h3 id="%E5%AE%89%E8%A3%85%EF%BC%9A">安装：</h3>

<p style="text-indent:50px;">服务器系统版本为Ubuntu14.04，首先在EMQ官网下载对应的安装包<a href="http://emqtt.com/downloads/latest/ubuntu14_04-deb">http://emqtt.com/downloads/latest/ubuntu14_04-deb</a>，进入目录 输入命令：sudo dpkg -i emqttd-ubuntu16.04_v2.0_amd64.deb进行安装。按照官方的说明完成上述操作之后还需要安装依赖lksctp-tools库apt-get install lksctp-tools。至此MQTT服务已经搭建好了，但是还需要一些配置方可使用。</p>

<h3 id="%E9%85%8D%E7%BD%AE%EF%BC%9A">配置：</h3>

<p style="text-indent:50px;">EMQ提供了Web 管理控制台，默认是开启的，URL 地址: <a href="http://localhost:18083/">http://localhost:18083</a> ，缺省用户名/密码: admin/public。登陆成功之后就能可查询 EMQ 消息服务器基本信息、统计数据、度量数据，查询系统客户端(Client)、会话(Session)、主题(Topic)、订阅(Subscription)，以及对插件的管理。</p>

<p style="text-indent:50px;">插件里面我觉得最重要的应该是认证插件，当然了是可以不需要认证功能的，但是呢安全性和规范性还是需要认证功能的，EMQ提供了很种方式的认证功能，我选择MySQL认证访问插件。</p>

<p style="text-indent:50px;">进入到插件管理页面，打开MySQL配置，第一步填写 MySQL数据库的相关信息，还需要注意一下要把加密方式给去掉，这样连接的时候要方便一些。完成这些配置之后要到MySQL对应的数据库创建用户和访问控制表：</p>

<pre class="has">
<code class="language-sql">CREATE TABLE `mqtt_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `salt` varchar(35) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mqtt_username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;</code></pre>

<pre class="has">
<code class="language-sql">CREATE TABLE `mqtt_acl` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `allow` int(1) DEFAULT NULL COMMENT '0: deny, 1: allow',
  `ipaddr` varchar(60) DEFAULT NULL COMMENT 'IpAddress',
  `username` varchar(100) DEFAULT NULL COMMENT 'Username',
  `clientid` varchar(100) DEFAULT NULL COMMENT 'ClientId',
  `access` int(2) NOT NULL COMMENT '1: subscribe, 2: publish, 3: pubsub',
  `topic` varchar(100) NOT NULL DEFAULT '' COMMENT 'Topic Filter',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `mqtt_acl` (`id`, `allow`, `ipaddr`, `username`, `clientid`, `access`, `topic`)
VALUES
    (1,1,NULL,'$all',NULL,2,'#'),
    (2,0,NULL,'$all',NULL,1,'$SYS/#'),
    (3,0,NULL,'$all',NULL,1,'eq #'),
    (5,1,'127.0.0.1',NULL,NULL,2,'$SYS/#'),
    (6,1,'127.0.0.1',NULL,NULL,2,'#'),
    (7,1,NULL,'dashboard',NULL,1,'$SYS/#');</code></pre>

<p style="text-indent:50px;">为了测试方便先在用户表里面插入一个测试账户信息，例如username：admin 、password：123456，至此认证功能基本上配置好了。</p>

<h3 id="%E6%B5%8B%E8%AF%95%EF%BC%9A">测试：</h3>

<p style="text-indent:50px;">现在还没有完成硬件部分的设计，只能通过EMQ提供的Websocket工具来测试连通性，打开websocket页面，填写好之前在用户表里面的账户和密码，点击连接测试能否连接成功，如果成功了那么整个MQTT服务的搭建也就顺利完成了。</p>

<p style="text-indent:50px;"> </p>

<p style="text-indent:50px;"> </p>