import sys
import random

ops = ['+', '-', '*']

with open("create_test.txt", "w+") as f:
    output = ""
    for i in range(1000):
        output += "" + str(random.randint(1, 100)) + str(random.choice(ops))
    output += str(random.randint(1, 100))
    f.write(output)
