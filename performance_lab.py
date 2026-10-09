# 🔍 Problem 1: Find Most Frequent Element  (OPTIMIZED)
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

from collections import Counter

def most_frequent(numbers):
    if not numbers:
        return None
    return Counter(numbers).most_common(1)[0][0]

"""
Optimized version of most_frequent.

Original approach (manual dict):
    - Built a frequency dictionary with a pure-Python loop
    - Then called max(..., key=counts.get)
    - Time  : Θ(n)
    - Space : O(k) where k = number of unique values

Optimized approach (collections.Counter):
    - Counter is implemented in C and is highly tuned for exactly this use-case
    - most_common(1) returns the (element, count) pair with the highest frequency
    - Same asymptotic complexity, but lower constant factors and cleaner code

Performance / space comparison:
    - Time complexity stays Θ(n) - we still have to look at every element
    - Space complexity stays O(k)
    - In practice Counter is noticeably faster on larger lists because the
      counting loop runs in C instead of the Python interpreter
    - Code is shorter and less error-prone (no manual .get(num, 0) logic)

Why this is better:
    We trade a tiny bit of “reinventing the wheel” for a battle-tested,
    faster implementation that still meets the same big-O guarantees.
"""


"""
Time and Space Analysis for problem 1 (optimized):
- Best-case: O(n)
- Worst-case: O(n)
- Average-case: O(n)
- Space complexity: O(k)  (k = number of unique elements)
- Why this approach? Counter is the idiomatic, highly-optimized tool for frequency counting in Python.
- Could it be optimized further? Not asymptotically. For extremely large data you could stream / use a reservoir, but that is outside the scope of this lab.
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result


"""
Time and Space Analysis for problem 2:
- Best-case: O(n) - still must visit every element.
- Worst-case: O(n) - hash-set lookups/inserts are amortized O(1).
- Average-case: O(n)
- Space complexity: O(k) for the set + O(k) for the result list (k = number of unique elements). Overall O(n) worst-case.
- Why this approach? A set gives O(1) average membership tests while the result list preserves insertion order. This is the classic linear-time solution.
- Could it be optimized? You can use dict.fromkeys(nums) in Python 3.7+ (dicts preserve order) which is a one-liner and still O(n), but the explicit loop is clearer for teaching purposes. Sorting + unique would be O(n log n) and loses original order unless you keep indices, so it is strictly worse for this requirement.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

def find_pairs(nums, target):
    seen = set()
    pairs = []
    for num in nums:
        complement = target - num
        if complement in seen:
            # Emit the pair in sorted order so the result is deterministic
            pairs.append(tuple(sorted((num, complement))))
        seen.add(num)
    return pairs


"""
Time and Space Analysis for problem 3:
- Best-case: O(n) - single pass; early exit is not possible in general because we must report every valid pair.
- Worst-case: O(n) - each element is processed once; set operations are amortized O(1).
- Average-case: O(n)
- Space complexity: O(n) for the seen set + O(p) for the output list where p is the number of pairs (p ≤ n/2).
- Why this approach? The classic two-sum hash-set technique finds each pair in constant time after seeing its complement, giving an overall linear solution. Because the problem guarantees no duplicates, we never have to worry about the same number pairing with itself.
- Could it be optimized? Sorting the array first and using two pointers is also O(n log n) time and O(1) extra space (if we may mutate the input). The hash-set method is asymptotically faster when extra space is allowed. Returning pairs in any order is fine per the spec.
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n):
    capacity = 1          # start with a tiny capacity so resizes are visible
    size = 0
    data = [None] * capacity

    for i in range(n):
        if size == capacity:
            # Simulate doubling: allocate a new array and copy everything
            new_capacity = capacity * 2
            print(f"Resizing: {capacity} → {new_capacity}")
            new_data = [None] * new_capacity
            for j in range(size):
                new_data[j] = data[j]
            data = new_data
            capacity = new_capacity
        data[size] = i    # “append” the next value
        size += 1

    print(f"Final size = {size}, capacity = {capacity}")
    return data[:size]


"""
Time and Space Analysis for problem 4:
- When do resizes happen? Whenever size == capacity, i.e. after 1, 2, 4, 8, … insertions (powers of two).
- What is the worst-case for a single append? O(n) - the append that triggers a resize must copy all existing elements.
- What is the amortized time per append overall? O(1). Over a sequence of n appends the total copying cost is
  1 + 2 + 4 + … + 2^{⌊log₂ n⌋} < 2n, therefore average cost per append is < 2 = O(1).
- Space complexity: O(n) - the final capacity is at most 2n, so extra space is still linear.
- Why does doubling reduce the cost overall? Geometric growth makes the expensive copy operations rare enough that their total cost is still linear; any growth factor > 1 yields amortized O(1), but doubling is the classic practical choice.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    if not nums:
        return []
    result = [0] * len(nums)
    result[0] = nums[0]
    for i in range(1, len(nums)):
        result[i] = result[i - 1] + nums[i]
    return result


"""
Time and Space Analysis for problem 5:
- Best-case: O(n) - every element must be examined.
- Worst-case: O(n)
- Average-case: O(n)
- Space complexity: O(n) for the output list (required). Extra auxiliary space is O(1).
- Why this approach? A single left-to-right scan keeps a running sum and writes it into the result array. This is optimal: both time and space are linear and unavoidable.
- Could it be optimized? Not really - you must produce n numbers, so Ω(n) time and space is a lower bound. In languages that allow mutating the input you could overwrite the original list in-place (still O(n) time, O(1) extra space), but the problem asks for a new list.
"""


# ---------------------------------------------------------------------------
# Simple test suite
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Problem 1: most_frequent ===")
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3
    assert most_frequent([5, 5, 5]) == 5
    assert most_frequent([1, 2, 3]) in (1, 2, 3)   # any is fine on a tie
    assert most_frequent([]) is None
    print("All most_frequent tests passed.")

    print("\n=== Problem 2: remove_duplicates ===")
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]
    assert remove_duplicates([]) == []
    assert remove_duplicates([1, 1, 1]) == [1]
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]
    print("All remove_duplicates tests passed.")

    print("\n=== Problem 3: find_pairs ===")
    pairs = find_pairs([1, 2, 3, 4], 5)
    assert set(pairs) == {(1, 4), (2, 3)}
    assert find_pairs([1, 2, 3], 10) == []
    assert find_pairs([], 5) == []
    print("All find_pairs tests passed.")

    print("\n=== Problem 4: add_n_items ===")
    result = add_n_items(6)
    assert result == [0, 1, 2, 3, 4, 5]
    print("add_n_items produced the expected values.")

    print("\n=== Problem 5: running_total ===")
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert running_total([]) == []
    assert running_total([7]) == [7]
    assert running_total([-1, 1, -1]) == [-1, 0, -1]
    print("All running_total tests passed.")

    print("\n✅ All tests passed!")