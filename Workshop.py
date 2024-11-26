from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
import hashlib
from random import randint
from tkinter import ttk

conn = sqlite3.connect("KSUWorkShop.db")
cursor1 = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS Student
             (stuID INT PRIMARY KEY NOT NULL,
             FName TEXT NOT NULL,
             LName TEXT NOT NULL,
             Password TEXT NOT NULL,
             Email TEXT NOT NULL,
             Number INT NOT NULL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS WorkShop
             (Number INT PRIMARY KEY NOT NULL,
             Name TEXT NOT NULL,
             Location TEXT NOT NULL,
             Capacity INT NOT NULL,
             date TEXT NOT NULL,
             time TEXT NOT NULL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Admin
             (Name TEXT PRIMARY KEY NOT NULL,
             Password TEXT NOT NULL);''')
print("************** Student info **************")
cursor1.execute("Select * from Student")
print(cursor.fetchall())
print("************** WorkShop info **************")
cursor1.execute("Select * from WorkShop")
print(cursor1.fetchall())
print("************** Admin info **************")
cursor1.execute("Select * from Admin")
print(cursor1.fetchall())
conn.close()


class GUI:
    def __init__(self):
        self.Main_window = tk.Tk()
        self.Main_window.title("SignUp")
        self.Main_window.geometry("500x500")
        self.Main_window.configure(background="white")
        self.frame1 = tk.Frame(self.Main_window)
        self.frame2 = tk.Frame(self.Main_window)
        self.frame3 = tk.Frame(self.Main_window)
        self.frame4 = tk.Frame(self.Main_window)
        self.frame5 = tk.Frame(self.Main_window)
        self.frame6 = tk.Frame(self.Main_window)
        self.frame7 = tk.Frame(self.Main_window)
        self.frame8 = tk.Frame(self.Main_window)
        self.label = tk.Label(self.frame1, text="Sign Up")
        self.label2 = tk.Label(self.frame2, text="First Name")
        self.label3 = tk.Label(self.frame3, text="Last Name")
        self.label4 = tk.Label(self.frame4, text="ID")
        self.label5 = tk.Label(self.frame5, text="Password")
        self.label6 = tk.Label(self.frame6, text="Email")
        self.label7 = tk.Label(self.frame7, text="Number")
        self.Fname_entry = tk.Entry(self.frame2)
        self.Lname_entry = tk.Entry(self.frame3)
        self.Id_entry = tk.Entry(self.frame4)
        self.Password_entry = tk.Entry(self.frame5)
        self.Email_entry = tk.Entry(self.frame6)
        self.number_entry = tk.Entry(self.frame7)
        self.button1 = tk.Button(self.frame8, text="Submit", command=self.saveInfo)
        self.button2 = tk.Button(self.frame8, text="student login", command=self.SLogin)
        self.button3 = tk.Button(self.frame8, text="Admin login", command=self.Alogin)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()
        self.frame6.pack()
        self.frame7.pack()
        self.frame8.pack()
        self.label1.pack()
        self.label2.pack(side=tk.LEFT)
        self.Fname_entry.pack(side=tk.RIGHT)
        self.label3.pack(side=tk.LEFT)
        self.Lname_entry.pack(side=tk.RIGHT)
        self.label4.pack(side=tk.LEFT)
        self.Id_entry.pack(side=tk.RIGHT)
        self.label5.pack(side=tk.LEFT)
        self.Password_entry.pack(side=tk.RIGHT)
        self.label6.pack(side=tk.LEFT)
        self.Email_entry.pack(side=tk.RIGHT)
        self.label7.pack(side=tk.LEFT)
        self.number_entry.pack(side=tk.RIGHT)
        self.button1.pack()
        self.button2.pack(side=tk.LEFT)
        self.button3.pack(side=tk.RIGHT)

        tk.mainloop()


def saveInfo(self):
    try:
        conn = sqlite3.connect('KSUWorkShop.db')
        cursor2 = conn.cursor()
        # first &last Name
        firstname = str(self.Fname_entry.get())
        lastname = str(self.Lname_entry.get())
        if not firstname or not lastname:
            messagebox.showinfo("missing input", "first name and last name should not be empty")
            return
        # student id
        stuID = str(self.Id_entry.get())
        reg = "^[0-9]{9}$"
        x = re.search(re.compile(reg), stuID)
        # validate StuID
        if not x:
            messagebox.showinfo("Invalid student ID", "Student ID must be 9 digits")
            return
        # validate password
        password = str(self.Password_entry.get())
        reg = "^[A-Za-z0-9]{6,15}$"
        pat = re.compile(reg)
        x = re.search(pat, password)
        if not x:
            password = ''
            messagebox.showinfo("invalid password format","password must consists at least of 6 digits or letters")
            return
        # password enc
        hashedpass=hashlib.sha256(password.encode()).hexdigest()

        # validate email
        email = str(self.Email_entry.get())
        reg = "^([a-zA-Z0-9\._-]+){9}(@student\.ksu\.edu\.sa)$"
        z = re.search(re.compile(reg), email)
        if not z:
            messagebox.showinfo("invalid Email", "Email should be in formate of xxxxxxxx@student.ksu.edu.sa ")
            return

        # validate phone
        mobile = str(self.number_entry.get())
        reg2 = "^(05)[0-9]{8}$"
        y = re.search(re.compile(reg2), mobile)
        if not y:
            messagebox.showinfo("Invalid Mobile Number","Mobile Number must be consists of 10 digits and starts with \'05\'")
            return

        # insert and check if id exists
        id = cursor2.execute(f"SELECT stuID FROM Student WHERE stuID = {stuID}")
        if len(id.fetchall()) == 0:
            sql = """INSERT INTO Student VALUES('{}','{}','{}','{}','{}','{}')""".format(stuID, firstname, lastname, hashedpass ,email, mobile)
            cursor2.execute(sql)
            conn.commit()
            messagebox.showinfo("Done", "Your information has been saved")

        else:
            messagebox.showinfo("Error", "ID already exist")
        conn.close()
    except sqlite3.Error:
        messagebox.showinfo("database error", "DataBase ERROR")

    except:
        messagebox.showinfo("error", "something wrong happend and record not saved")


def SLogin(self):
    self.Student_window = tk.Tk()
    self.Student_window.title("Login")
    self.Student_window.geometry("500x500")
    self.Student_window.configure(background="white")
    self.frame1 = tk.Frame(self.Student_window)
    self.frame2 = tk.Frame(self.Student_window)
    self.frame3 = tk.Frame(self.Student_window)
    self.frame4 = tk.Frame(self.Student_window)
    self.label1 = tk.Label(self.frame1, text="Student Login")
    self.label2 = tk.Label(self.frame2, text="ID")
    self.label3 = tk.Label(self.frame3, text="Password")
    self.Id_entry = tk.Entry(self.frame2)
    self.Password_entry = tk.Entry(self.frame3)
    self.button1 = tk.Button(self.frame4, text="Log in", command=self.ScheckLogIn)

    self.frame1.pack()
    self.frame2.pack()
    self.frame3.pack()
    self.frame4.pack()
    self.label1.pack()
    self.label2.pack(side=tk.LEFT)
    self.label3.pack(side=tk.LEFT)
    self.Id_entry.pack(side=tk.RIGHT)
    self.Password_entry.pack(side=tk.RIGHT)
    self.button1.pack()
    self.Student_window.mainloop()
    self.Student_window.destroy()

def ScheckLogIn(self):
    conn = sqlite3.connect('KSUWorkShop.db')
    cursor3 = conn.cursor()
    password = str(self.Password_entry.get())
    hashedpass = hashlib.sha256(password.encode()).hexdigest()
    id = cursor3.execute(f"SELECT Password FROM Student WHERE Password = {hashedpass}")
    if len(id.fetchall()) != 0:
        self.stuWindow()
    else:
        messagebox.showinfo("Error", "password is incorrect")

def stuWindow(self):
    self.Student_window2 = tk.Tk()
    self.Student_window2.title("Hello{}".format(self.Fname_entry.get()))
    self.Student_window2.geometry("500x500")
    self.Student_window2.configure(background="white")
    self.frame1 = tk.Frame(self.Student_window2)
    self.frame2 = tk.Frame(self.Student_window2)
    self.button1 = tk.Button(self.frame1, text="View Booking", command=self.ViewBook)
    self.button2 = tk.Button(self.frame1, text="Book", command=self.Book)
    self.button3 = tk.Button(self.frame2, text="Log out", command=self.Logout)

    self.frame1.pack()
    self.frame2.pack()
    self.button1.pack(side=tk.LEFT)
    self.button2.pack(side=tk.RIGHT)
    self.button3.pack()
    self.Student_window2.mainloop()
    self.Student_window2.destroy()

def Alogin(self):
    self.Admin_window = tk.Tk()
    self.Admin_window.title("login")
    self.Admin_window.geometry("500x500")
    self.Admin_window.configure(background="white")
    self.frame1 = tk.Frame(self.Admin_window)
    self.frame2 = tk.Frame(self.Admin_window)
    self.frame3 = tk.Frame(self.Admin_window)
    self.frame4 = tk.Frame(self.Admin_window)
    self.label1 = tk.Label(self.frame1, text="Admin Login")
    self.label2 = tk.Label(self.frame2, text="ID")
    self.label3 = tk.Label(self.frame3, text="Password")
    self.Id_entry = tk.Entry(self.frame2)
    self.Password_entry = tk.Entry(self.frame3)
    self.button1 = tk.Button(self.frame4, text="Log in", command=self.AcheckLogIn)

    self.frame1.pack()
    self.frame2.pack()
    self.frame3.pack()
    self.frame4.pack()
    self.label1.pack()
    self.label2.pack(side=tk.LEFT)
    self.label3.pack(side=tk.LEFT)
    self.Id_entry.pack(side=tk.RIGHT)
    self.Password_entry.pack(side=tk.RIGHT)
    self.button1.pack()
    self.Admin_window.mainloop()
    self.Admin_window.destroy()

def AcheckLogIn(self):
    conn = sqlite3.connect('KSUWorkShop.db')
    cursor4 = conn.cursor()
    password = str(self.Password_entry.get())
    hashedpass = hashlib.sha256(password.encode()).hexdigest()
    id = cursor4.execute(f"SELECT Password FROM Admin WHERE Password = {hashedpass}")
    if len(id.fetchall()) != 0:
        self.AdminWindow()
    else:
        messagebox.showinfo("Error", "password is incorrect")


def AdminWindow(self):
    self.Admin_window2 = tk.Tk()
    self.Admin_window2.title("Admin")
    self.Admin_window2.geometry("500x500")
    self.Admin_window2.configure(background="white")
    self.frame1 = tk.Frame(self.Admin_window2)
    self.frame2 = tk.Frame(self.Admin_window2)
    self.frame3 = tk.Frame(self.Admin_window2)
    self.frame4 = tk.Frame(self.Admin_window2)
    self.frame5 = tk.Frame(self.Admin_window2)
    self.frame6 = tk.Frame(self.Admin_window2)
    self.frame7 = tk.Frame(self.Admin_window2)
    self.frame8 = tk.Frame(self.Admin_window2)
    self.label1 = tk.Label(self.frame1, text="Rigster New workshop")
    self.label2 = tk.Label(self.frame2, text="workshop Name")
    self.label3 = tk.Label(self.frame3, text="Workshop location")
    self.label4 = tk.Label(self.frame3, text="Workshop capacity")
    self.label5 = tk.Label(self.frame4, text="Date")
    self.label6 = tk.Label(self.frame5, text="Time")
    self.name_entry = tk.Entry(self.frame2)
    self.location_entry = tk.Entry(self.frame3)
    self.capacity_entry = tk.Entry(self.frame4)
    self.date_entry = tk.Entry(self.frame5)
    self.time_entry = tk.Entry(self.frame6)
    self.button1 = tk.Button(self.frame7, text="create", command=self.createWorkshop)
    self.button2 = tk.Button(self.frame7, text="BackUp", command=self.BackUp)
    self.button3 = tk.Button(self.frame8, text="Log out", command=self.Logout)

    self.frame1.pack()
    self.frame2.pack()
    self.frame3.pack()
    self.frame4.pack()
    self.frame5.pack()
    self.frame6.pack()
    self.frame7.pack()
    self.frame8.pack()
    self.label1.pack()
    self.label2.pack(side=tk.LEFT)
    self.label3.pack(side=tk.LEFT)
    self.label4.pack(side=tk.LEFT)
    self.label5.pack(side=tk.LEFT)
    self.label6.pack(side=tk.LEFT)
    self.name_entry.pack(side=tk.RIGHT)
    self.location_entry.pack(side=tk.RIGHT)
    self.capacity_entry.pack(side=tk.RIGHT)
    self.date_entry.pack(side=tk.RIGHT)
    self.time_entry.pack(side=tk.RIGHT)
    self.button1.pack()
    self.button2.pack()
    self.button3.pack()
    self.Admin_window.mainloop()
    self.Admin_window.destroy()

def logout(self):
    self. __init__()

def workshop(self):

        