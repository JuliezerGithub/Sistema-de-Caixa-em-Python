from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

from sales import salesClass

class billClass:
    def __init__(self,root):
        self.root = root
        self.width = 1510
        self.height = 720
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        blank_space = " "
        self.root.title(220 * blank_space + "Encomendas")
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg="slate gray")
        self.cart_list=[]
        self.chk_print=0

        # Redimensionar a imagem
        self.icon_title = Image.open("images/logo_sem_fundo.png")
        self.icon_title = self.icon_title.resize((110, 100))
        self.icon_title = ImageTk.PhotoImage(self.icon_title)
        title = Label(self.root,text="ENCOMENDAS | VENDAS",image=self.icon_title,compound=LEFT,font=("ARIEL",40,"bold"),bg="slate gray",fg="white", anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=120)

       
        btn_logout = Button(self.root,text="Sair",command=self.logout,font=("ARIEL",15,"bold"),bg="white",cursor="hand2").place(x=1400,y=30,height=50,width=100)
        btn_faturas = Button(self.root,text="Ver Faturas",command=self.faturas,font=("ARIEL",15,"bold"),bg="khaki4", fg="white",cursor="hand2").place(x=1190,y=30,height=50,width=200)
       
        self.lbl_clock = Label(self.root,text="Bem-vindo...!!\t Data: DD-MM-YYYY\t\t Horas: HH:MM:SS",font=("ARIEL",14,"bold"),bg="dim gray",fg="white",borderwidth=1, relief="solid")
        self.lbl_clock.place(x=0,y=120,relwidth=1,height=30)

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=160,width=410,height=555)

        # Todos os Produtos
        pTitle=Label(ProductFrame1,text="Todos Produtos",font=("ARIEL",15,"bold"),bg="gray10",fg="white")
        pTitle.pack(side=TOP,fill=X)

       
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Pesquisar Produto por nome",font=("ARIEL",15,"bold"),bg="white",fg="gray2").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Prod nome",font=("ARIEL",15,"bold"),bg="white",fg="gray2").place(x=5,y=45) 
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("ARIEL",15),bg="#FAEDEA").place(x=130,y=47,width=150,height=22) 
        btn_search=Button(ProductFrame2,text="Pesquisar",command=self.search,font=("ARIEL",12,"bold"),bg="dark slate gray",fg="white",cursor="hand2").place(x=285,y=45,width=95,height=25)
        btn_show_all=Button(ProductFrame2,text="Todos",command=self.show,font=("ARIEL",15,"bold"),bg="light slate gray",fg="white",cursor="hand2").place(x=285,y=5,width=95,height=25)

  
       
        
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=385)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
       

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","itemname","hsncode","price","qty","discount"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview) 
        scrolly.config(command=self.product_Table.yview) 

        self.product_Table.heading("pid",text="ID")
        self.product_Table.heading("itemname",text="Prod_Nome")
        self.product_Table.heading("hsncode",text="HSN")
        self.product_Table.heading("price",text="Preco")
        self.product_Table.heading("qty",text="Qtidade")
        self.product_Table.heading("discount",text="Desconto")

        
        

        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("itemname",width=100)
        self.product_Table.column("hsncode",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("discount",width=100)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        

        lbl_note=Label(ProductFrame1,text="Nota: Insira 0 Quantidade para remover o produto do carrinho",font=("ARIEL",11),anchor='w',bg="white",fg="red")
        lbl_note.pack(side=BOTTOM,fill=X)

         # --------- Dados do Cliente --------- #
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=160,width=530,height=275)

        self.var_cname=StringVar()
        self.var_contact=StringVar()
        self.var_endereco=StringVar()
        self.var_numero=StringVar()
        self.var_bairro=StringVar()
        self.var_dataentrega=StringVar()
        self.var_anoacoes=StringVar()

        cTitle=Label(CustomerFrame,text="Detalhes Cliente",font=("ARIEL",15,"bold"),bg="gray10",fg="white")
        cTitle.pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Nome",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=5,y=33)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("ARIEL",15),bg="#FAEDEA").place(x=80,y=35,width=420) 

        lbl_contact=Label(CustomerFrame,text="Contato",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=5,y=66)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("ARIEL",15),bg="#FAEDEA").place(x=90,y=70,width=140) 

        lbl_dataentrega=Label(CustomerFrame,text="Data Entrega",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=240,y=66)
        txt_dataentrega=Entry(CustomerFrame,textvariable=self.var_dataentrega,font=("ARIEL",15),bg="#FAEDEA").place(x=380,y=70,width=120)
        
        lbl_endereco=Label(CustomerFrame,text="Endereço",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=5,y=100)
        txt_endereco=Entry(CustomerFrame,textvariable=self.var_endereco,font=("ARIEL",15),bg="#FAEDEA").place(x=110,y=104,width=390)


        lbl_numero=Label(CustomerFrame,text="Nº",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=5,y=137)
        txt_numero=Entry(CustomerFrame,textvariable=self.var_numero,font=("ARIEL",15),bg="#FAEDEA").place(x=40,y=140,width=80)

        lbl_bairro=Label(CustomerFrame,text="Bairro",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=130,y=137)
        txt_bairro=Entry(CustomerFrame,textvariable=self.var_bairro,font=("ARIEL",15),bg="#FAEDEA").place(x=200,y=140,width=300)

        #lbl_anotacoes=Label(CustomerFrame,text="Anotações",font=("ARIEL",15,"bold"),bg="white",fg="gray10").place(x=5,y=177)
        #txt_anotacoes=Entry(CustomerFrame,textvariable=self.var_dataentrega,font=("ARIEL",15),bg="#FAEDEA").place(x=120,y=180,height=80,width=380)

        # Label
        lbl_anotacoes = Label(
            CustomerFrame, 
            text="Anotações", 
            font=("ARIEL", 15, "bold"), 
            bg="white", 
            fg="gray10"
        )
        lbl_anotacoes.place(x=5, y=177)

        # Caixa de Texto com Placeholder
        self.txt_anotacoes = Text(CustomerFrame, font=("ARIEL", 13), bg="#FAEDEA", wrap=WORD)
        self.txt_anotacoes.place(x=120, y=180, height=80, width=380)
        
        # Adicionando Placeholder
        self.placeholder_text = "Detalhar cor, sabores, cobertura, decoração, tamanho..."
        self.txt_anotacoes.insert(1.0, self.placeholder_text)
        self.txt_anotacoes.bind("<FocusIn>", self.remove_placeholder)
        self.txt_anotacoes.bind("<FocusOut>", self.add_placeholder)

        # --------- Produtos no carrinho --------- #
        Cal_cartFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_cartFrame.place(x=420,y=555,width=530,height=160)
        
        CartFrame=Frame(Cal_cartFrame,bd=3,relief=RIDGE)
        CartFrame.place(x=5,y=5,width=512,height=150)
        self.cartTitle=Label(CartFrame,text="Carrinho \t Total Produtos: [0]",font=("ARIEL",10,"bold"),bg="gray10",fg="white")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(CartFrame,orient=VERTICAL)
        scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)
       

        self.cartTable=ttk.Treeview(CartFrame,columns=("pid","itemname","hsncode","price","qty","discount"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview) 
        scrolly.config(command=self.cartTable.yview) 

        self.cartTable.heading("pid",text="ID")
        self.cartTable.heading("itemname",text="Prod_Nome")
        self.cartTable.heading("hsncode",text="HSN")
        self.cartTable.heading("price",text="Preco")
        self.cartTable.heading("qty",text="Qtidade")
        self.cartTable.heading("discount",text="Desconto")
    
        

        self.cartTable["show"]="headings"

        self.cartTable.column("pid",width=30)
        self.cartTable.column("itemname",width=100)
        self.cartTable.column("hsncode",width=100)
        self.cartTable.column("price",width=90)
        self.cartTable.column("qty",width=30)
        self.cartTable.column("discount",width=100)
       
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
       
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_hsncode=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        self.var_discount=StringVar()

        # --------- Cadastro Produtos no carrinho --------- #
        Add_cartwidgetsFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Add_cartwidgetsFrame.place(x=420,y=440,width=530,height=110)

        lbl_pname=Label(Add_cartwidgetsFrame,text="Produto",font=("ARIEL",13,"bold"),bg="white",fg="gray10").place(x=5,y=5)
        txt_pname=Entry(Add_cartwidgetsFrame,textvariable=self.var_pname,font=("ARIEL",12),bg="#FAEDEA",state='readonly').place(x=5,y=30,width=190,height=22)

        lbl_p_price=Label(Add_cartwidgetsFrame,text="Preço Unidade ",font=("ARIEL",13,"bold"),bg="white",fg="gray10").place(x=230,y=5)
        txt_p_price=Entry(Add_cartwidgetsFrame,textvariable=self.var_price,font=("ARIEL",12),bg="#FAEDEA",state='readonly').place(x=230,y=30,width=150,height=22)

        lbl_p_qty=Label(Add_cartwidgetsFrame,text="Qtde",font=("ARIEL",13,"bold"),bg="white",fg="gray10").place(x=390,y=5)
        txt_p_qty=Entry(Add_cartwidgetsFrame,textvariable=self.var_qty,font=("ARIEL",12),bg="#FAEDEA").place(x=390,y=30,width=120,height=20)

        
        
        btn_clear_cart=Button(Add_cartwidgetsFrame,text="Limpar",command=self.clear_cart,font=("ARIEL",10,"bold"),bg="light slate gray",fg="white",cursor="hand2").place(x=5,y=65,width=150,height=30)
        
        btn_add_cart=Button(Add_cartwidgetsFrame,text="+ | Atualizar carrinho",command=self.add_update_cart,font=("ARIEL",10,"bold"),bg="dark slate gray",fg="white",cursor="hand2").place(x=340,y=65,width=180,height=30)

        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=160,width=550,height=410)


        btitle=Label(billFrame,text="Área de fatura do cliente",font=("ARIEL",15,"bold"),bg="khaki4",fg="white")
        btitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

   

        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=575,width=550,height=140)

        btn_generate_bill=Button(billMenuFrame,text='Gerar/Fatura',command=self.generate_bill,font=("ARIEL",15,"bold"),bg="khaki4",fg="white",cursor="hand2")
        btn_generate_bill.place(x=50,y=10,width=200,height=50)

        btn_clear_all=Button(billMenuFrame,text='Limpar tudo',command=self.clear_all,font=("ARIEL",15,"bold"),bg="khaki4",fg="white",cursor="hand2")
        btn_clear_all.place(x=360,y=10,width=160,height=50)

       
        
        btn_print=Button(billMenuFrame,text='Imprimir fatura',command=self.print_bill,font=("ARIEL",15,"bold"),bg="khaki4",fg="white",cursor="hand2")
        btn_print.place(x=50,y=75,width=470,height=50)

       

        

        self.show()
      
        self.update_date_time()
        


    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set(' ')


    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
           
            cur.execute("Select pid,itemname,hsncode,price,qty,discount from stock")
            rows=cur.fetchall()
            
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
               self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)  

    def search(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","A entrada de pesquisa deve ser obrigatória",parent=self.root)
            else:
                cur.execute("select pid,itemname,hsncode,price,qty,discount from stock where itemname LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Nenhum registro encontrado!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)  

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1]) 
        self.var_hsncode.set(row[2])
        self.var_price.set(row[3])
        
        self.var_stock.set(row[4])
        
        self.var_qty.set('1')
        self.var_discount.set(row[5])

    
    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1]) 
        self.var_hsncode.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.lbl_inStock.config(text=f"Em_estoque [{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_discount.set(row[5])
        
        

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Selecione o produto da lista",parent=self.root) 
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantidade necessária",parent=self.root)

        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error', "Quantidade inválida",parent=self.root)
        else:
           

            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),self.var_hsncode.get(),price_cal,self.var_qty.get(),self.var_discount.get(),self.var_stock.get()]

            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            
        
            if present=='yes':
                op = messagebox.askyesno('Confirmar', "Produto já presente\\Deseja atualizar|Remover da lista do carrinho", parent=self.root)
                if op==True: 
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        
                        self.cart_list[index_][4]=self.var_qty.get()
                        
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()


    def bill_updates(self):
        self.total_sales=0
        
        self.actualprice=0
        self.total_sales=0
        self.discount=0
        self.total_invoice_amount=0
        self.total_sgst=0
        self.total_cgst=0
        self.total_gst=0
        if self.discount > 0:
            for row in self.cart_list:
                self.actual_price=float(row[3])*float(row[4])
               
               
                self.discount=(self.actualprice*int(row[5]))/100
                self.reducedpay=self.actualprice-self.discount
                self.total_sales=self.total_sales+float(self.reducedpay)
                self.total_gst=(self.total_sales*int(18))/100
                self.total_sgst=self.total_gst/2
                self.total_cgst=self.total_gst/2
                self.total_invoice_amount=self.total_sales+self.total_gst

        
                
        

            print(str(self.total_sales))
            print(str(self.total_invoice_amount))

            
        else:
            for row in self.cart_list:
                self.actualprice=float(row[3])*float(row[4])
                self.total_sales=self.total_sales+self.actualprice
                self.total_gst=(self.total_sales*int(18))/100
                self.total_sgst=self.total_gst/2
                self.total_cgst=self.total_gst/2
                self.total_invoice_amount=self.total_sales+self.total_gst
            print(str(self.total_sales))
            print(self.total_invoice_amount)
           



    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
               self.cartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Erro devido a: {str(ex)} ",parent=self.root)  


    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror('Error', "Detalhes do cliente são obrigatórios",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror('Error', "Adicione o produto ao carrinho",parent=self.root)
        else:
           
            self.bill_top()
            
            self.bill_middle()
           
            self.bill_bottom()
           

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Salvo", "A fatura foi gerada/salva no backend",parent=self.root)
            self.chk_print=1


    
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tConffeitar - Confeitaria e Café
\n\t\tAvenida Dos Imigrantes, nº580
\t\tTelefone: (47) 9 9632-2030
\t\tEmail: conffeitar@gmail.com

{str("="*65)}
Nota No. {str(self.invoice)}\t\t\tData Impressão: {str(time.strftime("%d/%m/%Y"))}
Nome Cliente: {self.var_cname.get()}
tel no: {self.var_contact.get()}\t\t\tData Entrega:{self.var_dataentrega}
Endereço: {self.var_endereco}
nº:{self.var_numero}\t\t\tBairro:{self.var_bairro}
{str("="*65)}
Nome_Prod\t\t\tQde\t\t\tPreço
{str("="*65)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*65)}
Total Vendas(A)\t\t\t\tRs.{self.total_sales}
Total Taxa(9%)\t\t\t\tRs.{self.total_sgst}
Total Servico(9%)\t\t\t\tRs.{self.total_cgst}
Total Bens_ser(18%)(B)\t\t\t\tRs.{self.total_gst}
Valor da fatura(A+B)\t\t\tRs.{self.total_invoice_amount} 
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                discount=row[5]
                
             
                qty=int(row[6])-int(row[4])
               

                price=float(row[3])*int(row[4])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t"+row[2]+"\t"+row[4]+"\tRs."+price+"\t%."+discount)
               
                cur.execute('Update stock set qty=? where pid=?',(
                qty,
                pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a : {str(ex)} ",parent=self.root)  



    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_hsncode.set('') 
        self.var_price.set('')
        self.var_qty.set('')
        
        self.var_stock.set('')
        self.var_discount.set('')
    
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Carrinho \t Total de produtos: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Bem-vindo...!!\t\t Data: {str(date_)}\t\t Horas: {str(time_)}" )
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Imprimir", "Aguarde a impressão",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showinfo('Imprimir',"Por favor, gere a fatura para imprimir o recibo",parent=self.root)

    def logout(self):
        self.root.destroy()
        
    def faturas(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)   
    
    # Função para Remover Placeholder
    def remove_placeholder(self, event):
        current_text = self.txt_anotacoes.get("1.0", "end-1c")
        if current_text == self.placeholder_text:
            self.txt_anotacoes.delete("1.0", "end")
            self.txt_anotacoes.config(fg="black")

    # Função para Adicionar Placeholder
    def add_placeholder(self, event):
        current_text = self.txt_anotacoes.get("1.0", "end-1c")
        if current_text.strip() == "":
            self.txt_anotacoes.insert(1.0, self.placeholder_text)
            self.txt_anotacoes.config(fg="gray")
            

if  __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()