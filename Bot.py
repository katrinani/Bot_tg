import telebot
from telebot import types
import webbrowser
bot = telebot.TeleBot('6401248215:AAHb1ieiU5malll9Hga3-eqTsQgwLCZjXow')
@bot.message_handler(commands=['start', 'help'])
def main(message):
    mess = """<b><em>Вот, с чем я могу тебе помочь</em></b>:
    <em>/map</em> - выведу карты всех этажей главного корпуса и помогу найти дорогу до 4 корпуса
    <em>/timetable</em> - покажу актуальное рассписание на конкретный день
    <em>/info</em> - дам описание полезной информации о учёбе
    <em>/links_csu</em> - выведу ссылки, связанные с ЧелГУ и деятелностью его студентов
    <em>/links_it</em> - выведу полезные ссылки, помогающие в освоении it профессии
    <em>/help</em> - расскажу ещё раз про свои функции"""
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['map'])
def map_csu(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('0 этаж', callback_data='0fl')
    btn2 = types.InlineKeyboardButton('1 этаж', callback_data='1fl')
    btn3 = types.InlineKeyboardButton('2 этаж', callback_data='2fl')
    btn4 = types.InlineKeyboardButton('3 этаж', callback_data='3fl')
    btn5 = types.InlineKeyboardButton('4 этаж', callback_data='4fl')
    btn6 = types.InlineKeyboardButton('Расположение 4 корпуса', url='https://maps.google.com/maps?q=55.180035,61.335219&ll=55.180035,61.335219&z=16')
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6)
    bot.send_message(message.chat.id, 'Какой <em>этаж/корпус</em> Вас интересует?', reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == '0fl' or callback.data == '1fl' or callback.data == '2fl' or callback.data == '3fl' or callback.data == '4fl')
def callback_message(callback):
    first_char = str(callback.data)[0]
    file = open(f'./Этаж {first_char}.png', 'rb')
    bot.send_message(callback.message.chat.id, f'{first_char} этаж')
    bot.send_photo(callback.message.chat.id, file)
    bot.answer_callback_query(callback.id)


@bot.message_handler(commands=['timetable'])
def timetable(message):
    markup = types.InlineKeyboardMarkup()
    btn1, btn2 = types.InlineKeyboardButton('Нечетная неделя (1)', callback_data='n1'), types.InlineKeyboardButton('Четная неделя (2)', callback_data='n2')
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Выберите <em> неделю </em>', reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == 'n1' or callback.data == 'n2')
def one_step(callback):
    if callback.data == 'n1':
        markup2 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Понедельник', callback_data='1_1d')
        btn2 = types.InlineKeyboardButton('Вторник', callback_data='1_2d')
        btn3 = types.InlineKeyboardButton('Среда', callback_data='1_3d')
        btn4 = types.InlineKeyboardButton('Четверг', callback_data='1_4d')
        btn5 = types.InlineKeyboardButton('Пятница', callback_data='1_5d')
        btn6 = types.InlineKeyboardButton('Суббота', callback_data='1_6d')
        markup2.row(btn1, btn2)
        markup2.row(btn3, btn4)
        markup2.row(btn5, btn6)
        bot.send_message(callback.message.chat.id, 'Выберите <em>день недели</em>', reply_markup=markup2, parse_mode='html')
    elif callback.data == 'n2':
        markup3 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Понедельник', callback_data='2_1d')
        btn2 = types.InlineKeyboardButton('Вторник', callback_data='2_2d')
        btn3 = types.InlineKeyboardButton('Среда', callback_data='2_3d')
        btn4 = types.InlineKeyboardButton('Четверг', callback_data='2_4d')
        btn5 = types.InlineKeyboardButton('Пятница', callback_data='2_5d')
        btn6 = types.InlineKeyboardButton('Суббота', callback_data='2_6d')
        markup3.row(btn1, btn2)
        markup3.row(btn3, btn4)
        markup3.row(btn5, btn6)
        bot.send_message(callback.message.chat.id, 'Выберите <em>день недели</em>', reply_markup=markup3, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: str(callback.data) in '1_1d1_2d1_3d1_4d1_5d1_6d2_1d2_2d2_3d2_4d2_5d2_6d')
def step(callback):
    first_char = str(callback.data)[0:3]
    file = open(f'./day{first_char}.jpg', 'rb')
    bot.send_photo(callback.message.chat.id, file)
    bot.answer_callback_query(callback.id)


