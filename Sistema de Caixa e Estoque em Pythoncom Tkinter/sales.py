from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1390x800+220+130")
        blank_space = " "
        self.root.title(blank_space + "Vendas Realizadas")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.config(bg="white")

        self.bill_list = []
        self.var_invoice = StringVar()

        #ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        #ProductFrame1.place(x=6,y=150,width=410,height=550)
        lbl_title = Label(self.root, text="Área de fatura do cliente", font=("ARIEL", 30), bg="dim gray", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root, text="Nota No.", font=("ARIEL", 15), bg="white").place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("ARIEL", 15), bg="lightyellow").place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Pesquisar", command=self.search, font=("ARIEL", 15, "bold"), bg="dark slate gray", fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Limpar", command=self.clear, font=("ARIEL", 15, "bold"), bg="lightgray", cursor="hand2").place(x=490, y=100, width=120, height=28)

        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=600)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.sales_list = Listbox(sales_Frame, font=("ARIEL", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=600, height=600)

        lbl_title2 = Label(bill_Frame, text="Área de fatura do cliente", font=("ARIEL", 20), bg="orange").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        self.bill_photo = Image.open("images/cat2.jpg")
        self.bill_photo = self.bill_photo.resize((450, 355))
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=900, y=110)

        # Botão no canto inferior direito para abrir a pasta
        btn_open_folder = Button(self.root, text="Abrir Pasta", command=self.open_folder, font=("ARIEL", 15, "bold"), bg="dim gray", fg="white", cursor="hand2")
        btn_open_folder.place(x=1240, y=700, width=120, height=40)

        self.show()

    def show(self):
        self.show()

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)

        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)

        self.bill_area.delete('1.0', END)
        with open(f'bill/{file_name}', 'r') as fp:
            for i in fp:
                self.bill_area.insert(END, i)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Erro", "Número da fatura deve ser exigido", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                with open(f'bill/{self.var_invoice.get()}.txt', 'r') as fp:
                    self.bill_area.delete('1.0', END)
                    for i in fp:
                        self.bill_area.insert(END, i)
            else:
                messagebox.showerror("Erro", "Número da fatura inválido.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)

    def open_folder(self):
        # Abrir a pasta onde as notas estão salvas
        folder_path = os.path.abspath('bill')
        os.startfile(folder_path)

if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
