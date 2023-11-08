from tkinter import END,Label,Entry,Frame,Button,Tk,PhotoImage
from PIL import ImageTk
from tkinter import messagebox
import pyodbc

#Functionality Part

def email_connect():
   if usernameEntry.get()=="" or passwordEntry.get()=="":
     messagebox.showerror("Error","All fields are required!")
   elif usernameEntry.get()=="Email" or passwordEntry.get()=="Password":
     messagebox.showerror("Error","All fields are required!",parent=login_window)   
     return
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again")
           return
        cursor = conn.cursor()
        query = "use Bank"
        cursor.execute(query)
        query1 = "select * from data where email = ? and password = ?"
        cursor.execute(query1,(usernameEntry.get(),passwordEntry.get()))
        row = cursor.fetchone()
        if row == None:
           messagebox.showerror("Error","Incorrect Email or Password")
        else:
           messagebox.showinfo("Welcome","Login Successful. Redirecting to Application...")
        cursor.close()
        bank_page()  

def email_login():
   useemailButton.config(text="Use Username Instead",command=user_login,font=("Microsoft Yahei UI  Light",8,"bold"))
   useemailButton.place(x=575,y=298)
   usernameEntry.delete(0,END)
   usernameEntry.insert(0,"Email")
   usernameEntry.bind("<FocusIn>",user_enter)
   passwordEntry.delete(0,END)
   passwordEntry.insert(0,"Password")
   loginButton.config(command=email_connect)

def user_login():
   useemailButton.config(text="Use Email Instead",font=("Microsoft Yahei UI  Light",9,"bold"),command=email_login)
   useemailButton.place(x=575,y=295)
   usernameEntry.delete(0,END)
   usernameEntry.insert(0,"Username")
   usernameEntry.bind("<FocusIn>",user_enter)
   passwordEntry.delete(0,END)
   passwordEntry.insert(0,"Password")
   loginButton.config(command=login_user)

   
   
def forgot_pass():
   def email_execute():
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again")
           return
       cursor = conn.cursor()
       query = "select * from data where email=?"
       cursor.execute(query,(user_entry.get()))
       row = cursor.fetchone()
       if row == None:
          messagebox.showerror("Error","Incorrect Email",parent=window)
       else:
          query = "update data set password=? where email=?"
          cursor.execute(query,(newpass_entry.get(),user_entry.get()))
          conn.commit()
          conn.close()
          messagebox.showinfo("Success","Your Password has been reset successfully, please log in to countinue",parent=window)
          window.destroy()

   def user_changepass():
      userLabel.config(text="Username")
      useemailButton1.config(text="Use Email Instead",command=email_changepass)
      submitButton.config(command=change_password)


   def email_changepass():
      userLabel.config(text="Email")
      useemailButton1.config(text="Use Username Instead",command=user_changepass)
      submitButton.config(command=email_execute)
      user_entry.delete(0,END)
      newpass_entry.delete(0,END)
      confirmpass_entry.delete(0,END)
   def change_password():
    if user_entry.get()=="" or newpass_entry.get()=="" or confirmpass_entry.get() =="":
      messagebox.showerror("Error","All Fields Are Required",parent=window)
    elif newpass_entry.get()!=confirmpass_entry.get():
       messagebox.showerror("Error","Password and Confirm Password does not match",parent=window)
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again")
           return
       cursor = conn.cursor()
       query = "select * from data where username = ?"
       cursor.execute(query,(user_entry.get()))
       row = cursor.fetchone()
       if row == None:
          messagebox.showerror("Error","Incorrect Username",parent=window)
       else:
          query = "update data set password = ? where username = ?"
          cursor.execute(query,(newpass_entry.get(),user_entry.get()))
          conn.commit()
          conn.close()
          messagebox.showinfo("Success","Your Password has been reset successfully, please log in to countinue",parent=window)
          window.destroy()

   window = Tk()
   window.title("Reset Password")
   window.resizable(False,False)

   bgPic = ImageTk.PhotoImage(file="background.jpg")
   bgLabel1 = Label(window,image=bgPic)
   bgLabel1.grid()

   heading_Label = Label(window,text="RESET PASSWORD",font=("arial",18,"bold"),bg="white",fg="magenta2")
   heading_Label.place(x=480,y=60)

   userLabel = Label(window,text="Username",font=("arial",12,"bold"),bg="white",fg="orchid1")
   userLabel.place(x=470,y=130)

   user_entry = Entry(window,width=25,fg="magenta2",font=("arial",11,"bold"),bd=0)
   user_entry.place(x=470,y=160)

   passwordLabel = Label(window,text="New Password",font=("arial",12,"bold"),bg="white",fg="orchid1")
   passwordLabel.place(x=470,y=210)

   newpass_entry = Entry(window,width=25,fg="magenta2",font=("arial",11,"bold"),bd=0)
   newpass_entry.place(x=470,y=240)

   confirmpassLabel = Label(window,text="Confirm Password",font=("arial",12,"bold"),bg="white",fg="orchid1")
   confirmpassLabel.place(x=470,y=290)

   confirmpass_entry = Entry(window,width=25,fg="magenta2",font=("arial",11,"bold"),bd=0)
   confirmpass_entry.place(x=470,y=320)

   useemailButton1 = Button(window,text="Use Email Instead",bd=0,bg="white",activebackground="white",cursor="hand2",font=("Microsoft Yahei UI Light",9,"bold"),fg="magenta2",activeforeground="white",command=email_changepass)
   useemailButton1.place(x=467,y=355)

   submitButton = Button(window,text="Submit",bd=0,bg="magenta2",fg="white",font=("Open Sans",16,"bold"),width=19,cursor="hand2",activebackground="white",activeforeground="white",command=change_password)
   submitButton.place(x=470,y=390)   

   window.mainloop()

