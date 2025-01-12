from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class SalesForm:
    def __init__(self, root):
        self.root = root
        self.root.geometry("580x350")
        self.root.title("Formulário de Vendas")
        self.root.config(bg="white")

        Cal_cartFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_cartFrame.place(x=1,y=1,width=530,height=330)
        
        self.var_cal_input=StringVar()
        CalFrame=Frame(Cal_cartFrame,bd=9,relief=RIDGE,bg="white")
        CalFrame.place(x=5,y=10,width=268,height=300)

        txt_cal_input=Entry(CalFrame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,state='readonly',justify=RIGHT,relief=GROOVE)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(CalFrame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=2,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
        btn_8=Button(CalFrame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=2,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
        btn_9=Button(CalFrame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=2,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
        btn_sum=Button(CalFrame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=2,width=4,pady=10,cursor='hand2').grid(row=1,column=3)


        btn_4=Button(CalFrame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=2,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
        btn_5=Button(CalFrame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=2,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
        btn_6=Button(CalFrame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=2,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
        btn_sub=Button(CalFrame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=2,width=4,pady=10,cursor='hand2').grid(row=2,column=3)

        btn_1=Button(CalFrame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=2,width=4,pady=10,cursor='hand2').grid(row=3,column=0)
        btn_2=Button(CalFrame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=2,width=4,pady=10,cursor='hand2').grid(row=3,column=1)
        btn_3=Button(CalFrame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=2,width=4,pady=10,cursor='hand2').grid(row=3,column=2)
        btn_mul=Button(CalFrame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=2,width=4,pady=10,cursor='hand2').grid(row=3,column=3)

        btn_0=Button(CalFrame,text='0',font=('arial',14,'bold'),command=lambda:self.get_input(0),bd=2,width=4,pady=9,cursor='hand2').grid(row=4,column=0)
        btn_c=Button(CalFrame,text='c',font=('arial',14,'bold'),command=lambda:self.clear_cal(),bd=2,width=4,pady=9,cursor='hand2').grid(row=4,column=1)
        btn_eq=Button(CalFrame,text='=',font=('arial',14,'bold'),command=lambda:self.perform_cal(),bd=2,width=4,pady=9,cursor='hand2').grid(row=4,column=2)
        btn_div=Button(CalFrame,text='/',font=('arial',14,'bold'),command=lambda:self.get_input('/'),bd=2,width=4,pady=9,cursor='hand2').grid(row=4,column=3)


if __name__ == "__main__":
    root = Tk()
    app = SalesForm(root)
    root.mainloop()