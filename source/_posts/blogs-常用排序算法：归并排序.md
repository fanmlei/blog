<h3>算法思路：</h3>

<p style="text-indent:50px;">简单来说归并排序就是将两个有序的序列合并成一个完整的有序序列。具体步骤如下：<br />
           1. 选取序列1的第一个元素和序列2的第一个元素，较小的存放到新序列的第一位<br />
           2. 选序列1的第二个元素再和序列2的第一个元素比较，选较小的存放到新序列的低二位<br />
           3. 重复上述步骤直到序列1序列2没有下一个元素为止</p>

<p style="text-align:center;"><img alt="" class="has" height="209" src="https://img-blog.csdn.net/20181023233332595?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="699" /></p>

<p style="text-indent:50px;">那么问题来了，一个无序的序列又是如何分成两个有序序列然后执行上述的步骤呢，这个我们就需要先把原有的序列进行拆分，拆分到每个子序列长度都为1的时候所有子序列不就是有序的吗【手动滑稽】。那么一个完整的递归排序的过程就会分成两部分，第一拆分，第二合并，如下图所示</p>

<p style="text-align:center;"><img alt="" class="has" height="483" src="https://img-blog.csdn.net/20181024013350783?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="851" /></p>

<h3 style="text-indent:0px;">代码实现：</h3>

<pre class="has">
<code class="language-python">def merge(nums, low, mid, high):    # 合并
    i = low
    j = mid + 1
    array = []
    while i &lt;= mid and j &lt;= high:   # 循环从两边中取出较小的数放入新的空数组中
        if nums[i] &lt;= nums[j]:
            array.append(nums[i])
            i += 1
        else:
            array.append(nums[j])
            j += 1
    while i &lt;= mid:            # 当某一边取完了之后，直接将剩下一边的数据直接存入
        array.append(nums[i])
        i += 1
    while j &lt;= high:
        array.append(nums[j])
        j += 1
    nums[low:high + 1] = array


def merge_sort(nums, left, right):  # 拆分
    if left &lt; right:
        mid = (left + right) // 2
        merge_sort(nums, left, mid)
        merge_sort(nums, mid + 1, right)
        merge(nums, left, mid, right)</code></pre>

<h3>补充</h3>

<p style="text-indent:50px;">之前面试遇到一个问题，给一个4G内存的计算机，硬盘大小为1T，设计一种算法将100G的数据从小到大排序，第一个想到的就是归并，但是呢这个归并不同上面说的那种，因为内存太小了，放不下那么多数据啊。所以呢需要做一下改进。4G和100G差别太多，以4G和12G为例，首先先从硬盘中取出3G数据放入内存中使用排序算法构造成有序数据在写回到硬盘中，再取出下一个3G数据排好序，直到所有的数据都取出来并排好序了，这样我们就得到了4个有序的子序列，下一步呢就是用我们刚刚说的归并排序将4个有序序列合并成一个完整的有序序列。</p>