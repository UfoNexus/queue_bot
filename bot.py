from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot


print('Бот запущен. Нажмите Ctrl+C для завершения')

GREETING = 'В очереди никто не стоит'
QUEUE_SUCCESS = 'встал в очередь'
QUEUE_ALREADY_IN = 'Ты уже стоишь в очереди'
QUEUE_CURRENT = 'Стоят в очереди:\n'
QUEUE_COMPLETE = 'В очереди больше никого нет'
QUEUE_NEXT = ', к тебе взывают'
ADMIN_CONTROL = 'Взывать к людям из очереди может только админ группы'
BUTTON_CALL_NEXT = 'Возвать к следующему'
BUTTON_CALL_CURRENT = 'Разбудить'
WARNING = ('Кто-то все еще стоит в очереди.\n'
           'Очистите ее командой /clear.')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


chat_id = 0
current_queue = {}
queue_id_list = []
queue_name_list = []
queue_counter = 0
queue_message_id = 0


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def buttons_setup():
    button_list = [
        [
            InlineKeyboardButton(BUTTON_CALL_NEXT, callback_data='/call'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def on_start(update, context):
    global chat_id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    if len(current_queue) == 0:
        context.bot.send_message(
            chat_id=chat_id,
            text=GREETING,
            reply_markup=buttons_setup()
        )
        global queue_message_id
        queue_message_id = message_id + 1
        context.bot.pinChatMessage(
            chat_id=chat_id,
            message_id=queue_message_id
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=WARNING
        )


def get_in_queue(update, context):
    global chat_id
    user = update.message.from_user
    active_id = user['id']
    global queue_message_id
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
        update.message.reply_text(
            f'{active_truename} {QUEUE_SUCCESS}'
        )
        context.bot.edit_message_text(
            QUEUE_CURRENT + '\n'.join(queue_name_list_numbered),
            chat_id=chat_id,
            message_id=queue_message_id,
            reply_markup=buttons_setup()
        )
    else:
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(
            QUEUE_ALREADY_IN
        )


def call_next(update, context):
    global chat_id
    if update.effective_user.id in get_admin_ids(
        context.bot,
        update.message.chat_id
    ):
        global queue_counter
        if queue_counter < len(current_queue):
            queue_counter += 1
            next_user = (current_queue[queue_counter][0],
                         current_queue[queue_counter][1])
            next_userlink = f'(tg://user?id={str(next_user[0])})'
            next_user_mention = f'[{next_user[1]}]{next_userlink}'
            context.bot.send_message(
                chat_id=chat_id,
                text=f'{next_user_mention}{QUEUE_NEXT}',
                parse_mode="Markdown"
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text=QUEUE_COMPLETE
            )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=ADMIN_CONTROL
        )


def button(update, context):
    global chat_id
    if update.effective_user.id in get_admin_ids(
        context.bot,
        update.callback_query.message.chat_id
    ):
        bot = Bot(token=token)
        query = update.callback_query
        if query.data == '/call':
            global queue_counter
            if queue_counter < len(current_queue):
                queue_counter += 1
                next_user = (current_queue[queue_counter][0],
                             current_queue[queue_counter][1])
                next_userlink = f'(tg://user?id={str(next_user[0])})'
                next_user_mention = (
                    f'[{next_user[1]}]{next_userlink}{QUEUE_NEXT}'
                )
                bot.sendMessage(
                    chat_id=chat_id,
                    text=next_user_mention,
                    parse_mode="Markdown")
            else:
                bot.sendMessage(
                    chat_id=chat_id,
                    text=QUEUE_COMPLETE
                )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=ADMIN_CONTROL
        )


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in", get_in_queue))
dispatcher.add_handler(CommandHandler("call", call_next))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()
