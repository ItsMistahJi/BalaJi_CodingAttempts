#Handling file systems
import sys
#from sys import argv
from functools import reduce

#for argument in sys.argv:
#    print(argument)

'''def multiplyArgs(arg1):
    #total=1
    #for arg in arg1:
    #    total*=arg
    total1=reduce(lambda total,arg:total * arg,arg1,1)
    #print(total1)
    return total1

nums=[]
for i in range(1,6):
    nums.append(int(input(f"Enter number {i} to multiply:")))
#print(multiplyArgs(nums))
print(reduce(lambda total,arg:total * arg,nums,1))'''

#Experiment failed
'''num=[]
for argument in sys.argv:
    num.append(int(argument))
print(num)
print(reduce(lambda total, arg:total + arg,num,2))'''
#handling sys arguments when first one is passed as file name
'''total =0
for argument in sys.argv[1]:
    try:
        number = int(argument)
        total +=number
    except Exception as e:
        print("file name is passed")

print(total)'''

#file creating and writing if file doesn't exist
#file = open("test1.txt", "x")
#file.write("Testing file writing")
#file.close()

#if to override/overwrite then
#file=open("test1.txt","w")
#file.write("testing file overrwrite")
#file.close()

#append an existin file
#file=open("test1.txt","a")
#file.write("Appending test")
#file.close()

#Challenge: file creation after passing its name as argument
'''argument = sys.argv[1]
try:
    file=open(argument,"w")
    file.write("Testing file name passed as argument")
    file.close()
except Exception as TypeError:
    print("file name is passed as argument")'''

#####################################################################
#file=open("test.txt","r")
#file.write("Testing read of file")
#file_text= file.read()
#print(file_text)
#lines=file.readlines()
#print(lines)
#for line in file:
#    print(line)
#file.close()
#file=open("test.txt","r")
#total=1
#for line in file:
#    if line!=" " and line!="\n":
#          total*=int(line)
#    try:
#        total*=float(line)
#    except Exception as Typeerror:
#        pass
#print(total)    
#file.close()

############################################
#editing a file
#file=open("test.txt","r")
#lines=file.readlines()
#file.close()

#lines=["adding","\n","More addition","\n","more lines"]
#lines.insert(4,"inserting lines\n")
#lines[1]="insert from var\n"
#lines.append("\nBye")

#file=open("test.txt","w")
#file.writelines(lines)
#file.close()

###############################################
#challenge: multiply each number in the file by 2
file=open("test.txt","r")
lines=file.readlines()
file.close()

for x in range(len(lines)):
    try:
        number=float(lines[x])*2
        lines[x]=f"{number}\n"
    except Exception as SpaceError:
        pass

file=open("test.txt","w")
file.writelines(lines)
file.close()