import messages
import os
import http
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Bot, Update
)
from flask import Flask, request
from werkzeug.wrappers import Response


print('Бот запущен. Нажмите Ctrl+C для завершения')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)
app = Flask(__name__)
bot = Bot(token=os.environ["TOKEN"])


bot_status = 'inactive'
current_queue = {}
queue_id_list = []
queue_counter = 0
queue_message_id = 0
queue_name_list_numbered = []


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
    global bot_status
    if bot_status == 'inactive':
        bot_status = 'active'
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
    global bot_status
    if bot_status == 'inactive':
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.NO_START_ERROR
        )
        return
    global current_queue
    global queue_id_list
    global queue_message_id
    global queue_name_list_numbered
    global queue_counter
    user = update.message.from_user
    active_id = user['id']
    if user['last_name'] is None:
        active_truename = user["first_name"]
    else:
        active_truename = f'{user["first_name"]} {user["last_name"]}'
    if active_id not in queue_id_list:
        queue_number = len(current_queue) + 1
        current_queue[queue_number] = active_id, active_truename
        queue_id_list.append(current_queue[queue_number][0])
        queue_name_list_numbered.append(
            f'{queue_number}\\. {current_queue[queue_number][1]}'
        )
        update.message.reply_text(
            f'{active_truename} {messages.QUEUE_SUCCESS}'
        )
        context.bot.edit_message_text(
            messages.QUEUE_CURRENT + '\n'.join(queue_name_list_numbered),
            chat_id=chat_id,
            message_id=queue_message_id,
            reply_markup=buttons_setup(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        searched_number = queue_id_list.index(active_id) + 1
        if queue_counter == 0 or queue_counter >= len(queue_id_list):
            update.message.reply_text(
                messages.QUEUE_ALREADY_INACTIVE.format(
                    searched_number
                )
            )
        else:
            update.message.reply_text(
                messages.QUEUE_ALREADY_ACTIVE.format(
                    searched_number, queue_counter
                )
            )


def call_next(update, context):
    chat_id = update.effective_chat.id
    global bot_status
    if bot_status == 'inactive':
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.NO_START_ERROR
        )
        return
    global queue_message_id
    global queue_name_list_numbered
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
                parse_mode=ParseMode.MARKDOWN_V2
            )
            queue_name_list_numbered[queue_counter-1] = (
                f'~{queue_name_list_numbered[queue_counter-1]}~'
            )
            context.bot.edit_message_text(
                messages.QUEUE_CURRENT + '\n'.join(queue_name_list_numbered),
                chat_id=chat_id,
                message_id=queue_message_id,
                reply_markup=buttons_setup(),
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.QUEUE_COMPLETE
            )
    else:
        user = update.message.from_user
        active_id = user['id']
        active_name = user["first_name"]
        user_mention = f'[{active_name}](tg://user?id={active_id})'
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.ADMIN_CONTROL.format(user_mention),
            parse_mode=ParseMode.MARKDOWN_V2
        )


def button(update, context):
    chat_id = update.effective_chat.id
    global bot_status
    if bot_status == 'inactive':
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.NO_START_ERROR
        )
        return
    global queue_message_id
    global queue_name_list_numbered
    if update.effective_user.id in get_admin_ids(
        context.bot,
        update.callback_query.message.chat_id
    ):
        query = update.callback_query
        if query.data == '/call':
            global queue_counter
            if queue_counter < len(current_queue):
                queue_counter += 1
                next_user = (current_queue[queue_counter][0],
                             current_queue[queue_counter][1])
                next_userlink = f'(tg://user?id={str(next_user[0])})'
                next_user_mention = (
                    f'[{next_user[1]}]{next_userlink}'
                )
                context.bot.sendMessage(
                    chat_id=chat_id,
                    text=f'{next_user_mention}{messages.QUEUE_NEXT}',
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                queue_name_list_numbered[queue_counter-1] = (
                    f'~{queue_name_list_numbered[queue_counter-1]}~'
                )
                context.bot.edit_message_text(
                    messages.QUEUE_CURRENT +
                    '\n'.join(queue_name_list_numbered),
                    chat_id=chat_id,
                    message_id=queue_message_id,
                    reply_markup=buttons_setup(),
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            else:
                context.bot.sendMessage(
                    chat_id=chat_id,
                    text=messages.QUEUE_COMPLETE
                )
    else:
        user = update.effective_user
        active_id = user['id']
        active_name = user["first_name"]
        user_mention = f'[{active_name}](tg://user?id={active_id})'
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.ADMIN_CONTROL.format(user_mention),
            parse_mode=ParseMode.MARKDOWN_V2
        )


def clear(update, context):
    chat_id = update.effective_chat.id
    global bot_status
    global current_queue
    if bot_status == 'active':
        global queue_id_list
        global queue_counter
        global queue_message_id
        global queue_name_list_numbered
        current_queue = {}
        queue_id_list = []
        queue_counter = 0
        queue_message_id = 0
        queue_name_list_numbered = []
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.CLEAR
        )
        bot_status = 'inactive'
        context.bot.unpinChatMessage(
            chat_id=chat_id,
            message_id=queue_message_id
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.CLEAR_ERROR
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


@app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
