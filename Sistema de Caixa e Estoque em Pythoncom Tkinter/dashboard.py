from tkinter import*
from PIL import Image,ImageTk
from employee import employeeClass
from pdv import SalesDClass
from supplier import supplierClass
from stock import stockClass
from sales import salesClass
from billing import billClass
import sqlite3
from tkinter import messagebox
import os
import time
import tkinter as tk
from tkcalendar import DateEntry  # Usado para campos de data

class TBS:
    def __init__(self,root):
        self.root = root
        self.width = 1350
        self.height = 718
        # Obter a largura e altura da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calcular a posição x e y para centralizar a janela
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        blank_space = " "
        self.root.title(blank_space * 180 + "Dashboard")
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg="light gray")
        
#------------- title --------------
        # Redimensionar a imagem para 100x100
        self.icon_title = Image.open("images/foue1.png")
        self.icon_title = self.icon_title.resize((70, 60))
        self.icon_title = ImageTk.PhotoImage(self.icon_title)
        title=Label(self.root,text="Sistema de Gestão Estoque e Vendas",image=self.icon_title,compound=LEFT,font=("ARIEL",40,"bold"),bg="#4d636d",fg="white",anchor="w",padx=18).place(x=0,y=0,relwidth=1,height=70)

        #------------ logout button -----------
        btn_logout=Button(self.root,text="Sair",command=self.logout,font=("ARIEL",15,"bold"),bg="white",cursor="hand2").place(x=1190,y=10,height=50,width=150)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Bem-vindo ao Sistema de Gestão de Estoque\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("ARIEL",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        # Adicionar widgets para entrada de data
        self.start_date_label = tk.Label(self.root, text="Data Início:", font=("Arial", 12, "bold"),fg="white", bg="light gray")
        self.start_date_label.pack()
        self.start_date_label.place(x=280,y=480)

        self.start_date_entry = DateEntry(self.root, font=("Arial", 12), date_pattern="yyyy-mm-dd")
        self.start_date_entry.pack()
        self.start_date_entry.place(x=370,y=480)

        self.end_date_label = tk.Label(self.root, text="Data Fim:", font=("Arial", 12, "bold"), fg="white", bg="light gray")
        self.end_date_label.pack()
        self.end_date_label.place(x=280,y=518)

        self.end_date_entry = DateEntry(self.root, font=("Arial", 12), date_pattern="yyyy-mm-dd")
        self.end_date_entry.pack()
        self.end_date_entry.place(x=370,y=518)

        #---------------- left menu ---------------
        self.MenuLogo=Image.open("images/logo.png")
        self.MenuLogo=self.MenuLogo.resize((209,205))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="light gray")
        LeftMenu.place(x=0,y=102,width=210,height=560)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("Arial",18),bg="light gray").pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side1.png")


        # Adicionando o espaço entre os botões e removendo o overflow
        btn_employee = Button(LeftMenu, text="Usuários", command=self.employee, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("Arial", 18, "bold"), bg="#4d636d",fg="white", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X, pady=5)  # Ajuste no espaçamento

        btn_supplier = Button(LeftMenu, text="Fornecedores", command=self.supplier, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("Arial", 18, "bold"), bg="#4d636d",fg="white", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X, pady=5)  # Ajuste no espaçamento

        btn_stock = Button(LeftMenu, text="Estoque", command=self.stock, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("Arial", 18, "bold"), bg="#4d636d",fg="white", bd=3, cursor="hand2")
        btn_stock.pack(side=TOP, fill=X, pady=5)  # Ajuste no espaçamento

        btn_sales = Button(LeftMenu, text="Vendas", command=self.sales, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("Arial", 18, "bold"), bg="#4d636d",fg="white", bd=3, cursor="hand2")
        btn_sales.pack(side=TOP, fill=X, pady=5)  # Ajuste no espaçamento

        btn_billing = Button(LeftMenu, text="Cobranças", command=self.billing, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("Arial", 18, "bold"), bg="#4d636d",fg="white", bd=3, cursor="hand2")
        btn_billing.pack(side=TOP, fill=X, pady=5)  # Ajuste no espaçamento
       
        # Dashboard

        # Empregados
        self.lbl_employee=Label(self.root,text="Total Employee\n{ 0 }",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("Arial",18,"bold"))
        self.lbl_employee.place(x=300,y=118,height=150,width=300)

        # Fornecedores
        self.lbl_supplier=Label(self.root,text="Total Supplier\n{ 0 }",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("Arial",18,"bold"))
        self.lbl_supplier.place(x=650,y=118,height=150,width=300)

        # Entradas
        self.lbl_entrada=Label(self.root,text="Total Entradas\n{ 0 }",bd=5,relief=RIDGE,bg="green",fg="white",font=("Arial",18,"bold"))
        self.lbl_entrada.place(x=1018,y=118,height=150,width=300)

        # Estoque
        self.lbl_stocks=Label(self.root,text="Total Product\n{ 0 }",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("Arial",18,"bold"))
        self.lbl_stocks.place(x=300,y=300,height=150,width=300)

        # Vendas
        self.lbl_sale=Label(self.root,text="Total Sales\n{ 0 }",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("Arial",18,"bold"))
        self.lbl_sale.place(x=650,y=300,height=150,width=300)      

        # Saidas
        self.lbl_saidas=Label(self.root,text="Total Saidas\n{ 0 }",bd=5,relief=RIDGE,bg="red",fg="white",font=("Arial",18,"bold"))
        self.lbl_saidas.place(x=1018,y=300,height=150,width=300)
      
        lbl_footer = Label(self.root,text="Sistema de gerenciamento e faturamento de vendas | Juliezer Silva \nPara quaisquer problemas técnicos, entre em contato: + 47996858478",font=("ARIEL 10 bold"),bg="#4d636d",fg="white",borderwidth=1, relief="solid")
        lbl_footer.place(x=0,y=670,relwidth=1,height=50)

        self.update_content()

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def stock(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=stockClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalesDClass(self.new_win)

    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=billClass(self.new_win)
    
    def update_content(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            # Pegando as datas do período selecionado
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()

            # Ajustar as consultas SQL para filtrar por data
            # Total de produtos no estoque
            cur.execute("select * from stock")
            product = cur.fetchall()
            self.lbl_stocks.config(text=f'Estoque\n[ {str(len(product))} ]')

            # Total de fornecedores
            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Fornecedores\n[ {str(len(supplier))} ]')

            # Total de funcionários
            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Funcionários\n[ {str(len(employee))} ]')

        # Contabilizar as vendas do tipo 'Entrada' diretamente da tabela sales
            cur.execute("SELECT COUNT(*) FROM sales WHERE tipo='Entrada'")
            entrada_sales_count = cur.fetchone()[0]  # Pega a quantidade de entradas

        # Atualiza o label com o total de vendas 'Entrada'
            self.lbl_sale.config(text=f'Número de Vendas\n {str(entrada_sales_count)}')

            # Total de entradas no período
            query = f"""
            SELECT SUM(Sales) FROM sales WHERE tipo='Entrada' AND data BETWEEN ? AND ?
            """
            cur.execute(query, (start_date, end_date))
            total_sales = cur.fetchone()[0]  # Pega o valor somado
            total_sales = total_sales if total_sales else 0  # Garante que o valor não seja None
            self.lbl_entrada.config(text=f'Entradas\nR$ {total_sales:.2f}')

            # Total de saídas no período
            query = f"""
            SELECT SUM(Sales) FROM sales WHERE tipo='Saída' AND data BETWEEN ? AND ?
            """
            cur.execute(query, (start_date, end_date))
            total_sales = cur.fetchone()[0]  # Pega o valor somado
            total_sales = total_sales if total_sales else 0  # Garante que o valor não seja None
            self.lbl_saidas.config(text=f'Saídas\nR$ {total_sales:.2f}')

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a : {str(ex)} ", parent=self.root)

        # Atualiza o clock
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"São Bento do Sul-SC\t\t Data: {str(date_)}\t\t Horas: {str(time_)}")
        self.lbl_clock.after(180, self.update_content)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")



if  __name__=="__main__":
    root=Tk()
    obj=TBS(root)
    root.mainloop()