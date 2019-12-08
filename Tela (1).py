#Imports
import MySQLdb
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import MySQLdb
import re
import datetime
import tkMessageBox


from random import randint
from datetime import timedelta
from Tkinter import *
from time import strftime

# Informacoes do broker de mensagens
Broker = "192.168.0.177"

sub_topic = "sensor/instructions"    # receive messages on this topic

pub_topic = "sensor/data"       # send messages to this topic


############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()


def index_alarmes(i_atual,method):
	if method == "SUM":
		i = i_atual+1
	elif method == "SBT":
		i = i_atual-1
	
	return i

def consultar(query):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	cur.execute(query)
	
	for row in cur.fetchall():
		Nome = str(row[0])
		reposta = '{0}'.format(Nome)
		
    	return resposta

def consultar_opc(query):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	cur.execute(query)
	resposta1 = cur.fetchall()
		
	return resposta1

def consultar_estoque(query):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	cur.execute(query)
	
	for row in cur.fetchall():
		estoque = str(row[0])
		resposta = '{0}'.format(estoque)
		
    	return resposta

def consultar_medicamento(query):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	cur.execute(query)
	
	for row in cur.fetchall():
		composto = str(row[0])
		quantidade = str(row[1])
		unidade = str(row[2])
		via = str(row[3])
		resposta = '{0} {1} {2} {3}'.format(composto,quantidade,unidade,via)
		
    	return resposta
	
def cadastrar_pacientes(nome,sobrenome,cpf,id_hosp,plano,data):
	
	query = StringVar()
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	cur = db.cursor()
	
	query = """INSERT INTO `pacientes`(`Nome`, `Sobrenome`, `CPF`, `ID_Hospital`, `Plano`, `Data_Int`) VALUES ('%s','%s','%s','%s','%s','%s')""" % (nome,sobrenome,cpf,id_hosp,plano,data)
	
	cur.execute(query)
	db.commit()
	
    	return

def cadastrar_medicamentos(composto,quantidade,unidade,via,fabricante):
	
	query = StringVar()
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	cur = db.cursor()
	
	query = """INSERT INTO  `medicamentos`(`Composto`, `Quantidade`, `Unidade_de_Medida`, `Via`, `Fabricante`) VALUES ('%s','%s','%s','%s','%s')""" % (composto,quantidade,unidade,via,fabricante)
	
	cur.execute(query)
	
	db.commit()
	
    	return

