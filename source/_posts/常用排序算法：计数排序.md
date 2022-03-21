<h3>算法思路：</h3>

<p style="text-indent:50px;">顾名思义计数排序就是统计每个数出现的次数，例如给0-20范围内的数排序，首先建立一个长度为21的空数组，然后统计每个数出现的次数，再按照下标存入空数组中，例如1出现10次那么数组中的第二个元素为10 ，统计完所有的数之后呢在新建一个数组，在遍历之前存放次数的数组，按照个数往新数组中添加对应的数。</p>

<p style="text-indent:50px;">以一个例子来说明[1,2,3,1,0,4,1,3,4,2,0,1,2,3,4]排序过程如下图所示</p>

<p style="text-align:center;"><img alt="" class="has" height="301" src="https://img-blog.csdn.net/20181024172139600?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="947" /></p>

<p style="text-indent:50px;">计数排序虽然时间复杂度小O(n)，但是局限性很大，首先是需要知道最大数是多少，其次当无序列表分布很分散例如[1,3,1000000]，明明只有三个数但是却需要开辟一个长度为1000000的空列表，会造成空间浪费。所以计数排序只适合在特定的情况下使用。</p>

<h3 style="text-indent:0px;">代码实现：</h3>

<pre class="has">
<code class="language-python">def count_sort(nums, max_num):
    """
    计数排序
    :param nums: 无序数组
    :param max_num: 最大数
    """
    count = [0 for x in range(max_num+1)]  # 新建一个统计数组
    for i in nums:  # 计数
        count[i] += 1
    nums.clear()  # 清空原有数组
    for c, i in enumerate(count):  # 往空数组中添加元素
        while i &gt; 0:
            nums.append(c)
            i -= 1</code></pre>

<p> </p>