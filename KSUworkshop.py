from curses.ascii import isdigit
from sys import exception
from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
import hashlib
from random import randint
from tkinter import ttk
import csv
from datetime import datetime

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
             time TEXT NOT NULL,
             membersNum INT NOT NULL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Admin
             (Name TEXT PRIMARY KEY NOT NULL,
             Password TEXT NOT NULL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Booking
             (studentID INT UNIQUE NOT NULL,
             workshopID INT UNIQUE NOT NULL,
             FOREIGN KEY(studentID) REFERENCES Student(stuID) ,
             FOREIGN KEY(workshopID) REFERENCES WorkShop(Number) ,
             PRIMARY KEY (studentID,workshopID));''')
print("************** Student info **************")
cursor1.execute("Select * from Student")
print(cursor1.fetchall())
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
        self.label1 = tk.Label(self.frame1, text="Sign Up")
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
            reg = "^[0-9]{9}(@student.ksu.edu.sa)$"
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
            messagebox.showinfo("error", "something wrong happened and record not saved")


    def SLogin(self):
        self.Student_window = tk.Tk()
        self.Student_window.title("Login")
        self.Student_window.geometry("400x300")
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
        id=str(self.Id_entry.get())
        reg = "^[0-9]{9}$"
        x = re.search(re.compile(reg), id)
        if not x:
            messagebox.showinfo("Invalid student ID", "Student ID must be 9 digits")
            return
        password = str(self.Password_entry.get())
        hashedpass = hashlib.sha256(password.encode()).hexdigest()
        check = cursor3.execute("SELECT stuID FROM Student WHERE stuID = ? AND Password = ?", (id,hashedpass))
        if len(check.fetchall()) != 0:
            student_id = id
            # Create and show the student window
            self.stuWindow(student_id)
            self.Student_window.destroy()  # Close the login window
        else:
            messagebox.showinfo("Error", "password is incorrect")

    def stuWindow(self, student_id):
        self.student_id = student_id
        self.window = tk.Tk()
        self.window.title("Student Window")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Book a Workshop
        self.book_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.book_tab, text="Book a Workshop")

        # Create a Treeview to display workshops
        self.workshop_tree = ttk.Treeview(self.book_tab, columns=("Workshop ID", "Name", "Location", "Date", "Time"), show="headings")
        self.workshop_tree.heading("Workshop ID", text="Workshop ID")
        self.workshop_tree.heading("Name", text="Name")
        self.workshop_tree.heading("Location", text="Location")
        self.workshop_tree.heading("Date", text="Date")
        self.workshop_tree.heading("Time", text="Time")
        self.workshop_tree.pack(fill="both", expand=True)

        # Button to book a workshop
        self.book_button = tk.Button(self.book_tab, text="Book Workshop", command=self.book_workshop)
        self.book_button.pack()

        # Tab 2: View My Workshops
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="View My Workshops")

        # Create a Treeview to display booked workshops
        self.my_workshops_tree = ttk.Treeview(self.view_tab, columns=("Workshop ID", "Name", "Location", "Date", "Time"), show="headings")
        self.my_workshops_tree.heading("Workshop ID", text="Workshop ID")
        self.my_workshops_tree.heading("Name", text="Name")
        self.my_workshops_tree.heading("Location", text="Location")
        self.my_workshops_tree.heading("Date", text="Date")
        self.my_workshops_tree.heading("Time", text="Time")
        self.my_workshops_tree.pack(fill="both", expand=True)

        # Logout button
        self.logout_button = tk.Button(self.window, text="Logout", command=self.logout)
        self.logout_button.pack(side="bottom")

        self.populate_workshop_tree()
        self.populate_my_workshops_tree(student_id)

        self.window.mainloop()

    def populate_workshop_tree(self):
        conn = sqlite3.connect('KSUWorkShop.db')
        cursor = conn.cursor()

        # Modify query to match your table structure
        cursor.execute("SELECT Number, Name, Location, date, time FROM Workshops WHERE Capacity > (SELECT COUNT(*) FROM Bookings WHERE Bookings.workshopID = Workshops.Number)")
        workshops = cursor.fetchall()

        for workshop in workshops:
            self.workshop_tree.insert("", "end", values=workshop)

        conn.close()

    def populate_my_workshops_tree(self, student_id):
        conn = sqlite3.connect('KSUWorkShop.db')
        cursor = conn.cursor()

        # Modify query to match your table structure
        cursor.execute("SELECT Workshops.Number, Name, Location, date, time FROM Bookings INNER JOIN Workshops ON Bookings.workshopID = Workshops.Number WHERE Bookings.studentID = ?", (student_id))
        bookings = cursor.fetchall()

        for booking in bookings:
            self.my_workshops_tree.insert("", "end", values=booking)

        conn.close()

    def book_workshop(self):
        #selected_item = self.workshop_tree.selection()[0]
        #workshop_id = self.workshop_tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('KSUWorkShop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Workshop WHERE Number = workshopID AND Capacity > membersNum")
        workshop_info = cursor.fetchone()
        if not workshop_info:
            messagebox.showerror("Error", "Workshop is full or already booked")
            return

        cursor.execute("SELECT * FROM Booking WHERE studentID = stuID AND workshopID = number")
        if cursor.fetchone():
            messagebox.showerror("Error", "You have already booked this workshop")
            return

            # Book the workshop
        cursor.execute("INSERT INTO Booking (studentID, workshopID) VALUES (stuID, number)")
        cursor.execute("UPDATE Workshop SET membersNum = membersNum + 1 WHERE Number = number")
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Workshop booked successfully!")
        self.populate_my_workshops(self.student_id)  # Update the view



    def Alogin(self):
        self.Admin_window = tk.Tk()
        self.Admin_window.title("login")
        self.Admin_window.geometry("400x300")
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
        ID = str(self.Id_entry.get())
        reg = "^[0-9]{9}$"
        x = re.search(re.compile(reg), ID)
        if not x:
            messagebox.showinfo("Invalid ID", "ID must be 9 digits")
            return
        password = str(self.Password_entry.get())
        hashedpass = hashlib.sha256(password.encode()).hexdigest()
        check = cursor4.execute(f"SELECT Password FROM Admin WHERE Password = {hashedpass}")
        if len(check.fetchall()) != 0:
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


    def createWorkshop(self):
        try:
            conn = sqlite3.connect('KSUWorkShop.db')
            cursor5 = conn.cursor()
            # workshop info
            name = str(self.name_entry.get())
            if not name:
                messagebox.showinfo("missing input", "workshop name should not be empty")
                return
            location = str(self.location_entry.get())
            if not location:
                messagebox.showinfo("missing input", "workshop location should not be empty")
                return

            capacity = str(self.Capacity_entry.get())
            if isdigit(capacity):
                capacity = int(capacity)
            else:
                messagebox.showinfo("invalid input", "workshop capacity should be integer")
            # validate date
            date = str(self.date_entry.get())
            reg = "^(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/[0-9]{4}$"
            x = re.search(re.compile(reg), date)
            if not x:
                messagebox.showinfo("invalid Date format","date format must be dd/mm/yyyy")
                return
            time = str(self.time_entry.get())
            # validate time
            reg = "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
            x = re.search(re.compile(reg), time)
            if not x:
                messagebox.showinfo("invalid Time format", "Time format must be in form of hh:MM")
                return
            number=str(randint(10000, 99999))
            sql = """INSERT INTO WorkShop VALUES('{}','{}','{}','{}','{}','{}',{})""".format(number,name, location, capacity, date, time,0)
            cursor5.execute(sql)
            conn.commit()
            messagebox.showinfo("Done", "workshop information has been saved")
        except sqlite3:
            messagebox.showinfo("Error","something wrong in database")
        except:
            messagebox.showinfo("Error","something wrong")


    def BackUp(self):
        file=open("workshop.CSV","a",newline='')
        csvwriter=csv.writer(file)
        csvwriter.writerow(['number','Name','Location','Capacity','Date','Time'])
        conn = sqlite3.connect('KSUWorkShop.db')
        cursor6 = conn.cursor()
        date=cursor6.execute("SELECT * FROM WorkShop")
        csvwriter.writerows(date)
        file.close()
        conn.close()




    def logout(self):
        self. __init__()

test=GUI()

