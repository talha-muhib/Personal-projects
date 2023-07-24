# Sorting Algorithm Visualizer (In-place)

Credit to Tech With Tim for his Pygame tutorials:
https://www.youtube.com/@TechWithTim

Designed a visualizer for some in-place sorting algorithms; bubble sort, insertion sort, and selection sort. 
If you want to try out this program, run the Python file Sorting.py on your terminal.

Bubble sort, sometimes referred to as sinking sort, is a simple sorting algorithm that repeatedly steps through the input list element by element, comparing the current element with the one after it, swapping their values if needed. These passes through the list are repeated until no swaps had to be performed during a pass, meaning that the list has become fully sorted.

Insertion sort is a sorting algorithm that places an unsorted element at its suitable place in each iteration. Insertion sort works similarly as we sort cards in our hand in a card game. We assume that the first card is already sorted then, we select an unsorted card.

Selection sort proceeds by finding the smallest (or largest, depending on sorting order) element in the unsorted sublist, exchanging (swapping) it with the leftmost unsorted element (putting it in sorted order), and moving the sublist boundaries one element to the right.

All of these algorithms run in O(n^2) time on average, which is why these are typically not used for very large inputs. Better comparison sorting algorithms are merge sort or quick sort, which tend to run in O(nlg(n)) time. However, those algorithms are not in-place.
