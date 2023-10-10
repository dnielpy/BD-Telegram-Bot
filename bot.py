# 6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

token = '6195133432:AAGQPBBZzA2uaB1d20OkjcrrMQWHTJCBE9w'
my_id = 740635631
repartidores = [my_id]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.effective_user.id == my_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome back boss")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def newClient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def getNumber():
        dirty_message = str(update.message.text)
        
        texto_sin_newclient = dirty_message.replace("/NewClient ", "")
        return texto_sin_newclient

    if(update.effective_user.id == my_id):
        for repartidor in repartidores:
            await context.bot.send_message(chat_id=repartidor, text="Nuevo usuario ha contactado ⭕️\n\nPresiona aquí para hablar con él: 📩\n\nhttps://wa.me/"+ getNumber() +"?text=Usuario%20Contactado")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No estás autorizado a usar esta función")


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    newClient_handler = CommandHandler('NewClient', newClient)
    application.add_handler(newClient_handler)

    application.run_polling()