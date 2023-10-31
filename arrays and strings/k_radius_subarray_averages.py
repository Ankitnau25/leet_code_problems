class Solution:
    def getAverages(self, nums, k: int):
        rang = 2*k+1
        s=nums[0]
        res = [-1]*len(nums)
        rev_ind = 0
        if k==0:
            res[0] = nums[0]
        for i in range(1,len(nums)):
            if i < rang-1:
               s += nums[i]
            elif i == rang-1:
               s += nums[i]  
               res[i-k] = s//rang    
            else:
               s += nums[i]-nums[rev_ind] 
               rev_ind+=1 
               res[i-k] = s//rang   
        return res        
obj = Solution()
print(obj.getAverages([7,4,3,9,1,8,5,2,6],1))

       