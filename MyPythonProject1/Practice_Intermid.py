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
dog2.bark()'''

class square:
    sides = 4

    def __init__(self):
        self.height = 0
        self.width = 0 
    
    def caculate_area(self):
        return self.height * self.width


square1 = square()
square1.height = int(input("Enter height: "))
square1.width = int(input("Enter width: "))
print(square1.caculate_area())


