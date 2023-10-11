from typing import Any

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

password = 123456
token = '6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w'
my_id = 740635631
my_name = "@dnielpy"
repartidores = [my_name]
usernumber = []
group_id = "-4072784469"
Ventas = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == my_id:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def newClient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == my_id:
        def getNumber():
            dirty_message = str(update.message.text)
            texto_sin_newclient = dirty_message.replace("/NewClient ", "")
            usernumber.append(texto_sin_newclient)
        getNumber()

        for repartidor in repartidores:
            keyboard = [
                [
                    InlineKeyboardButton("Contactar 💬", callback_data="1"),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=group_id, text="🟢Nuevo usuario ha contactado🟢", reply_markup=reply_markup)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No estás autorizado a usar esta función")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await context.bot.send_message(chat_id=context._user_id, text="📩 Presiona aquí para hablar con él: 📩\n\nhttps://wa.me/"+ usernumber[-1] +"/?text=Usuario%20Contactado")
    await VentaCompletada(update, context)  # Esperar a que VentaCompletada se complete
    await query.edit_message_text(text=f"Usuario Atendido por " + update.effective_user.name +" ✅\nTiene " + str(Ventas[update.effective_user.name]) + " ventas en el día de hoy")

async def VentaCompletada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agregar una venta al vendedor
    if update.effective_user.name in Ventas:
        Ventas[update.effective_user.name] += 1

async def updateBD(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agregar todos los vendedores a la lista de vendedores
    for vendedor in repartidores:
        Ventas[vendedor] = 0
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Base de datos actualizada con exito ✅")
    

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_usuarios = len(usernumber)
    vendedor_con_mas_ventas = max(Ventas, key=Ventas.get)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"⚡️ Reporte ⚡️ \nTotal de usuarios que han contactado 💰: {total_usuarios}\nVendedor con más ventas 🎁: {vendedor_con_mas_ventas}")

async def addSeller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password_input = update.message.text[11:]  # Extraer la contraseña ingresada
    if password_input == str(password):
        repartidores.append(update.effective_user.name)
        Ventas[update.effective_user.name] = 0
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Vendedor agregado correctamente. Se recomienda hacer un /update")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Contraseña incorrecta")
    

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("NewClient", newClient))
    application.add_handler(CommandHandler("update", updateBD))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("addseller", addSeller))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()