import customtkinter as ctk
from tkinter import END
app = ctk.CTk()
app.title('laern')

def sw_s():
    if sw.get():
        ctk.set_appearance_mode('Dark')
    else:
        ctk.set_appearance_mode('Light')    
def btn1():
    txt = ent.get()
    lbl.configure(text='hello  '+txt)
    ent.delete('0',END)

   
app.geometry('650x550')
ctk.set_appearance_mode('Light')
ctk.set_default_color_theme('blue')
frm = ctk.CTkFrame(app,width=600,height=500)
frm.pack(padx=20,pady=20,fill='both',expand=True)
lbl = ctk.CTkLabel(frm,text='',font=('arial',20,'bold'))
lbl.pack()
sw = ctk.CTkSwitch(frm,width=60,height=30,command=sw_s)
sw.pack(pady=20)
ent = ctk.CTkEntry(frm,width=200,height=30,placeholder_text='entry your name')
ent.pack(pady=20)
btn = ctk.CTkButton(frm,width=170,text='lets go',text_color='black',command=btn1,hover_color='green')
btn.pack(pady=20)





app.mainloop()