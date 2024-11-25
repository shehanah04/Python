from curses.ascii import isdigit


class Student:
    def __init__(self, first_name, last_name,ID,password,email,number):
        self.first_name = first_name
        self.last_name = last_name
        if len(ID)==9 and isdigit(ID):
            self.ID = ID
        if len(password)>=6:
            self.password = password
        temp=email.split('@')
        if temp[1]=="student.ksu.edu.sa":
            self.email = email
        if number.startswith("05") and len(number)==10:
            self.number = number



