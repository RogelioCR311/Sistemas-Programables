#Importamos las librerias
from machine import Pin
from mfrc522 import MFRC522
import time

#Indicamos en que pines esta conectado el RFID RC522       
lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

#Indicamos en que pines esta el led RGB
rojo = Pin(13, Pin.OUT)
verde = Pin(12, Pin.OUT)

#Agregamos las variables con las ID de nuestra tarjeta o tag
TARJETA = 2766409360
LLAVERO = 0

#Indicamos que nuestro programa ya esta funcionando
print("Lector activo...\n")

#Creamos un ciclo para leer nuestra tarjeta
while True:
    #Iniciamos nuestro lector RFID RC522
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            
            #Concedemos acceso si el identificador coindice con la tarjeta a la que dimos acceso
            if identificador == TARJETA:
                print("UID: "+ str(identificador)+" Acceso concedido")
                rojo.value(0)
                verde.value(1)
                time.sleep(2)
                verde.value(0)
            
            #Negamos acceso si el identificador no coindice con la tarjeta a la que dimos acceso
            else:
                print("UID: "+ str(identificador)+" desconocido: Acceso denegado")
                rojo.value(1)
                verde.value(0)
                time.sleep(2)
                rojo.value(0)