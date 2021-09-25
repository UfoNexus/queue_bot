from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


print('Бот запущен. Нажмите Ctrl+C для завершения')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


def start(update, context):
    


def button(update, context):
    chat = update.effective_chat
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=chat.id, text=f"Selected option: {query.data}")


dispatcher = updater.dispatcher
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()
