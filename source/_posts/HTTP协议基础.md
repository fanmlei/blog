## HTTP协议基础
**总结于图解HTTP协议**


### 什么是URI和URL？

URI（统一资源标识符）表示的是某一个互联网资源， URL（统一资源定位符）相交于URI我们对于URL要更为熟悉一些，我们在浏览器上输入的网站地址其实就是一个URL 例如：http://www.google.com ，URL表示的是资源的地点，所以呢URL是URI的一个子集，URI中包含URL的。

用一个形象点的例子来说明URI和URL的区别：我们每一个人都有身份证，每一个人的身份证号都是不同的，可以根据这个号码来找到这个唯一的人，这就相当于URI，而URL呢则类似于身份证上的地址信息，例如（某某省/某某市/某某区/某某街道/某某门牌号/姓名）通过这个地址我们也能找到这个人。

### URI格式

绝对URI格式
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305020813962.png)
一个绝对的URI包含了

1. 协议名
   - 使用 http: 或 https: 等协议方案名获取访问资源时要指定协议类型。不区分字母大小写，最后附一个冒号
2. 认证信息（可选）
   - 指定用户名和密码作为从服务器端获取资源时必要的登录信息
3. 服务器地址
   - 使用绝对 URI 必须指定待访问的服务器地址。地址可以是类似google.com 这种 DNS 可解析的名称，或是 192.168.1.1 这类 IPv4 地址名，还可以是 [0:0:0:0:0:0:0:1] 这样用方括号括起来的 IPv6 地址名。
4. 服务器端口号（可选）
   - 指定服务器连接的网络端口号。此项也是可选项，若用户省略则自动使用默认端口号。
5. 带层次的文件路径
   - 指定服务器上的文件路径来定位特指的资源。这与 UNIX 系统的文件目录结构相似。
6. 查询字符串（可选）
   - 针对已指定的文件路径内的资源，可以使用查询字符串传入任意参数。
7. 片段标识位（可选）





### HTTP协议用于客户端和服务器端之间的通信

在应用HTTP协议的时候必定一端为客户端而另一端为服务端角色，客户端通过请求，服务器端反馈响应实现两者之间的通信（请求必定是客户端发送的，服务器端在没有接收到请求的时候是不能发送响应的）

- 发送请求

  一个简单的请求报文内容

  ```http
  GET /index.html HTTP/1.1
  Host: baidu.com
  Connection: keep-alive
  ```

  起始行首先声明了请求访问服务器的类型为GET ， 随后的字符串`/index.html`指明了请求访问的资源对象，最后是HTTP协议的版本号

  下面的是请求首部字段，这里面通常会有Host、Connection、Content-Type等等，除了这些可能还会包含内容实体用于发送请求的数据

- 返回响应

  ```http
  HTTP/1.1 200 OK
  Date: Mon, 04 Mar 2019 07:34:18 GMT
  Content-Type: text/html
  
  <html>
  </html>
  ```

  同样的在第一行中HTTP/1.1 表示了服务器对应的HTTP版本， 200 OK表示请求的处理结构的状态码和原因短语，第二行显示了创建响应的日期和时间，接着空一行，之后的就是响应的资源实体了

- **HTTP协议是不保存状态的协议**

  HTTP本身是无状态的协议，自身不会对请求和响应之间的通信状态进行保存，但是往往我们在浏览网页的时候进行页面跳转需要保留我们的登陆信息以便服务器知道每次请求是谁发送的，所以就有了Cookie技术

- **使用Cooke实现状态管理**

  Cookie技术通过在请求和响应报文中写入Cookie信息来实现对客户端的状态的控制

  首先Cookie会根据服务器端响应报文内的set-cookie字段信息通知客户端保存cookie，下次客户端再请求的时候将接收到的cookie值添加到请求报文中发出

  客户端在接收到携带有cookie的请求后会根据cookie值和服务器上的记录进行比对以此来确定客户端的状态

  - 没有cookie时候的请求报文

    ```http
    GET /index.html HTTP/1.1
    Host: baidu.com
    ```

  - 服务器接收到没有cookie的响应返回

    ```http
    HTTP/1.1 200 OK
    Date: Mon, 04 Mar 2019 07:34:18 GMT
    Content-Type: text/html
    ＜Set-Cookie: sid=1342077140226724; path=/; expires=Mon, 04 Mar 2019 07:34:18 GMT＞
    
    <html>
    </html>
    ```

  - 客户端携带cookie发送请求

    ```http
    GET /index.html HTTP/1.1
    Host: baidu.com
    Cookie: sid=1342077140226724
    ```

