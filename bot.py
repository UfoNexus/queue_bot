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


current_queue = {}


def get_in_queue(update, context):
    queue_number = len(current_queue)
    current_queue[queue_number + 1] = f'login{queue_number+1}', f'name{queue_number+1}'
    login, name = current_queue[1]
    queue_login_list = [(current_queue[i])[0] for i in current_queue]
    queue_name_list = [(current_queue[i])[1] for i in current_queue]
    update.message.reply_text(f'{name} встал в очередь',
                              quote=True)
    update.message.reply_text('Стоят в очереди:\n'
                              + "\n".join(queue_name_list))


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in_queue", get_in_queue))
dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()
