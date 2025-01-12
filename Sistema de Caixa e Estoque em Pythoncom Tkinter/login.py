import os
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class Login_Sistema:
    def __init__(self, root):
        self.root = root
        self.width = 550
        self.height = 700
        
        # Centralizar a janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.title(" " * 10 + "Sistema de Faturamento")
        self.root.config(bg="slate gray")

        # Abrir, redimensionar e exibir a imagem
        img = Image.open("images/logo_sem_fundo.png")  # Abrir a imagem
        img = img.resize((310, 270), Image.Resampling.LANCZOS)  # Redimensionar (largura=200, altura=200)
        self.logo_image = ImageTk.PhotoImage(img)  # Converter para formato compatível com Tkinter

        # Adicionar a imagem ao Label
        self.lbl_Logo_image = Label(self.root, image=self.logo_image, bg="slate gray")
        self.lbl_Logo_image.place(x=120, y=20)

        #Frame do Login
        self.employeeid=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="slate gray")
        login_frame.place(x=100,y=350,width=350,height=300)

        title=Label(login_frame,text="Bem-vindo", font=("Andalus",25,"bold"), bg="slate gray", fg="gray1").place(x=90,y=10)

        lbl_employeeid=Label(login_frame,text="ID Usuário",font=("Andalus",15),bg="slate gray",fg="gray1").place(x=50,y=70)
        txt_username=Entry(login_frame,textvariable=self.employeeid,font=("Andalus",15),bg="#ECECEC").place(x=50,y=100,width=250)

        lbl_pass=Label(login_frame,text="Senha",font=("Andalus",15),bg="slate gray",fg="gray1").place(x=50,y=130)
        txt_username=Entry(login_frame,textvariable=self.password,show="*",font=("Andalus",15),bg="#ECECEC").place(x=50,y=160,width=250)

        #Definir o Botão
        btn_login = Button(
            login_frame,
            command=self.login,
            text="Entrar",
            font=("Andalus",15),
            bg="gray1",
            activebackground="black",
            fg="white",
            cursor="hand2",
        )
        btn_login.place(x=50,y=230,width=250,height=35)

    def login(self):
        con =sqlite3.connect(database=r'tbs.db')
        cur =con.cursor()
        try:
            if self.employeeid.get()=="" or self.password.get()=="":
                messagebox.showerror("Erro","TODOS OS CAMPOS SÃO OBRIGATÓRIOS", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employeeid.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Erro","NOME DE USUÁRIO/SENHA INVALIDA", parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Erro",f"Erro devido a: {str(ex)}", parent=self.root)



# Executar a aplicação
root = Tk()
obj = Login_Sistema(root)
root.mainloop()
