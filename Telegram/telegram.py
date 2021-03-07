# Librería Telethon para manejo de la cuenta de Telegram

from telethon.sync import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest

from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest

# Librería Colorama
from colorama import Fore, Back, Style

# Librerías del sistema
import os
import time
import random
from random import randint
from time import sleep

# Listado de mensajes 
from . import mensajes

class TelegramBot():
    """
    BOT de Telegram que hace uso de cuentas reales para SPAMEAR y secuestrar USUARIOS. 
    """

    def __init__(self, usuario, api_id, api_hash, phone):
        
        self.cliente = TelegramClient(usuario, api_id, api_hash)

        # Conectamos el Cliente
        self.cliente.connect()
        
        # Si el cliente no esta autorizado envíamos un mensaje de confirmación a su tlf. 
        if not self.cliente.is_user_authorized():
            self.cliente.send_code_request(phone)
            self.cliente.sign_in(phone, input('Introduce el código: '))

    def scraping_grupos(self): 

        chats = []
        last_date = None
        chunk_size = 250
        self.grupos = []

        result = self.cliente(
            GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            )  
        )

        chats.extend(result.chats)

        # Recorremos el chat y almacenamos los usuarios
        for chat in chats:
            try:
                if chat.megagroup == True:
                    self.grupos.append(chat)
            except:
                continue

        print(Fore.RED + "Selecciona el Grupo para extraer los usuarios:")

        # Recorremos e imprimimos los grupos
        contador = 0
        for listado_grupos in self.grupos:
            print(Fore.GREEN + str(contador) + Style.RESET_ALL +  " - " + listado_grupos.title)
            contador+=1 

        # Selección por parte del usuario del grupo
        grupos_numero = input("Introduce el número del grupo: ")
        self.grupo_seleccionado = self.grupos[int(grupos_numero)]

        # Guardamos el ID y el HASH del Grupo por si el usuario lo necesita. 
        self.grupo_id = self.grupo_seleccionado.id
        self.grupo_hash = self.grupo_seleccionado.access_hash

        # Extraeemos miembros del grupo.
        print(Fore.RED + 'Extrayendo usuarios...' + Fore.GREEN)
        self.todos_miembros = []
        self.todos_miembros = self.cliente.get_participants(self.grupo_seleccionado, aggressive=True)


    def spamear_usuarios(self): 


        # Recorremos los miembrso del grupo y les envíamos un mensaje.
        for datos_usuario in self.todos_miembros:

            # Seleccionamos un mensaje de manera aleatoria. 
            mensaje = random.choice(mensajes.mensajes)

            # Si el usuario tiene Nombre lo sustituimos, si no, nos referimos con su username.
            if datos_usuario.first_name: 
                mensaje = mensaje.replace("{{nombre}}", datos_usuario.first_name)
            else: 
                mensaje = mensaje.replace("{{nombre}}", datos_usuario.username)
            # Añadimos el nombre del grupo
            mensaje = mensaje.replace("{{grupo}}", self.grupo_seleccionado.title)

            try: 
                print (Fore.RED + "Enviando mensaje a : ", datos_usuario.username + Style.RESET_ALL)
                receptor = InputPeerUser(datos_usuario.id, datos_usuario.access_hash)

                self.cliente.send_message(receptor, mensaje)
                sleep(randint(10,100))

            except Exception as e: 
                print (Fore.YELLOW + "No se ha podido enviar un mensaje a %s. El error es: %s" % (datos_usuario.id, e))
    
    def secuestrar_usuarios(self): 

        # El usuario selecciona el grupo dónde enviar los usuarios
        grupos_numero = input("Introduce el número del grupo al que quieres importar los usuarios: ")
        grupo_seleccionado_secuestro = self.grupos[int(grupos_numero)]
        grupo_seleccionado_entidad = InputPeerChannel(grupo_seleccionado_secuestro.id,grupo_seleccionado_secuestro.access_hash)

        for datos_usuario in self.todos_miembros:
            
            usuario_a_anadir = InputPeerUser(int(datos_usuario.id), int(datos_usuario.access_hash))
            
            # Se intenta invitar al usuario al grupo. Si no se consigue se hace una pausa grande. 
            try: 
                self.cliente(InviteToChannelRequest(grupo_seleccionado_entidad,[usuario_a_anadir]))
                print (Fore.GREEN + "Se ha añadido a %s al grupo." % (datos_usuario.id) + Style.RESET_ALL)
                print (Fore.BLUE + "    * Durmiendo entre %s y %s segundos." % (180, 300))
                sleep(randint(180,300))
            
            except Exception as e: 
                print (Fore.YELLOW + "No se ha podido añadir a %s." % (datos_usuario.id))
                print (e)
                sleep(randint(10,20))

       

    def guardar_datos(self): 
        
        # Abrimos el archivo en el directorio datos. Aquí guardaremos toda la Info.  
        f = open("%s/datos/%s.csv" % (os.getcwd(), self.grupo_seleccionado.title.replace(" ", "-")), "w+", encoding="utf-8")
        
        # Guardamos los nombres de las Columnas del CSV 
        f.write("Título del Grupo, ID del Grupo, ID del Usuario, HASH del Usuario, Nickname, Nombre, Apellido\n")
        
        # Recorremos los datos
        for datos_usuario in self.todos_miembros:

            string_datos = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(

                self.grupo_seleccionado.title,
                self.grupo_seleccionado.id,
                self.grupo_seleccionado.access_hash,

                datos_usuario.id, 
                datos_usuario.access_hash, 
                
                datos_usuario.username, 
                datos_usuario.first_name,
                datos_usuario.last_name
            )
            
            f.write(string_datos + "\n")


        f.close()

        print ("Usuarios extraídos con éxito")
