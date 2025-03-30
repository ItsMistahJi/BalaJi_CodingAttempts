#lists
'''list1 = [1,2,3,4,5,True,"string",6.7]
print(list1)

length=len(list1)
print(length)
print(list1[7])
list1.append("IronMan")
print(list1)
list1.insert(3,45)
print(list1)
list1.remove(list1[8])
print(list1)
while list1 != []:
    n = len(list1) - 1
    list1.remove(list1[n])
    print(list1)

#tuples
tuple1 = (1,2,3,4,5,6,7,8,9,10)
print(tuple1)
print(tuple1[5])
print(tuple1[1:5])
print(tuple1[1:10:2])
print(tuple1[10:1:-2])

for i in range(40):
    print((i + 1) *2)

#Dictionary
#key value pair
cats = {"Jane":6, "John":4, "Jill":3, "Jack":7}
print(cats["Jill"])
cats["Jill"] = 10
print(cats["Jill"])
print(cats.keys())
print(cats.values())
print("Length of Dict:",len(cats))
print("Items:",cats.items())
Test={"1":True, "2":False, "3":True,"4":False, "5":True, "6":False}
print(Test)
print("Length of Dict:",len(Test))
print("Keys:",Test.keys())
print("Values:",Test["5"])
print("Items:",Test.items())

sum = 0
def your_code():
    numbers = [1,2,3,4,5,6,7,8,9,10]

    for i in numbers:
        if i % 2 == 0:
            sum = i
            sum = sum + sum
    print(sum)
    return sum

result = your_code()
print(result)

##string, split and lyric finder
text = """The Gettysburg Address is a speech delivered by Abraham Lincoln, the 16th U.S. president, following the Battle of Gettysburg during the American Civil War."""

print(type(text))
print(len(text))
print(text[0:100])
print(len(text.split()))
print(text.count("the"))
print(text.count("The"))
word_count = {}
for word in text.lower().split():
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(word_count)

#Function
def bark():
    print("Woof Woof")

bark()

def hello(name):
    print(f"Hello {name}!")

hello("jo")

def add(a,b):
    return a + b

print(add(2,3))

def dog_info(name,age):
    print(f"{name} is {age} years old")

dog_info("Tommy", 5)

def double(number):
    return number*2

print(double(5))

def allCaps(string):
    return string.upper()

print(allCaps("whotheboss"))

user_input = input("Enter a text: ")
user_input1 = input("Enter 1 for Upper case, 2 for Lower case, 3 for Title case: ")
if user_input1 == "1":
    print(user_input.upper())
elif user_input1 == "2":
    print(user_input.lower())
elif user_input1 == "3":
    print(user_input.title())
else:
    print("Invalid input")

def has_remainder(num1,num2):
    if num1 % num2 == 0:
        return False
    else:
        return True

print(has_remainder(10,5))
print(has_remainder(10,3))

#number guessing game
user_input = 0
import random
random_number = 4

while user_input != random_number:
    user_input = int(input("Enter a number between 1 and 10: "))
    if user_input == random_number:
        print("You guessed it right")
    else:
        print("Try again")

s = input("Enter a string: ")
c = input("Enter a character: ")
f = float(input("Enter a float: "))
i = int(input("Enter an integer: "))
print(s,c,f,i)'''

#guessing game
print("Welcome to the guessing game")
import random
randy = random.randint(1,10)
user_input = 0
guess_count = 0
import time

while user_input != randy:
    user_input= int(input("input a number between 1 and 10: "))
    print("Hmm, let me think...")
    time.sleep(2)
    guess_count +=1
    if user_input == randy:
        print("Yipee")
    else:
        print("Try again")

print(f"You guessed it right in {guess_count} tries")