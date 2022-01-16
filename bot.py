import logging
import messages
import os

from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
)
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, CallbackContext
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print('Бот запущен. Нажмите Ctrl+C для завершения')

logger = logging.getLogger(__name__)
TOKEN = ''
PORT = int(os.environ.get('PORT', 80))


bot_status = 'inactive'
current_queue = {}
queue_id_list = []
queue_counter = 0
queue_message_id = 0
queue_name_list_numbered = []


def upd(context: CallbackContext):
    print('Uptime 25 minutes')


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def call_button():
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
    global bot_status
    if bot_status == 'inactive':
        bot_status = 'active'
        msg = context.bot.send_message(
            chat_id=chat_id,
            text=messages.GREETING,
            reply_markup=call_button()
        )
        global queue_message_id
        queue_message_id = msg.message_id
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
            reply_markup=call_button(),
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


def change_position(update, context):
    chat_id = update.effective_chat.id
    global bot_status
    if bot_status == 'inactive':
        context.bot.send_message(
            chat_id=chat_id,
            text=messages.NO_START_ERROR
        )
        return

    if update.effective_user.id in get_admin_ids(
            context.bot,
            update.message.chat_id
    ):
        if len(context.args) == 0:
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.ZERO_ARGS
            )
            return
        if len(context.args) == 1:
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.ONE_ARG
            )
            return
        if type(context.args[0]) != int or type(context.args[1]) != int:
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.WRONG_TYPE
            )
        global current_queue
        old_position = int(context.args[0])
        new_position = int(context.args[1])
        if (old_position not in current_queue.keys() or
                new_position not in current_queue.keys()):
            context.bot.send_message(
                chat_id=chat_id,
                text=messages.POSITION_ERROR
            )
            return
        target_user = current_queue.get(old_position)
        moving_user = target_user

        if new_position < old_position:
            for i in range(1, len(current_queue)+1, 1):
                value = current_queue.get(i)
                if new_position == i:
                    current_queue[new_position] = moving_user
                    if value == target_user:
                        break
                    moving_user = value
                    new_position += 1
        if new_position > old_position:
            for i in range(len(current_queue), 0, -1):
                value = current_queue.get(i)
                if new_position == i:
                    current_queue[new_position] = moving_user
                    if value == target_user:
                        break
                    moving_user = value
                    new_position = new_position - 1
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
                reply_markup=call_button(),
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
    if update.effective_user.id in get_admin_ids(
        context.bot,
        update.callback_query.message.chat_id
    ):
        query = update.callback_query
        if query.data == '/call':
            global queue_message_id
            global queue_name_list_numbered
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
                    reply_markup=call_button(),
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
    if update.effective_user.id in get_admin_ids(
            context.bot,
            update.callback_query.message.chat_id
    ):
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


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.job_queue.run_repeating(upd, interval=1500)
    dispatcher.add_handler(CommandHandler("help", help_user))
    dispatcher.add_handler(CommandHandler("start", on_start))
    dispatcher.add_handler(CommandHandler("get_in", get_in_queue))
    dispatcher.add_handler(CommandHandler("change", change_position))
    dispatcher.add_handler(CommandHandler("call", call_next))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=(
                              'https://arcane-forest-43632.herokuapp.com/' +
                              TOKEN))
    updater.idle()


if __name__ == '__main__':
    main()
