class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        mi = 0
        res = {'b':0,'a':0,'l':0,'o':0,'n':0}
        for i in text:
            if res.get(i,-1)>-1:
                res[i]+=1
            
        return min(res['b'],res['a'],res['l'],res['l'],res['o'],res['n'])      