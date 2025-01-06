#n = input("Number of rows:")
n = 5
for i in range(0,n):
    for j in range(0,i+1):
        print("* ",end="")
    print("\r")

print("====================================")

#using list
myList = []
for i in range(1,n+1):
    myList.append("* "*i)
print("\t\n".join(myList))

print("====================================")

#triangle
k = n - 1
for i in range(0,n):
    for j in range(0,k):
        print(end=" ")
    k = k - 1
    for j in range(0, i+1):
        print("# ",end="")
    print("\r")

print("====================================")

k2 = 2*n - 2
for i in range(0,n):
    for j in range(0,k2):
        print(end=" ")
    k2 = k2 - 2
    for j in range(0, i+1):
        print("£ ",end="")
    print("\r")

print("====================================")