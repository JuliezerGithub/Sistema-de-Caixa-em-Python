import time
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class SalesDClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1580x780")
        self.root.title("Formulário de Vendas")
        self.root.config(bg="light gray")

        # Variáveis
        self.var_sales = StringVar()
        self.var_recebeu = StringVar()
        self.var_troco = StringVar()
        self.var_tipo = StringVar()
        self.var_data = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.var_hora = StringVar(value=datetime.now().strftime("%H:%M:%S"))
        self.var_pagamento = StringVar()
        self.var_descricao = StringVar()
        self.var_search_criteria = StringVar()  # Variável para o critério de pesquisa

        # Títulos e entradas
        Label(self.root, text="Vendas Diárias", font=("Arial", 20, "bold"), bg="light gray").pack(pady=5)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Registro de Vendas Diretas!\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("ARIEL",12),bg="dim gray",fg="white")
        self.lbl_clock.place(x=0,y=42,relwidth=1,height=25)
 
         # Chama a função para atualizar a hora
        self.update_clock()

        #------------ Formulário de vendas-----------------
        Label(self.root, text="Pagamento:", font=("Arial", 12), bg="light gray").place(x=30, y=80)
        pagamento_cb = ttk.Combobox(self.root, textvariable=self.var_pagamento, font=("Arial", 12),
                                    values=["Dinheiro", "Pix", "Cartão de Crédito", "Cartão de Débito"], state="readonly")
        pagamento_cb.place(x=200, y=80, width=250)
        pagamento_cb.bind("<<ComboboxSelected>>", self.toggle_recebeu)

        Label(self.root, text="Valor da Venda (R$):", font=("Arial", 12), bg="light gray").place(x=30, y=120)
        Entry(self.root, textvariable=self.var_sales, font=("Arial", 12)).place(x=200, y=120, width=250)

        Label(self.root, text="Valor Recebido (R$):", font=("Arial", 12), bg="light gray").place(x=30, y=160)
        self.entry_recebeu = Entry(self.root, textvariable=self.var_recebeu, font=("Arial", 12), state="disabled")
        self.entry_recebeu.place(x=200, y=160, width=250)

        Label(self.root, text="Troco (R$):", font=("Arial", 12), bg="light gray").place(x=30, y=200)
        Entry(self.root, textvariable=self.var_troco, font=("Arial", 12), state="readonly").place(x=200, y=200, width=250)

        Label(self.root, text="Tipo:", font=("Arial", 12), bg="light gray").place(x=30, y=240)
        ttk.Combobox(self.root, textvariable=self.var_tipo, font=("Arial", 12),
                     values=["Entrada", "Saída"], state="readonly").place(x=200, y=240, width=250)

        Label(self.root, text="Descrição:", font=("Arial", 12), bg="light gray").place(x=30, y=280)
        Entry(self.root, textvariable=self.var_descricao, font=("Arial", 12)).place(x=200, y=280, width=250)

        Label(self.root, text="Data:", font=("Arial", 12), bg="light gray").place(x=30, y=320)
        Entry(self.root, textvariable=self.var_data, font=("Arial", 12), state="readonly").place(x=200, y=320, width=250)

        Label(self.root, text="Hora:", font=("Arial", 12), bg="light gray").place(x=30, y=360)
        Entry(self.root, textvariable=self.var_hora, font=("Arial", 12), state="readonly").place(x=200, y=360, width=250)

        # Botões
        Button(self.root, text="Salvar", command=self.save, font=("Arial", 14), bg="dark slate gray", fg="white").place(x=350, y=420, width=100)
        Button(self.root, text="Limpar", command=self.clear, font=("Arial", 14), bg="slate gray", fg="white").place(x=240, y=420, width=100)

        # Frame para exibição e pesquisa
        self.frame_right = Frame(self.root, bg="light gray", bd=2, relief=RIDGE)
        self.frame_right.place(x=470, y=80, width=980, height=670)

        Label(self.frame_right, text="Pesquisar por:", font=("Arial", 12), bg="light gray").place(x=10, y=10)

        # Combobox para escolher o critério de pesquisa
        search_criteria_cb = ttk.Combobox(self.frame_right, textvariable=self.var_search_criteria, font=("Arial", 12),
                                           values=["Tipo", "Descricao"], state="readonly")
        search_criteria_cb.place(x=200, y=10, width=150)

        Label(self.frame_right, text="Pesquisar:", font=("Arial", 12), bg="light gray").place(x=10, y=50)
        self.var_search = StringVar()
        Entry(self.frame_right, textvariable=self.var_search, font=("Arial", 12)).place(x=200, y=50, width=250)

        Button(self.frame_right, text="Pesquisar", command=self.search, font=("Arial", 12), bg="dark slate gray", fg="white").place(x=460, y=48, width=100)
        Button(self.frame_right, text="Mostrar Todos", command=self.show_all, font=("Arial", 12), bg="slate gray", fg="white").place(x=570, y=48, width=120)

        # Tabela para exibição dos dados
        self.table_frame = Frame(self.frame_right, bg="light gray")
        self.table_frame.place(x=10, y=120, width=950, height=540)

        columns = ("ID", "Vendas", "Recebeu", "Troco", "Tipo", "Descricao", "Data", "Hora", "Pagamento")
        self.sales_table = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=25)
        self.sales_table.pack(fill=BOTH, expand=1)

        # Configurando cabeçalhos e tamanhos das colunas
        self.sales_table.heading("ID", text="ID")
        self.sales_table.heading("Vendas", text="Vendas")
        self.sales_table.heading("Recebeu", text="Recebeu")
        self.sales_table.heading("Troco", text="Troco")
        self.sales_table.heading("Tipo", text="Tipo")
        self.sales_table.heading("Descricao", text="Descrição")
        self.sales_table.heading("Data", text="Data")
        self.sales_table.heading("Hora", text="Hora")
        self.sales_table.heading("Pagamento", text="Pagamento")

        # Ajuste das larguras das colunas
        self.sales_table.column("ID", width=30, anchor="center")
        self.sales_table.column("Vendas", width=80, anchor="center")
        self.sales_table.column("Recebeu", width=80, anchor="center")
        self.sales_table.column("Troco", width=80, anchor="center")
        self.sales_table.column("Tipo", width=80, anchor="center")
        self.sales_table.column("Descricao", width=150, anchor="center")
        self.sales_table.column("Data", width=30, anchor="center")
        self.sales_table.column("Hora", width=30, anchor="center")
        self.sales_table.column("Pagamento", width=50, anchor="center")

        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL, command=self.sales_table.xview)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL, command=self.sales_table.yview)
        self.sales_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)


        # Configurando cabeçalhos e tamanhos das colunas
        self.sales_table.heading("ID", text="ID")
        self.sales_table.heading("Vendas", text="Vendas")
        self.sales_table.heading("Recebeu", text="Recebeu")
        self.sales_table.heading("Troco", text="Troco")
        self.sales_table.heading("Tipo", text="Tipo")
        self.sales_table.heading("Descricao", text="Descrição")
        self.sales_table.heading("Data", text="Data")
        self.sales_table.heading("Hora", text="Hora")
        self.sales_table.heading("Pagamento", text="Pagamento")

        # Ajuste das larguras das colunas
        self.sales_table.column("ID", width=50, anchor="center")
        self.sales_table.column("Vendas", width=120, anchor="center")
        self.sales_table.column("Recebeu", width=120, anchor="center")
        self.sales_table.column("Troco", width=120, anchor="center")
        self.sales_table.column("Tipo", width=80, anchor="center")
        self.sales_table.column("Descricao", width=150, anchor="center")
        self.sales_table.column("Data", width=100, anchor="center")
        self.sales_table.column("Hora", width=100, anchor="center")
        self.sales_table.column("Pagamento", width=120, anchor="center")

        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL, command=self.sales_table.xview)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL, command=self.sales_table.yview)
        self.sales_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)


        # Configurando cabeçalhos e tamanhos das colunas
        for col in columns:
            self.sales_table.heading(col, text=col)
            self.sales_table.column(col, width=100, anchor="center")

        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL, command=self.sales_table.xview)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL, command=self.sales_table.yview)
        self.sales_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Busca os dados ao iniciar
        self.fetch_data()

    def toggle_recebeu(self, event=None):
        """Habilita ou desabilita o campo de valor recebido e calcula o troco se necessário."""
        if self.var_pagamento.get() == "Dinheiro":
            self.entry_recebeu.config(state="normal")
            self.var_recebeu.trace_add("write", self.calculate_troco)
        else:
            self.entry_recebeu.config(state="disabled")
            self.var_recebeu.set("0.0")
            self.var_troco.set("0.0")

    def calculate_troco(self, *args):
        """Calcula o troco automaticamente quando o valor recebido é alterado."""
        try:
            sales = float(self.var_sales.get())
            if self.var_recebeu.get():
                recebeu = float(self.var_recebeu.get())
                troco = recebeu - sales
                if troco < 0:
                    self.var_troco.set("Valor insuficiente")
                else:
                    self.var_troco.set(f"{troco:.2f}")
        except ValueError:
            self.var_troco.set("")

    def save(self):
        # Validações simples
        if not self.var_sales.get() or not self.var_tipo.get() or not self.var_pagamento.get() or not self.var_data.get() or not self.var_hora.get():
            messagebox.showerror("Erro", "Os campos Pagamento, Valor da Venda, Tipo, Data e Hora são obrigatórios!", parent=self.root)
            return

        # Salvando no banco de dados
        try:
            con = sqlite3.connect("tbs.db")
            cur = con.cursor()
            cur.execute(""" 
                INSERT INTO sales (Sales, Recebeu, Troco, Tipo, data, hora, horaVenda, Pagamento, Descricao) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """, (
                float(self.var_sales.get()),
                float(self.var_recebeu.get()) if self.var_pagamento.get() == "Dinheiro" and self.var_recebeu.get() else 0.0,
                float(self.var_troco.get()) if self.var_pagamento.get() == "Dinheiro" and self.var_troco.get() else 0.0,
                self.var_tipo.get(),
                self.var_data.get(),
                self.var_hora.get(),
                datetime.now(),
                self.var_pagamento.get(),
                self.var_descricao.get() or None
            ))
            con.commit()
            con.close()
            messagebox.showinfo("Sucesso", "Venda salva com sucesso!", parent=self.root)
            self.clear()
            
            # Atualiza a tabela com os dados mais recentes
            self.fetch_data()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {str(ex)}", parent=self.root)

    def fetch_data(self):
        """Busca os dados do banco e exibe na tabela."""
        try:
            con = sqlite3.connect("tbs.db")
            cur = con.cursor()
            cur.execute("SELECT rowid, Sales, Recebeu, Troco, Tipo, Descricao, data, hora, Pagamento FROM sales")
            rows = cur.fetchall()
            con.close()

            # Limpa a tabela antes de adicionar novos dados
            self.sales_table.delete(*self.sales_table.get_children())
            for row in rows:
                self.sales_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {str(ex)}", parent=self.root)

    def search(self):
        """Pesquisa os dados no banco de dados de acordo com o critério selecionado."""
        try:
            con = sqlite3.connect("tbs.db")
            cur = con.cursor()

            # Verifica qual critério de pesquisa foi escolhido
            if self.var_search_criteria.get() == "Descricao":
                cur.execute("SELECT rowid, Sales, Recebeu, Troco, Tipo, Descricao, data, hora, Pagamento FROM sales WHERE Descricao LIKE ?", (f"%{self.var_search.get()}%",))
            else:  # Pesquisa por Tipo
                cur.execute("SELECT rowid, Sales, Recebeu, Troco, Tipo, Descricao, data, hora, Pagamento FROM sales WHERE Tipo LIKE ?", (f"%{self.var_search.get()}%",))

            rows = cur.fetchall()
            con.close()

            # Limpa a tabela antes de adicionar novos dados
            self.sales_table.delete(*self.sales_table.get_children())
            if rows:
                for row in rows:
                    self.sales_table.insert("", END, values=row)
            else:
                messagebox.showinfo("Info", "Nenhum registro encontrado.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {str(ex)}", parent=self.root)

    def show_all(self):
        """Exibe todos os dados da tabela."""
        self.var_search.set("")
        self.fetch_data()

    def update_clock(self):
        # Obtém a data e hora atual
        current_time = time.strftime("Registro de Vendas Diretas!\t\t Date: %d/%m/%Y\t\t Time: %H:%M:%S")
        
        # Atualiza o texto do label
        self.lbl_clock.config(text=current_time)
        
        # Agendar para atualizar novamente em 1000ms (1 segundo)
        self.root.after(1000, self.update_clock)        
    
    def clear(self):
        # Limpar todos os campos
        self.var_sales.set("")
        self.var_recebeu.set("")
        self.var_troco.set("")
        self.var_tipo.set("")
        self.var_data.set(datetime.now().strftime("%Y-%m-%d"))
        self.var_hora.set(datetime.now().strftime("%H:%M:%S"))
        self.var_pagamento.set("")
        self.var_descricao.set("")
        self.entry_recebeu.config(state="disabled")


if __name__ == "__main__":
    root = Tk()
    app = SalesDClass(root)
    root.mainloop()
