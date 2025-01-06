#Positive or negative
num = float(input("Enter a number: "))

if num > 0:
    print(num," is Positive")
    num = int(num)
    #Odd and even number test
    if((num % 2) == 0):
        print("{0} is even".format(num))
    else:
        print("{0} is Odd".format(num))

    #Armstrong number: abc = a^n + b^n + c^n where n=3 (any int)
    #num2 = int(input("Enter a number for Armstrong check: "))

    #power
    n = len(str(num))
    sum = 0

    temp = num
    while(temp > 0):
        digit = temp % 10
        sum += digit ** n
        temp //= 10

    if (num == sum):
        print(num,"is an Armstrong")
    else:
        print(num,"is not an Armstrong")

    #Prime numbers
    #num3 = int(input("Enter your Prime number check: "))

    if num > 1:
        for i in range(2,num):
            if (num % i) == 0:
                print(num,"is not a prime number")
                print(i,"times",num//i,"is",num)
                break
        else:
            print(num,"is a prime number")
    else:
        print("Enter a number greater than ",num)

    #Factorial of a number
    factorial = 1
    for i in range(1,int(num) + 1):
        factorial = factorial*i
    
    print("Factorial of ",num," is ",factorial)

elif num == 0:
    print(num," is Zero")
    print("Factorial for Zero is 1")
    print("Factorial does not exist for a negative number")
else:
    print(num," is Negative")