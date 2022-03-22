---
title: Leet Code OJ  简单（一）
date: 2018-04-17 19:42:49
categories: 
- 算法
- leetcode
tags:
- 算法
---
1.两数之和  3780ms
```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i in range(len(nums)):
            for m in range(i+1, len(nums)):
                if nums[i]+nums[m] == target:
                    return [i, m]
```

7.反转整数 80ms （python的负数取余和C语言 不同
```python
class Solution:
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        y = 0
        while x:
            if x &gt; 0:
                y *= 10
                y += x % 10
                x = x // 10
            else:
                y *= 10
                if x % 10:
                    y += x % 10 - 10
                    x = x // 10 + 1
                else:
                    y += x % 10
                    x = x // 10

        if y &gt; -pow(2, 31) and y &lt; pow(2, 31) - 1:
            return y
        else:
            return 0
```

9.回文数  408ms
```python
class Solution:
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        x = str(x)
        for i in range(len(x)):
            if x[i] != x[-i-1]:
                return False
        return True
```

13.罗马数字转整数 212ms
```python 
class Solution:
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        rec = 0
        num = {'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10, 'XL': 40, 'L': 50, 'XC': 90, 'C': 100, 'CD': 400, 'D': 500, 'CM': 900, 'M': 1000}
        while s:
            for i in range(2, 0, -1):
                if s[:i] in num:
                    rec += num[s[:i]]
                    s = s[i:]
                    break
        return rec
```

14.最长公共前缀 54ms
```python
class Solution:
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if strs:
            for i in range(len(strs[0])+1):
                for s in range(1, len(strs)):
                    if strs[0][:i] != strs[s][:i]:
                        if strs[0][:i - 1]:
                            return strs[0][:i-1]
                        else:
                            return ""
            return strs[0]

        else:
            return ""
```