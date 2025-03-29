#To Do application by fetching arguments and adding it to a file
#option to remove
import sys
todolist=[]
#provide options

#Read a file
file=open("test.txt","r")
todolist=file.readlines()
file.close

#add to Do
try:
    if len(sys.argv) >=3 and sys.argv[1].lower()=="add":
        todolist.append(f"\n{sys.argv[2]}")
    else:
        pass
        #print(f"{todolist}\n")
except Exception as ArgumentsError:
    print("check the menu")  


#Remove to Do
try:
    if len(sys.argv) >=3 and sys.argv[1].lower()=="remove":
        todolist.remove(f"{todolist[int(sys.argv[2])-1]}")
    else:
        pass
        #print(f"{todolist}\n")
except Exception as ArgumentsError:
    print("check the menu")

#Write , save and close
file=open("test.txt","w")
file.writelines(todolist)
file.close()

#Print the rules
print("#######################################")
print("This is your To Do list:")
print("#######################################")
print(f"{todolist}\n")
print("#######################################")
print("To add To Do, pass the below as args")
print("script add your_ToDo")
#print(f"{sys.argv[1]} {sys.argv[2]}")
print("#######################################")
print("To remove To Do, pass the below as args")
print("script remove 2")
#print(f"{sys.argv[1]} {sys.argv[2]}")
print("#######################################")
print("To add To Do, pass the below as args")
print("script")
print("#######################################")