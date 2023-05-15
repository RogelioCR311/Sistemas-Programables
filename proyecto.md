```python
import tkinter as tk
from tkinter import *
from tkinter import Tk, Button, filedialog
from PIL import Image
import os
import cv2
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
import numpy as np
from PIL import Image, ImageTk

#------------------------ Declaramos variables para crear carpeta donde se almacenaran las imagenes ---------------------

direccion = os.path.dirname(__file__) #c:\Users\rogel\Desktop\Login
carpeta = os.path.join(direccion, "Usuarios") #c:\Users\rogel\Desktop\Login\Usuarios

#------------------------ Creamos una carpeta llamada Usuarios en caso de que no exista
if not os.path.exists(carpeta):
    print('Carpeta creada: ', carpeta)
    os.makedirs(carpeta)
#------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------

carpeta_registros = os.path.join(direccion, "Usuarios")

def registrar_usuario():
    usuario_info = usuario.get() #Obtenemos la informacion almacenada en usuario
    contra_info = contra.get() #Obtenemos la informacion almacenada en contra

    carpeta_usuario = os.path.join(direccion, "Usuarios", usuario_info)

    if not os.path.exists(carpeta_usuario):
        print('Carpeta creada: ', carpeta_usuario)
        os.makedirs(carpeta_usuario)

    archivo = open(carpeta_usuario + '/' + usuario_info, "w") #Abriremos la informacion en modo escritura
    archivo.write(usuario_info + "\n")   #escribimos la info
    archivo.write(contra_info)
    archivo.close()

    #Limpiaremos los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    #Ahora le diremos al usuario que su registro ha sido exitoso
    Label(pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()
    

#--------------------------- Funcion para almacenar el registro facial --------------------------------------
    
def registro_facial():
    #Vamos a capturar el rostro
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Registro Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_img = usuario.get()

    carpeta_usuario = carpeta_registros + '/' + usuario.get()

    if not os.path.exists(carpeta_usuario):
        print('Carpeta creada: ', carpeta_usuario)
        os.makedirs(carpeta_usuario)

    cv2.imwrite(carpeta_usuario + '/' + usuario_img+".jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   #Limpiamos los text variables
    Label(pantalla5, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).pack()

    #----------------- Detectamos el rostro y exportamos los pixeles --------------------------
    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)   
#---------------------------- Funcion para ingresar una idenficacion del usuario ------------------------------------    
def ingresar_identificacion():
    ruta_imagen = filedialog.askopenfilename()
    
    # Obtener la ruta de destino para guardar la imagen
    ruta_destino = 'C:/Users/rogel/Desktop/Login/Usuarios' + '/' + usuario.get()

    # Cargar la imagen
    imagen = Image.open(ruta_imagen)

    # Guardar la imagen en la carpeta de destino
    nombre_archivo = usuario.get() + "ID.jpg"
    ruta_guardado = os.path.join(ruta_destino + '/' + nombre_archivo )
    imagen.save(ruta_guardado)
    print("Imagen guardada en:", ruta_guardado)
    usuario_entrada.delete(0, END)   #Limpiamos los text variables
    Label(pantalla6, text = "Registro de Identificacion Exitoso", fg = "green", font = ("Calibri",11)).pack()
#--------------------- Pantalla para elegir si quieren registro tradicional o facial ----------------------------------
def elecciones_registro():
    global pantalla4
    pantalla4 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla4.title("Registro")
    pantalla4.geometry("980x400")  #Asignamos el tamaño de la ventana

    Label(pantalla4, text = "Registro facial: debe de asignar un usuario:").pack()
    Label(pantalla4, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla4, text = "Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla4, text = "").pack()  #Dejamos un poco de espacio

    Label(pantalla4, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla4, text = "Registro Tradicional", width = 15, height = 1, command = registro_tradicional).pack()  #Creamos el boton

    #------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla4, text = "").pack()
    Button(pantalla4, text = "Registro Facial", width = 15, height = 1, command = registro_rostro).pack()

    Label(pantalla4, text = "").pack()
    Button(pantalla4, text = "Registro Identificacion", width = 17, height = 1, command = registro_id).pack()

#------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro_tradicional():
    pantalla4.destroy()
    global usuario
    global contra  #Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("980x400")  #Asignamos el tamaño de la ventana
    
    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text = "Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla1, text = "Usuario * ").pack()  #Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack()  #Mostramos en la pantalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra) #Creamos un text variable para que el usuario ingrese la contra
    contra_entrada.pack()
    Label(pantalla1, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla1, text = "Registrar", width = 15, height = 1, command = registrar_usuario).pack()  #Creamos el boton

#------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro_rostro():
    pantalla4.destroy()
    global usuario
    global usuario_entrada
    global pantalla5
    pantalla5 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla5.title("Registro")
    pantalla5.geometry("980x400")  #Asignamos el tamaño de la ventana
    
    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    
    Label(pantalla5, text = "Registro facial: debe de asignar un usuario:").pack()
    Label(pantalla5, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla5, text = "Usuario * ").pack()  #Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla5, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla5, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla5, text = "Registrar", width = 15, height = 1, command = registro_facial).pack()  #Creamos el boton

def registro_id():
    pantalla4.destroy()
    global usuario
    global usuario_entrada
    global pantalla6
    pantalla6 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla6.title("Registro")
    pantalla6.geometry("980x400")  #Asignamos el tamaño de la ventana
    
    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    
    Label(pantalla6, text = "Registro identificacion: debe de subir un documento:").pack()
    Label(pantalla6, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla6, text = "Usuario * ").pack()  #Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla6, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla6, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla6, text = "Subir documento", width = 17, height = 1, command = ingresar_identificacion).pack()  #Creamos el boton
#------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------
    
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()
    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    path = carpeta_registros + '/' + log_usuario
    lista_archivos = os.listdir(path)   #Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
        archivo2 = open(carpeta_registros + '/' + log_usuario + '/' + log_usuario, "r")  #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
    
#--------------------------Funcion para el Login Facial --------------------------------------------------------
def login_facial():
#------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Login Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_login = verificacion_usuario.get()    #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)   #Limpiamos los text variables
    contra_entrada2.delete(0, END)

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    path = carpeta_registros + '/' + usuario_login
    im_archivos = os.listdir(path)   #Vamos a importar la lista de archivos con la libreria os
    if usuario_login+".jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.95:
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
            mostrarID()
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
            

#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("980x400")  #Asignamos el tamaño de la ventana
    Label(pantalla2, text = "Login facial: debe de asignar un usuario:").pack()
    Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla2, text = "").pack()  #Dejamos un poco de espacio
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    #---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text = "Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text = "Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text = "").pack()
    Button(pantalla2, text = "Inicio de Sesion Tradicional", width = 20, height = 1, command = verificacion_login).pack()

    #------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "").pack()
    Button(pantalla2, text = "Inicio de Sesion Facial", width = 20, height = 1, command = login_facial).pack()

#--------------------- Funcion con la que mostraremos el ID del usuario cuando iniciemos sesion
def mostrarID():
    usuario = verificacion_usuario.get()
    carpeta_principal = 'C:/Users/rogel/Desktop/Login/Usuarios' + '/' + usuario

    imagen = Image.open(carpeta_principal + usuario + '/' + 'ID.jpg')

    imagen_tk = ImageTk.PhotoImage(imagen)
    etiqueta = tk.Label(pantalla, image=imagen_tk)
    etiqueta.pack()

#------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    pantalla3.destroy()
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = tk.Tk()
    pantalla.state('zoomed') #Pantalla completa sin quitar barra de herramientas
    pantalla.title("Login Inteligente")       #Asignamos el titulo de la pantalla
    Label(text = "Login Inteligente", bg = "gray", width = "300", height = "2", font = ("Verdana", 13)).pack() #Asignamos caracteristicas de la ventana
    
#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "").pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", height = "2", width = "30", command = login).pack()
    Label(text = "").pack() #Creamos el espacio entre el primer boton y el segundo boton
    Button(text = "Registro", height = "2", width = "30", command = elecciones_registro).pack()

    imagenID = 'C:/Users/rogel/Desktop/Login/Usuarios/rcarrillo/rcarrilloID.jpg'

    imagen = tk.PhotoImage(file="IA.png")
    label = tk.Label(image = imagen)
    label.pack()

    pantalla.mainloop()

#------------------------- Funcion de nuestra pantalla de presentacion ------------------------------------------------
def pantalla_presentacion():
    global pantalla3
    pantalla3 = tk.Tk()
    pantalla3.title("Presentacion")       #Asignamos el titulo de la pantalla
    pantalla3.state('zoomed') #Pantalla completa sin quitar barra de herramientas
    pantalla3.configure(bg="black")
    presentacion = "Bienvenido a Login Inteligente por Carrillo Rogelio, Rodriguez Arturo y Vazquez Ernesto."
    presentacion2 = """Este programa tiene como funcion crear la base de un login de usuario teniendo 
    como principal caracteristica el uso del reconocimiento facial con inteligencia 
    artificial para añadir un extra seguridad al momento de iniciar sesion."""
    imagen = tk.PhotoImage(file="IA.png")
    label = tk.Label(image = imagen, bg="black")
    label.pack()
    Label(text = presentacion, bg = "black", width = "300", height = "2", font = ("Verdana", 24), fg="white").pack() #Asignamos caracteristicas de la ventana
    Label(text = presentacion2, bg = "black", width = "300", height = "7", font = ("Verdana", 24), fg="white").pack() #Asignamos caracteristicas de la ventana
    borde_boton = tk.Frame(pantalla3, highlightbackground="white", highlightthickness="2", bd=0)
    btn = tk.Button(borde_boton, text = "Iniciar programa", height = "2", width = "30", bg="#04C4D9", font=("Verdana", 16), fg="white", command=pantalla_principal)
    btn.pack()
    borde_boton.pack()

    pantalla3.mainloop()

pantalla_presentacion()
```
