from telegram.ext import Updater, CommandHandler


print('Бот запущен. Нажмите Ctrl+C для завершения')

GREETING = 'Привет, я бот очередей'
QUEUE_SUCCESS = 'встал в очередь'
QUEUE_ALREADY_IN = 'Ты уже стоишь в очереди'
QUEUE_CURRENT = 'Стоят в очереди:\n'
QUEUE_COMPLETE = 'В очереди больше никого нет'
QUEUE_NEXT = ', к тебе взывают'
ADMIN_CONTROL = 'Взывать к людям из очереди может только админ группы'

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


current_queue = {}
queue_id_list = []
queue_name_list = []
queue_counter = 0


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def on_start(update, context):
    update.message.reply_text(GREETING, quote=False)


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
                                  '\n'.join(queue_name_list_numbered),
                                  quote=False)
    else:
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(QUEUE_ALREADY_IN)
        update.message.reply_text(QUEUE_CURRENT +
                                  '\n'.join(queue_name_list_numbered),
                                  quote=False)


def call_next(update, context):
    if update.effective_user.id in get_admin_ids(context.bot,
                                                 update.message.chat_id):
        global queue_counter
        if queue_counter < len(current_queue):
            queue_counter += 1
            next_user = (current_queue[queue_counter][0],
                         current_queue[queue_counter][1])
            next_userlink = f'(tg://user?id={str(next_user[0])})'
            next_user_mention = f'[{next_user[1]}]{next_userlink}{QUEUE_NEXT}'
            update.message.reply_text(next_user_mention, parse_mode="Markdown")
        else:
            update.message.reply_text(QUEUE_COMPLETE, quote=False)
    else:
        update.message.reply_text(ADMIN_CONTROL, quote=False)


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in", get_in_queue))
dispatcher.add_handler(CommandHandler("call", call_next))

updater.start_polling()
updater.idle()
