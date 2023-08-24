import random
import math

def generate_num():
    r = math.floor(random.random() * 4 + 2)
    return r ** 2

def generate_grid(n):
    grid = []
    for _ in range(n):
        grid.append([0] * n)
    return grid

def fill_grid(grid):
    for row in range(len(grid)):
        for col in range(len(grid)):
            num = round(random.random() * len(grid))
            p = random.random() * 4
            if is_valid_move(grid, row, col, num) and p < 1:
                grid[row][col] = num

def is_valid_move(grid, row, col, number):
    n = len(grid)

    for x in range(n):
        if grid[row][x] == number:
            return False
    
    for y in range(n):
        if grid[y][col] == number:
            return False
        
    sqrt_n = int(math.sqrt(n))
    row_corner = row - (row % sqrt_n)
    col_corner = col - (col % sqrt_n)
    for y in range(sqrt_n):
        for x in range(sqrt_n):
            if grid[row_corner + y][col_corner + x] == number:
                return False
    
    return True

def solve(grid, row, col):
    if col == len(grid):
        if row == len(grid) - 1:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    
    for num in range(1, len(grid) + 1):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num

            if solve(grid, row, col + 1):
                return True
            
        grid[row][col] = 0
    
    return False


def main():
    n = generate_num()
    grid = generate_grid(n)
    fill_grid(grid)

    print(f"Our starting grid with dimensions = {n}x{n}")
    for row in grid:
        print(row)

    if solve(grid, 0, 0):
        print(f"\nWe have a solution for our grid:")
        for row in grid:
            print(row)
    else:
        print(f"\nThe grid has no possible solution")

main()