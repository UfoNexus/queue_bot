from telegram.ext import Updater, CommandHandler


print('Бот запущен. Нажмите Ctrl+C для завершения')
QUEUE_SUCCESS = 'встал в очередь'
QUEUE_ERROR = 'Ты уже стоишь в очереди'
QUEUE_CURRENT = 'Стоят в очереди:\n'

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


def on_start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я бот очередей')


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
        current_queue[queue_number] = active_truename
        queue_username_list.append((current_queue[queue_number])[0])
        queue_name_list.append(current_queue[1])
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(f'{active_truename} {QUEUE_SUCCESS}',
                                  quote=True)
        update.message.reply_text(queue_name_list_numbered[0])
        update.message.reply_text(queue_name_list)
        update.message.reply_text(QUEUE_CURRENT + "\n".join(queue_name_list_numbered))
    elif active_username in queue_username_list:
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(QUEUE_ERROR,
                                  quote=True)
        update.message.reply_text(QUEUE_CURRENT + "\n".join(queue_name_list_numbered))


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in_queue", get_in_queue))

updater.start_polling()
updater.idle()
