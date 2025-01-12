from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import tkinter.ttk as tkk
import sqlite3
import time
import os
import tempfile

class employeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+200+130")
        blank_space =" "
        self.root.title(blank_space * 140 + "Cadastro de Colaboradores")
        self.root.focus_force()
        self.root.config(bg="slate gray")

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()



        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()




       
        SearchFrame=LabelFrame(self.root,text="Pesquisar Funcionarios",font=("goudy old style",12),bg="slate gray",fg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

     
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="white",bd=3).place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Pesquisar",command=self.search,font=("goudy old style",15,"bold"),bg="dark slate gray",fg="white",cursor="hand2").place(x=440,y=10,width=150,height=30)


     
        title=Label(self.root,text="Detalhes do funcionario",font=("goudy old style",15,"bold"),bg="dim gray",fg="white",bd=3).place(x=50,y=100,width=1000)


        lbl_empid=Label(self.root,text="Emp ID",font=("goudy old style",14),bg="slate gray",fg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Sexo",font=("goudy old style",14),bg="slate gray",fg="white").place(x=370,y=150)
        lbl_contact=Label(self.root,text="Contato",font=("goudy old style",14),bg="slate gray",fg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("ARIEL",14)).place(x=150,y=150,width=180)
        
        
        
       
        cmb_search = ttk.Combobox(
            SearchFrame, 
            textvariable=self.var_searchby, 
            values=("Selecione", "Email", "Nome", "Contato"), 
            state='readonly', 
            justify=CENTER, 
            font=("goudy old style", 12)
        )
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

       
        self.search_map = {
            "Email": "email",
            "Nome": "name",
            "Contato": "contact"
        }
        
        
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("ARIEL",14),bg="white").place(x=850,y=150,width=180)


        
       
        lbl_name=Label(self.root,text="Nome",font=("goudy old style",14),bg="slate gray",fg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D_Nac",font=("goudy old style",14),bg="slate gray",fg="white").place(x=370,y=190)
        lbl_doj=Label(self.root,text="D_Emp",font=("goudy old style",14),bg="slate gray",fg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("ARIEL",14),bg="white").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("ARIEL",14),bg="white").place(x=450,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("ARIEL",14),bg="white").place(x=850,y=190,width=180)
        txt_gender=Entry(self.root,textvariable=self.var_gender,font=("ARIEL",14),bg="white").place(x=450,y=150,width=180)
       
        
        
     
        lbl_email=Label(self.root,text="Email",font=("goudy old style",14),bg="slate gray",fg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Senha",font=("goudy old style",14),bg="slate gray",fg="white").place(x=370,y=230)
        lbl_utype=Label(self.root,text="Usuario",font=("goudy old style",14),bg="slate gray",fg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("ARIEL",14),bg="white").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("ARIEL",14),bg="white").place(x=450,y=230,width=180)
        
        
        
        cmb_utype=ttk.Combobox(
        self.root,textvariable=self.var_utype,
        values=("Admin","Funcionario"),
        state='readonly',
        justify=CENTER,
        font=("goudy old style",12))

        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        self.cmb_utype = {
            "Admin": "Admin",
            "Funcionario": "Employee"
        }

       
        lbl_address=Label(self.root,text="Address",font=("goudy old style",14),bg="slate gray",fg="white").place(x=50,y=270)
        

        self.txt_address=Text(self.root,font=("ARIEL",14),bg="white")
        self.txt_address.place(x=150,y=280,width=300,height=60)
       
       
        
        btn_add=Button(self.root,text="Salvar",command=self.add,font=("goudy old style",15),bg="dark slate gray",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Atualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Deletar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Limpar",command=self.clear,font=("goudy old style",15),bg="light slate gray",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        
      
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=380,relwidth=1,height=120)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
       

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview) 
        scrolly.config(command=self.EmployeeTable.yview) 

        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Nome")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Sexo")
        self.EmployeeTable.heading("contact",text="Contato")
        self.EmployeeTable.heading("dob",text="Data Nasc")
        self.EmployeeTable.heading("doj",text="Data Contrato")
        self.EmployeeTable.heading("pass",text="Senha")
        self.EmployeeTable.heading("utype",text="Tipo Usuario")
        self.EmployeeTable.heading("address",text="Endereco")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=200)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()



    def add(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Erro","ID do funcionário necessária",parent=self.root)
            else:
                cur.execute("Select * from employee id where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Erro", "Esta ID de funcionário já foi atribuída, tente uma ID diferente",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address) values(?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_name.get(),  
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                    
                                        self.var_dob.get(),
                                        self.var_doj.get(),

                                    
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a : {str(ex)} ",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a: {str(ex)} ",parent=self.root)   

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
       
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])  
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])

    
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])

    
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END),  
        self.txt_address.insert(END,row[9])


    def update(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error" ,"ID do funcionário necessária",parent=self.root)
            else:
                cur.execute("Select * from employee id where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Erro", "ID de funcionário inválido",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=? where eid=?",(
                                       
                                        self.var_name.get(),  
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                    
                                        self.var_dob.get(),
                                        self.var_doj.get(),

                                    
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_emp_id.get(),                    
                                ))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a",f"Error due to : {str(ex)}" ,parent=self.root)

    
    def delete(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()

        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Erro", "ID do funcionário necessário",parent=self.root)
            else:
                cur.execute("Select * from employee id where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Erro", "ID de funcionário inválido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar", "Você realmente deseja excluir o registro selecionado?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Excluir", "Funcionário excluído com sucesso",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a: {str(ex)} ",parent=self.root)
    
    def clear(self):                                
        self.var_emp_id.set("")
        self.var_name.set("")  
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("") 

    
        self.var_dob.set("")
        self.var_doj.set("")

    
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END),  
        self.var_searchtxt.set("")
        self.var_searchby.set("")
        self.show()

    
    def search(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            searchby = self.var_searchby.get()
            if searchby == "Selecione":
                messagebox.showerror("Erro", "Selecione uma opção de pesquisa", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Erro", "O campo de pesquisa não pode estar vazio", parent=self.root)
            else:
               
                column = self.search_map.get(searchby, "")
                if column: 
                    cur.execute(f"SELECT * FROM employee WHERE {column} LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                    rows = cur.fetchall()
                    if rows:
                        self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                        for row in rows:
                            self.EmployeeTable.insert('', END, values=row)
                    else:
                        messagebox.showinfo("Informação", "Nenhum registro encontrado", parent=self.root)
                else:
                    messagebox.showerror("Erro", "Opção de pesquisa inválida", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()   

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()