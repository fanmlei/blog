---
title: Leet Code OJ  简单（三）
date: 2018-04-19 19:42:49
categories: 
- 算法
- leetcode
tags:
- 算法
---

58.最后一个单词的长度  52ms
```python 
class Solution:
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        s = s.split(' ')
        while "" in s:
            s.remove("")
        if not s:
            return 0
        return len(s[-1])
```

66.加一 56ms
```python
class Solution:
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        sum = 0
        r = []
        for index, i in enumerate(digits):
            sum += i*pow(10,len(digits)-index-1)
        sum += 1
        while sum:
            i = 1
            r.append(sum % pow(10,i))
            sum = sum // pow(10,i)
            i += 1

        r.reverse()
        return r
```

67.二进制求和 60ms
```python
class Solution:
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        return (bin(int(a, 2) + int(b, 2))[2:])
```

69.x的平方根 76ms    击败了81.06% 的用户
```python
class Solution:
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        return int(pow(x, 0.5))
```

83.删除排序链表重复元素  76ms  击败了48.84% 的用户
```python 
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if not head:
            return None
        cur = head
        while cur.next:
            if cur.val == cur.next.val:
                if cur.next.next:
                    t = cur.next.next
                    cur.next = t
                else:
                    cur.next = None
            else:
                cur = cur.next
        return head
```