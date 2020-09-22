
d = {1:1, 10:10, 2:2}
print(type(d))

print(sorted(d.items()))

for a, b in sorted(d.items()):
    print(a, b)

print(type(d))
d = sorted(d.items())
print(d)
print(type(d))
