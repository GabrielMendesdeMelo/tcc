from tkinter import *
import mysql.connector

###Criação da variável da Tela inicial
telaInicial = Tk()

###Conexão com o banco de dados
con = mysql.connector.connect(host='localhost',database='projetotcc',user='root',password='12345678')

if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao Banco de dados",db_info)

### Classe principal
class Application():
    ##Inicialização da Tela
    def __init__(self):
        self.telaInicial = telaInicial
        self.telaConfig()
        self.widgets()
        telaInicial.mainloop()

    def telaConfig(self):
        #Configurações referente à tela inicial
        self.telaInicial.title("Detector de Distanciamento Social")
        self.telaInicial.configure(background='#C0C0C0')
        self.telaInicial.geometry("900x550")
        self.telaInicial.resizable(False, False)

    def widgets(self):
        #Criação do Botão de iniciar
        self.btnIniciar = Button(self.telaInicial, text="INICIAR")
        self.btnIniciar.place(relx=0.77, rely=0.85, relwidth=0.20, relheight=0.10)

        #Criação do Texto Inicial
        self.label_bemvindo = Label(self.telaInicial, text="Bem-Vindo!")
        self.label_bemvindo.place(relx=0.47, rely=0.05)

        #Criação do Texto e Entrada da quantidade máxima de pessoas
        self.label_qtdPessoas = Label(self.telaInicial, text="Digite o máximo de pessoas permitidas no ambiente:")
        self.label_qtdPessoas.place(relx=0.35, rely=0.2)
        #Entrada de dados
        self.entry_qtdPessoas = Entry(self.telaInicial)
        self.entry_qtdPessoas.place(relx=0.44, rely=0.25, relheight=0.04)

Application()
