<h3>算法思路：</h3>

<p style="text-indent:50px;">希尔排序算是插入排序的一种，是改进版的直接插入排序，和直接插入排序不同的是它是按组进行插入排序的。步骤如下：</p>

<ol><li style="text-indent:0px;">取一个整数d1 = n / 2,将元素分成d1个组，每组相邻元素之间距离d1，然后在每组内部进行直接插入排序。</li>
	<li style="text-indent:0px;">取第二个整数d2 = d1 / 2再将元素分成d2个组，然后再在每组内部进行插入排序。</li>
	<li style="text-indent:0px;">
	<p style="text-indent:0;">重复上面的步骤直到d = 1 的时候即所有元素在同一组进行插入排序。</p>
	</li>
</ol><p style="text-indent:50px;">例如数组 [4,3,5,1,6,0,7,2]排序过程如下图所示</p>

<p style="text-align:center;"><img alt="" class="has" height="417" src="https://img-blog.csdn.net/20181024153628923?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="994" /></p>

<p style="text-indent:50px;">希尔排序并每趟并不是使某些元素有序，而是使整体数据越来越有序，只会在最后一趟排序能使得所有元素都有序。</p>

<h3 style="text-indent:0px;">代码实现：</h3>

<pre class="has">
<code class="language-python">def shell_sort(nums):
    d = len(nums) // 2
    while d &gt; 0:   # 分组到一的时候停止
        for i in range(d, len(nums)):  # 第i个分组
            temp = nums[i]  #无序区第一位
            j = i - d  # 有序区最后一位
            while j &gt;= 0 and nums[j] &gt; temp:  # 如果有序区大于无序区
                nums[j + d] = nums[j]
                j -= d
            nums[j+d] = temp
        d //= 2</code></pre>

<p style="text-indent:50px;"> </p>