class Solution:
    def minStartValue(self, nums) :
        out = [0]*len(nums)
        out[0] = nums[0]
        mim = out[0]
        for i in  range(1,len(nums)):
            out[i] = out[i-1]+nums[i] 
            if mim > out[i]:
                mim = out[i]   
        if mim < 1:
            return 1-mim
        else:
            return 1   
obj = Solution()
print(obj.minStartValue([2,3]))
print(obj.minStartValue([-3,2,-3,4,2]))