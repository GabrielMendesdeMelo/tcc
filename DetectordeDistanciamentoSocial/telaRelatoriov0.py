from tkinter import *
import mysql.connector

###Criação da variável da Tela inicial
telaRelatorio = Tk()

###Conexão com o banco de dados
con = mysql.connector.connect(host='localhost',database='projetotcc',user='root',password='12345678')

if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao Banco de dados",db_info)

### Classe principal
class Application():
    ##Inicialização da Tela
    def __init__(self):
        self.telaRelatorio = telaRelatorio
        self.telaConfig()
        self.widgets()
        telaRelatorio.mainloop()

    def telaConfig(self):
        #Configurações referente à tela inicial
        self.telaRelatorio.title("Detector de Distanciamento Social")
        self.telaRelatorio.configure(background='#C0C0C0')
        self.telaRelatorio.geometry("900x550")
        self.telaRelatorio.resizable(False, False)

    def widgets(self):
        #Criação do Botão de Finalizar
        self.btnFinalizar = Button(self.telaRelatorio, text="FINALIZAR")
        self.btnFinalizar.place(relx=0.77, rely=0.85, relwidth=0.20, relheight=0.10)

        #Criação do Texto Inicial
        self.label_relatorio = Label(self.telaRelatorio, text="Relatório de Execução:")
        self.label_relatorio.place(relx=0.47, rely=0.05)

Application()