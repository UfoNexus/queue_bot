GREETING = ('Регистрация в очередь открыта\n'
            'Для помощи по командам введи /help')
NO_START_ERROR = 'Сначала нужно начать работу командой /start'
QUEUE_SUCCESS = 'встал в очередь'
QUEUE_ALREADY_ACTIVE = ('Ты уже стоишь в очереди под номером {}.\n'
                        'Последним был вызван номер {}')
QUEUE_ALREADY_INACTIVE = ('Ты уже стоишь в очереди под номером {}.\n'
                          'Сейчас никто не вызван')
QUEUE_CURRENT = 'Стоят в очереди:\n'
QUEUE_COMPLETE = ('В очереди больше никого нет.\n'
                  'Рекомендую завершить работу командой /clear.')
QUEUE_NEXT = ', к тебе взывают \U0001F608'
ADMIN_CONTROL = '{}, взывать к людям из очереди может только админ группы'
BUTTON_CALL_NEXT = 'Возвать к следующему'
BUTTON_CALL_CURRENT = 'Разбудить'
WARNING = ('В прошлый раз не завершили работу бота.\n'
           'Сделай это сейчас командой /clear.')
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
    '4. /change - команда позволит администратору переместить человека в '
    'очереди. Для изменения позиции человека в очереди необходимо указать 2 цифры после'
    ' команды /change: текущую позицию, затем - куда переместить. Пример - '
    '/change 8 2, где 8 - текущая позиция в очереди, 2 - куда переместить.\n'
    '5. /clear - очищает текущую очередь и завершает мою работу.\n\n'
    'Приятного пользования!\n'
    'Если нашли баги или есть предложения - пишите в телегу @Kiminstir'
)
CLEAR = 'Список очищен, работа с очередью завершена'
CLEAR_ERROR = 'Работа была завершена ранее (или не начиналась вовсе)'
POSITION_ERROR = 'Введеная новая или старая позиция не совпадает с длиной очереди'
ZERO_ARGS = (
    'Для изменения позиции человека в очереди необходимо указать 2 цифры после '
    'команды /change: текущую позицию, затем - куда переместить. Пример - '
    '/change 8 2, где 8 - текущая позиция в очереди, 2 - куда переместить.'
)
ONE_ARG = ('Недостаточно информации для перемещения человека в очереди. Укажите '
           'вторым числом, на какую позицию переместить человека.')
WRONG_TYPE = ('Команда принимает только числа - текущую и новую позицию '
              'человека в очереди.')
