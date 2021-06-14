from tkinter import *
import mysql.connector


import numpy as np
import time
import cv2
import math
import imutils

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
        self.btnIniciar = Button(self.telaInicial, text="INICIAR", command=self.carregaDetectorDistanciaSocial)
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

    def carregaDetectorDistanciaSocial(self):

        self.telaInicial.destroy()

        labelsPath = "./coco.names"
        CONTORNO = open(labelsPath).read().strip().split("\n")

        np.random.seed(42)
        CORES = np.random.randint(0, 255, size=(len(CONTORNO), 3), dtype="uint8")

        weightsPath = "./yolov3.weights"
        configPath = "./yolov3.cfg"

        print("Carregando Machine Learning...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        # inicia Banco de Dados

        def criar_conexao(host, usuario, senha, banco):
            return mysql.connector.connect(host=host, user=usuario, password=senha, database=banco)

        def fechar_cobexao(con):
            return con.close()

        # --------------------------------------------------------
        # Contador
        Pessoa_Local = []
        Total_pessoas = []
        Id_pessoa = []
        # ------------------------------------------------------

        # inicia camera

        print("Iniciando CÃ¢mera...")
        cap = cv2.VideoCapture(0)

        while (cap.isOpened()):
            ret, image = cap.read()
            image = imutils.resize(image, width=800)
            (H, W) = image.shape[:2]
            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()
            print("Tempo de captura/frame : {:.6f} segundos".format(end - start))
            boxes = []
            confidences = []
            classIDs = []

            # identifica pessoas na imagem e define objetos

            for output in layerOutputs:
                for deteccao in output:
                    scores = deteccao[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > 0.1 and classID == 0:
                        box = deteccao[0:4] * np.array([W, H, W, H])
                        (centroX, centroY, width, height) = box.astype("int")
                        x = int(centroX - (width / 2))
                        y = int(centroY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
            ind = []
            for i in range(0, len(classIDs)):
                if (classIDs[i] == 0):
                    ind.append(i)
            a = []
            b = []

            # ------------------------------------------------------------------
            # Calcula Pessoas
            #    if boxes not in Id_pessoa:
            #       Id_pessoa.append(boxes)

            # ------------------------------------------------------------

            # calcula distancia dos objetos

            if len(idxs) > 0:
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    a.append(x)
                    b.append(y)

            distancia = []
            nsd = []
            for i in range(0, len(a) - 1):
                for k in range(1, len(a)):
                    if (k == i):
                        break
                    else:
                        x_dist = (a[k] - a[i])
                        y_dist = (b[k] - b[i])
                        d = math.sqrt(x_dist * x_dist + y_dist * y_dist)
                        distancia.append(d)
                        if (d <= 220):
                            nsd.append(i)
                            nsd.append(k)
                        nsd = list(dict.fromkeys(nsd))
                        print(nsd)
            color = (0, 0, 255)

            # verifica se a distancia foi violada

            for i in nsd:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "Distancia violada"
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            color = (0, 255, 0)
            if len(idxs) > 0:
                for i in idxs.flatten():
                    if (i in nsd):
                        break
                    else:
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])
                        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                        text = 'Distancia aceitavel'
                        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                # calcula pessoas
                Pessoa_Local = len(boxes)
                Total_pessoas = len(Id_pessoa)

                Pessoa_Local_txt = "Pessoas_no_Local: {}".format(Pessoa_Local)
                Total_pessoas_txt = "Total_de_Pessoas: {}".format(Total_pessoas)

                cv2.putText(image, Pessoa_Local_txt, (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                cv2.putText(image, Total_pessoas_txt, (5, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                # -------------------------------------------------------------------------------------------------
            cv2.imshow("Detector de Distancia Social", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()




Application()
