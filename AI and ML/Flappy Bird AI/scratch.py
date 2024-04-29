
question = int(input("Please enter a number between 1 and 19:\n"))

total_rows = 2 * question - 1
arc = 1 - question
pattern = ""

for i in range(total_rows):
    spaces = " " * abs(arc)
    stars = "*" * (2 * question - 2 * abs(arc) - 1)
    pattern += spaces + stars

    arc += 1
    if i != total_rows - 1:
        pattern += "\n"

print(pattern)