GREETING = ('Регистрация в очередь открыта\n'
            'Для помощи по командам введи /help')
QUEUE_SUCCESS = 'встал в очередь'
QUEUE_ALREADY_ACTIVE = ('Ты уже стоишь в очереди под номером {}.\n'
                        'Последним был вызван номер {}')
QUEUE_ALREADY_INACTIVE = ('Ты уже стоишь в очереди под номером {}.\n'
                          'Сейчас никто не вызван')
QUEUE_CURRENT = 'Стоят в очереди:\n'
QUEUE_COMPLETE = ('В очереди больше никого нет.\n'
                  'Рекомендую очистить список командой /clear.')
QUEUE_NEXT = ', к тебе взывают'
ADMIN_CONTROL = 'Взывать к людям из очереди может только админ группы'
BUTTON_CALL_NEXT = 'Возвать к следующему'
BUTTON_CALL_CURRENT = 'Разбудить'
WARNING = ('Кто-то все еще стоит в очереди.\n'
           'Очистите ее командой /clear.')
HELP_MESSAGE = (
    'Привет! Я бот электронной очереди.\n\n'
    'Для корректной работы, сделай меня админом группы.\n\n'
    'Позволь рассказать о том, как мной управлять:\n'
    '1. /start - открывает возможность встать в очередь. Создает сообщение, '
    'куда впоследствии будут добавляться люди, которые стали в очередь. '
    'Для удобства это сообщение будет закреплено в группе.\n'
    '2. /get_in - отправив эту команду, ты встанешь в текущую очередь. '
    'На всякий случай проверяй, появился ли ты в закрепленном сообщении\n'
    '3. /call - альтернатива кнопки "Возвать к следующему", которая находится '
    'под списком людей в очереди. Она вызывает следующего человека в очереди. '
    'И кнопка, и эта команда сработают только от их активации администратором '
    'этой группы.\n'
    '4. /clear - очищает текущую очередь и возвращает меня в исходное '
    'состояние.\n\n'
    'Приятного пользования!\n'
    'Если нашли баги или есть предложения - пишите в телегу @Kiminstir'
)
CLEAR = 'Список очищен, работа с очередью завершена'