- **更进一步：session的使用**

  session的应用是基于cookie的，cookie无法存储复杂的数据，这时候就需要用到session来实现，session保存于服务器端类似以key-value结构，其中key值可以使用cookie存放，每次请求过来时候服务器端可以通过cookie值去session中获取对应的用户信息，以此记录控制客户端的状态（cookie存放在客户端中，session保存于服务器端）

- **http请求方法**

  - GET：获取资源

  - POST：传输实体主体

  - PUT：传输文件

  - DELETE：删除文件

  - HEAD：获取报文首部

  - OPTIONS：询问支持的方法

    响应报文

    ```http
    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    ```

  - TRACE：追踪路径，让服务器端将之前的请求通信环回给客户端（可以用来查询请求是如何加工或者传递到服务器端的）

  - CONNECT: 使用隧道协议连接代理

    CONNECT 方法要求在与代理服务器通信时建立隧道，实现用隧道协议进行 TCP 通信。主要使用 SSL（Secure Sockets Layer，安全套接层）和 TLS（Transport Layer Security，传输层安全）协议把通信内容加 密后经网络隧道传输。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305020900941.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)
- 长连接

  在早期的http协议中，每次通信就需要断开TCP连接，随着时代的发展一个页面可能需要请求很多次，这样一来就会不断的断开连接增加通信的开销，所以在1.1和部分1.0版本中出现了持久连接，只要一端没有明确提出断开连接，那么就会保持TCP的连接状态

- HTTP报文内的HTTP信息

  HTTP报文大致可分为报文首部+报文主体两块，两者通过（CR+LF）来划分
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305020933712.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)

- 获取部分内容的范围请求

  执行范围请求的时候，请求体的首部字段Range需要用来指定资源的byte范围

  ```http
  GET /index.html HTTP/1.1
  Range: bytes=5001-10000   请求50001-10000字节内容
  Range: bytes=5001-        请求5001之后的所有内容    
  Range: bytes=-3000, 6000-7000   请求前3000字节和6000-7000字节内容的多重范围
  ```

  范围请求的响应会返回状态码为206 Partial Content的响应报文，多重范围响应会在首部字段Content-type标明multipart/byteranges，如果服务器不支持范围请求那么会返回200 OK和全部实体内容



### HTTP状态码
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305021012587.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)
- 2XX成功   （服务器返回2XX表明请求被正常处理了）

  - 200 OK

    表示客服端发送的请求被服务器端正常处理了

  - 204 No Content

    表示客服端发送的请求被服务器端正常处理了，但是在返回的响应报文中不包含实体部分

  - 206 Partial Content

    就是上面说的范围请求响应

- 3XX重定向  （浏览器需要执行某些其他的处理才能服务器端才能正常处理请求）

  - 301 Moved Permanently

    永久性的重定向，表明改请求资源的URI发生更改了，需要请求新的URI

  - **302 Found**

    临时重定向，和上面的不同，服务器希望本次使用新的URI进行访问，只是临时性的

  - 303 See Other

    表示请求的资源存在另一个URI，应该使用GET方法请求该资源，例如使用POST方法访问某个资源，但是服务器处理的结果是希望客户端使用GET方法来请求这个资源

  - 304 Not Modified

    该状态码表示客户端使用GET方法并且请求报文中包含 If-Match，If-ModifiedSince，If-None-Match，If-Range，If-Unmodified-Since 中任一首部，服务器端允许请求访问资源，但未满足条件的情况。304 状态码返回时，不包含任何响应的主体部分。

  - 307 Temporary Redirect

    临时重定向和302相同，但是禁止POST变成GET

- 4XX 客户端错误 （客服端发送的请求服务器无法正确处理）

  - **400Bad Request**

    请求报文中存在语法错误

  - 401 Unauthorized

    需要通过HTTP认证才可访问（BASIC认证、DIGEST认证）

  - **403 Forbidden**

    这次请求被服务器拒绝了

  - **404 Not Found**

    服务器无法找到此次请求的资源

- 5XX 服务器错误

  - **500 Internal Server Error**

    服务器处理请求是发生错误

  - 503 Service Unavailable

    服务器超载，无法处理请求



### WEB服务器

- 在一台主机上部署多个web站点

  在HTTP/1.1协议规范中允许一台服务器搭建多个web网站，假如一台服务器中绑定了www.baidu.com和www.google.com 两个域名的时候，我们输入这两个域名的时候都会解析到同一个IP地址上，这个时候如果想要区分用户请求的是那个域名就必须在请求首部Host指定域名。

