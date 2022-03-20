<p>configparser是python中自带的一个配置文件读写的库，python2中为ConfigParser在python3中更名为configparser，首先我们建立一个test.ini的配置文件，内容如下：</p><pre class="python">[device]
port=COM9
baud_rate=9600</pre><h5>读操作：</h5><p>实例：</p><pre class="python">import configparser
cf=configparser.ConfigParser()
cf.read("test.ini")
print(cf.sections())
print(cf.options("device"))
print(cf.items("device"))
print(cf.get("device","port"))</pre><p>首先导入configparser模块，再使用read方法读取配置文件内容。<br /></p><p>sections()方法返回文件中所有section<br /></p><p>options(section_name)方法返回该section_name下所有的option<br /></p><p>items(section_name)方法以元祖的格式返回该section_name下的所有option的key和value<br /></p><p>get(section_name, option_name)方法只返回key<br />运行结果<br /></p><p></p><p><img src="https://img-blog.csdn.net/20180501224730635?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt="" /></p><h5>写操作：<br /></h5><p>实例：</p><pre class="python">cf.add_section("section1")
cf.set('section1','key1','value1')
cf.write(open("test.ini",'w'))

print(cf.sections())
print(cf.items("section1"))</pre><p>add_section(new_section_name)：新建一个section，如果已存在会报错。<br /></p><p>set(section_name, option_name, value): 如果option_name存在则更新value，如果不存在则新建一个option和value，但是如果section不存在会报错。<br />write(）方法将内容重新写入到文件中，需要注意的是如果在写之前没有读去过这个文件那么这次写入将会导致之前的文件内容被覆盖掉。<br />运行结果<br /></p><p></p><p><img src="https://img-blog.csdn.net/20180501233400538?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt="" /></p><h5>删除：</h5><p>实例：</p><pre class="python">cf.remove_option("section1","key1")
print(cf.sections())
print(cf.items("section1"))

cf.remove_section("section1")
print(cf.sections())</pre><p>remove_option(section_name,option_name)：删除指定的option，section不存在会报错。<br /></p><p>remove_section(section_name)：删除指定的section。<br />需要注意这里的删除仅仅只是在内存中进行的，还要进行write()操作写入到文件中，否则配置文件实际上是没有被更改的。<br /></p><p>运行结果：<br /><img src="https://img-blog.csdn.net/20180501235039847?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt="" /><br /><br /></p>                                                                             <p></p><p></p><p></p><p></p>