import customtkinter as ctk
from PIL import Image

# Configurar o CustomTkinter para usar o tema moderno
ctk.set_appearance_mode("Dark")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "dark-blue", "green"

class LoginSistema:
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
        self.root.title("Sistema de Faturamento")

        # Abrir, redimensionar e exibir a imagem
        img = Image.open("images/logo_sem_fundo_black.png")
        img_resized = img.resize((350, 300))  # Redimensionar a imagem
        self.logo_image = ctk.CTkImage(img_resized, size=(350, 300))  # Criar CTkImage

        # Adicionar a imagem ao Label
        self.lbl_logo_image = ctk.CTkLabel(self.root, image=self.logo_image, text="")
        self.lbl_logo_image.place(x=100, y=20)

        # Frame do Login
        self.employeeid = ctk.StringVar()
        self.password = ctk.StringVar()

        login_frame = ctk.CTkFrame(self.root, corner_radius=10, width=350, height=300)
        login_frame.place(x=100, y=350)  # Apenas a posição é definida aqui

        title = ctk.CTkLabel(login_frame, text="Bem-vindo", font=("Andalus", 25, "bold"))
        title.place(x=90, y=10)

        lbl_employeeid = ctk.CTkLabel(login_frame, text="Usuário", font=("Andalus", 15))
        lbl_employeeid.place(x=50, y=70)

        txt_username = ctk.CTkEntry(
            login_frame,
            textvariable=self.employeeid,
            font=("Andalus", 15),
            width=250,  # Largura definida aqui
        )
        txt_username.place(x=50, y=100)

        lbl_pass = ctk.CTkLabel(login_frame, text="Senha", font=("Andalus", 15))
        lbl_pass.place(x=50, y=130)

        txt_password = ctk.CTkEntry(
            login_frame,
            textvariable=self.password,
            font=("Andalus", 15),
            show="*",
            width=250,  # Largura definida aqui
        )
        txt_password.place(x=50, y=160)

        # Definir o Botão
        btn_login = ctk.CTkButton(
            login_frame,
            text="Entrar",
            font=("Andalus", 15),
            command=self.login,
            width=250,  # Largura definida aqui
            height=35,  # Altura definida aqui
        )
        btn_login.place(x=50, y=230)

    def login(self):
        username = self.employeeid.get()
        password = self.password.get()

        if username == "admin" and password == "1234":
            ctk.CTkMessageBox(title="Login", message="Login realizado com sucesso!")
        else:
            ctk.CTkMessageBox(title="Login", message="Usuário ou senha incorretos!")

# Executar a aplicação
root = ctk.CTk()
obj = LoginSistema(root)
root.mainloop()
