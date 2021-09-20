from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


print('Бот запущен. Нажмите Ctrl+C для завершения')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


def on_start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я бот очередей')


def on_message(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Тестовый ввод')


def get_in_queue(update, context):
    current_queue = {1: 'test1'}
    update.message.reply_text(f'test\n{current_queue[1]}',
                              quote=True)


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in_queue", get_in_queue))
dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()
