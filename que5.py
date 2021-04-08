def movingTotal(n, c):
    l = range(1, n+1)
    p = []
    for i in range(0, n):
        if i+2==n:
            break
        p.append(sum([l[i], l[i+1], l[i+2]]))
    if c in p:
        return True
    else:
        return False

n = int(input("Enter the total list size: "))
c = int(input("Enter the checking value: "))
b = movingTotal(n, c)
print(b)
