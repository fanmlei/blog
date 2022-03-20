<p>88.合并两个有序数组     56ms  提交中击败了47.05% 的用户</p>

<pre class="has">
<code class="language-python">class Solution:
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        for i in range(n):
            temp = nums2[i]
            j = m-1
            while j &gt;=0 and nums1[j] &gt; temp:
                nums1[j+1] = nums1[j]
                j -= 1
            nums1[j+1] = temp
            m += 1</code></pre>

<p>100. 相同的树   48 ms 击败了58.92% 的用户</p>

<pre class="has">
<code class="language-python"># Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isSameTree(self, p, q):
        """
        :type p: TreeNode
        :type q: TreeNode
        :rtype: bool
        """
        if not p and not q:
            return True
        if p and q and p.val == q.val:
            left = self.isSameTree(p.left,q.left)
            right = self.isSameTree(p.right,q.right)
            return left and right
        else:
            return False</code></pre>

<p>101. 对称二叉树   56 ms 击败了81.40% 的用户</p>

<pre class="has">
<code class="language-python"># Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isSymmetric(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        def isSame(left,right):
            if not left:
                return right == None
            if not right:
                return left == None
            if left.val == right.val:
                return isSame(left.left,right.right) and isSame(left.right,right.left)
            else:
                return False
        if not root:
            return True
        return isSame(root.left, root.right)</code></pre>

<p>104. 二叉树的最大深度 : 64 ms 击败了79.70% 的用户</p>

<pre class="has">
<code class="language-python"># Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """         
        if not root:
            return 0
        left =  self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return 1 + max(left,right)</code></pre>

<p> </p>