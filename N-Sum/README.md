# N-Sum:
Given an array of n elements, a number k, and a target sum, the program determines if the target sum can be acquired using k elements of the array. If the target is found, it returns a list of numbers that sum up to the target. Otherwise it returns an empty list.
I tried making the structure of the program in such a way that for similar problems, the same code can be used with minimal changes.
For example, I had a version of this project where instead of returning a list of numbers that sum to the target, the project just returns
TRUE or FALSE, depending on whether the sum was valid. The code structure was exactly the same with minimal type changes. Even for problems
like the Additive Number, I believe the same structure will work with minima changes.

On a side note, this program only works with inputs that are already sorted, which is why it also has a sorting algorithm running in the background. The algorithm runs in O(n) time is loosely based off counting sort, but it's not the same. It was something I experimented with as I was working on this project. The trade-off for this algorithm is that it also uses O(n) space. 

However, the running time of the overall project is O(C(n, k)), where C(n, k) denotes "n choose k". So for larger and larger inputs, the sorting algorithm doesn't matter in the long term.
