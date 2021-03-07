from Telegram.telegram import TelegramBot
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
        listado_opciones[opciones]()