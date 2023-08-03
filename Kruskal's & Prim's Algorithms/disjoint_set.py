"""
We're doing an array-based representation
of the Union-Find data structure
"""
class UnionFind:
    #Initialize an array of n elements (At the start each element is in its own set)
    def __init__(self, n):
        self.parent = [-1] * n

    #Return the identifier of the set containing x
    def simple_find(self, x):
        while self.parent[x] >= 0:
            x = self.parent[x]
        return x

    #Return the rank of the set containing x
    def rank(self, x):
        while self.parent[x] >= 0:
            x = self.parent[x]
        return -self.parent[x]

    #Return the identifier of the set containing x (Uses path compression)
    def compression_find(self, x):
        if self.parent[x] == -1:
            return x
        root = self.compression_find(self.parent[x])
        self.parent[x] = root
        return root

    #Do a union of two sets based on their rank (ie. tree height)
    def union(self, s, t):     
        s = self.simple_find(s)
        t = self.simple_find(t)

        max_root, min_root = max(s, t), min(s, t)
        min_rank = self.parent[min_root]

        self.parent[min_root] = max_root
        self.parent[max_root] = min(self.parent[max_root], min_rank - 1)
        return max_root
    
    #Return the entire array
    def as_array(self):
        return self.parent
    
    #Return the string representation of elements being in their respective sets
    def array_str(self):
        for e in range(len(self.parent)):
            print(f'{e} is an element in the set with root {self.simple_find(e)}')