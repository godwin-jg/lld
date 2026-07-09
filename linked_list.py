import heapq
from typing import List, Optional

# 1. Definition for a singly-linked list node.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 2. Solution Class containing your optimized Heap approach
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        head = ListNode(0)
        tail = head

        heap = []
        tie_breaker = 0
        
        # Initialize the heap with the head node of each non-empty list
        while lists:
            node = lists.pop()
            if node:
                heapq.heappush(heap, (node.val, tie_breaker, node))
                tie_breaker += 1
        
        # Process the heap dynamically
        while heap:
            val, _, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            
            # If the popped node has a next node, push it to the heap
            if node.next:
                heapq.heappush(heap, (node.next.val, tie_breaker, node.next))
                tie_breaker += 1

        return head.next

# 3. Helper functions to make running and testing easy
def build_linked_list(arr):
    """Converts a Python list into a Linked List."""
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def print_linked_list(node):
    """Prints a Linked List in a readable format."""
    elements = []
    while node:
        elements.append(str(node.val))
        node = node.next
    print(" -> ".join(elements) if elements else "Empty List")


# 4. Execution Block (Driver Code)
if __name__ == "__main__":
    # Example Input: [[1, 4, 5], [1, 3, 4], [2, 6]]
    list1 = build_linked_list([1, 4, 5])
    list2 = build_linked_list([1, 3, 4])
    list3 = build_linked_list([2, 6])
    
    input_lists = [list1, list2, list3]
    
    print("Merging sorted lists...")
    solution = Solution()
    merged_head = solution.mergeKLists(input_lists)
    
    print("Result:")
    print_linked_list(merged_head)