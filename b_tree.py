from collections import defaultdict, deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def PathSum(self, root, target):
        prefix = defaultdict(int)
        prefix[0] = 1
        
        def traverse(root, path_sum):
            if not root:
                return 0
           
            path_sum += root.val
             
            found = prefix[path_sum - target]
            
            prefix[path_sum] += 1
            
            found += traverse(root.left, path_sum) + traverse(root.right, path_sum)
            
            prefix[path_sum] -= 1
            
            return found

        return traverse(root, 0)

def build_tree(nums): #level order build
    if not nums or nums[0] is None:
        return None
    
    root = TreeNode(nums[0])
    q = deque([root])
    
    i = 1
    while q:
        node = q.popleft()
        
        if i < len(nums) and nums[i] is not None:
            node.left = TreeNode(nums[i])
            q.append(node.left)
        
        i += 1
        
        if i < len(nums) and nums[i] is not None:
            node.right = TreeNode(nums[i])
            q.append(node.right)
        
        i += 1
    
    return root

# def build_tree(nums): # inorder build
#     if not nums or nums[0] is None:
#         return None
    
#     val = nums.pop(0)
        
#     root = TreeNode(val)

#     root.left = build_tree(nums)    
#     root.right = build_tree(nums)
#     return root
    

# nums = [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]
# targetSum = 8

nums = [5,4,8,11,None,13,4,7,2,None,None,5,1]
targetSum = 22

root = build_tree(nums)
sol = Solution()

print(sol.PathSum(root, targetSum))