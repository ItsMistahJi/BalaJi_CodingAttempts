#pickle_ToDo
#Failed to revisit time to time
#To Do application by fetching arguments and adding it to a file
#option to remove
import sys
import pickle
todolist=[]
file_name="pickletest.txt"
#provide options

#Read a file
try:
    #file=open("test.txt","r")
    file=open(file_name,"rb")
    #todolist=file.readlines()
    todolist=pickle.load(file)
    file.close()
except FileNotFoundError:
    print(f"{file_name} is not found")
except (EOFError,pickle.UnpicklingError) as e:
    print(f"Error: {e}")

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
try:
    #file=open("test.txt","w")
    file=open(file_name,"wb")
    #file.writelines(todolist)
    pickle.dump(todolist,file)
    file.close()
except Exception as e:
    print(f"Error: {e}")


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