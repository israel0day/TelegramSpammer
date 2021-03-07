# TelegramSpammer

Un simple script para hacer SPAM por Telegram. Podrás enviar mensajes SPAM o secuestrar los usuarios de un grupo.
![](https://israelperez.ninja/wp-content/uploads/2021/03/photo_2021-03-07_11-32-36.jpg
)


## Instalación

Utiliza el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar los requisitos.

```bash
pip install -r requeriments.txt
```

## ¿Cómo utilizarlo?
El archivo start.py contiene los datos necesarios para arrancar el programa. 

```from Telegram.telegram import TelegramBot
from Telegram.datos import configuracion

bot = TelegramBot(
    configuracion["usuario"],
    configuracion["api_id"],
    configuracion["api_hash"],
    configuracion["phone"]
)

bot.scraping_grupos()

# Listado de Opciones del BOT. Añadir aquí las opciones futuras. 
listado_opciones = {
    "¿Quieres SPAMEAR a los miembros de este grupo? Y/N: " : bot.spamear_usuarios,
    "¿Quieres IMPORTAR los usuarios de este grupo? Y/N: " : bot.secuestrar_usuarios,
    "¿Quieres almacenar la lista de usuarios? Y/N: " : bot.guardar_datos
}

for opciones in listado_opciones:
    print (opciones)
    if input("Respuesta: ").upper() == "Y":
        listado_opciones[opciones]()'
```

### Configuración de la cuenta
Dentro de la carpeta Telegram encontrarás un archivo llamado datos.py 
```

configuracion = {
    "usuario" : "", # Nombre de Usuario (Sólo se usa para guardar la sesión)
    "api_id" : 00000, # API_ID generado desde my.telegram.org 
    "api_hash" : '000000000', # API_HASH generado desde my.telegram.org
    "phone":'+34654.....' # Teléfono (Debe incluir el prefijo)
}
```
Introduce tu nombre de usuario, la api_id, el api_hash y el número de Teléfono.

Obtendrás el API_ID y el API_HASH al crear una nueva aplicación en [my.telegram.org](https://my.telegram.org/auth)
![](https://israelperez.ninja/wp-content/uploads/2021/03/photo_2021-03-07_16-21-39.jpg)

### Arranca el Script

```bash
python start.py
```
