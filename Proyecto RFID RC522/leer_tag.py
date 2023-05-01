#Importamos las librerias
from mfrc522 import MFRC522
import time

#Indicamos en que pines esta conectado el RFID RC522
lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

#Indicamos que nuestro programa ya esta funcionando

print("Lector activo...\n")

#Creamos un ciclo para leer nuestra tarjeta
while True:
    #Iniciamos nuestro lector RFID RC522
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        #Pedimos al programa que imprima en consola el ID detectado
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            print("UID: "+str(identificador))
    time.sleep(1) 