def login_user():
    if usernameEntry.get()=="" or passwordEntry.get()=="":
     messagebox.showerror("Error","All fields are required!",parent=login_window)
     return
    elif usernameEntry.get()=="Username" or passwordEntry.get()=="Password":
     messagebox.showerror("Error","All fields are required!",parent=login_window)   
     return
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again")
           return
        cursor = conn.cursor()
        query = "use Bank"
        cursor.execute(query)
        query1 = "select * from data where username = ? and password = ?"
        cursor.execute(query1,(usernameEntry.get(),passwordEntry.get()))
        row = cursor.fetchone()
        if row == None:
           messagebox.showerror("Error","Incorrect Username or Password",parent=login_window)
           return
        else:
           messagebox.showinfo("Welcome","Login Successful. Redirecting to Appliation",parent=login_window)
           cursor.close()
           bank_page()

def bank_page():
    login_window.destroy()
    import bank

def signup_page():
    login_window.destroy()
    import signup

def show():
    closeeye.config(file="openeye.png")
    passwordEntry.config(show="")
    eyeButton.config(command=hide)

def hide():
    closeeye.config(file="closeye.png")
    passwordEntry.config(show="*")
    eyeButton.config(command=show)

def user_enter(event):
    if usernameEntry.get()=="Username" or usernameEntry.get()=="Email":
        usernameEntry.delete(0,END)

def pass_enter(event):
    if passwordEntry.get()=="Password":
        passwordEntry.delete(0,END)

#GUI Part
login_window = Tk()
login_window.geometry("990x660+50+50")
login_window.resizable(False,False)
login_window.title("Login Page")
img = PhotoImage(file="Signin.png")
login_window.iconphoto(False,img)

bgImage = ImageTk.PhotoImage(file="bg.jpg")
bgLabel = Label(login_window,image=bgImage)
bgLabel.pack()

heading = Label(login_window,text="USER LOGIN",font=("Microsoft Yahei UI Light",23,"bold"),bg="white",fg="firebrick1")
heading.place(x=605,y=120)

usernameEntry = Entry(login_window,width=25,font=("Microsoft Yahei UI Light",11,"bold"),bd=0,fg='firebrick1')
usernameEntry.place(x=580,y=200)
usernameEntry.insert(0,"Username")
usernameEntry.bind("<FocusIn>",user_enter)

frame1 = Frame(login_window,width=250,height=2,bg="firebrick1")
frame1.place(x=580,y=222)

passwordEntry = Entry(login_window,width=25,font=("Microsoft Yahei UI Light",11,"bold"),bd=0,fg='firebrick1')
passwordEntry.place(x=580,y=260)
passwordEntry.insert(0,"Password")
passwordEntry.config(show="*")
passwordEntry.bind("<FocusIn>",pass_enter)

frame2 = Frame(login_window,width=250,height=2,bg="firebrick1")
frame2.place(x=580,y=282)

closeeye = PhotoImage(file="closeye.png")
eyeButton = Button(login_window,image=closeeye,bd=0,bg="white",activebackground="white",cursor="hand2",command=show)
eyeButton.place(x=800,y=255)

forgotButton = Button(login_window,text="Forgot Password?",bd=0,bg="white",activebackground="white",cursor="hand2",font=("Microsoft Yahei UI Light",9,"bold"),fg="firebrick1",activeforeground="firebrick1",command=forgot_pass)
forgotButton.place(x=715,y=295)

useemailButton = Button(login_window,text="Use Email Instead",bd=0,bg="white",activebackground="white",cursor="hand2",font=("Microsoft Yahei UI Light",9,"bold"),fg="firebrick1",activeforeground="firebrick1",command=email_login)
useemailButton.place(x=575,y=295)

loginButton = Button(login_window,text = "Login", font = ("Open Sans",16,"bold"),fg="white",bg="firebrick1",activeforeground="firebrick1",activebackground="white",cursor="hand2",bd=0,width=19,command=login_user)
loginButton.place(x=578,y=350)

orLabel = Label(login_window,text="-------------- OR --------------",font=("Open Sans",16),fg = "firebrick1",bg="white")

facebook_logo = PhotoImage(file="facebook.png")
fbLabel = Label(login_window,image=facebook_logo,bg="white")
fbLabel.place(x=640,y=440)

google_logo = PhotoImage(file="google.png")
googleLabel = Label(login_window,image=google_logo,bg="white")
googleLabel.place(x=690,y=440)

twitter_logo = PhotoImage(file="twitter.png")
twitterLabel = Label(login_window,image=twitter_logo,bg="white")
twitterLabel.place(x=740,y=440)

signupLabel = Label(login_window,text="Don't have an account?",font=("Open Sans",9,"bold"),fg="firebrick1",bg="white")
signupLabel.place(x=590,y=500)

newaccountButton = Button(login_window,text = "Create One", font = ("Open Sans",9,"bold underline"),fg="blue",bg="white",activeforeground="blue",activebackground="white",cursor="hand2",bd=0,command=signup_page)
newaccountButton.place(x=727,y=500)

login_window.mainloop()