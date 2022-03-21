<h3 id="%E7%AE%97%E6%B3%95%E6%80%9D%E8%B7%AF%EF%BC%9A">算法思路：</h3>

<p style="text-indent:50px;">步骤：1. 创建10个队列(0-9)<br />
                      2. 遍历每个数位，按照位数存入不同的桶中<br />
                      3. 然后再将桶中的元素依次取出，放回到原有列表中<br />
                      4. 继续执行上两步操作，直到列表中每个数的每一位都做完成排序<br />
                      5. 最后取出桶内元素，排序完成</p>

<p style="text-align:center;"><img alt="" class="has" height="357" src="https://img-blog.csdn.net/20181025144312786?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="800" /></p>

<p style="text-indent:50px;">时间复杂度： O(kn)  k为最大数位数                   空间复杂度：O(k+n)</p>

<h3 id="%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B0%EF%BC%9A">代码实现：</h3>

<pre class="has">
<code class="language-python">def radix_sort(nums):
    max_num = max(nums)
    bucket = [[] for _ in range(10)]  # 创建空桶
    i = 0
    while 10 ** i &lt; max_num:
        # 按位数将数组存入桶中
        for num in nums:
            bucket[num // (10 ** i) % 10].append(num)
        nums.clear()
        for j in bucket:  # 取出桶中元素，顺便情况桶
            nums.extend(j)
            j.clear()
        i += 1</code></pre>

<p> </p>