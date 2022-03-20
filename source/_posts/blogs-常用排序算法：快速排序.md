<h3>算法思路</h3>

<p style="text-indent:50px;">快速排序差不多是面试中问的最多的一种排序算法了，快排是比较容易理解的，核心思路就是，选取一个数作为基准，将原来的列表分为两个部分，一部分全部小于这个基准数，另外一部分全部大于这个基准数，然后呢再按照这个方法对划分出来的两部分继续做同样的操作，直到无法划分的时候排序也就完成了。</p>

<p style="text-indent:50px;">以数组[3,2,1,5,4,6]为例，其排序过程如下图所示。<img alt="" class="has" height="315" src="https://img-blog.csdn.net/20181023002351996?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="837" /></p>

<p style="text-indent:50px;">关于时间复杂度问题， 平均复杂度n log(n) 最坏情况 n^2，以长度为16的list为例：<img alt="" class="has" height="465" src="https://img-blog.csdn.net/2018102315000133?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="706" /></p>

<h3>代码实现</h3>

<p style="text-indent:0;">方法一：</p>

<p style="text-indent:50px;">按照上述的思路可分为两个部分来写代码，一部分是使用递归，一部分是调整位置。</p>

<pre class="has">
<code class="language-python">def partition(nums, left, right):
    temp = nums[left]
    while left &lt; right:
        while left &lt; right and nums[right] &gt;= temp:   # 从右往左搜索比基准值小
            right -= 1   # 没有则往右走一位
        nums[left] = nums[right]  # 找到了比基准值小的则调整顺序
        while left &lt; right and nums[left] &lt;= temp:  # 从左往右找比基准大的数
            left += 1
        nums[right] = nums[left]
    nums[left] = temp   # 交换完成之后归位
    return left  # 返回基准值的位置


def quick_sort(nums, left, right):
    if left &lt; right:
        mid = partition(nums, left, right)
        quick_sort(nums, left, mid - 1)   # 比基准值小的一部分再次进行快排
        quick_sort(nums, mid + 1, right)  # 比基准值大的一部分</code></pre>

<p style="text-indent:0;">方法二：</p>

<p style="text-indent:50px;">上面这种呢是在原有的list进行变换，如果不考虑原有变换还有一种更直观的方法来实现，使用列表生成式来实现，只不过在数据量很大的时候会占用更多的空间。不考虑交换操作，直接简单粗暴的把list分割成两部分。</p>

<pre class="has">
<code class="language-python">def quick_sort(nums):
    if len(nums) &lt;= 1:
        return nums
    pivot = nums[len(nums)//2]
    left = [x for x in nums if x &lt; pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x &gt; pivot]
    return quick_sort(left) + middle + quick_sort(right)</code></pre>

<p> </p>