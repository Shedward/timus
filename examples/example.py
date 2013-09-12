import sys

sum = 0
for line in sys.stdin:
    for word in line.split():
        sum += int(word)

print(sum)
