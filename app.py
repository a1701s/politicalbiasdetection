from ideology import finalpred
from scraper import lengthofsearch

inp = str(input("Query: "))
inp2 = str(input("Article Index: "))
length = lengthofsearch(inp)

while int(inp2) > int(length) or inp2.isdigit():
    inp2 = int(input(f"Try again, max length is {length}:"))

print(finalpred(int(inp2), inp))