def cadastrar_prescricao(cpf,nome,sobrenome,composto,quantidade,unidade,via,periodicidade,datainicio,proxdose):
	
	query = StringVar()
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	cur = db.cursor()
	
	query = """INSERT INTO `prescricoes`(`CPF`, `Nome`, `Sobrenome`, `Composto`, `Dosagem`, `Unidade`, `Via`, `Periodicidade`, `Data_Inicio`, `Proxima_Dose`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (cpf,nome,sobrenome,composto,quantidade,unidade,via,periodicidade,datainicio,proxdose)
	
	cur.execute(query)
	db.commit()

def atualizar_gavetas(gavetaATT,new_Composto,new_Quantidade,new_Unidade_de_Medida,new_Via,new_Estoque):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	
	query1 = """UPDATE `medicamentos` SET `Gaveta` = '0' WHERE `Gaveta` = '%s'""" % (gavetaATT)
	query2 = """UPDATE `medicamentos` SET `Gaveta` = '%s', `Estoque` = '%s' WHERE `Composto` = '%s' AND `Quantidade` = '%s' AND `Unidade_de_Medida` = '%s' AND `Via` = '%s'""" % (gavetaATT,new_Estoque,new_Composto,new_Quantidade,new_Unidade_de_Medida,new_Via)
	
	cur.execute(query1)
	cur.execute(query2)
	db.commit()
	cur.close()

def atualizar_estoque_gavetax(gavetaX,new_Estoque_Atualizar):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	
	query = """UPDATE `medicamentos` SET `Estoque` = '%s' WHERE `Gaveta` = '%s'""" % (new_Estoque_Atualizar,gavetaX)
	
	cur.execute(query)
	db.commit()
	cur.close()

def consultar_alarmes_ativos(query):
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	
	cur = db.cursor()
	cur.execute(query)
	resposta1 = cur.fetchall()
		
	return resposta1

def apagarChamadoAtendido(nome,sobrenome,composto,dosagem,unidade,via,periodicidade,proxima_Dose,nova_ProximaDose):

	query = StringVar()
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	cur = db.cursor()
	
	query = """UPDATE `prescricoes` SET `Proxima_Dose` = '%s' WHERE `Nome` ='%s' AND `Sobrenome` ='%s' AND `Composto` ='%s' AND `Dosagem` ='%s' AND `Unidade` ='%s' AND `Via`  ='%s'AND `Proxima_Dose`  ='%s'""" % (nova_ProximaDose,nome,sobrenome,composto,dosagem,unidade,via,proxima_Dose)
	
	cur.execute(query)
	
	db.commit()
	
    	return




#Classe de Inicio login
class Welcome():
    
    def __init__(self,master):
        
        #Inicializa a Tela Principal como Master
        self.master = master
        
        #Define os tamanhos e a posicaoo de inicio da Tela Principal
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
        yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('TCC - Guilherme Curtolo: Supply Point')
	self.master.configure(bg='white')
        
        #Widgets da Tela Principal
	
	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()
	
	self.relBanco = Label(self.master,bg='white', font=("Helvetia",12))
	self.relBanco.place(x=630,y=100)
	self.tacBanco()
	
        self.fotoIFSPc = Canvas(self.master, width=225,height=225,highlightthickness=0)
	self.fotoIFSP  = PhotoImage(file = '/home/pi/imagens/ifsp.png')
	self.photoIFSP = self.fotoIFSPc.create_image(112,112, image=self.fotoIFSP)
	self.fotoIFSPc.image = self.fotoIFSP
	self.fotoIFSPc.place(x=10,y=10)
	
	self.canvasText = Canvas(self.master, width=300,height=100,bg='white',highlightthickness=0)
	self.canvasText_t = self.canvasText.create_text(150,50,text='SUPPLY POINT',font=("Helvetica",27))
	self.canvasText.place(x=250,y=50)	
	
	self.Fbutton1 = Frame(self.master,width = 300,height = 50)
	self.Fbutton1.pack_propagate(0)
	self.Fbutton1.place(x=250,y=300)
        self.button1 = Button(self.Fbutton1,text="OK",bg='white',command=self.gotoMenu,font=("Helvetica",18)).pack(fill=BOTH, expand=1)
	
	self.Fbutton2 = Frame(self.master,width = 100,height = 50)
	self.Fbutton2.pack_propagate(0)
	self.Fbutton2.place(x=690,y=420)
        self.button2 = Button(self.Fbutton2,text="EXIT",bg='white',command=self.finish,font=("Helvetica",12)).pack(fill=BOTH, expand=1)

    #Funcao que chama a Segunda Tela
    def gotoMenu(self):
        root2=Toplevel(self.master)
        myGUI = MenuPrincipal(root2)
    
    #Funcao que destroy a Tela Principal
    def finish(self):
	FecharYN = tkMessageBox.askyesno("EXIT","Deseja Encerrar o Supply Point?",parent=self.master)
	if FecharYN == True:
		self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)
	
    def ticBanco(self):
	if len(consultar_alarmes_ativos("SELECT `Nome`,`Sobrenome`,`Composto`,`Dosagem`,`Unidade`,`Via`, `Periodicidade`, `Proxima_Dose` FROM `prescricoes` WHERE `Proxima_Dose` <= NOW() order by `Proxima_Dose`")) > 0:
		print("Ha Alarmes Ativos!")
		client.publish(pub_topic,"Ha Alarmes Ativos!")
	else:
		print("Nao ha Alarmes Ativos!")
		client.publish(pub_topic,"Nao ha Alarmes Ativos!")

    def tacBanco(self):
	self.ticBanco()
	self.relBanco.after(5000,self.tacBanco)


#Classe da tela do Menu Principal
class MenuPrincipal():

    def __init__(self,master):
        
        #Variaveis que irao ser utilizadas nessa tela
        self.nhours=DoubleVar()
        self.salaryh=DoubleVar()
	self.nome = StringVar()
        
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Enfermeiro: ')
	self.master.configure(bg='white')

        #Widgets da Segunda Tela

	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	self.fotoIFSPc = Canvas(self.master, width=225,height=225,highlightthickness=0)
	self.fotoIFSP  = PhotoImage(file = '/home/pi/imagens/ifsp.png')
	self.photoIFSP = self.fotoIFSPc.create_image(112,112, image=self.fotoIFSP)
	self.fotoIFSPc.image = self.fotoIFSP
	self.fotoIFSPc.place(x=10,y=10)
	
	self.canvasText = Canvas(self.master, width=225,height=70,bg='white',highlightthickness=0)
	self.canvasText_t = self.canvasText.create_text(112,50,text='Bem vindo ao Supply Point, \nEnfermeiro:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText.place(x=10,y=220)

	self.texto = Label(self.master, bg='white', textvariable=self.nome,font=("Helvetia",10))
	#self.nome.set(consultar("SELECT Nome from mydb.tabela_1 WHERE `ID` = '2'"))
	self.texto.place(x=50,y=300)

        self.can1 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto1 = PhotoImage(file = '/home/pi/imagens/1.gif')
	self.photo1 = self.can1.create_image(25,25, image=self.foto1)
	self.can1.image = self.foto1
	self.can1.place(x=280,y=65)

	self.can2 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto2= PhotoImage(file = '/home/pi/imagens/2.gif')
	self.photo2 = self.can2.create_image(25,25, image=self.foto2)
	self.can2.image = self.foto2
	self.can2.place(x=280,y=125)

	self.can3 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto3 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo3 = self.can3.create_image(25,25, image=self.foto3)
	self.can3.image = self.foto3
	self.can3.place(x=280,y=185)

	self.can4 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto4 = PhotoImage(file = '/home/pi/imagens/4.gif')
	self.photo4 = self.can4.create_image(25,25, image=self.foto4)
	self.can4.image = self.foto4
	self.can4.place(x=280,y=245)

	self.can5 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto5 = PhotoImage(file = '/home/pi/imagens/5.gif')
	self.photo5 = self.can5.create_image(25,25, image=self.foto5)
	self.can5.image = self.foto5
	self.can5.place(x=280,y=305)

	self.can6 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto6 = PhotoImage(file = '/home/pi/imagens/6.gif')
	self.photo6 = self.can6.create_image(25,25, image=self.foto6)
	self.can6.image = self.foto6
	self.can6.place(x=280,y=365)
	
	self.can7 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto7 = PhotoImage(file = '/home/pi/imagens/7.gif')
	self.photo6 = self.can7.create_image(25,25, image=self.foto7)
	self.can7.image = self.foto7
	self.can7.place(x=650,y=165)
	
	
	self.botao1 = Button(self.master, text='Retirada Livre',command=self.RetiradaLivre, width=20, height=2,bg='white')
        self.botao1.place(x=370,y=65)

	self.botao2 = Button(self.master, text='Atender Alarmes',command = self.AtenderAlarmes, width=20, height=2,bg='white')
        self.botao2.place(x=370,y=125)

	self.botao3 = Button(self.master, text='Verificar Estoque', command = self.VerificarEstoque, width=20, height=2,bg='white')
        self.botao3.place(x=370,y=185)

	self.botao4 = Button(self.master, text='Atualizar Estoque', command = self.AtualizarEstoque, width=20, height=2,bg='white')
        self.botao4.place(x=370,y=245)

	self.botao5 = Button(self.master, text='Cadastrar Pacientes', command = self.CadastrarPacientes, width=20, height=2,bg='white')
        self.botao5.place(x=370,y=305)

	self.botao6 = Button(self.master, text='Cadastrar Medicamentos', command = self.CadastrarMedicamentos, width=20, height=2,bg='white')
        self.botao6.place(x=370,y=365)
	
	self.botao7 = Button(self.master, text='Prescrever Medicamentos', command = self.PrescreverMedicamentos, width=20, height=2,bg='white')
        self.botao7.place(x=580,y=220)

	self.botao8 = Button(self.master, text='SAIR', command=self.myQuit, width=15, height=2,bg='white')
	self.botao8.place(x=630,y=420)


    #Funcao que volta pra Tela Principal
    def myQuit(self):
	FecharYN = tkMessageBox.askyesno("LOG-OUT","Enfermeiro: \nDeseja fazer Log-out?",parent=self.master)
	if FecharYN == True:
		self.master.destroy()
    
    #Funcao que vai para a tela Retirada Livre
    def RetiradaLivre(self):
        root3=Toplevel(self.master)
        myGUI = RetiradaLivreTela(root3)
        
    #Funcao que vai para a tela Atender Alarmes
    def AtenderAlarmes(self):
        root3=Toplevel(self.master)
        myGUI = AtenderAlarmes(root3)
	
    #Funcao que vai para a tela Verificar Estoque
    def VerificarEstoque(self):
        root3=Toplevel(self.master)
        myGUI = VerificarEstoque(root3)

    #Funcao que vai para a tela Atualizar Estoque
    def AtualizarEstoque(self):
        root3=Toplevel(self.master)
        myGUI = AtualizarEstoque(root3)
	
    #Funcao que vai para a tela Cadastrar Pacientes
    def CadastrarPacientes(self):
        root3=Toplevel(self.master)
        myGUI = CadastrarPacientes(root3)

    #Funcao que vai para a tela Cadastrar Pacientes
    def CadastrarMedicamentos(self):
        root3=Toplevel(self.master)
        myGUI = CadastrarMedicamentos(root3)

    def PrescreverMedicamentos(self):
	    root3=Toplevel(self.master)
	    myGUI = PrescreverMedicamentos(root3)

    #funcao para o relogio funcionar
    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)


#Classe da Tela de Retirada Livre
class RetiradaLivreTela():
    
    def __init__(self,master):
	    
	self.mdc1 = StringVar()
	self.mdc2 = StringVar()
	self.mdc3 = StringVar()
	self.mdc4 = StringVar()
	
	self.qtd1 = IntVar()
	self.qtd2 = IntVar()
	self.qtd3 = IntVar()
	self.qtd4 = IntVar()
        
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Retirada Livre')
	self.master.configure(bg='white')
        
        #Widgets da Segunda Tela

        self.can1 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto1 = PhotoImage(file = '/home/pi/imagens/1.gif')
	self.photo1 = self.can1.create_image(25,25, image=self.foto1)
	self.can1.image = self.foto1
	self.can1.place(x=300,y=50)
	
	self.Text1 = Canvas(self.master, width=150,height=50,bg='white',highlightthickness=0)
	self.Text1_t = self.Text1.create_text(75,25,text='Retirada Livre',font=("Helvetica",15),justify='center')
	self.Text1.place(x=350,y=50)



	self.can31 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto31 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo31 = self.can31.create_image(25,25, image=self.foto31)
	self.can31.image = self.foto31
	self.can31.place(x=110,y=170)
	
	self.texto1 = Label(self.master, bg='white', textvariable=self.mdc1,font=("Helvetia",10))
	self.mdc1.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='1'"))
	self.texto1.place(x=160,y=175)
	
	self.entry1 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd1, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd1.set("")
	self.entry1.place(x=160,y=195)
	
	self.botao1 = Button(self.master, text = 'Retirar', command=self.retirada01, width=6, height=1, font=("Helvetia",7))
	self.botao1.place(x=215,y=195)
	
	
	
	self.can32 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto32 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo32 = self.can32.create_image(25,25, image=self.foto32)
	self.can32.image = self.foto32
	self.can32.place(x=445,y=170)
	
	self.texto2 = Label(self.master, bg='white', textvariable=self.mdc2,font=("Helvetia",10))
	self.mdc2.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='2'"))
	self.texto2.place(x=495,y=175)
	
	self.entry2 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd2, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd2.set("")
	self.entry2.place(x=495,y=195)
	
	self.botao2 = Button(self.master, text = 'Retirar', command=self.retirada02, width=6, height=1, font=("Helvetia",7))
	self.botao2.place(x=550,y=195)
	
	
	
	self.can33 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto33 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo33 = self.can33.create_image(25,25, image=self.foto33)
	self.can33.image = self.foto33
	self.can33.place(x=110,y=275)
	
	self.texto3 = Label(self.master, bg='white', textvariable=self.mdc3,font=("Helvetia",10))
	self.mdc3.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='3'"))
	self.texto3.place(x=160,y=280)
	
	self.entry3 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd3, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd3.set("")
	self.entry3.place(x=160,y=300)
	
	self.botao3 = Button(self.master, text = 'Retirar', command=self.retirada03, width=6, height=1, font=("Helvetia",7))
	self.botao3.place(x=215,y=300)
	
	
	
	self.can34 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto34 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo34 = self.can34.create_image(25,25, image=self.foto34)
	self.can34.image = self.foto34
	self.can34.place(x=445,y=275)
	
	self.texto4 = Label(self.master, bg='white', textvariable=self.mdc4,font=("Helvetia",10))
	self.mdc4.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='4'"))
	self.texto4.place(x=495,y=280)
	
	self.entry4 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd4, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd4.set("")
	self.entry4.place(x=495,y=300)
	
	self.botao4 = Button(self.master, text = 'Retirar', command=self.retirada04, width=6, height=1, font=("Helvetia",7))
	self.botao4.place(x=550,y=300)
	


	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcao para voltar para o menu principal
    def myQuit(self):
        self.master.destroy()

    #funcoes para funcionar o relogio
    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)

    #funcoes para retirar os medicamentos do estoque
    
    def retirada01(self):
	
	if all(x.isdigit() for x in self.entry1.get()):
		
		self.retiraQTD_01 = int(self.entry1.get())
		self.qtdAtual1 = int(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '1'")[0])
		
		if self.qtdAtual1 < self.retiraQTD_01:
			self.warning("01")
		elif self.qtdAtual1 >= self.retiraQTD_01:
			self.resultado1 = self.qtdAtual1 - self.retiraQTD_01
			atualizar_estoque_gavetax("1",str(self.resultado1))
			self.retiradaConcluida("1",self.mdc1.get(),str(self.retiraQTD_01))
			
	else: 
		self.verificarNumerosQtd("01")
	
	self.qtd1.set("")
		
    def retirada02(self):
	    
	if all(x.isdigit() for x in self.entry2.get()):
		
		self.retiraQTD_02 = int(self.entry2.get())
		self.qtdAtual2 = int(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '2'")[0])
		
		if self.qtdAtual2 < self.retiraQTD_02:
			self.warning("02")
		elif self.qtdAtual2 >= self.retiraQTD_02:
			self.resultado2 = self.qtdAtual2 - self.retiraQTD_02
			atualizar_estoque_gavetax("2",str(self.resultado2))
			self.retiradaConcluida("2",self.mdc2.get(),str(self.retiraQTD_02))
		
		
	
	else:
		self.verificarNumerosQtd("02")
		
	self.qtd2.set("")
		
    def retirada03(self):
	    
	if all(x.isdigit() for x in self.entry3.get()):
		
		self.retiraQTD_03 = int(self.entry3.get())
		self.qtdAtual3 = int(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '3'")[0])
		
		if self.qtdAtual3 < self.retiraQTD_03:
			self.warning("03")
		elif self.qtdAtual3 >= self.retiraQTD_03:
			self.resultado3 = self.qtdAtual3 - self.retiraQTD_03
			atualizar_estoque_gavetax("3",str(self.resultado3))
			self.retiradaConcluida("3",self.mdc3.get(),str(self.retiraQTD_03))
	
	else: 
		self.verificarNumerosQtd("03")
    
	self.qtd3.set("")
    
    def retirada04(self):
	    
	if all(x.isdigit() for x in self.entry4.get()):
		
		self.retiraQTD_04 = int(self.entry4.get())
		self.qtdAtual4 = int(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '4'")[0])
		
		if self.qtdAtual4 < self.retiraQTD_04:
			self.warning("04")
		elif self.qtdAtual4 >= self.retiraQTD_04:
			self.resultado4 = self.qtdAtual4 - self.retiraQTD_04
			atualizar_estoque_gavetax("4",str(self.resultado4))
			self.retiradaConcluida("4",self.mdc4.get(),str(self.retiraQTD_04))
		
	else:
		self.verificarNumerosQtd("04")
	
	self.qtd4.set("")
	
    def warning(self,gaveta):
	self.titulo = """Gaveta %s""" % gaveta
	tkMessageBox.showerror(self.titulo, "Nao ha estoque suficiente desse medicamento!",parent=self.master)
	
    def retiradaConcluida(self,gaveta,composto,qtd):
	self.titulo = """Gaveta %s""" % gaveta
	self.mensagem = """Retirada:\n\nMedicamento: %s\nQtd: %s""" % (composto,qtd) 
	tkMessageBox.showinfo(self.titulo,self.mensagem,parent=self.master)

    def verificarNumerosQtd(self,gaveta):
	self.titulo = """Gaveta %s""" % gaveta
	tkMessageBox.showerror(self.titulo, "Caracter invalido em um campo numerico!",parent=self.master)
	

#Classe da Tela de Atender Alarmes
class AtenderAlarmes():
    
    def __init__(self,master):
        
        #Inicializa a Segunda tela como Master
        self.master=master
	
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Atender Alarmes')
	self.master.configure(bg='white')
        
	alarmesAtivos = consultar_alarmes_ativos("SELECT `Nome`,`Sobrenome`,`Composto`,`Dosagem`,`Unidade`,`Via`, `Periodicidade`, `Proxima_Dose` FROM `prescricoes` WHERE `Proxima_Dose` <= NOW() order by `Proxima_Dose`")
	
        #Widgets da Segunda Tela

	self.can2 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto2= PhotoImage(file = '/home/pi/imagens/2.gif')
	self.photo2 = self.can2.create_image(25,25, image=self.foto2)
	self.can2.image = self.foto2
	self.can2.place(x=290,y=50)
	
	self.Text2 = Canvas(self.master, width=170,height=50,bg='white',highlightthickness=0)
	self.Text2_t = self.Text2.create_text(85,25,text='Atender Alarmes',font=("Helvetica",15),justify='center')
	self.Text2.place(x=340,y=50)
	
	scrollbarV = Scrollbar(self.master, orient=VERTICAL)
	
	self.alarmes = Listbox(self.master, width=60, selectmode=SINGLE, yscrollcommand=scrollbarV.set, relief=SUNKEN)
	self.alarmes.place(x=80,y=170)
	self.alarmes.insert(END,*alarmesAtivos)
	
	
	self.i = 0
	self.select(self.i)

	self.botaoUp = Button(self.master, text='>', command=self.botaoUp, width=5, height=2,bg='white')
	self.botaoUp.place(x=600,y=195)
	
	self.botaoDown = Button(self.master, text='<', command=self.botaoDown, width=5, height=2,bg='white')
	self.botaoDown.place(x=600,y=255)
	
	
	self.botaoAtender = Button(self.master, text='Atender Alarme', command=self.botaoAtenderAlarme, width=30, height=2,bg='white')
	self.botaoAtender.place(x=190,y=350)


	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes da paginabutton1

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)

    def botaoUp(self):
	if self.i < (self.alarmes.size()-1):
		self.i = index_alarmes(self.i,"SUM")
		self.select(self.i)
	else:
		self.i = (self.alarmes.size()-1)
		self.select(self.i)
	
    def botaoDown(self):
	if self.i > 0:
		self.i = index_alarmes(self.i,"SBT")
		self.select(self.i)
	else:
		self.i = 0
		self.select(self.i)
		
    def botaoAtenderAlarme(self):
	    
	self.alarmeAtendido = self.alarmes.get(self.alarmes.curselection())
	
	self.nome = self.alarmeAtendido[0]
	self.sobrenome = self.alarmeAtendido[1]
	self.composto = self.alarmeAtendido[2] 
	self.dosagem = self.alarmeAtendido[3]
	self.unidade = self.alarmeAtendido[4]
	self.via = self.alarmeAtendido[5]
	self.periodicidade = self.alarmeAtendido[6]
	self.proxima_Dose = self.alarmeAtendido[7]
	
	if self.periodicidade == "04/04 hrs":
		
		self.nova_ProximaDose = (datetime.datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")
		
	elif self.periodicidade == "06/06 hrs":
		
		self.nova_ProximaDose = (datetime.datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
		
	elif self.periodicidade == "08/08 hrs":
		
		self.nova_ProximaDose = (datetime.datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
		
	elif self.periodicidade == "12/12 hrs":
		
		self.nova_ProximaDose = (datetime.datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M")
		
	elif self.periodicidade == "24/24 hrs":
		
		self.nova_ProximaDose = (datetime.datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
	
	print(self.nova_ProximaDose)
	
	
	
	apagarChamadoAtendido(self.nome,self.sobrenome,self.composto,self.dosagem,self.unidade,self.via,self.periodicidade,self.proxima_Dose,self.nova_ProximaDose)
        
	self.alarmes.delete(0, END)
	alarmesAtivos = consultar_alarmes_ativos("SELECT `Nome`,`Sobrenome`,`Composto`,`Dosagem`,`Unidade`,`Via`, `Periodicidade`, `Proxima_Dose` FROM `prescricoes` WHERE `Proxima_Dose` <= NOW() order by `Proxima_Dose`")
	self.alarmes.insert(END,*alarmesAtivos)
	self.atendimentoConcluido(self.nome,self.sobrenome,self.composto,self.dosagem,self.unidade,self.via,self.periodicidade,self.proxima_Dose)
	
	self.select(0)
	
    def select(self, index):
	    self.alarmes.select_clear(0, "end")
	    self.alarmes.selection_set(index)
	    self.alarmes.see(index)
	    self.alarmes.activate(index)
	    self.alarmes.selection_anchor(index)

    def atendimentoConcluido(self,nome1,sobrenome1,composto1,dosagem1,unidade1,via1,periodicidade1,proxima_Dose1):
	self.titulo = "Alarme Atendido"
	self.mensagem = """Alarme atendido com sucesso!\n\nPaciente: %s %s\nMedicamento: %s %s%s\nVia: %s\nHorario Previsto: %s\nHorario de realizacao: %s""" % (nome1,sobrenome1,composto1,dosagem1,unidade1,via1,proxima_Dose1,strftime('%Y-%m-%d\n%H:%M:%S')) 
	tkMessageBox.showinfo(self.titulo,self.mensagem,parent=self.master)


#Classe da Tela de Verificar Estoque
class VerificarEstoque():
    
    def __init__(self,master):
        
	self.mdc1 = StringVar()
	self.mdc2 = StringVar()
	self.mdc3 = StringVar()
	self.mdc4 = StringVar()
	
	self.qtd1 = StringVar()
	self.qtd2 = StringVar()
	self.qtd3 = StringVar()
	self.qtd4 = StringVar()
	
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Verificar Estoque')
	self.master.configure(bg='white')
        
        #Widgets da Segunda Tela

	self.can3 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto3 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo3 = self.can3.create_image(25,25, image=self.foto3)
	self.can3.image = self.foto3
	self.can3.place(x=290,y=50)

	self.Text3 = Canvas(self.master, width=170,height=50,bg='white',highlightthickness=0)
	self.Text3_t = self.Text3.create_text(85,25,text='Verificar Estoque',font=("Helvetica",15),justify='center')
	self.Text3.place(x=340,y=50)



	#Gaveta 01
	self.can31 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto31 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo31 = self.can31.create_image(25,25, image=self.foto31)
	self.can31.image = self.foto31
	self.can31.place(x=110,y=170)
	
	self.texto1 = Label(self.master, bg='white', textvariable=self.mdc1,font=("Helvetia",10))
	self.mdc1.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='1'"))
	self.texto1.place(x=160,y=175)
	
	self.txt1 = Label(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd1, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd1.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '1'"))
	self.txt1.place(x=160,y=195)
	
	
	
	#Gaveta 02
	self.can32 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto32 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo32 = self.can32.create_image(25,25, image=self.foto32)
	self.can32.image = self.foto32
	self.can32.place(x=445,y=170)
	
	self.texto2 = Label(self.master, bg='white', textvariable=self.mdc2,font=("Helvetia",10))
	self.mdc2.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='2'"))
	self.texto2.place(x=495,y=175)
	
	self.txt2 = Label(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd2, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd2.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '2'"))
	self.txt2.place(x=495,y=195)
	
	
	
	#Gaveta 03
	self.can33 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto33 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo33 = self.can33.create_image(25,25, image=self.foto33)
	self.can33.image = self.foto33
	self.can33.place(x=110,y=275)
	
	self.texto3 = Label(self.master, bg='white', textvariable=self.mdc3,font=("Helvetia",10))
	self.mdc3.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='3'"))
	self.texto3.place(x=160,y=280)
	
	self.txt3 = Label(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd3, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd3.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '3'"))
	self.txt3.place(x=160,y=300)
	
	
	
	#Gaveta 04
	self.can34 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto34 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo34 = self.can34.create_image(25,25, image=self.foto34)
	self.can34.image = self.foto34
	self.can34.place(x=445,y=275)
	
	self.texto4 = Label(self.master, bg='white', textvariable=self.mdc4,font=("Helvetia",10))
	self.mdc4.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`, `Via` FROM `medicamentos` WHERE `Gaveta`='4'"))
	self.texto4.place(x=495,y=280)
	
	self.txt4 = Label(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd4, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd4.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta` = '4'"))
	self.txt4.place(x=495,y=300)
	


	#Relogio
	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	#Funcao voltar menu
	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes da paginabutton1

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)


#Classe da Tela de Atualizar Estoque
class AtualizarEstoque():
    
    def __init__(self,master):
        
	self.mdc1 = StringVar()
	self.mdc2 = StringVar()
	self.mdc3 = StringVar()
	self.mdc4 = StringVar()
	
	self.qtd1 = IntVar()
	self.qtd2 = IntVar()
	self.qtd3 = IntVar()
	self.qtd4 = IntVar()
	
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Atualizar Estoque')
	self.master.configure(bg='white')
        
        #Widgets da Segunda Tela
	
	#Opcao do Menu 
	self.can4 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto4 = PhotoImage(file = '/home/pi/imagens/4.gif')
	self.photo4 = self.can4.create_image(25,25, image=self.foto4)
	self.can4.image = self.foto4
	self.can4.place(x=290,y=50)

	self.Text4 = Canvas(self.master, width=170,height=50,bg='white',highlightthickness=0)
	self.Text4_t = self.Text4.create_text(85,25,text='Atualizar Estoque',font=("Helvetica",15),justify='center')
	self.Text4.place(x=340,y=50)


	#Opcoes da list box
	choices = consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos`")
	

	#Gaveta 01
	self.can31 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto31 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo31 = self.can31.create_image(25,25, image=self.foto31)
	self.can31.image = self.foto31
	self.can31.place(x=110,y=165)
	
	self.tkvar1 = StringVar()
	self.tkvar1.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'"))
	self.listbox1 = OptionMenu(self.master, self.tkvar1, *choices, command=self.func1)
	self.listbox1.place(x=160,y=165)
	
	self.entry1 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd1, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd1.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='1'"))
	self.entry1.place(x=160,y=205)
	
	self.func1(consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'")[0])
	self.botao1 = Button(self.master, text = 'Atualizar', command = self.att1, width=6, height=1, font=("Helvetia",7))
	self.botao1.place(x=230,y=205)
	
	
	#Gaveta 02
	self.can32 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto32 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo32 = self.can32.create_image(25,25, image=self.foto32)
	self.can32.image = self.foto32
	self.can32.place(x=445,y=165)
	
	self.tkvar2 = StringVar()
	self.tkvar2.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'"))
	self.listbox2 = OptionMenu(self.master, self.tkvar2, *choices, command=self.func2)
	self.listbox2.place(x=495,y=165)
	
	self.entry2 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd2, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd2.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='2'"))
	self.entry2.place(x=495,y=205)
	
	self.func2(consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'")[0])
	self.botao2 = Button(self.master, text = 'Atualizar', command = self.att2, width=6, height=1, font=("Helvetia",7))
	self.botao2.place(x=565,y=205)
	
	
	#Gaveta 03
	self.can33 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto33 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo33 = self.can33.create_image(25,25, image=self.foto33)
	self.can33.image = self.foto33
	self.can33.place(x=110,y=275)
	
	self.tkvar3 = StringVar()
	self.tkvar3.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'"))
	self.listbox3 = OptionMenu(self.master, self.tkvar3, *choices, command=self.func3)
	self.listbox3.place(x=160,y=280)
	
	self.entry3 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd3, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd3.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='3'"))
	self.entry3.place(x=160,y=320)
	
	self.func3(consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'")[0])
	self.botao3 = Button(self.master, text = 'Atualizar', command = self.att3, width=6, height=1, font=("Helvetia",7))
	self.botao3.place(x=230,y=320)
	
	
	#Gaveta 04
	self.can34 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto34 = PhotoImage(file = '/home/pi/imagens/3.gif')
	self.photo34 = self.can34.create_image(25,25, image=self.foto34)
	self.can34.image = self.foto34
	self.can34.place(x=445,y=275)
	
	self.tkvar4 = StringVar()
	self.tkvar4.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'"))
	self.listbox4 = OptionMenu(self.master, self.tkvar4, *choices, command=self.func4)
	self.listbox4.place(x=495,y=280)
	
	self.entry4 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.qtd4, justify = 'center', width=5, font=("Helvetia",10))
	self.qtd4.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='4'"))
	self.entry4.place(x=495,y=320)
	
	self.func4(consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'")[0])
	self.botao4 = Button(self.master, text = 'Atualizar', command = self.att4, width=6, height=1, font=("Helvetia",7))
	self.botao4.place(x=565,y=320)


	# Relogio
	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()
	
	# Botao Voltar Menu
	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)
 
    def func1(self,value):
	self.opcao1 = (value)

    def func2(self,value):
	self.opcao2 = (value)

    def func3(self,value):
	self.opcao3 = (value)

    def func4(self,value):
	self.opcao4 = (value)
	
	
	
    def att1(self):
	
	if all(x.isdigit() for x in self.entry1.get()):
		
		self.gaveta2 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'")[0])
		self.gaveta3 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'")[0])
		self.gaveta4 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'")[0])
		
		
		if (self.opcao1 == self.gaveta2) or (self.opcao1 == self.gaveta3) or (self.opcao1 == self.gaveta4):
			
			self.verificarGavetas("01")
			self.tkvar1.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'"))
			self.qtd1.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='1'"))
			
		else:
			
			print(self.opcao1[0])
			print(self.opcao1[1])
			print(self.opcao1[2])
			print(self.opcao1[3])
			print(self.entry1.get())
			print("1")

			atualizar_gavetas("1",self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao1[3],self.entry1.get())
			self.atualizacaoOK("1",self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao1[3],self.entry1.get())
		
	else:
		self.verificarNumerosQtd("01")
		
	self.qtd1.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='1'"))

    def att2(self):
	
	if all(x.isdigit() for x in self.entry2.get()):
		
		self.gaveta1 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'")[0])
		self.gaveta3 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'")[0])
		self.gaveta4 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'")[0])
		
		
		if (self.opcao2 == self.gaveta1) or (self.opcao2 == self.gaveta3) or (self.opcao2 == self.gaveta4):
			
			self.verificarGavetas("02")
			self.tkvar2.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'"))
			self.qtd2.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='2'"))
		
		else:
			
			print(self.opcao2[0])
			print(self.opcao2[1])
			print(self.opcao2[2])
			print(self.opcao2[3])
			print(self.entry2.get())
			print("2")
			
			atualizar_gavetas("2",self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.entry2.get())
			self.atualizacaoOK("2",self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.entry2.get())
	
	else:
		self.verificarNumerosQtd("02")
		
	self.qtd2.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='2'"))

    def att3(self):
	
	if all(x.isdigit() for x in self.entry3.get()):
		
		self.gaveta1 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'")[0])
		self.gaveta2 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'")[0])
		self.gaveta4 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'")[0])
		
		
		if (self.opcao3 == self.gaveta1) or (self.opcao3 == self.gaveta2) or (self.opcao3 == self.gaveta4):
			
			self.verificarGavetas("03")
			self.tkvar3.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'"))
			self.qtd3.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='3'"))
		
		else:
		
			print(self.opcao3[0])
			print(self.opcao3[1])
			print(self.opcao3[2])
			print(self.opcao3[3])
			print(self.entry3.get())
			print("3")
			
			atualizar_gavetas("3",self.opcao3[0],self.opcao3[1],self.opcao3[2],self.opcao3[3],self.entry3.get())
			self.atualizacaoOK("3",self.opcao3[0],self.opcao3[1],self.opcao3[2],self.opcao3[3],self.entry3.get())
	
	else: 
		self.verificarNumerosQtd("03")
		
	self.qtd3.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='3'"))

    def att4(self):
	
	if all(x.isdigit() for x in self.entry4.get()):
		
		self.gaveta1 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='1'")[0])
		self.gaveta2 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='2'")[0])
		self.gaveta3 = (consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='3'")[0])
		
		
		if (self.opcao4 == self.gaveta1) or (self.opcao4 == self.gaveta2) or (self.opcao4 == self.gaveta3):
			
			self.verificarGavetas("04")
			self.tkvar4.set(consultar_medicamento("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta`='4'"))
			self.qtd4.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='4'"))
		
		else:
		
			print(self.opcao4[0])
			print(self.opcao4[1])
			print(self.opcao4[2])
			print(self.opcao4[3])
			print(self.entry4.get())
			print("4")
			
			atualizar_gavetas("4",self.opcao4[0],self.opcao4[1],self.opcao4[2],self.opcao4[3],self.entry4.get())
			self.atualizacaoOK("4",self.opcao4[0],self.opcao4[1],self.opcao4[2],self.opcao4[3],self.entry4.get())
	
	else:
		self.verificarNumerosQtd("04")
		
	self.qtd4.set(consultar_estoque("SELECT `Estoque` FROM `medicamentos` WHERE `Gaveta`='4'"))


    def atualizacaoOK(self,gaveta,composto,quantidade,unidademedida,via,newEstoque):
	self.titulo = """Gaveta %s""" % gaveta
	self.mensagem = """Gaveta %s Atualizada com sucesso!\n\nMedicamento:\n%s\n%s%s\nVia %s\n\nNova quantidade em estoque: %s""" % (gaveta,composto,quantidade,unidademedida,via,newEstoque)
	tkMessageBox.showinfo(self.titulo,self.mensagem,parent=self.master)

    def verificarNumerosQtd(self,gaveta):
	self.titulo = """Gaveta %s""" % gaveta
	tkMessageBox.showerror(self.titulo, "Letra Presente no campo de Quantidade!",parent=self.master)

    def verificarGavetas(self,gaveta):
	self.titulo = """Gaveta %s""" % gaveta
	tkMessageBox.showerror(self.titulo, "Esse medicamento ja esta cadastrado em outra gaveta!",parent=self.master)


#Classe da Tela de Cadastrar Pacientes
class CadastrarPacientes():
    
    def __init__(self,master):
        
	self.nome = StringVar()
	self.nome_e = StringVar() #empty string
	self.sobrenome = StringVar()
	self.sobrenome_e = StringVar() #empty string
	self.CPF = StringVar()
	self.CPF_e = StringVar() #empty string
	self.IDHospital = StringVar()
	self.IDHospital_e = StringVar() #empty string
	self.Plano = StringVar()
	self.Plano_e = StringVar() #empty string
	self.Data = StringVar()
	self.Data_e = StringVar() #empty string
	
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Cadastrar Pacientes')
	self.master.configure(bg='white')
        
        #Widgets da Segunda Tela

	self.can5 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto5 = PhotoImage(file = '/home/pi/imagens/5.gif')
	self.photo5 = self.can5.create_image(25,25, image=self.foto5)
	self.can5.image = self.foto5
	self.can5.place(x=250,y=50)
	
	self.Text5 = Canvas(self.master, width=200,height=70,bg='white',highlightthickness=0)
	self.Text5_t = self.Text5.create_text(100,35,text='Cadastrar Pacientes',font=("Helvetica",15),justify='center')
	self.Text5.place(x=300,y=50)








	self.canvasText1 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText1_t = self.canvasText1.create_text(100,15,text='Nome:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText1.place(x=50,y=150)
	
	self.entry1 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.nome_e, justify = 'center', width=35, font=("Helvetia",10))
	self.nome_e.set("")
	self.entry1.place(x=270,y=155)



	self.canvasText2 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText2_t = self.canvasText2.create_text(100,15,text='Sobrenome:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText2.place(x=50,y=190)
	
	self.entry2 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.sobrenome_e, justify = 'center', width=35, font=("Helvetia",10))
	self.sobrenome_e.set("")
	self.entry2.place(x=270,y=195)
	
	
	
	self.canvasText3 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText3_t = self.canvasText3.create_text(100,15,text='CPF:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText3.place(x=50,y=230)
	
	self.entry3 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.CPF_e, justify = 'center', width=35, font=("Helvetia",10))
	self.CPF_e.set("")
	self.entry3.place(x=270,y=235)
	
	
	
	self.canvasText4 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText4_t = self.canvasText4.create_text(100,15,text='ID_Hospital:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText4.place(x=50,y=270)
	
	self.entry4 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.IDHospital_e, justify = 'center', width=35, font=("Helvetia",10))
	self.IDHospital_e.set("")
	self.entry4.place(x=270,y=275)



	self.canvasText5 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText5_t = self.canvasText5.create_text(100,15,text='Plano:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText5.place(x=50,y=310)
	
	self.entry5 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.Plano_e, justify = 'center', width=35, font=("Helvetia",10))
	self.Plano_e.set("")
	self.entry5.place(x=270,y=315)
	
	
	
	self.canvasText6 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText6_t = self.canvasText6.create_text(100,15,text='Data de Internacao:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText6.place(x=50,y=350)
	
	self.entry6 = Entry(self.master,bg='#ECECEC',fg = 'black',textvariable = self.Data_e, justify = 'center', width=35, font=("Helvetia",10))
	self.Data_e.set("")
	self.entry6.place(x=270,y=355)
	
	self.canvasText7 = Canvas(self.master, width=100,height=15,bg='white',highlightthickness=0)
	self.canvasText7_t = self.canvasText7.create_text(50,7,text='dd-mm-aaaa',font=("Helvetica",8,'bold'),justify='center')
	self.canvasText7.place(x=360,y=380)
	
	
	self.botaotoday = Button(self.master, text='Hoje', command=self.preencherHoje, width=5, height=1,bg='white')
	self.botaotoday.place(x=560,y=352)



	self.botaocad = Button(self.master, text='Cadastrar', command=self.chamar_Cadastro, width=15, height=2,bg='white')
	self.botaocad.place(x=630,y=240)

	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes da paginabutton1

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)

    def preencherHoje(self):
	    self.Data_e.set(strftime('%d-%m-%Y'))

    def chamar_Cadastro(self):
	    
	self.nome = self.entry1.get()
	self.sobrenome = self.entry2.get()
	self.CPF = self.entry3.get()
	self.IDHospital = self.entry4.get()
	self.Plano = self.entry5.get()
	self.Data = self.entry6.get()
	
	if (self.nome != "") and (self.sobrenome != "") and (self.CPF != "") and (self.IDHospital != "") and (self.Plano != "") and (self.Data != ""):
		if len(self.CPF) == 11 and all(x.isdigit() for x in self.CPF):
			if all(x.isdigit() for x in self.IDHospital):
				if (self.Plano == "Y") or (self.Plano == "N") or (self.Plano == "y") or (self.Plano == "n"):
					if (self.Data[2] == "-") and (self.Data[5] == "-") and (len(self.Data) == 10) and (int(self.Data[0] + self.Data[1]) <= 31) and (int(self.Data[3] + self.Data[4]) <= 12):
						
						self.converteData = datetime.datetime.strptime(self.Data,'%d-%m-%Y').strftime('%Y-%m-%d')
						cadastrar_pacientes(self.nome,self.sobrenome,self.CPF,self.IDHospital,self.Plano,self.converteData)
						
						self.nome_e.set("")
						self.sobrenome_e.set("")
						self.CPF_e.set("")
						self.IDHospital_e.set("")
						self.Plano_e.set("")
						self.Data_e.set("")
						
						tkMessageBox.showinfo("Sucesso!","Paciente Cadastrado com Sucesso!",parent=self.master)
					
					else:
						tkMessageBox.showerror("Erro!", "Data em formato invalido!\n\nFormato padrao:\ndd-mm-yyyy",parent=self.master)
						self.Data_e.set("")
					
				else:
					tkMessageBox.showerror("Erro!", "Plano INVALIDO!\nResponda (Y/N)",parent=self.master)
					self.Plano_e.set("")
			else:
				tkMessageBox.showerror("Erro!", "ID Hospital INVALIDO!",parent=self.master)
				self.IDHospital_e.set("")	
		else:
			tkMessageBox.showerror("Erro!", "CPF INVALIDO!",parent=self.master)
			self.CPF_e.set("")
	else:
		tkMessageBox.showerror("Erro!", "Existem campos que nao foram preenchidos!",parent=self.master)


#Classe da Tela de Cadastrar Medicamentos
class CadastrarMedicamentos():
    
    def __init__(self,master):
        
	self.compost = StringVar()
	self.compost_e = StringVar ()
	self.quantidade = StringVar()
	self.quantidade_e = StringVar ()
	self.unidade = StringVar()
	self.unidade_e = StringVar ()
	self.via = StringVar()
	self.via_e = StringVar ()
	self.fabri = StringVar()
	self.fabri_e = StringVar ()
	
        #Inicializa a Segunda tela como Master
        self.master=master
        
        #Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
    	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
        
        #Define o titulo e background da Tela Principal        
        self.master.title('Supply Point - Cadastrar Medicamentos')
	self.master.configure(bg='white')
        
        #Widgets da Segunda Tela

	self.can6 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto6 = PhotoImage(file = '/home/pi/imagens/6.gif')
	self.photo6 = self.can6.create_image(25,25, image=self.foto6)
	self.can6.image = self.foto6
	self.can6.place(x=250,y=50)
	
	self.Text6 = Canvas(self.master, width=250,height=50,bg='white',highlightthickness=0)
	self.Text6_t = self.Text6.create_text(125,25,text='Cadastrar Medicamentos',font=("Helvetica",15),justify='center')
	self.Text6.place(x=300,y=50)




	self.canvasText1 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText1_t = self.canvasText1.create_text(100,15,text='Composto:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText1.place(x=50,y=140)
	
	self.entry1 = Entry(self.master,bg='#ECECEC',fg = 'black',textvariable = self.compost_e, justify = 'center', width=35, font=("Helvetia",10))
	self.compost_e.set("")
	self.entry1.place(x=270,y=145)


	self.canvasText2 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText2_t = self.canvasText2.create_text(100,15,text='Dosagem:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText2.place(x=50,y=180)
	
	self.entry2 = Entry(self.master,bg='#ECECEC',fg = 'black',textvariable = self.quantidade_e, justify = 'center', width=35, font=("Helvetia",10))
	self.quantidade_e.set("")
	self.entry2.place(x=270,y=185)
	
	
	self.canvasText3 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText3_t = self.canvasText3.create_text(100,15,text='Unidade de Medida:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText3.place(x=50,y=220)
	
	self.entry3 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.unidade_e, justify = 'center', width=35, font=("Helvetia",10))
	self.unidade_e.set("")
	self.entry3.place(x=270,y=225)
	
	
	self.canvasText4 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText4_t = self.canvasText4.create_text(100,15,text='Via de Administracao:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText4.place(x=50,y=260)
	
	self.entry4 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.via_e, justify = 'center', width=35, font=("Helvetia",10))
	self.via_e.set("")
	self.entry4.place(x=270,y=265)


	self.canvasText5 = Canvas(self.master, width=200,height=30,bg='white',highlightthickness=1)
	self.canvasText5_t = self.canvasText5.create_text(100,15,text='Fabricante:',font=("Helvetica",12,'bold'),justify='center')
	self.canvasText5.place(x=50,y=300)
	
	self.entry5 = Entry(self.master,bg='#ECECEC',fg = 'black', textvariable = self.fabri_e, justify = 'center', width=35, font=("Helvetia",10))
	self.fabri_e.set("")
	self.entry5.place(x=270,y=305)
	
	
	
	
	
	self.botaocad = Button(self.master, text='Cadastrar', command=self.chamar_Cadastro, width=15, height=2,bg='white')
	self.botaocad.place(x=630,y=240)

	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()

	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes da paginabutton1

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)

    def chamar_Cadastro(self):
	    
	self.compost = self.entry1.get()
	self.quantidade = self.entry2.get()
	self.unidade = self.entry3.get()
	self.via = self.entry4.get()
	self.fabri = self.entry5.get()
	
	if (self.compost != "") and (self.quantidade != "") and (self.unidade != "") and (self.via != "") and (self.fabri != ""):
	
		cadastrar_medicamentos(self.compost,self.quantidade,self.unidade,self.via,self.fabri)
		
		self.compost_e.set("")
		self.quantidade_e.set("")
		self.unidade_e.set("")
		self.via_e.set("")
		self.fabri_e.set("")
		
		tkMessageBox.showinfo("Sucesso!","Medicamento cadastrado com Sucesso!",parent=self.master)
	else:
		tkMessageBox.showerror("Erro!", "Existem campos que nao foram preenchidos!",parent=self.master)


#Classe da Tela de Prescricao de medicamentos
class PrescreverMedicamentos():
	
    def __init__(self,master):
	    
	#Inicializa a Segunda tela como Master
	self.master=master
		
	#Define os tamanhos e a posicao de inicio da Segunda Tela
	width=800
	height=480
	screen_width = self.master.winfo_screenwidth()
	screen_height = self.master.winfo_screenheight()
	xCentro = (screen_width/2) - (width/2)
	yCentro = (screen_height/2) - (height/2)
	self.master.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
	
	#Define o titulo e background da Tela Principal        
	self.master.title('Supply Point - Prescrever Medicamentos')
	self.master.configure(bg='white')
	
	#Opcoes da list box
	choices1 = consultar_opc("SELECT `Composto`,`Quantidade`,`Unidade_de_Medida`,`Via` FROM `medicamentos` WHERE `Gaveta` <> '0'")
	choices2 = consultar_opc("SELECT `CPF`,`Nome`,`Sobrenome` FROM `pacientes` ORDER BY `Nome`")
	choices3 = {'06/06 hrs','04/04 hrs','08/08 hrs','12/12 hrs','24/24 hrs'}
	
	#Widgets da Tela Prescrever Medicamentos

	self.canvasText1 = Canvas(self.master, width=100,height=20,bg='white',highlightthickness=1)
	self.canvasText1_t = self.canvasText1.create_text(50,10,text='Paciente:',font=("Helvetica",10,'bold'),justify='center')
	self.canvasText1.place(x=170,y=140)

	self.can31 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto31 = PhotoImage(file = '/home/pi/imagens/5.gif')
	self.photo31 = self.can31.create_image(25,25, image=self.foto31)
	self.can31.image = self.foto31
	self.can31.place(x=110,y=145)
	
	self.tkvar1 = StringVar()
	self.tkvar1.set("Selecione o Paciente:")
	self.listbox1 = OptionMenu(self.master, self.tkvar1, *choices2, command=self.func1)
	self.listbox1.place(x=170,y=170)
	
	self.canvasText2 = Canvas(self.master, width=100,height=20,bg='white',highlightthickness=1)
	self.canvasText2_t = self.canvasText2.create_text(50,10,text='Medicamento:',font=("Helvetica",10,'bold'),justify='center')
	self.canvasText2.place(x=170,y=225)

	self.can32 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto32 = PhotoImage(file = '/home/pi/imagens/6.gif')
	self.photo32 = self.can32.create_image(25,25, image=self.foto32)
	self.can32.image = self.foto32
	self.can32.place(x=110,y=225)
	
	self.tkvar2 = StringVar()
	self.tkvar2.set("Selecione o Medicamento:")
	self.listbox2 = OptionMenu(self.master, self.tkvar2, *choices1, command=self.func2)
	self.listbox2.place(x=170,y=255)
	
	self.canvasText3 = Canvas(self.master, width=100,height=20,bg='white',highlightthickness=1)
	self.canvasText3_t = self.canvasText3.create_text(50,10,text='Periodicidade:',font=("Helvetica",10,'bold'),justify='center')
	self.canvasText3.place(x=170,y=310)

	self.can33 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto33 = PhotoImage(file = '/home/pi/imagens/8.gif')
	self.photo33 = self.can33.create_image(25,25, image=self.foto33)
	self.can33.image = self.foto33
	self.can33.place(x=110,y=310)

	self.tkvar3 = StringVar()
	self.tkvar3.set("Selecione a Periodicidade:")
	self.listbox3 = OptionMenu(self.master, self.tkvar3, *choices3, command=self.func3)
	self.listbox3.place(x=170,y=340)
	
	self.can6 = Canvas(self.master, width=50,height=50,highlightthickness=0)
	self.foto6 = PhotoImage(file = '/home/pi/imagens/7.gif')
	self.photo6 = self.can6.create_image(25,25, image=self.foto6)
	self.can6.image = self.foto6
	self.can6.place(x=250,y=50)
	
	self.Text6 = Canvas(self.master, width=250,height=50,bg='white',highlightthickness=0)
	self.Text6_t = self.Text6.create_text(125,25,text='Prescrever Medicamentos',font=("Helvetica",15),justify='center')
	self.Text6.place(x=300,y=50)

	self.rel = Label(self.master,bg='white', font=("Helvetia",12))
	self.rel.place(x=630,y=30)
	self.tac()
	
	self.botaocad = Button(self.master, text='Prescrever', command=self.Prescrever, width=15, height=2,bg='white')
	self.botaocad.place(x=630,y=240)
	
	self.botao7 = Button(self.master, text='Voltar ao Menu', command=self.myQuit, width=15, height=2,bg='white')
	self.botao7.place(x=630,y=420)

    #funcoes da paginabutton1

    def myQuit(self):
        self.master.destroy()

    def tic(self):
	self.rel['text'] = strftime('%d-%m-%Y\n%H:%M:%S')

    def tac(self):
	self.tic()
	self.rel.after(1000,self.tac)

    def func1(self,value):
	self.opcao1 = (value)

    def func2(self,value):
	self.opcao2 = (value)

    def func3(self,value):
	self.opcao3 = (value)

    def Prescrever(self):
	
	try:	
		if (self.opcao3 == '04/04 hrs'):
			self.proximaDose = datetime.datetime.now()
			cadastrar_prescricao(self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3,strftime("%Y-%m-%d %H:%M"),self.proximaDose.strftime("%Y-%m-%d %H:%M"))
			     
		elif (self.opcao3 == '06/06 hrs'):
			self.proximaDose = datetime.datetime.now()
			cadastrar_prescricao(self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3,strftime("%Y-%m-%d %H:%M"),self.proximaDose.strftime("%Y-%m-%d %H:%M"))
		    
		elif (self.opcao3 == '08/08 hrs'):
			self.proximaDose = datetime.datetime.now()
			cadastrar_prescricao(self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3,strftime("%Y-%m-%d %H:%M"),self.proximaDose.strftime("%Y-%m-%d %H:%M"))
			     
		elif (self.opcao3 == '12/12 hrs'):
			self.proximaDose = datetime.datetime.now()
			cadastrar_prescricao(self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3,strftime("%Y-%m-%d %H:%M"),self.proximaDose.strftime("%Y-%m-%d %H:%M"))
			     
		elif (self.opcao3 == '24/24 hrs'):
			self.proximaDose = datetime.datetime.now()
			cadastrar_prescricao(self.opcao1[0],self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3,strftime("%Y-%m-%d %H:%M"),self.proximaDose.strftime("%Y-%m-%d %H:%M"))
		
		self.PrescricaoOk(self.opcao1[1],self.opcao1[2],self.opcao2[0],self.opcao2[1],self.opcao2[2],self.opcao2[3],self.opcao3)
		
	except AttributeError:
		tkMessageBox.showerror("Erro","Selecione todos os campos!",parent=self.master)
	
    def PrescricaoOk(self,nome2,sobrenome2,composto2,dosagem2,unidade2,via2,periodicidade2):
	    
	    self.mensagem = StringVar()
	    
	    self.mensagem = """ Prescricao realizada com sucesso!\n\nPaciente: %s %s\nMedicamento: %s %s%s - Via %s\nPeriodicidade: %s""" % (nome2,sobrenome2,composto2,dosagem2,unidade2,via2,periodicidade2) 
	    
	    tkMessageBox.showinfo("Prescricao Realizada",self.mensagem,parent=self.master)


#Funcao main
def main():
    root = Tk()
    myGUIWelcome = Welcome(root)
    root.mainloop()

if __name__ == '__main__':
	main()
