#Advanced comparisons of IF statements
#nested IF
'''age = 7
height = 5
#and/or
if age >= 7 or height == 100:
    print("good")
else:
    print("not good")

if age >= 7 and height != 5:
    print("good")
elif age == 7 or height > 5:
    print("level1")
else:
    print("not good")'''

#Switch cases
'''direction = input("enter one of the directions:")

match direction.lower():
    case "north":
        print("up")
    case "south":
        print("down")
    case "east":
        print("right")
    case "west":
        print("left")
    case _:
        print("just the NEWS")'''

#swith case for number
number = int(input("enter a integer number:"))

match (number<0):
    case True:
        print("negative")
    case False:
        print("positive")
    case _:
        print("enter integers please")

#if number != 0:
#    print(number!=0)