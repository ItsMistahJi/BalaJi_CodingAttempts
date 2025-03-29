#Map_Filter in python
'''class student:
    def __init__(self,name,score):
        self.name = name
        self.score = score

students = [student("Joe",0.46),student("Mac",0.56),student("Mark",0.76),student("Zach",0.75)]

students_result = []
for student in students:
#   if student.score >= 0.5:
#        students_result.append(f"{student.name} passed")
#    else:
#        students_result.append(f"{student.name} Failed")
    students_result.append(f"{student.name} Passed" if student.score >=0.5 else f"{student.name} Failed")

print(students_result)

map_results = list(map(lambda student:student.name,students))
map_results2=list(map(lambda student:student.score,students))
map_results3=list(map(lambda student:f"{student.name} Passed" if student.score >0.50 else f"{student.name} Failed",students))
map_results4=list(map(lambda student:f"{student.score}" if student.score <= 0.50 else f"{student.name}",students))
map_results5=list(map(lambda x:f"{student.score}" if student.score <= 0.50 else f"{student.name}",students))
print(map_results,map_results2,"\n",map_results3,"\n",map_results4,"\n\t",map_results5)'''

#my challnege
#multiply all numbers in the list by 2
'''numbers = [1,2,3,4,5]
print(numbers)
map_results=list(map(lambda number:number*2,numbers))
print(map_results)
map_results1=1
for number in numbers:
    map_results1*=number
#map_results1=map(lambda x:for number in numbers: map_results1*=number,numbers)
print(map_results1)'''

#filters
'''class student():
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def __repr__(self):
        return(f"{self.name}: {self.score}")
    
students = [student("Joe",0.46),student("Yao",0.42),student("Mac",0.56),student("Mark",0.76),student("Zach",0.75)]

fail_results=[]
for student in students:
    if student.score < 0.5:
        fail_results.append(f"{student.name}: {student.score}")

print(fail_results)
fail_results1=[]
fail_results1=list(filter(lambda student: student.score<0.50,students))
print(fail_results1)

#Reduce functions
total_score=0
for student in students:
    total_score+=student.score
print(total_score)
print(total_score/len(students))

from functools import reduce
reduce_avg = reduce(lambda total, student:student.score + total,students,0)
print(reduce_avg)
#challenge to filter only even numbers from list
numbers=[1,2,3,4,5]
even_numbers=[]
even_numbers=list(filter(lambda number:number % 2 == 0,numbers))
print(even_numbers)

from functools import reduce
reduce_list_sum=reduce(lambda total,number:number + total ,numbers,0)
reduce_list_multiply1=reduce(lambda total,number:number*total,numbers)
reduce_list_multiply2=reduce(lambda total,number:number*total,numbers,1)
print(reduce_list_sum)
print(reduce_list_multiply1)
print(reduce_list_multiply2)'''

#code challenge
class Student:
	def __init__(self, name, score):
		self.name = name
		self.score = score
	
	def __repr__(self): 
		return f"{self.name}: {self.score}"
	
students = [Student("Joe", 0.46), Student("Amy", 0.72), Student("Mark", 0.88), Student("Zach", 0.75), Student("Jane", 0.84), Student("Sarah", 0.63), Student("Mary", 0.55)]

names_with_M = list(filter(lambda student:student.name.startswith("M"),students))
print(names_with_M)