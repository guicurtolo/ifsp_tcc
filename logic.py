import MySQLdb
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO 

indexDB = 0

Broker = "192.168.0.177"

sub_topicUP = "botaoup/pressionado"    # receive messages on this topic
sub_topicDOWN = "botaodown/pressionado"    # receive messages on this topic

pub_topic = "chamados/novochamado"       # send messages to this topic


############### sensehat inputs ##################

def consulta_banco():
    
	resposta = []
	
	db = MySQLdb.connect(host="localhost",user="guicurtolo",passwd="225561gui", db="mydb")
	cur = db.cursor()
	cur.execute("SELECT `Nome`,`Sobrenome`,`Composto`, `Dosagem`, `Unidade`, `Via`, `Proxima_Dose` from mydb.`prescricoes` WHERE `Proxima_Dose` <= now()")
	for row in cur.fetchall():
		Nome = str(row[0])
		Sobrenome = str(row[1])
		Composto = str(row[2])
		Dosagem = str(row[3])
		Unidade = str(row[4])
		Via = str(row[5])
		Prox_Dose = str(row[6])
		resposta.append('{0} {1}\n{2}\n{3} {4} {5}\n{6}'.format(Nome,Sobrenome,Composto,Dosagem,Unidade,Via,Prox_Dose))
    	
	return resposta

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topicUP)
    client.subscribe(sub_topicDOWN)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    
    global indexDB
    message = str(msg.payload)
    
    dadosDB_now = consulta_banco()
    
    if message == "OPEN01":
		GPIO.output(5,0)
		GPIO.output(6,1)
		if indexDB < (len(dadosDB_now)-1): 
			indexDB = indexDB + 1
		else:
			indexDB = 0
	
    if message == "OPEN02":
		GPIO.output(12,0)
		GPIO.output(13,1)
		if indexDB < (len(dadosDB_now)-1): 
			indexDB = indexDB + 1
		else:
			indexDB = 0

    if message == "OPEN03":
		GPIO.output(16,0)
		GPIO.output(19,1)
		if indexDB < (len(dadosDB_now)-1): 
			indexDB = indexDB + 1
		else:
			indexDB = 0

    if message == "OPEN04":
		GPIO.output(26,0)
		GPIO.output(20,1)
		if indexDB < (len(dadosDB_now)-1): 
			indexDB = indexDB + 1
		else:
			indexDB = 0

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

GPIO.setmode(GPIO.BCM)            
GPIO.setup(5, GPIO.OUT, initial=0) #GAVETA 01 - A
GPIO.setup(6, GPIO.OUT, initial=1) #GAVETA 01 - B
GPIO.setup(12, GPIO.OUT, initial=0) #GAVETA 02 - A
GPIO.setup(13, GPIO.OUT, initial=1) #GAVETA 02 - B
GPIO.setup(16, GPIO.OUT, initial=0) #GAVETA 03 - A
GPIO.setup(19, GPIO.OUT, initial=1) #GAVETA 03 - B
GPIO.setup(26, GPIO.OUT, initial=0) #GAVETA 04 - A
GPIO.setup(20, GPIO.OUT, initial=1) #GAVETA 04 - B

while True:
    
    dadosDB = consulta_banco()
    
    if len(dadosDB) >= 1:
	client.publish(pub_topic,dadosDB[indexDB])
    else:
	client.publish(pub_topic,"Nao ha alarmes ativos!")
   
    time.sleep(1)

