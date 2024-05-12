from tkinter import *
root =Tk()
root.geometry('700x500+500+150')
root.resizable(False,False)
root.iconbitmap('C:\\Users\\Baria\\OneDrive\\Desktop\\icon.ico')
root.title('My project')
root.config(background='gray')
frm1 = Frame(width='350',height='500',bg='green')
frm1.place(x =1,y=1)
frm2 = Frame(width='350',height='500',bg='red')
frm2.place(x =350,y=1)

bt1 = Button(frm1 ,text='click me', bg='red' ,fg='white',cursor='heart')
bt1.place(x=150, y=450)

btn2 = Button(frm2 ,text='click me', bg='green' ,fg='white')
btn2.place(x=150, y=450)

lbl1 = Label(frm1 ,text='buonjorno',fg='white',bg='green',font=12)
lbl1.place(x=10 ,y=20)

lbl2 = Label(frm2 ,text='buonjorno',fg='white',bg='red',font=12)
lbl2.place(x=10 ,y=20)
root.mainloop()