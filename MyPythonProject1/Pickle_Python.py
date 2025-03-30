#Pickle and Python
#first to understand
'''import pickle
class ToDo:
    def __init__(self,title,important,category="Normal"):
        self.title = title
        self.important= important
        self.category = category

todos_from_class = [ToDo("Eat",True),ToDo("sleep",True),ToDo("Repeat",False)]
listData = [23,34,5,45,6,7,8,88]

file=open("pickle_text.txt","wb")
#pickle.dump(listData,file)
pickle.dump(todos_from_class,file)
file.close()

file=open("pickle_text.txt","rb")
#printData = pickle.load(file)
printData = pickle.load(file)
file.close()

print(printData)'''