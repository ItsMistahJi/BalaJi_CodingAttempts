string = input('Enter the string: ')

#string = str.casefold()
#string == reversed(string)
if(string == string[::-1]):
    print("Yes")
else:
    print("No")