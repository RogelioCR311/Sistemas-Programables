```python
from machine import Pin, I2C
from time import sleep
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
from mfrc522 import MFRC522
import utime

#--------------------------Configuracion Teclado Matricial---------------------------------------------------

TECLA_ARRIBA  = const(0)
TECLA_ABAJO = const(1)

teclas = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

# Pines del GPIO  
filas = [6,7,8,9]
columnas = [10,11,12,13]

# define los pines de filas como salidas
fila_pines = [Pin(nombre_pin, mode=Pin.OUT) for nombre_pin in filas]

# define los pines de columnas como entradas
columna_pines = [Pin(nombre_pin, mode=Pin.IN, pull=Pin.PULL_DOWN) for nombre_pin in columnas]
#----------------------------------------------------------------------------------------------------------

#------------Configuracion Oled Display-----------------------------
WIDTH =128
HEIGHT= 64
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
#-------------------------------------------------------------------------

#-------------------- Configuracion Lector RFID ----------------------------
#Indicamos en que pines esta conectado el RFID RC522       
lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

#Agregamos las variables con las ID de nuestra tarjeta o tag
listaAccesos = [538321312]
#---------------------------------------------------------------------------------

def init():
    for fila in range(0,4):
        for columna in range(0,4):
            fila_pines[fila].low()


def scan(fila, columna):
    """ escanea todo el teclado """

    # define la columna actual en alto -high-
    fila_pines[fila].high()
    tecla = None

    # verifica por teclas si hay teclas presionadas
    if columna_pines[columna].value() == TECLA_ABAJO:
        tecla = TECLA_ABAJO
    if columna_pines[columna].value() == TECLA_ARRIBA:
        tecla = TECLA_ARRIBA
    fila_pines[fila].low()

    # devuelve el estado de la tecla
    return tecla

def mostrarTexto(texto1, texto2, texto3, texto4, texto5):
    #oled.text(texto, ancho, alto)
    oled.fill(0)
    oled.text(texto1, 0, 0)
    oled.text(texto2, 0, 20)
    oled.text(texto3, 0, 30)
    oled.text(texto4, 0, 40)
    oled.text(texto5, 0, 50)
    oled.show()

def leer_tag(identificador):
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            print("UID: "+str(identificador))
    
    return identificador

print("Listo en espera")

# define todas las columnas bajo -low-
init()

def iniciarPrograma():
    opc = "F"
    tag = 0
    acceso = 0
    password = "1234"
    passw = ""
    contra = ""
    while True:
        if opc == "F":
            mostrarTexto("Lector Activo", "", contra, "", "#: Opciones")
            for fila in range(4):
                for columna in range(4):
                    tecla = scan(fila, columna)
                    if tecla == TECLA_ABAJO:
                        entrada = teclas[fila][columna]
                        if entrada == "#":
                            opc = "#"
                        print("Tecla Presionada", entrada)
                        sleep(0.5)
                        ultima_tecla_presionada = teclas[fila][columna]
                        passw = passw + ultima_tecla_presionada
                        contra = contra + "*"
            tag = leer_tag(0)
            if tag != 0:
                if tag in listaAccesos:
                    mostrarTexto("", "Acceso", "Concedido", "", "")
                    utime.sleep(5)
                    iniciarPrograma()
                else:
                    mostrarTexto("", "Acceso", "Denegado", "", "")
                    utime.sleep(5)
                    iniciarPrograma()
            if len(passw) == 4:
                    if passw == password:
                        mostrarTexto("", "Acceso", "Concedido", "", "")
                        utime.sleep(5)
                        iniciarPrograma()
                    else:
                        mostrarTexto("", "Acceso", "Denegado", "", "")
                        utime.sleep(5)
                        iniciarPrograma()
        
        if opc == "#":
            passw = ""
            contra = ""
            while True:
                mostrarTexto("Ingresa", "contrasena", "", contra, "")
                for fila in range(4):
                    for columna in range(4):
                        tecla = scan(fila, columna)
                        if tecla == TECLA_ABAJO:
                            entrada = teclas[fila][columna]
                            print("Tecla Presionada", entrada)
                            sleep(0.5)
                            ultima_tecla_presionada = teclas[fila][columna]
                            passw = passw + ultima_tecla_presionada
                            contra = contra + "*"
            
                    if len(passw) == 4:
                        if passw == password:
                            while True:
                                mostrarTexto("Opciones:", "A: Agregar ID", "B: Eliminar ID", "C: Cancelar", "")
                                for fila in range(4):
                                    for columna in range(4):
                                        tecla = scan(fila, columna)
                                        if tecla == TECLA_ABAJO:
                                            entrada = teclas[fila][columna]
                                            opc = entrada
                                            print("Tecla Presionada", entrada)
                                            sleep(0.5)
                                            ultima_tecla_presionada = teclas[fila][columna]
                                if opc == "A":
                                    while True:
                                        mostrarTexto("", "Acerca el", "identificador a", "registrar", "")
                                        tag = leer_tag(0)
                                        if tag != 0:
                                            if tag in listaAccesos:
                                                mostrarTexto("", "Identificador ya", "se encuentra", "registrado", "")
                                                utime.sleep(5)
                                                iniciarPrograma()
                                            else:
                                                listaAccesos.append(tag)
                                                mostrarTexto("", "Identificador", "registrado", "con exito", "")
                                                utime.sleep(5)
                                                iniciarPrograma()
                                if opc == "B":
                                    while True:
                                        mostrarTexto("", "Acerca el", "identificador a", "remover", "")
                                        tag = leer_tag(0)
                                        if tag != 0:
                                            if tag in listaAccesos:
                                                listaAccesos.remove(tag)
                                                mostrarTexto("", "Identificador", "removido", "con exito", "")
                                                utime.sleep(5)
                                                iniciarPrograma()
                                            else:
                                                mostrarTexto("", "Identificador", "no esta", "registrado", "")
                                                utime.sleep(5)
                                                iniciarPrograma()
                                if opc == "C":
                                    iniciarPrograma()
                                    
                        else:
                            mostrarTexto("", "Acceso", "Denegado", "", "")
                            utime.sleep(5)
                            iniciarPrograma()
            

iniciarPrograma()

```
