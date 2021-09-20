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
queue_username_list = []
queue_name_list = []


def get_in_queue(update, context):
    user = update.message.from_user
    active_username = user['username']
    active_truename = f'{user["first_name"]} {user["last_name"]}'
    queue_username_list = [(current_queue[i])[0] for i in current_queue]
    queue_name_list = [(current_queue[i])[1] for i in current_queue]
    if active_username not in queue_username_list:
        queue_number = len(current_queue) + 1
        current_queue[queue_number] = f'{active_username}', f'{active_truename}'
        queue_username_list.append((current_queue[queue_number])[0])
        queue_name_list.append((current_queue[queue_number])[1])
        update.message.reply_text(f'{active_username} встал в очередь',
                                  quote=True)
        update.message.reply_text('Стоят в очереди:\n'
                                  + "\n".join(queue_name_list))
    elif active_username in queue_username_list:
        update.message.reply_text('Ты уже стоишь в очереди',
                                  quote=True)
        update.message.reply_text('Стоят в очереди:\n'
                                  + "\n".join(queue_name_list))


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in_queue", get_in_queue))
dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()
