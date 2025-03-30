#classes
'''class Dog:
    info = "Dogs are loyal"

print(Dog.info)

#create a class for something around me
#create a class variable inside the class
import random

class Lamp:
    color = "Blue"
    print("inside class")

    def __init__(self,name):
        print("The lamp is turned on")
        self.lucky_num=(random.randint(1,5))
        self.name = name

Lamp("RRR")
print(Lamp.color)
lamp1 = Lamp("RRr")
lamp2 = Lamp("Rrr")
print(lamp1.lucky_num)
print(lamp2.lucky_num)

lamp1.name = "yo"
print(lamp1.name)
print(lamp2.name) #error

class Dog:
    print("inside class dog")
    part = "Tail"

Dog()
Dog.part = "Leg"
print(Dog.part)
import random
class Dog:
    info = "Dogs are loyal"
    print("inside class dog")

    def __init__(self,name):
        print("inside self")
        self.lucky_num = random.randint(1,5)
        self.name = name
    
    def bark(self):
        print("Woof Woof")
        print(f"name is {self.name} and lucky number is {self.lucky_num}")
        #print(f"name is {self.name} and lucky number is ")


#Dog("Tommy")
#Dog("Tommy2")
dog1=Dog("Tom1")
dog2=Dog("Tom2")

dog1.bark()
dog2.bark()

#my own parent class, child classes
class shape:
    print("this is parent class Shape")

    def __init__(self,height=0,width=0):
        print("inside init of class shape")
class square:
    info = "This is child class of Shape - Square"
    print(info)
    #sides = 4

    def __init__(self,height=0,width=0):
        self.height = 0
        self.width = 0 
        print("Inside init class of square")
    
    def caculate_area(self):
        return self.height * self.width

class rectangle(shape):
    print("this is child class of shape")

    def __init__(self,height=0,width=0):
        super().__init__(self)
        print("Inside init class of rectangle")
    
    def caculate_area(self):
        return self.height * self.width * 2

def main():
    #shape()
    sq1 = square()
    rec1 = rectangle()
    sq1.height = int(input("Enter height: "))
    sq1.width = int(input("Enter width: "))
    rec1.width = int(input("Enter width: "))
    rec1.height = int(input("Enter height: "))
    print(sq1.caculate_area())
    print(rec1.caculate_area())

main()

##My attempt at creating a class and inheriting it
class numbers():
    #print("inside class numbers")

    def __init__(self,num):
        #print("inside init of numbers")
        self.num = num

class even(numbers):
    #print("inside class even")

    def __init__(self,num):
        super().__init__(num)
        #print("inside init of even")
    
    def check_even(self):
        if self.num % 2 == 0:
            print(f"{self.num} is an even number")
        else:
            print(f"{self.num} is not an even number")
class prime(numbers):
    #print("inside class prime")

    def __init__(self,num):
        #print("inside init of prime")
        super().__init__(num)

    def check_prime(self):
        if self.num > 1:
            for i in range(2,self.num):
                if self.num % i == 0:
                    print(f"{self.num} is not a prime number")
                    break
            else:
                print(f"{self.num} is a prime number")
        else:
            print(f"{self.num} is not a prime number")
        

def main():
    num = int(input("Enter a number: "))
    even1 = even(num)
    prime1 = prime(num)
    even1.check_even()
    prime1.check_prime()

main() 

##################################################################################
# #My attempt at creating a class and inheriting it
class cars():
    def __init__(self,name):
        self.name = name

class fuel(cars):
    def __init__(self,name):
        super().__init__(name)
        self.fuelType = {"Petrol", "diesel"}

class electric(cars):
    def __init__(self,name):
        super().__init__(name)
        self.fuleType = {"electric","hybrid"}

def main():
    name= input("Enter a car name:")
    runson = input("Enter the fule it runs on:")
    if runson == "petrol" or runson == "diesel":
        fuel1 = fuel(name)
        print(fuel1.name)
    elif runson == "electric" or runson == "hybrid":
        electric1 = electric(name)
        print(electric1.name)
    else:
        print("Invalid input: please enter petrol, diesel, electric or hybrid")

main() '''

######################################################################################
#try and except
'''try:
    #info = "inside try"
    4/0
    #print(name)
except NameError:
    print("NameError: name is not defined")
except ZeroDivisionError as z:
    print("ZeroDivisionError: division by zero ",z)
except:
    print("inside except")

class cheeseError(Exception):
    pass

def upper_fun(word):
    if len(word) <=0:
        raise cheeseError("Word is empty")
    return word.upper()

print(upper_fun("hello"))
print(upper_fun("")) 

#attempt1
try:
    num = int(input("Enter a number: "))
    print(num)
except ValueError:
    print("ValueError: invalid literal for int() with base 10")

class thathu(Exception):
    info = "inside class thathu"

def check_num(num):
    if num < 0:
        raise thathu("Number is negative")
    return num

print(check_num(1))
#print(num)'''
######################################################################################

class Student():
    scores = [65,75,85,95]

    def __init__(self):
        pass

    def average_score(self):
        total=0
        for i in self.scores:
            total += i 
        return total / len(self.scores)

def main():
    student = Student().average_score()
    print(f"Average score is {student}")

main()

