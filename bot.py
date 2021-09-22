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
queue_id_list = []
queue_name_list = []


def get_in_queue(update, context):
    user = update.message.from_user
    active_id = user['id']
    if active_id not in queue_id_list:
        if user['last_name'] is None:
            active_truename = user["first_name"]
        else:
            active_truename = f'{user["first_name"]} {user["last_name"]}'
        queue_number = len(current_queue) + 1
        current_queue[queue_number] = active_id, active_truename
        queue_id_list.append(current_queue[queue_number][0])
        queue_name_list.append(current_queue[queue_number][1])
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(f'{active_truename} {QUEUE_SUCCESS}')
        update.message.reply_text(QUEUE_CURRENT +
                                  '\n'.join(queue_name_list_numbered))
    else:
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(QUEUE_ERROR, quote=True)
        update.message.reply_text(QUEUE_CURRENT +
                                  '\n'.join(queue_name_list_numbered))


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in", get_in_queue))

updater.start_polling()
updater.idle()