@bot.message_handler(commands=['info'])
def info(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Информация о интернет-ресурсах ЧелГУ', callback_data='csu')
    btn2 = types.InlineKeyboardButton('Ресурсы для программистов', callback_data='it')
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Какая <em>информация</em> Вас интересует?', reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == 'csu' or callback.data == 'it')
def callback_mes(callback):
    if callback.data == 'csu':
        bot.send_message(callback.message.chat.id, """<b><em>Сайты, связанные с ЧелГУ</em></b>:
        <u>Мудл ЧелГУ</u>- супер сайт с курсами
        <u>Мудл ИИТ</u>-мега сайт с курсами всеми
        <u>Сайт ЧелГУ</u>
        <u>Научная Библиотека ЧелГУ</u>-мега библиотека
        <u>ЦТС(ЦентрТворчестваСтудентов)</u>
        <u>Профсоюзный Комитет(вк)</u>-не лезь,сожрет
        
        <em>Хочешь ссылки? Жми /links_csu</em>""", parse_mode='html')
        bot.answer_callback_query(callback.id)
    elif callback.data == 'it':
        bot.send_message(callback.message.chat.id, """<b><em>Общие ресурсы (независимо от языка программирования)</em></b>:
        <u>Habr</u> - сайт, созданный для публикации новостей, аналитических статей, мыслей, связанных с информационными технологиями и интернетом.
        <u>GitHab</u> - крупнейший веб-сервис для хостинга IT-проектов и их совместной разработки. На сайте представлен свободный исходный код, с которым вы можете ознакомиться.
        <u>Metanit</u> - сайт посвящен различным языкам и технологиям программирования, компьютерам, мобильным платформам и ИТ-технологиям c различные руководства и учебные материалы, статьи и примеры
        <u>Открытый лекторий Летних школ от Яндекса</u> - более 150 лекций в онлайн-формате, общение с топовыми экспертами из Яндекса, прокачка знаний по востребованным IT‑специальностям и решение сложных бизнес‑кейсов
        <u>Киберфорум</u> - форум программистов и системных администраторов, помощь в решении задач по программированию, математике, физике и другим наукам, решение проблем с компьютером, операционными системами
        <u>Библиотека программиста</u> - материалы, которые научат и помогут программировать. Книги и лекции, видеоуроки и советы, тесты знаний и обсуждение горячих тем
        <u>Roadmap</u> - собрание дорожных карт, руководств и другого образовательного контента, которое поможет разработчикам выбрать правильный путь и направлять их обучение.
        
        <em>Заинтересовало? Жми /links_it для получения ссылок</em>""", parse_mode='html')
        bot.answer_callback_query(callback.id)  # обработка команды закончена


@bot.message_handler(commands=['links_csu'])
def csu(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Мудл ЧелГУ', url='https://moodle.uio.csu.ru/')
    btn2 = types.InlineKeyboardButton('Мудл ИИТ', url='https://eu.iit.csu.ru')
    btn3 = types.InlineKeyboardButton('Сайт ЧелГУ', url='https://www.csu.ru/')
    btn4 = types.InlineKeyboardButton('Научная Библиотека ЧелГУ', url='https://library.csu.ru/ru/')
    btn5 = types.InlineKeyboardButton('ЦТС (Центр Творчества Студентов)', url='https://ctsofficial.ru/')
    btn6 = types.InlineKeyboardButton('Профсоюзный Комитет (вк)', url='https://vk.com/profcomcsu')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5)
    markup.row(btn6)
    bot.send_message(message.chat.id, 'Выберите <em>рессурс</em>, на который хотите перейти', reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['links_it'])
def it(message):
    markup = types.InlineKeyboardMarkup()
    btn1, btn2 = types.InlineKeyboardButton('Habr', url='https://habr.com/ru/'), types.InlineKeyboardButton('GitHab', url='https://github.com/')
    btn3 = types.InlineKeyboardButton('Metanit', url='https://metanit.com/')
    btn4 = types.InlineKeyboardButton('Открытый лекторий Летних школ от Яндекса', url='https://yandex.ru/yaintern/schools/open-lectures')
    btn5 = types.InlineKeyboardButton('Киберфорум', url='https://www.cyberforum.ru/')
    btn6 = types.InlineKeyboardButton('Библиотека программиста', url='https://proglib.io/')
    btn7 = types.InlineKeyboardButton('Roadmap', url='https://roadmap.sh/')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5, btn7)
    markup.row(btn6)
    bot.send_message(message.chat.id, 'Выберите <em>рессурс</em>, на который хотите перейти', reply_markup=markup, parse_mode='html')


bot.polling(none_stop=True)  # бот работает бесконечно, процесс не завершается(bot.infinity_polling()-для бесконечн работы