- 代理服务器

  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305021046421.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)

  代理服务器最基本的功能就是接受客户端的请求，并将请求转发给其他的服务器，代理并不会改变请求的URL，会直接将请求进行转发，每次通过代理服务器转发请求的或者响应的时候都会在首部添加Via信息，最常见的代理服务就是我们使用的翻墙服务。

  代理服务还细分为正向代理和反向代理，通俗来说正向代理是针对于客户端（服务器端并不知道客户端的真实信息），反向代理是针对于服务器端（客户端不知道服务器端的实际地址）

  

  正向代理的作用：

  1. 翻墙（访问客户端无法访问的资源）
  2. 缓存，加速访问速度
  3. 对外隐藏真实的客户端信息

  反向代理的作用：

  1. 保证内网的安全
  2. 负载均衡

- 网关

  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305021103779.png)

  网关和代理的作用很类似，但是网关能够实现非HTTP协议的服务，利用网关可以提高通信的安全性。

- 隧道

  ![在这里插入图片描述](https://img-blog.csdnimg.cn/2019030502111797.png)

  在客户端和服务器端建立一条加密的通信线路，确保客户端和服务器端的安全通信，隧道本身不会解析HTTP请求，会原样将请求转发给服务器。



### HTTP首部

之前提到过一个HTTP的报文主要分为首部和主体两个部分，主体部分不是客户端和服务器端根据操作生成的所以没有办法去介绍，在此只介绍部分常见的首部字段的作用和用法。

下图是分别是请求报文和响应报文的首部构成：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305021127721.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)

字段结构：**字段名：字段值1, 字段值2....**

报文首部主要分为以下四个部分： 

1. 通用首都字段
2. 实体首部字段
3. 请求实体字段
4. 响应实体字段

**常见字段一览**

- 通用首部字段

  | 字段名            | 说明                       |
  | ----------------- | -------------------------- |
  | Cache-Control     | 控制缓存行为               |
  | Connection        | 逐跳首部、连接的管理       |
  | Date              | 创建报文的时间和日期       |
  | Pragma            | 报文指令                   |
  | Trailer           | 报文末端的首部一览         |
  | Transfer-Encoding | 指定报文主体的传输编码方式 |
  | Upgrade           | 升级为其他协议             |
  | Via               | 代理服务器相关信息         |
  | Warning           | 错误通知                   |

- 实体首部字段

  | 字段名           | 说明                         |
  | ---------------- | ---------------------------- |
  | Allow            | 资源可支持的HTTP方法         |
  | Content-Encoding | 实体主体适用的编码方式       |
  | Content-Language | 实体主体的自然语言           |
  | Content-Length   | 实体主体的大小（单位：字节） |
  | Content-Location | 替代对应资源的URI            |
  | Content-MD5      | 实体主体的报文摘要           |
  | Content-Range    | 实体主体的范围位置           |
  | Content-Type     | 实体主体的媒体类型           |
  | Expires          | 实体主题过期的日期和时间     |
  | Last-Modified    | 资源的最后修改日期和时间     |

- 请求首部字段

  | 字段名              | 说明                                          |
  | ------------------- | --------------------------------------------- |
  | Accept              | 用户代理可处理的媒体类型                      |
  | Accept-Charset      | 优先的字符集                                  |
  | Accept-Encoding     | 优先的内容编码                                |
  | Accept-Language     | 优先的自然语言                                |
  | Authorization       | Web认证信息                                   |
  | Expect              | 期待服务器的特定行为                          |
  | From                | 用户的电子邮箱地址                            |
  | Host                | 请求资源所在服务器                            |
  | If-Match            | 比较实体标记（ETag)                           |
  | If-Modified-Since   | 比较资源的更新时间                            |
  | If-None-Match       | 比较实体标记（与If-Match想法）                |
  | If-Range            | 资源为更新时发送实体Byte的范围请求            |
  | If-Unmodified-Since | 比较资源的更新时间（与If-Modified-Since相反） |
  | Max-Forwards        | 最大传输逐跳数                                |
  | Proxy-Authorization | 代理服务器要求客户端的认证信息                |
  | Range               | 实体的字节范围请求                            |
  | User-Agent          | HTTP客户端程序的信息                          |

- 响应首部字段

  | 字段名             | 说明                         |
  | ------------------ | ---------------------------- |
  | Accept-Ranges      | 是否接收字节范围请求         |
  | Age                | 推算资源创建经过的时间       |
  | Etag               | 资源的匹配信息               |
  | Location           | 命令客户端重定向至指定URI    |
  | Proxy-Authenticate | 代理服务器对客户端的认证信息 |
  | Retry-After        | 对再次发送请求的时机要求     |
  | Server             | HTTP服务器安装信息           |
  | Vary               | 代理服务器缓存的管理信息     |
  | WWW-Authenticate   | 服务器对客户端的认证信息     |



