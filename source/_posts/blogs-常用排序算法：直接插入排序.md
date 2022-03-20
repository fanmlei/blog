<h3>算法思路</h3>

<p style="text-indent:50px;">插入排序就跟我们打扑克抽牌是一样的形式，每次新抽的牌插入到已有的有序牌中，是牌始终保持有序状态，例如[1,3, 2,4,0] 数组，先将1作为起始牌，下一张牌为3，第一趟完成后变成[1, 3]有序数组和[2,4,0]无序数组，接下来插入2，有序数组变成[1,2,3]，无序数组变成[4,0]，以此类推知道将所有的无序数组都插入完毕就能完成排序操作。</p>

<p style="text-indent:50px;">插入排序算法适用于少量数据的排序，时间复杂度为 O(n^2)。是一种稳定的排序方法。</p>

<h3 style="text-indent:0px;">代码实现</h3>

<pre class="has">
<code class="language-python">def insert_sort(nums):
    for i in range(1,len(nums)):  # 无序区[i:]
        temp = nums[i]  # 无序区的第一个数
        j = i - 1  # 有序区的最后一个
        while j &gt;= 0 and nums[j] &gt; temp:  # 执行插入操作
            nums[j+1] = nums[j] 
            j -= 1
        nums[j+1] = temp
        print(nums)


insert_sort([1,3, 2,4,0])

# [1, 3, 2, 4, 0]
# [1, 2, 3, 4, 0]
# [1, 2, 3, 4, 0]
# [0, 1, 2, 3, 4]</code></pre>

<p> </p>