# 6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


token = '6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w'
my_id = 740635631
repartidores = [my_id]
usernumber = []
group_id = "-4072784469"
Ventas = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.effective_user.id == my_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def newClient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.effective_user.id == my_id):
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
    
            #await update.message.reply_text("🟢Nuevo usuario ha contactado🟢", reply_markup=reply_markup)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No estás autorizado a usar esta función")   

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await context.bot.send_message(chat_id=context._user_id, text="📩 Presiona aquí para hablar con él: 📩\n\nhttps://wa.me/"+ usernumber[-1] +"/?text=Usuario%20Contactado")   
    VentaCompletada(update, context, update.effective_user.id)
    await query.edit_message_text(text=f"Usuario Atendido por " + update.effective_user.name +" ✅ \n\nVentas: " + str(Ventas[update.effective_user.id]))

async def VentaCompletada(update: Update, context: ContextTypes.DEFAULT_TYPE, vendedorID):
    Ventas[vendedorID]+1

async def StartRunning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Agregar todos los vendedores a la lista de vendedores
    for vendedor in vendedores:
        Ventas[vendedor] = 0





def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("NewClient", newClient))
    application.add_handler(CommandHandler("StartRunning", StartRunning))



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()