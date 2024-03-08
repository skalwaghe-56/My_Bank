_developer_ = "Shreyash Kalwaghe"
_copyright_ = "Copyright (C) 2023, Shreyash Kalwaghe"
_credits_ = "Shreyash Kalwaghe"
_version_ = "1.1.1"
_email_ = "skalwaghe56@gmail.com"
_status_ = "Beta"

_Appname_ = "Shreyash's Bank"

from tkinter import messagebox,Tk,Label,Button,Entry,END,Toplevel
from PIL import ImageTk,Image
import pyodbc,urllib3,webbrowser

#lock part

def lock_login():
    if cusidentry.get() == "Customer ID" or passwordentry.get() == "Password":
        messagebox.showerror("Error","All Fields Are Required",parent=window)
        return
    elif cusidentry.get() == "" or passwordentry.get()=="":
        messagebox.showerror("Error","All Fields Are Required",parent=window)
        return
    elif cusidentry.get().isnumeric() == False:
        messagebox.showerror("Error","Please enter a valid Customer Id",parent=window)
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=window)
           return
        cursor = conn.cursor()
        query = "use Bank"
        cursor.execute(query)
        query1 = "select * from data where CustomerId = ? and password = ?"
        cursor.execute(query1,(cusidentry.get(),passwordentry.get()))
        ft = cusidentry.get()
        row = cursor.fetchone()
        if row == None:
           messagebox.showerror("Error","Incorrect CustomerId or Password",parent=window)
           return
        else:
           messagebox.showinfo("Welcome","Opening Application...",parent=window)
        cursor.close()
        window.destroy()
        #Bank app

        def show_name():
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=bank_window)
           return 
          cursor = conn.cursor()
          query = "use Bank"
          cursor.execute(query)
          query1 = "select username from data where CustomerId = ?"
          cursor.execute(query1,ft)
          for row in cursor:
           username = [elem for elem in row]
          name = username[0] 
          cursor.close()
          accholdername.config(text=f"A/C Holder Name: {name}")
          showname.config(text="Hide A/C Holder Name",command=hide_name)

        def hide_name():
          accholdername.config(text="A/C Holder Name: XXXXXX XXXXX XXXXXXXX")
          showname.config(text="Show A/C Holder Name",command=show_name)   

        def hide_amount():
          amountlabel.config(text="₹X,XXX,XXX")
          showamount.config(text="Show \nAmount",command=show_amount)                    

        def transfer_window():
           def transfer_money():
            if amounttransferentry.get() == "" or receivername.get() == "":
               messagebox.showerror("Error","Please fill all the fields.",parent=transfer_win)
               return
            elif amounttransferentry.get().isnumeric() == False:
               messagebox.showerror("Error","Please enter a valid amount!",parent=transfer_win)
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
                  messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=transfer_win)
                  return
               totransfer = int(amounttransferentry.get())
               cursor = conn.cursor()
               query2 = "use Bank"
               cursor.execute(query2)
               query3 = "select Amount from data2 where CustomerId = ?"
               cursor.execute(query3,ft)
               for row in cursor:
                  prevamount = [elem for elem in row]
               preamount = prevamount[0]
               realtransfer =  preamount - totransfer
               query4 = "select * from data where username = ?"
               cursor.execute(query4,receivername.get())
               row= cursor.fetchone()
               if realtransfer < 0:
                  messagebox.showerror("Error","No Sufficient Balance.",parent=transfer_win)
                  return
               elif row == None:
                  messagebox.showerror("Error","No such user.",parent=transfer_win)
                  return
               else:
                  query5 = "select CustomerId from data where username = ?"
                  cursor.execute(query5,receivername.get())
                  for row in cursor:
                     receiverid = [elem for elem in row]
                  receiversid = receiverid[0]
                  query6 = "select Amount from data2 where CustomerId = ?"
                  cursor.execute(query6,receiversid)
                  for row in cursor:
                     receiveramt = [elem for elem in row]
                  receiversamt = receiveramt[0]
                  if receiversamt + totransfer > 100000000:
                     messagebox.showerror("Error","Receiver's Amount limit reached.",parent=transfer_win)
                     return
                  else:
                     finaltransfer = receiversamt + totransfer
                     query7 = "update data2 set Amount = ? where CustomerId = ?"
                     cursor.execute(query7,finaltransfer,receiversid)
                     query8 = "update data2 set Amount = ? where CustomerId = ?"
                     cursor.execute(query8,realtransfer,ft)
                     cursor.commit()
                     cursor.close()
                     messagebox.showinfo("Success",f"You have transferred ₹{totransfer} to {receivername.get()} successfully.",parent=transfer_win)
                     transfer_win.destroy()
                     bank_window.deiconify()

           def cancel_transfer():
             if messagebox.askokcancel("Quit","Do you want to quit transferring?",parent=transfer_win):
                transfer_win.destroy()
                bank_window.deiconify()

           bank_window.withdraw()
           transfer_win = Toplevel()
           transfer_win.geometry("%dx%d+%d+%d" % (300,150,600,300))
           transfer_win.title("Transfer")
           transfer_win.resizable(False,False)
           transfer_win.config(bg="white")
           img = ImageTk.PhotoImage(file="_internal/Transfer.png")
           transfer_win.iconphoto(False,img)

           implabel = Label(transfer_win,text="Transfer Money to Bank A/C",font=("arial",10,"bold"),bg="white",fg="dark blue")
           implabel.place(x=5,y=5)

           amountttotransfer = Label(transfer_win,text="Amount to Transfer:",font=("arial",10,"bold"),bg="white",fg="black")
           amountttotransfer.place(x=5,y=50)

           amounttransferentry = Entry(transfer_win,width=10,font=("arial",10,"bold"),bd=0,fg="black",bg="grey")
           amounttransferentry.place(x=143,y=51)

           whomtotransfer = Label(transfer_win,text="Receiever's Username:",font=("arial",10,"bold"),bg="white",fg="black")
           whomtotransfer.place(x=5,y=80)

           receivername = Entry(transfer_win,width=10,font=("arial",10,"bold"),bd=0,fg="black",bg="grey")
           receivername.place(x=160,y=81)

           transferbutton = Button(transfer_win,width=15,text="Transfer Money",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=transfer_money)
           transferbutton.place(x=100,y=110)

           canceltransferbutton = Button(transfer_win,width=8,text="Cancel",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=cancel_transfer)
           canceltransferbutton.place(x=220,y=110)

           def transferclose():
              if messagebox.askokcancel("Quit","Do you want to quit transferring?",parent=transfer_win):
                  transfer_win.destroy()
                  bank_window.deiconify()
           transfer_win.protocol("WM_DELETE_WINDOW",transferclose)

        def withdraw_window():
           def withdraw_money():
              if amountentry.get() == "":
                 messagebox.showerror("Error","Please enter a valid number.",parent=withdraw_win)
                 return
              elif amountentry.get().isnumeric() == False:
                 messagebox.showerror("Error","Please enter a valid amount!",parent=withdraw_win)
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
                  messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=withdraw_win)
                  return  
                 towithdraw = int(amountentry.get())
                 cursor = conn.cursor()
                 query2 = "use Bank"
                 cursor.execute(query2)
                 query3 = "select Amount from data2 where CustomerId = ?"
                 cursor.execute(query3,ft)
                 for row in cursor:
                  amt = [elem for elem in row]
                 previousamt = amt[0]
                 presentamt = previousamt - towithdraw
                 if presentamt < 0:
                    messagebox.showerror("Error","No Sufficient Balance",parent=withdraw_win)
                    return
                 else:
                  query4 = "update data2 set Amount = ? where CustomerId = ?"
                  cursor.execute(query4,presentamt,ft)
                  conn.commit()
                  cursor.close()
                  messagebox.showinfo("Success",f"You have withdrawn ₹{towithdraw} successfully.",parent=withdraw_win)
                  withdraw_win.destroy()
                  bank_window.deiconify()  
            
           def cancel_withdraw():
             if messagebox.askokcancel("Quit","Do you want to quit withdrawing?",parent=withdraw_win):
                withdraw_win.destroy()
                bank_window.deiconify()

           bank_window.withdraw()
           withdraw_win = Toplevel()
           withdraw_win.geometry("%dx%d+%d+%d" % (300,150,600,300))
           withdraw_win.title("Withdraw")
           withdraw_win.resizable(False,False)
           withdraw_win.config(bg="white")
           img = ImageTk.PhotoImage(file="_internal/Withdraw.png")
           withdraw_win.iconphoto(False,img)

           implabel = Label(withdraw_win,text="Withdraw Money from your Bank A/C",font=("arial",10,"bold"),bg="white",fg="dark blue")
           implabel.place(x=5,y=5)

           amttowithdraw = Label(withdraw_win,text="Amount to Withdraw:",font=("arial",10,"bold"),bg="white",fg="black")
           amttowithdraw.place(x=5,y=50)

           amountentry = Entry(withdraw_win,width=10,font=("arial",10,"bold"),bd=0,fg="black",bg="grey")
           amountentry.place(x=143,y=51)

           withdrawbutton = Button(withdraw_win,width=15,text="Withdraw Money",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=withdraw_money)
           withdrawbutton.place(x=100,y=100)

           canbutton = Button(withdraw_win,width=8,text="Cancel",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=cancel_withdraw)
           canbutton.place(x=220,y=100)

           def withdrawclose():
              if messagebox.askokcancel("Quit","Do you want to quit withdrawing?",parent=withdraw_win):
                  withdraw_win.destroy()
                  bank_window.deiconify()
           withdraw_win.protocol("WM_DELETE_WINDOW",withdrawclose)              
  
        def deposit_window():
           def deposit_money():
              if amtentry.get() == "":
                 messagebox.showerror("Error","Please enter a valid number.",parent=deposit_win)
                 return
              elif amtentry.get().isnumeric() == False:
                 messagebox.showerror("Error","Please enter a valid amount!",parent=deposit_win)
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
                  messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=deposit_win)
                  return  
                 todeposit = int(amtentry.get())
                 cursor = conn.cursor()
                 query2 = "use Bank"
                 cursor.execute(query2)
                 query3 = "select Amount from data2 where CustomerId = ?"
                 cursor.execute(query3,ft)
                 for row in cursor:
                  amt = [elem for elem in row]
                 previousamt = amt[0] 
                 presentamt = previousamt + todeposit
                 if presentamt > 100000000:
                    messagebox.showerror("Error","Balance limit crossed",parent=deposit_win)
                    return
                 else:
                  query4 = "update data2 set Amount = ? where CustomerId = ?"
                  cursor.execute(query4,presentamt,ft)
                  conn.commit()
                  cursor.close()
                  messagebox.showinfo("Success",f"You have deposited ₹{todeposit} successfully.",parent=deposit_win)
                  deposit_win.destroy()
                  bank_window.deiconify()  
            
           def cancel_deposit():
             if messagebox.askokcancel("Quit","Do you want to quit depositing?",parent=deposit_win):
                deposit_win.destroy()
                bank_window.deiconify()

           bank_window.withdraw()
           deposit_win = Toplevel()
           deposit_win.geometry("%dx%d+%d+%d" % (300,150,600,300))
           deposit_win.title("Deposit")
           deposit_win.resizable(False,False)
           deposit_win.config(bg="white")
           img = ImageTk.PhotoImage(file="_internal/Deposit.png")
           deposit_win.iconphoto(False,img)

           mainlabel = Label(deposit_win,text="Deposit Money into your Bank A/C",font=("arial",12,"bold"),bg="white",fg="dark blue")
           mainlabel.place(x=5,y=5)

           amttodeposit = Label(deposit_win,text="Amount to Deposit:",font=("arial",10,"bold"),bg="white",fg="black")
           amttodeposit.place(x=5,y=50)

           amtentry = Entry(deposit_win,width=10,font=("arial",12,"bold"),bd=0,fg="black",bg="grey")
           amtentry.place(x=140,y=51)

           depositbutton = Button(deposit_win,width=15,text="Deposit Money",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=deposit_money)
           depositbutton.place(x=100,y=100)

           cancelbutton = Button(deposit_win,width=8,text="Cancel",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=cancel_deposit)
           cancelbutton.place(x=220,y=100)

           def depositclose():
              if messagebox.askokcancel("Quit","Do you want to quit depositing?",parent=deposit_win):
                  deposit_win.destroy()
                  bank_window.deiconify()
           deposit_win.protocol("WM_DELETE_WINDOW",depositclose)              

        def show_amount():
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
           messagebox.showerror("Error","Could not establish Database Connection, Please Try Again",parent=bank_window)
           return
          cursor = conn.cursor()
          query = "use Bank"
          cursor.execute(query)
          query1 = "select Amount from data2 where CustomerId = ?"
          cursor.execute(query1,ft)
          for row in cursor:
           amount = [elem for elem in row]
          amt = amount[0] 
          amountlabel.config(text=f"₹{amt}")
          showamount.config(text="Hide \nAmount",command=hide_amount)

        def sign_out():
           result = messagebox.askyesno("Confirm","Do you want to sign out?",parent=bank_window)
           if result == True:
              bank_window.destroy()
              import signin
           else:
              return   


        def close_acc():
           def cancel_close():
              messagebox.askyesno("Confirm","Are you sure you want to quit?",parent=closeacc_win)
              closeacc_win.destroy()
              bank_window.deiconify()
           def close_ac():
              if customeridentry.get() == "" or passwordentry1.get()=="":
                 messagebox.showerror("Error","Please fill out all the fields.",parent=closeacc_win)
                 return
              elif customeridentry.get().isnumeric() == False:
                 messagebox.showerror("Error","Please enter a valid CustomerId!",parent=closeacc_win)
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
                    messagebox.showerror("Error","Database Connectivity Issue! Please try again later.",parent=closeacc_win)
                    return
                 cursor = conn.cursor()
                 query2 = "use Bank"
                 cursor.execute(query2)
                 query3 = "select * from data where CustomerId = ? and password = ?"
                 cursor.execute(query3,customeridentry.get(),passwordentry1.get())
                 row = cursor.fetchone()
                 if row == None:
                    messagebox.showerror("Error","Incorrect CustomerId or Password.",parent=closeacc_win)
                    return
                 else:
                    result = messagebox.askyesno("Warning","All your balance will be lost. Make sure the balance is 0.",parent=closeacc_win)
                    if result == False:
                       return
                    else:
                     query4 = "delete from data where CustomerId = ?"
                     cursor.execute(query4,customeridentry.get())
                     query5 = "delete from data2 where CustomerId = ?"
                     cursor.execute(query5,customeridentry.get())
                     cursor.commit()
                     cursor.close() 
                     messagebox.showinfo("Success","Your A/C has been deleted Successfully!",parent=closeacc_win)
                     closeacc_win.destroy()
                     bank_window.destroy()
                     import signup

           bank_window.withdraw()
           closeacc_win = Toplevel()
           closeacc_win.geometry("%dx%d+%d+%d" % (300,150,600,300))
           closeacc_win.title("Close A/C")
           closeacc_win.resizable(False,False)
           closeacc_win.config(bg="white")
           img = ImageTk.PhotoImage(file="_internal/DeleteA_C.png")
           closeacc_win.iconphoto(False,img)
           
           implabel = Label(closeacc_win,text="Close Bank A/C",font=("arial",15,"bold"),bg="white",fg="dark blue")
           implabel.place(x=10,y=5)

           customerid = Label(closeacc_win,text="CustomerId:",font=("arial",10,"bold"),bg="white",fg="black")
           customerid.place(x=10,y=50)

           customeridentry = Entry(closeacc_win,width=10,font=("arial",10,"bold"),bd=0,fg="black",bg="grey")
           customeridentry.place(x=100,y=51)

           password1 = Label(closeacc_win,text="Password:",font=("arial",10,"bold"),bg="white",fg="black")
           password1.place(x=10,y=80)

           passwordentry1 = Entry(closeacc_win,width=10,font=("arial",10,"bold"),bd=0,fg="black",bg="grey")
           passwordentry1.place(x=100,y=81)

           closeacbutton = Button(closeacc_win,width=15,text="Close A/C",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=close_ac)
           closeacbutton.place(x=100,y=110)

           cancelcloseacbutton = Button(closeacc_win,width=8,text="Cancel",font=("arial",8,"bold"),bd=0,fg="white",bg="blue",activebackground="white",activeforeground="black",command=cancel_close)
           cancelcloseacbutton.place(x=220,y=110)

           def closeacclose():
                  closeacc_win.destroy()
                  bank_window.deiconify()
           closeacc_win.protocol("WM_DELETE_WINDOW",closeacclose)

        def checkfor_updates():
               try:
                  r = urllib3.request("GET","https://raw.githubusercontent.com/skalwaghe-56/My_Bank/main/version.txt")
                  data = r.data.decode("utf-8").strip()
                  if data != _version_:
                     result = messagebox.askyesno("Software Update",f"A newer update to version {data} from {_version_} is available. Do you want to install it?",parent=bank_window)
                     if result == True:
                        webbrowser.open_new_tab("https://github.com/skalwaghe-56/My_Bank/releases/")
                        bank_window.destroy()
                     else:
                        return
                  else:
                     messagebox.showinfo("Software Update",f"You are on the latest version! Version : {_version_}",parent=bank_window)
               except:
                  messagebox.showerror("Software Update",f"Unable to Check for Update. Network or site related issue.",parent=bank_window)

        bank_window = Tk()
        width= bank_window.winfo_screenwidth()
        height= bank_window.winfo_screenheight()    
        bank_window.geometry("%dx%d" % (width, height))
        bank_window.title("Shreyash's Bank")
        bank_window.resizable(True,True)
        img = ImageTk.PhotoImage(file="_internal/Bank.png")
        bank_window.iconphoto(False,img)

        bg = Image.open("_internal/bg2.png")
        bg = bg.resize((width,height))
        bgimg = ImageTk.PhotoImage(bg)
        bgLabel = Label(bank_window,image=bgimg)
        bgLabel.grid()

        amountlabel = Label(bank_window,text="₹X,XXX,XXX",font=("arial",60,"bold"),bg="#dc1414",fg="black")
        amountlabel.place(x=400,y=40)

        showamount = Button(bank_window,text="Show \nAmount",bd=0,bg="#dc1414",activebackground="#dc1414",cursor="hand2",font=("arial",20,"bold"),fg="black",activeforeground="white",command=show_amount)
        showamount.place(x=870,y=40)

        accholdername = Label(bank_window,text="A/C Holder Name: XXXXXX XXXXX XXXXXXXX",font=("arial",20,"bold"),bg="#dc1414",fg="black")
        accholdername.place(x=400,y=140)
        showname = Button(bank_window,text="Show A/C Holder Name",bd=0,bg="#dc1414",activebackground="#dc1414",cursor="hand2",font=("arial",20,"bold"),fg="black",activeforeground="white",command=show_name)
        showname.place(x=680,y=180)

        depositbutton = Button(bank_window,text="Deposit",bd=2,bg="dark blue",activebackground="yellow",cursor="hand2",font =("arial",16,"bold"),fg="white",activeforeground="yellow",command=deposit_window)
        depositbutton.place(x=400,y=300)

        withdrawbutton = Button(bank_window,text="Withdraw",bd=2,bg="dark blue",activebackground="yellow",cursor="hand2",font=("arial",16,"bold"),fg="white",activeforeground="yellow",command=withdraw_window)
        withdrawbutton.place(x=900,y=300)

        transferbutton = Button(bank_window,text="Transfer",bd=2,bg="dark blue",activebackground="yellow",cursor ="hand2",font=("arial",16,"bold"),fg="white",activeforeground="yellow",command=transfer_window)
        transferbutton.place(x=400,y=600)

        signoutbutton = Button(bank_window,text="Sign Out [->",bd=2,bg="dark blue",activebackground="yellow",cursor="hand2",font=("arial",16,"bold"),fg="white",activeforeground="yellow",command=sign_out)
        signoutbutton.place(x=1100,y=40)

        checkforupdatesbutton = Button(bank_window,text="Check for Updates",bd=2,bg="dark blue",activebackground="yellow",cursor="hand2",font=("arial",16,"bold"),fg="white",activeforeground="yellow",command=checkfor_updates)
        checkforupdatesbutton.place(x=1080,y=95)

        closeaccbutton = Button(bank_window,text="Close A/C",bd=2,bg="dark blue",activebackground="yellow",cursor="hand2",font=("arial",16,"bold"),fg="white",activeforeground="yellow",command=close_acc)
        closeaccbutton.place(x=900,y=600)

        bank_window.mainloop()

