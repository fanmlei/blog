<p>20. 有效括号  48ms</p>

<pre class="has">
<code class="language-python">class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        if len(s) % 2 :
            return False
        brackets = {'(': ')', '{': '}', '[': ']'}
        stack = []
        for i in s:
            if i in brackets:
                stack.append(i)
            else:
                if not stack or brackets[stack.pop()] != i:
                    return False
        if stack:
            return False
        return True</code></pre>

<p>26.删除排序数组中的重复项  96ms</p>

<pre class="has">
<code class="language-python">class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) &lt;= 1:
            return len(nums)
        s = 0
        for f in range(1, len(nums)):
            if nums[s] != nums[f]:
                s += 1
                nums[s] = nums[f]
        return s + 1</code></pre>

<p>27.移除元素  56ms</p>

<pre class="has">
<code>class Solution:
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        if val not in nums:
            return len(nums)
        while val in nums:
            nums.remove(val)
        return len(nums)</code></pre>

<p>28.实现strStr()  48ms</p>

<pre class="has">
<code>class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        if not needle:
            return 0
        if needle not in haystack:
            return -1
        else:
            return haystack.index(needle)</code></pre>

<p>35.搜索插入位置  48ms</p>

<pre class="has">
<code>class Solution:
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if target in nums:
            return nums.index(target)
        if target &lt; nums[0]:
            return 0
        if target &gt; nums[-1]:
            return len(nums)
        for i in range(len(nums)-1):
            if nums[i]&lt;target and nums[i+1]&gt;target:
                return i+1</code></pre>

<p> </p>