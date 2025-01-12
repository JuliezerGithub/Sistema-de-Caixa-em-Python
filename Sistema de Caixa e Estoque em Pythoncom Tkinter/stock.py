from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import tkinter.ttk as ttk
import sqlite3


def add_placeholder(entry, placeholder_text):
    # Define as funções para lidar com os eventos
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg="black")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg="grey")
    
    # Configure o placeholder
    entry.insert(0, placeholder_text)
    entry.config(fg="grey")
    
    # Associe os eventos
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)




class stockClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        blank_space =" "
        self.root.title(blank_space + "Estoque")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.config(bg="slate gray")


    

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_hsncode=StringVar()
        self.var_discount=StringVar()
        self.sup_list=[]
        self.var_sup=StringVar()
       
        self.fetch_sup()
       
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        stock_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        stock_Frame.place(x=10,y=10,width=450,height=480)

        title=Label(stock_Frame,text="Detalhes do estoque",font=("ARIEL",18,"bold"),bg="slate gray",fg="white",bd=3)
        title.pack(side=TOP,fill=X)

       
        lbl_pid=Label(stock_Frame,text="ID",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=60)
        lbl_supplier=Label(stock_Frame,text="Fornecedor",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=110)
       
        lbl_item_name=Label(stock_Frame,text="Produto",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=160)
        lbl_hsn_code=Label(stock_Frame,text="HSN",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=210)
        lbl_price=Label(stock_Frame,text="Preço",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=260)
        lbl_qty=Label(stock_Frame,text="Quantidade",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=310)
        lbl_discount=Label(stock_Frame,text="Desconto",font=("ARIEL",15,"bold"),bg="white",bd=3).place(x=30,y=360)
       


       


        
        cmb_sup=ttk.Combobox(stock_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("ARIEL",12))
        cmb_sup.place(x=150,y=110,width=280)
        cmb_sup.current(0)

        



        txt_pid=Entry(stock_Frame,textvariable=self.var_pid,font=("ARIEL",12),bg="white").place(x=150,y=60, width=280)
        txt_name=Entry(stock_Frame,textvariable=self.var_name,font=("ARIEL",12),bg="white").place(x=150,y=160,width=280)
        
        var_hsncode = StringVar()
        txt_hsn_code = Entry(stock_Frame, textvariable=var_hsncode, font=("ARIEL", 12), bg="white")
        txt_hsn_code.place(x=150, y=210, width=280)
        add_placeholder(txt_hsn_code, "Nomenclatura do Sistema Harmonizado")

        txt_price=Entry(stock_Frame,textvariable=self.var_price,font=("ARIEL",12),bg="white").place(x=150,y=260, width=280)
        txt_qty=Entry(stock_Frame,textvariable=self.var_qty,font=("ARIEL",12),bg="white").place(x=150,y=320, width=280)
        txt_discount=Entry(stock_Frame,textvariable=self.var_discount,font=("ARIEL",12),bg="white").place(x=150,y=370, width=280)
       


        btn_add=Button(stock_Frame,text="Salvar",command=self.add,font=("ARIEL",15),bg="dark slate gray",fg="white",cursor="hand2").place(x=10,y=425,width=100,height=40)
        btn_update=Button(stock_Frame,text="Atualizar",command=self.update,font=("ARIEL",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=425,width=100,height=40)
        btn_delete=Button(stock_Frame,text="Deletar",command=self.delete,font=("ARIEL",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=425,width=100,height=40)
        btn_clear=Button(stock_Frame,text="Limpar",command=self.clear,font=("ARIEL",15),bg="light slate gray",fg="white",cursor="hand2").place(x=340,y=425,width=100,height=40)



      
        SearchFrame=LabelFrame(self.root,text="Pesquisar Funcionario",font=("ARIEL",12),bg="slate gray",bd=3,fg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

      
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Supplier","Itemname"),state='readonly',justify=CENTER,font=("ARIEL",12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)


        
        cmb_search = ttk.Combobox(
            SearchFrame, 
            textvariable=self.var_searchby, 
            values=("Selecione", "Fornecedor", "Prod_Nome"), 
            state='readonly', 
            justify=CENTER, 
            font=("ARIEL", 12)
        )
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

       
        self.search_map = {
            "Fornecedor": "supplier",
            "Prod_Nome": "itemname"
        }

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("ARIEL",15),bg="white",bd=1).place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Pesquisar",command=self.search,font=("ARIEL",15,"bold"),bg="black",fg="white",bd=0,cursor="hand2").place(x=440,y=10,width=140,height=30)

       
        s_Frame=Frame(self.root,bd=3,relief=RIDGE)
        s_Frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(s_Frame,orient=VERTICAL)
        scrollx=Scrollbar(s_Frame,orient=HORIZONTAL)
       

        self.StockTable=ttk.Treeview(s_Frame,columns=("pid","Supplier","itemname","hsncode","price","qty","discount"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.StockTable.xview) 
        scrolly.config(command=self.StockTable.yview) 

        self.StockTable.heading("pid",text="ID")
        self.StockTable.heading("Supplier",text="Fornecedor")
        self.StockTable.heading("itemname",text="Nome Prod")
        self.StockTable.heading("hsncode",text="HSN")
        self.StockTable.heading("price",text="Preco")
        self.StockTable.heading("qty",text="Quantidade")
        self.StockTable.heading("discount",text="Disconto")

        self.StockTable["show"]="headings"

        self.StockTable.column("pid",width=90)
        self.StockTable.column("Supplier",width=100)
        self.StockTable.column("itemname",width=100)
        self.StockTable.column("hsncode",width=100)
        self.StockTable.column("price",width=100)
        self.StockTable.column("qty",width=100)
        self.StockTable.column("discount",width=100)
        self.StockTable.pack(fill=BOTH,expand=1)
        self.StockTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_sup()


    def fetch_sup(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            self.sup_list.append("Empty")
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)   


    def add(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","Todos os campos são obrigatórios",parent=self.root)
            else:
                cur.execute("Select * from stock where itemname=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Produto já presente, tente diferente",parent=self.root)
                else:
                    cur.execute("Insert into stock (supplier,itemname,hsncode,price,qty,discount) values(?,?,?,?,?,?)",(
                                        self.var_sup.get(),  
                                        self.var_name.get(),
                                        self.var_hsncode.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_discount.get()
                                    
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso","Item adicionado com sucesso",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from stock")
            rows=cur.fetchall()
          
            self.StockTable.delete(*self.StockTable.get_children())
            for row in rows:
               self.StockTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)  



    def get_data(self,ev):
        f=self.StockTable.focus()
        content=(self.StockTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_sup.set(row[1])  
        self.var_name.set(row[2])
        self.var_hsncode.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_discount.set(row[6])




    def update(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Selecione o item da lista",parent=self.root)
            else:
                cur.execute("Select * from stock where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Item inválido",parent=self.root)
                else:
                    cur.execute("Update stock set supplier=?,itemname=?,hsncode=?,price=?,qty=?,discount=? where pid=?",(
                                        self.var_sup.get(),  
                                        self.var_name.get(),
                                        self.var_hsncode.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_discount.get(),
                                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso","Item atualizado com sucesso",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)}" ,parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()

        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Selecione o item da lista",parent=self.root)
            else:
                cur.execute("Select * from stock where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Produto inválido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Você realmente deseja excluir o registro selecionado?",parent=self.root)
                    if op==True:
                        cur.execute("delete from stock where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Excluir","Item excluído com sucesso",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)

    def clear(self):                               
        self.var_sup.set("Selecione"),  
        self.var_name.set(""),
        self.var_hsncode.set("")
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_pid.set("") ,
        self.var_discount.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Selecione")
        self.show()


    def search(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            searchby = self.var_searchby.get()
            if searchby == "Selecione":
                messagebox.showerror("Error", "Selecione uma opcao de pesquisa", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "prencha o campo pesquisa", parent=self.root)
            else:
             
                column = self.search_map.get(searchby, "")
                if column:  
                    cur.execute(f"SELECT * FROM stock WHERE {column} LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                    rows = cur.fetchall()
                    if rows:
                        self.StockTable.delete(*self.StockTable.get_children())
                        for row in rows:
                            self.StockTable.insert('', END, values=row)
                    else:
                        messagebox.showinfo("Information", "Cadastro nao encontrado", parent=self.root)
                else:
                    messagebox.showerror("Error", "Opcao de pesquisa invalido", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"error de : {str(ex)}", parent=self.root)
        finally:
            con.close()   




if __name__=="__main__":
    root=Tk()
    obj=stockClass(root)
    root.mainloop()