from tkinter import Tk,Label,Frame,Entry,Button,Checkbutton,IntVar
from PIL import ImageTk
import webbrowser
from tkinter import messagebox
import pyodbc
import re

def mailused():
   try:
         conn = pyodbc.connect(
            "Driver=SQL Server;"
            r"Server=HP-Notebook\SHREYASH;"
            "Database=Bank;"
            "Trusted_connection=No;"
            "UID=Bankapp;"
            "PWD=Bank123@1;"
         )
   except:
        messagebox.showerror("Error","Database Connectivity Issue! Please Try Again")
        return
   cursor = conn.cursor()
   cursor.execute("use Bank")
   cursor.execute("select * from data where email=?",(emailEntry.get()))
   row = cursor.fetchone()
   if row != None:
        return True
   else:
       return False

def checkmail(email):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
   if re.match(pat,email):
      return True
   return False

def connect_database():
    if emailEntry.get()=="" or passwordEntry.get()=="" or confirmEntry.get()=="" or usernameEntry.get()=="":
        messagebox.showerror("Error","All Fields are Required!")
    elif checkmail(emailEntry.get()) ==False:
        messagebox.showerror("Error","Please enter an valid mail")    
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror("Error","Password does not match")
    elif check.get()==0:
        messagebox.showerror("Error","Please Accept the Terms & Conditions")
    else:
        try:
         conn = pyodbc.connect(
            "Driver=SQL Server;"
            r"Server=HP-Notebook\SHREYASH;"
            "Database=Bank;"
            "Trusted_connection=No;"
            "UID=Bankapp;"
            "PWD=Bank123@1;"
         )
        except:
            messagebox.showerror("Error","Database Connectivity Issue! Please Try Again")
            return
        if mailused() == True:
            messagebox.showerror("Error","Email Already used!")
        else:
        
         cursor = conn.cursor()
         cursor.execute("use Bank")
         cursor.execute("select * from data where username=?",(usernameEntry.get ()))
         row = cursor.fetchone()
        
         if row != None:
            messagebox.showerror("Error","Username already taken")
         
         else:
          query = "insert into data(email,password,username) values (?,?,?)"
          cursor.execute(query,(emailEntry.get(),passwordEntry.get(),usernameEntry.get()))
          conn.commit()
          query2 = "insert into data2(Amount) values (0)"
          cursor.execute(query2)
          conn.commit()
          query1 = "select CustomerId from data where username = ?"
          cursor.execute(query1,usernameEntry.get())
          idtogive = cursor.fetchval()
          conn.close()
          messagebox.showinfo("Success",f"Your Account has been successfully created. Please login to continue. At the time of opening the application use your ID No. which is \"{idtogive}\"")
          login_page()


def login_page():
    signup_window.destroy()
    import signin

signup_window = Tk()
signup_window.title("Signup Page")
signup_window.resizable(False,False)
img = ImageTk.PhotoImage(file="CreateA_C.png")
signup_window.iconphoto(False,img)

background = ImageTk.PhotoImage(file="bg.jpg") 

bgLabel = Label(signup_window,image=background)
bgLabel.grid()

frame = Frame(signup_window,bg="white")
frame.place(x=546,y=101)

heading = Label(frame,text="CREATE AN ACCOUNT",font=("Microsoft Yahei UI Light",18,"bold"),bg="white",fg="firebrick1")
heading.grid(row=0,column=0,padx=10,pady=10)

emailLabel = Label(frame,text="Email",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="firebrick1")
emailLabel.grid(row=1,column=0,sticky="w",padx=25,pady=(10,0))

emailEntry = Entry(frame,width=20,font=("Microsoft Yahei UI Light",10,"bold"),bg="firebrick1",fg="white")
emailEntry.grid(row=2,column=0,sticky="w",padx=25)

usernameLabel = Label(frame,text="Username",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="firebrick1")
usernameLabel.grid(row=3,column=0,sticky="w",padx=25,pady=(10,0))

usernameEntry = Entry(frame,width=20,font=("Microsoft Yahei UI Light",10,"bold"),bg="firebrick1",fg="white")
usernameEntry.grid(row=4,column=0,sticky="w",padx=25)

passwordLabel = Label(frame,text="Password",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="firebrick1")
passwordLabel.grid(row=5,column=0,sticky="w",padx=25,pady=(10,0))

passwordEntry = Entry(frame,width=20,font=("Microsoft Yahei UI Light",10,"bold"),bg="firebrick1",fg="white")
passwordEntry.grid(row=6,column=0,sticky="w",padx=25)

confirmLabel = Label(frame,text="Confirm Password",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="firebrick1")
confirmLabel.grid(row=7,column=0,sticky="w",padx=25,pady=(10,0))

confirmEntry = Entry(frame,width=20,font=("Microsoft Yahei UI Light",10,"bold"),bg="firebrick1",fg="white")
confirmEntry.grid(row=8,column=0,sticky="w",padx=25)

check = IntVar()
termsandconditions = Checkbutton(frame,bg="white",activebackground="white",variable=check)
termsandconditions.grid(row=9,column=0,sticky="w",pady=10,padx=15)

thelink = Label(frame,text="I agree to the Terms and Conditions",fg="firebrick1",cursor="hand2",font=("Microsoft Yahei UI Light",9,"bold","underline"),bg="white")
thelink.grid(row=9,column=0,sticky="w",pady=10,padx=35)

thelink.bind("<Button-1>",
             lambda x:webbrowser.open_new_tab("https://www.app-privacy-policy.com/live.php?token=cfZtef5y0iwcWVnLe3NFkVq8Pt4Cimvd"))

signupbutton = Button(frame,text="Signup",font=("Open Sans",16,"bold"),bd=0,bg="firebrick1",fg="white",activebackground="firebrick1",activeforeground="white",width=17,command=connect_database,cursor="hand2")
signupbutton.grid(row=10,column=0,pady=10)

alreadyaccount = Label(frame,text="Already have a account?",font=("Opens Sans",9,"bold"),bg="white",fg="firebrick1")
alreadyaccount.grid(row=11,column=0,sticky="w",padx=25,pady=10)

loginbutton = Button(frame,text="Log In",font=("Open Sans",9,"bold","underline"),bg="white",fg="blue",bd=0,cursor="hand2",activebackground="white",activeforeground="blue",command=login_page)
loginbutton.place(x=170,y=401)

signup_window.mainloop()
