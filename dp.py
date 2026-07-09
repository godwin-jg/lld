nums = "1542219"
x = 3

# nums = "50800"

def dp(nums, temp):
    num = str(int(temp)) if temp else ''
    if len(temp) == target:
        res.append(int(num))
        return
    for i in range(len(nums)):
        dp(nums[i+1:], temp + nums[i])

    

res = []
target = len(nums) - x 
dp(nums, '')
print(res)
print("ans: ",min(res))
