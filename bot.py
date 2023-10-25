from typing import Any
import logging
import time
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, Application, CallbackQueryHandler, CommandHandler, ContextTypes


password = 123456
#Token real
token = '6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w'


my_id = 740635631
my_name = "@dnielpy"
repartidores = [my_name]
usernumber = []
group_id = "-4062202920"
Ventas = {}
VentasConfirmadas = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Bienvenido al Servicio de Gestión de Ventas de Armando Flavio Buenadela ☘️.   \n\nSi aún no eres un vendedor, pulsa aqui: /AgregarVendedor ")
    print(update.effective_chat.id)

async def NuevoCliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == my_id:
        def getNumber():
            dirty_message = str(update.message.text)
            texto_sin_newclient = dirty_message.replace("/NuevoCliente ", "")
            texto_sin_newclient = texto_sin_newclient.replace("+", "")
            texto_sin_newclient = texto_sin_newclient.replace(" ", "")
            usernumber.append(texto_sin_newclient)
        getNumber()
        keyboard = [
            [
                InlineKeyboardButton("Contactar 💬", callback_data="1"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.  bot.send_message(chat_id=group_id, text="Nuevo usuario ha contactado⚡️", reply_markup=reply_markup)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No estás autorizado a usar esta función")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # Obtener el tiempo actual antes de enviar el mensaje
    start_time = time.time()

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await context.bot.send_message(chat_id=context._user_id, text="📩 Presiona aquí para hablar con él: 📩\n\nhttps://wa.me/"+ usernumber[-1] +"/?text=Hola!%20Gracias%20por%20contactar%20con%20Armando%20Flavio%20Buenadela.%20Estoy%20aquí%20para%20atender%20su%20pedido.")
    # Esperar a que AtencionCompletada se complete
    await AtencionCompletada(update, context)

    # Obtener el tiempo transcurrido después de completar la venta
    elapsed_time = time.time() - start_time

    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()

    #crear una variable que contenga la cantidad de ventas que tiene el vendedor en la base de datos
    cursor.execute("SELECT atenciones FROM Atenciones WHERE vendedor = ?", (update.effective_user.name,))
    userventas = cursor.fetchone()
    userventasstr = str(userventas)
    #eliminar los simbolos () y , de la variable
    userventasstr = userventasstr.replace("(", "")
    userventasstr = userventasstr.replace(")", "")
    userventasstr = userventasstr.replace(",", "")

    # Generar el mensaje final con el tiempo transcurrido y actualizar el mensaje original
    message_text = f"Usuario Atendido por {update.effective_user.name} ✅\n" \
                   f"Tiempo de atención: {elapsed_time:.2f} segundos\n" \
                   f"Tiene {userventasstr} atenciones en esta semana"

    await query.edit_message_text(text=message_text)
    conexion.commit()
    conexion.close()

async def AtencionCompletada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agregar una venta al vendedor
    if update.effective_user.name in Ventas:
        Ventas[update.effective_user.name] += 1
   
    # Guardar los datos en la base de datos
    # Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT atenciones FROM Atenciones WHERE vendedor = ?", (update.effective_user.name,))
    userventas = cursor.fetchone()
    #si el vendedor no tiene ventas, se le asigna 0
    if userventas == None:
        userventas = 0
    else:
        userventas = userventas[0]

    #Borrar en la base de datos los datos que existan de ese vendedor
    cursor.execute("DELETE FROM Atenciones WHERE vendedor = ?", (update.effective_user.name,))
    
    cursor.execute("INSERT INTO Atenciones VALUES (?, ?)", (update.effective_user.name, int(userventas) + 1))
    conexion.commit()
    conexion.close()

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Tomar los datos de la base de datos
    # Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Atenciones")
    atenciones = cursor.fetchall()
    
    total_de_atenciones = 0
    for i in atenciones:
        total_de_atenciones += i[1]

    atenciones.sort(key=lambda x: x[1], reverse=True)
    vendedor_con_mas_atenciones = atenciones[0][0]

    await context.bot.send_message(chat_id=group_id, text=f"⚡️ Reporte ⚡️ \nTotal de usuarios que han contactado 💰: {total_de_atenciones}\nVendedor con más ventas 🎁: {vendedor_con_mas_atenciones}")
    #cerrar la conexion a la base de datos
    conexion.close()

async def CerrarDia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #llamar a la funcion report para obtener los datos
    await report(update, context)
    #obtener la fecha actual
    fecha = time.strftime("%d/%m/%y")
    #Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Atenciones")
    atenciones = cursor.fetchall()
    
    total_de_atenciones = 0
    for i in atenciones:
        total_de_atenciones += i[1]

    texto_a_escribir = fecha + "\nVendedores: \n\n" + str(atenciones) + "\nTotal de usuarios que han contactado: " + str(total_de_atenciones)
    #agregar el texto al txt llamado "reporte" junto con al texto que ya existe
    with open("reporte.txt", "a") as myfile:
        myfile.write("\n\n" + texto_a_escribir)
    myfile.close()
    conexion.close()
    
    #Asignar el valor de 0 a las ventas de cada vendedor en la base de datos
    # Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Atenciones")
    atenciones = cursor.fetchall()
    for i in atenciones:
        cursor.execute("DELETE FROM Atenciones WHERE vendedor = ?", (i[0],))
        cursor.execute("INSERT INTO Atenciones VALUES (?, ?)", (i[0], 0))
    conexion.commit()
    conexion.close()
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Reporte guardado en reporte.txt")
    #Enviar el archivo de texto a myname
    await context.bot.send_document(chat_id=my_id, document=open('reporte.txt', 'rb'))


async def AgregarVendedor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repartidores.append(update.effective_user.name)
    Ventas[update.effective_user.name] = 0
    await context.bot.send_message(chat_id=update.effective_chat.id, text="⚡️ Felicidades! Ahora formas parte de nuestro Equipo de Ventas⚡️")

    #agregar el vendedor a la base de datos
    # Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Vendedores (vendedor text)")
    #buscar en que posicion del array repartidores se encuentra el vendedor

    #agrear el vendedor solo si no existe
    username = str(update.effective_user.name)
    cursor.execute("INSERT INTO Vendedores VALUES (?)", (username,))
    conexion.commit()
    conexion.close()

#crear un metodo para enviar el archivo de la base de datos a myname
async def EnviarBD(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == my_id:
        await context.bot.send_document(chat_id=my_id, document=open('bade_de_datos.db', 'rb'))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No estás autorizado a usar esta función")

async def VentaCompletada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Si el usuario envia una foto se le agrega una venta en la base de datos
    # Agregar una venta al vendedor
    if update.effective_user.name in VentasConfirmadas:
        VentasConfirmadas[update.effective_user.name] += 1
    
    # Guardar los datos en la base de datos
    # Conexión a la base de datos
    conexion = sqlite3.connect("bade_de_datos.db")
    cursor = conexion.cursor()

    #crear una variable que contenga la cantidad de ventas que tiene el vendedor en la base de datos
    cursor.execute("SELECT ventas FROM ventas WHERE vendedor = ?", (update.effective_user.name,))
    userventas = cursor.fetchone()
    #si el vendedor no tiene ventas, se le asigna 0
    if userventas == None:
            userventas = 0
    else:
        userventas = userventas[0]

    #Borrar en la base de datos los datos que existan de ese vendedor
    cursor.execute("DELETE FROM Ventas WHERE vendedor = ?", (update.effective_user.name,))
        
    cursor.execute("INSERT INTO Ventas VALUES (?, ?)", (update.effective_user.name, int(userventas) + 1))
    
    cursor.execute("SELECT ventas FROM Ventas WHERE vendedor = ?", (update.effective_user.name,))
    userventas = cursor.fetchone()
    userventasstr = str(userventas)
    #eliminar los simbolos () y , de la variable
    userventasstr = userventasstr.replace("(", "")
    userventasstr = userventasstr.replace(")", "")
    userventasstr = userventasstr.replace(",", "")

    # Generar el mensaje final con el tiempo transcurrido y actualizar el mensaje original
    message_text = f"Venta Confirmada por {update.effective_user.name} ✅\n" \
                   f"Tiene {userventasstr} ventas en esta semana"
    
    
    conexion.commit()
    conexion.close()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)   


def main() -> None:

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("NuevoCliente", NuevoCliente))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("AgregarVendedor", AgregarVendedor))
    application.add_handler(CommandHandler("Ayuda", help))
    application.add_handler(CommandHandler("EnviarBD", EnviarBD))
    application.add_handler(CommandHandler("CerrarDia", CerrarDia))

    application.add_handler(MessageHandler(filters.PHOTO & (~filters.COMMAND), VentaCompletada))



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()