import messages
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot


print('Бот запущен. Нажмите Ctrl+C для завершения')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


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
            InlineKeyboardButton(
                messages.BUTTON_CALL_NEXT,
                callback_data='/call'
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def help_user(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=messages.HELP_MESSAGE
    )


def on_start(update, context):
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    if len(current_queue) == 0:
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.GREETING,
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
            text=messages.WARNING
        )


def get_in_queue(update, context):
    chat_id = update.effective_chat.id
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
            f'{active_truename} {messages.QUEUE_SUCCESS}'
        )
        context.bot.edit_message_text(
            messages.QUEUE_CURRENT + '\n'.join(queue_name_list_numbered),
            chat_id=chat_id,
            message_id=queue_message_id,
            reply_markup=buttons_setup()
        )
    else:
        queue_name_list_numbered = []
        for i, name in enumerate(queue_name_list):
            queue_name_list_numbered.append(f'{i+1}. {queue_name_list[i]}')
        update.message.reply_text(
            messages.QUEUE_ALREADY_IN
        )


def call_next(update, context):
    chat_id = update.effective_chat.id
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
                text=f'{next_user_mention}{messages.QUEUE_NEXT}',
                parse_mode="Markdown"
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.QUEUE_COMPLETE
            )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.ADMIN_CONTROL
        )


def button(update, context):
    chat_id = update.effective_chat.id
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
                    f'[{next_user[1]}]{next_userlink}{messages.QUEUE_NEXT}'
                )
                bot.sendMessage(
                    chat_id=chat_id,
                    text=next_user_mention,
                    parse_mode="Markdown")
            else:
                bot.sendMessage(
                    chat_id=chat_id,
                    text=messages.QUEUE_COMPLETE
                )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.ADMIN_CONTROL
        )


def clear(update, context):
    chat_id = update.effective_chat.id
    global message_id
    global current_queue
    global queue_id_list
    global queue_name_list
    global queue_counter
    global queue_message_id
    context.bot.unpinChatMessage(
        chat_id=chat_id,
        message_id=queue_message_id
    )
    current_queue = {}
    queue_id_list = []
    queue_name_list = []
    queue_counter = 0
    queue_message_id = 0
    context.bot.send_message(
        chat_id=chat_id,
        text=messages.CLEAR
    )


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("help", help_user))
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("get_in", get_in_queue))
dispatcher.add_handler(CommandHandler("call", call_next))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(CommandHandler("clear", clear))

updater.start_polling()
updater.idle()