def cusid_enter(event):
      if cusidentry.get()=="Customer ID":
          cusidentry.delete(0,END)

def pass_enter(event):
  if passwordentry.get()=="Password":
    passwordentry.delete(0,END)

window = Tk()

width = 300
height = 300
window.geometry("%dx%d" % (width, height))
window.title("Verfification")
window.resizable(False,False)
window.eval('tk::PlaceWindow . center')
window.configure(bg="grey")
img = ImageTk.PhotoImage(file="_internal/Lock.png")
window.iconphoto(False,img)

cusidlab = Label(window,text="Customer ID:",font=("Microsoft Yahei UI Light",12,"bold"),fg="black",bg="grey")
cusidlab.place(x=10,y=50)

cusidentry = Entry(window,width=12,font=("Microsoft Yahei UI Light",12,"bold"),bd=0,fg='black')
cusidentry.place(x=125,y=51)
cusidentry.insert(0,"Customer ID")
cusidentry.bind("<FocusIn>",cusid_enter)

passwordlab = Label(window,text="Password:",font=("Microsoft Yahei UI Light",12,"bold"),fg="black",bg="grey")
passwordlab.place(x=10,y=80)

passwordentry = Entry(window,width=15,font=("Microsoft Yahei UI Light",12,"bold"),bd=0,fg='black')
passwordentry.place(x=100,y=81)
passwordentry.insert(0,"Password")
passwordentry.bind("<FocusIn>",pass_enter)

submitButton = Button(window,text="Submit",bg="white",fg="black",font=("Open Sans",16,"bold"),width=15,cursor="hand2",activebackground="white",activeforeground="white",command=lock_login)
submitButton.place(x=50,y=150)

window.mainloop()