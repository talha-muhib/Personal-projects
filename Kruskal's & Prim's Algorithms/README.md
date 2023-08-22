# Kruskal's Algorithm vs. Prim's Algorithm
Created a visualizer in Pygame to show the difference between Kruskal's Algorithm and Prim's Algorithm for minimum cost spanning trees on graphs with 1-11 vertices. I also added a small probability of getting disconnected graphs to show that neither algorithm works correctly unless the graph is connected.  

NOTE on Kruskal's algorithm:  
A data structure called Union-Find is used to detect cycles while running the algorithm. The disjoint_set.py file shows an array-based implementation.  

Notes on Union-Find:  
https://www.cs.umd.edu/class/fall2022/cmsc420-0201/Lects/lect04-union-find.pdf  

Note on mst.py and mst2.ipynb:  
Both of those files contain the exact same code. mst2 is a Jupyter file, so if you prefer that then run that file instead.
