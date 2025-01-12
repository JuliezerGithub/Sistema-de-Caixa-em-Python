from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import tkinter.ttk as ttk
import sqlite3

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+200+130")
        blank_space =" "
        self.root.title(110 * blank_space + "Sistema de faturamento e gerenciamento de faturas | Fornecedores")
        self.root.config(bg="slate gray")
        self.root.focus_force()
     
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_searchbyparcela=StringVar()
        self.var_searchbypagamento=StringVar()
        self.var_sup_invoice=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_supdate=StringVar()
        self.var_valor=StringVar()
        self.var_pagamento=StringVar()
        self.var_datavenc=StringVar()
        self.var_parcela=StringVar()
        self.var_observacao=StringVar()

        #---------Pesquisa---------
        lbl_search=Label(self.root,text="Nota No.",bg="slate gray",font=("ARIEL",15))
        lbl_search.place(x=700,y=80)

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("ARIEL",15),bg="white").place(x=795,y=80,width=180)
        btn_search=Button(self.root,command=self.search,text="Pesquisar",font=("ARIEL",12),bg="dark slate gray",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        title=Label(self.root,text="Detalhes Do Fornecedor",font=("ARIEL",20,"bold"),bg="gray15",fg="white").place(x=50,y=10,width=1000,height=40)

        #---------Textor e Entradas---------
        lbl_supplier_invoice=Label(self.root,text="Nota No.",font=("ARIEL",15),bg="slate gray").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("ARIEL",15),bg="white").place(x=180,y=80,width=200)
        
        lbl_supdate=Label(self.root,text="Data Entrada",font=("ARIEL",14),bg="slate gray").place(x=390,y=80)
        var_supdate=Entry(self.root,textvariable=self.var_supdate,font=("ARIEL",14),bg="white").place(x=510,y=80,width=140)
       
        lbl_name=Label(self.root,text="Nome",font=("ARIEL",15),bg="slate gray").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("ARIEL",15),bg="white").place(x=180,y=120,width=470)
        
       
        lbl_contact=Label(self.root,text="Contato",font=("ARIEL",15),bg="slate gray").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("ARIEL",15),bg="white").place(x=180,y=160,width=200)
        

        lbl_datavenc=Label(self.root,text="Data Venci.",font=("ARIEL",14),bg="slate gray").place(x=390,y=160)
        var_datavenc=Entry(self.root,textvariable=self.var_datavenc,font=("ARIEL",15),bg="white").place(x=510,y=160,width=140)
        
        lbl_valor=Label(self.root,text="Valor R$",font=("ARIEL",15),bg="slate gray").place(x=50,y=200)
        txt_valor=Entry(self.root,textvariable=self.var_valor,font=("ARIEL",15),bg="white").place(x=180,y=200,width=200)
        
        lbl_parcela=Label(self.root,text="Nº Parcelas",font=("ARIEL",14),bg="slate gray").place(x=390,y=200)
        cmb_parcela=ttk.Combobox(self.root,textvariable=self.var_searchbyparcela,values=("1x","2x","3x"),state='readonly',justify=CENTER,font=("goudy old style",12))
        cmb_parcela.place(x=510,y=200,width=140)
        cmb_parcela.current(0)
        
        lbl_pagamento=Label(self.root,text="Pagamento",font=("ARIEL",15),bg="slate gray").place(x=50,y=240)
        cmb_pagamento=ttk.Combobox(self.root,textvariable=self.var_searchbypagamento,values=("A Pagar","Pago 1ª Parcela","Pago 2ª Parcela", "Pago", "A Vista"),state='readonly',justify=CENTER,font=("goudy old style",12))
        cmb_pagamento.place(x=180,y=240,width=200)
        cmb_pagamento.current(0)

        lbl_observacao=Label(self.root,text="Observações:",font=("ARIEL",15),bg="slate gray").place(x=50,y=280)
        txt_observacao=Entry(self.root,textvariable=self.var_observacao,font=("ARIEL",15),bg="white").place(x=180,y=280, width=470)
       
        #---------Botões---------
        btn_add=Button(self.root,text="Salvar",command=self.add,font=("ARIEL",15),bg="dark slate gray",fg="white",cursor="hand2").place(x=180,y=430,width=110,height=35)
        btn_update=Button(self.root,text="Atualizar",command=self.update,font=("ARIEL",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=430,width=110,height=35)
        btn_delete=Button(self.root,text="Deletar",command=self.delete,font=("ARIEL",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=430,width=110,height=35)
        btn_clear=Button(self.root,text="Limpar",command=self.clear,font=("ARIEL",15),bg="light slate gray",fg="white",cursor="hand2").place(x=540,y=430,width=110,height=35)
      
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
       
        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","supdate","valor","pagamento","datavenc","parcela","observacao"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview) 
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Nota.")
        self.supplierTable.heading("name",text="Nome")
        self.supplierTable.heading("contact",text="Contato")
        self.supplierTable.heading("supdate",text="Data Atualizacao")
        self.supplierTable.heading("valor",tex="Valor")
        self.supplierTable.heading("pagamento",text="Pagamento")
        self.supplierTable.heading("datavenc",text="Data Vencimento")
        self.supplierTable.heading("parcela",text="Parcela")
        self.supplierTable.heading("observacao",text="Obs")

        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("supdate",width=100)
        self.supplierTable.column("valor",width=100)
        self.supplierTable.column("pagamento",width=100)
        self.supplierTable.column("datavenc",width=100)
        self.supplierTable.column("parcela",width=100)
        self.supplierTable.column("observacao",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

    

    def add(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Notas obrigatorio",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","ESTA NOTA JA EXISTE NO NOSSO BANCO DE DADOS COM ESTE ID,TENTA UM ID DIFERENTE",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,supdate,valor,pagamento,datavenc,parcela,observacao) values(?,?,?,?,?,?,?,?,?)", (
                    self.var_sup_invoice.get(),
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.var_supdate.get(),
                    self.var_valor.get(),
                    self.var_pagamento.get(),
                    self.var_datavenc.get(),
                    self.var_parcela.get(),
                    self.var_observacao.get()
                ))

                    con.commit()
                    messagebox.showinfo("Success","FORNECEDOR CADASTRADO COM SUCESSO",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"OCORREU UM ERROR DE : {str(ex)}", parent=self.root)
    

    def show(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error de : {str(ex)}", parent=self.root)

    

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])  
        self.var_contact.set(row[2])
        self.var_supdate.set(row[3])
        self.var_supdate.set(row[4])
        self.var_valor.set(row[5]),
        self.var_pagamento.set(row[6]),
        self.var_parcela.set(row[7]),
        self.var_datavenc.set(row[8]),
        self.var_observacao.set(row[9]),
        self.var_supdate.set(row[10])


    def update(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","numero de fatura necessario",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()

                if row is None:
                    
                    messagebox.showerror("Error","numero da fatura invalido.",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,supdate=? where invoice=?",(
                        self.var_name.get(),  
                        self.var_contact.get(),
                        self.var_supdate.get(),
                        self.var_sup_invoice.get(),                    
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Fornecedor atualizado com sucesso",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a : {str(ex)}" ,parent=self.root)
        finally:
            con.close()



    def delete(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()

        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error", "Número da fatura necessário",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Número da fatura inválido.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Você realmente deseja excluir o registro selecionado?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Excluir", "Fornecedor excluído com sucesso",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)
    
    def clear(self): 
        self.var_sup_invoice.set("")                                
        self.var_name.set("")  
        self.var_contact.set("") 
        self.var_supdate.set("")  
        self.var_searchtxt.set("")
        self.var_valor.set("")
        self.var_pagamento.set("")
        self.var_datavenc.set("")
        self.var_parcela.set("")
        self.var_searchbyparcela.set("")
        self.var_searchbypagamento.set("")
        self.show()

    
    def search(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Número da fatura deve ser exigido",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Nenhum registro encontrado!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root) 
 

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()