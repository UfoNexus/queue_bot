from telegram.ext import Updater, CommandHandler
from telegram import ParseMode


print('Бот запущен. Нажмите Ctrl+C для завершения')

token = '2011946261:AAFClQ54uJ9UvKiwBv4Fipcn47cEwxv7szQ'
updater = Updater(token, use_context=True)


def test(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text='~Тестовый текст~',
        parse_mode=ParseMode.MARKDOWN_V2
    )


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("test", test))

updater.start_polling()
updater.idle()
