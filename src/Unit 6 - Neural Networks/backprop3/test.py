x = [3, 234, 24, 33, 4111, 332, 113, 65, 78, 29]
new_x = []
count = 0
while count < len(x):
    new_x.append(0)
    new_x.append(x[count])
    
    new_x.append(x[count + 1])
    count += 2

print(x)
print(new_x)