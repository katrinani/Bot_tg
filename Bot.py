import aiogram
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, executor
bot = Bot(token='6401248215:AAHb1ieiU5malll9Hga3-eqTsQgwLCZjXow')
dp = Dispatcher()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=['start', 'help'])
async def main(chat_id: int):
    mess = """<b><em>Вот, с чем я могу тебе помочь</em></b>:
    <em>/map</em> - выведу карты всех этажей главного корпуса и помогу найти дорогу до 4 корпуса
    <em>/timetable</em> - покажу актуальное рассписание на конкретный день
    <em>/info</em> - дам описание полезной информации о учёбе
    <em>/links_csu</em> - выведу ссылки, связанные с ЧелГУ и деятелностью его студентов
    <em>/links_it</em> - выведу полезные ссылки, помогающие в освоении it профессии
    <em>/help</em> - расскажу ещё раз про свои функции"""
    await bot.send_message(chat_id, text=mess, parse_mode='HTML')


@dp.message(commands=['map'])
async def map_csu(message: types.Message):
    markup = types.InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='0 этаж', callback_data='0fl')
    btn2 = types.InlineKeyboardButton(text='1 этаж', callback_data='1fl')
    btn3 = types.InlineKeyboardButton(text='2 этаж', callback_data='2fl')
    btn4 = types.InlineKeyboardButton(text='3 этаж', callback_data='3fl')
    btn5 = types.InlineKeyboardButton(text='4 этаж', callback_data='4fl')
    url_per = 'https://maps.google.com/maps?q=55.180035,61.335219&ll=55.180035,61.335219&z=16'
    btn6 = types.InlineKeyboardButton(text='Расположение 4 корпуса', url=url_per)
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6)
    mes = 'Какой <em>этаж/корпус</em> Вас интересует?'
    await message.answer(text=mes, reply_markup=markup.as_markup(), parse_mode='HTML')


@dp.callback_query(F.data == '0fl' or F.data == '1fl' or F.data == '2fl' or F.data == '3fl' or F.data == '4fl')
async def callback_message(callback: types.CallbackQuery):
    first_char = str(callback.data)[0]  # 1 число поступающего колбэка
    # file = open(f'./Этаж {first_char}.png', 'rb')
    file = FSInputFile(f'./Этаж {first_char}.png')
    await bot.send_message(chat_id, text=f'{first_char} этаж')
    await bot.send_photo(chat_id, file)
    # await bot.answer_callback_query(callback.id)


@dp.message_handler(commands=['timetable'])
async def timetable(chat_id: int):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Нечетная неделя (1)', callback_data='n1')
    btn2 = types.InlineKeyboardButton(text='Четная неделя (2)', callback_data='n2')
    markup.row(btn1)
    markup.row(btn2)
    await bot.send_message(chat_id, text='Выберите <em> неделю </em>', reply_markup=markup, parse_mode='HTML')


@dp.callback_query_handler(func=lambda callback: callback.data == 'n1' or callback.data == 'n2')
async def one_step(chat_id: int):
    if callback.data == 'n1':
        markup2 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Понедельник', callback_data='1_1d')
        btn2 = types.InlineKeyboardButton(text='Вторник', callback_data='1_2d')
        btn3 = types.InlineKeyboardButton(text='Среда', callback_data='1_3d')
        btn4 = types.InlineKeyboardButton(text='Четверг', callback_data='1_4d')
        btn5 = types.InlineKeyboardButton(text='Пятница', callback_data='1_5d')
        btn6 = types.InlineKeyboardButton(text='Суббота', callback_data='1_6d')
        markup2.row(btn1, btn2)
        markup2.row(btn3, btn4)
        markup2.row(btn5, btn6)
        await bot.send_message(chat_id, text='Выберите <em>день недели</em>', reply_markup=markup2, parse_mode='HTML')
    elif callback.data == 'n2':
        markup3 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Понедельник', callback_data='2_1d')
        btn2 = types.InlineKeyboardButton(text='Вторник', callback_data='2_2d')
        btn3 = types.InlineKeyboardButton(text='Среда', callback_data='2_3d')
        btn4 = types.InlineKeyboardButton(text='Четверг', callback_data='2_4d')
        btn5 = types.InlineKeyboardButton(text='Пятница', callback_data='2_5d')
        btn6 = types.InlineKeyboardButton(text='Суббота', callback_data='2_6d')
        markup3.row(btn1, btn2)
        markup3.row(btn3, btn4)
        markup3.row(btn5, btn6)
        await bot.send_message(chat_id, text='Выберите <em>день недели</em>', reply_markup=markup3, parse_mode='HTML')


@dp.callback_query_handler(func=lambda callback: str(callback.data) in '1_1d1_2d1_3d1_4d1_5d1_6d2_1d2_2d2_3d2_4d2_5d2_6d')
async def step(chat_id: int):
    first_char = str(callback.data)[0:3]
    file = FSInputFile(f'./day{first_char}.jpg')
    await bot.send_photo(chat_id, file)
    await bot.answer_callback_query(callback.id)


@dp.message_handler(commands=['info'])
async def info(chat_id: int):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Информация о интернет-ресурсах ЧелГУ', callback_data='csu')
    btn2 = types.InlineKeyboardButton(text='Ресурсы для программистов', callback_data='it')
    markup.row(btn1)
    markup.row(btn2)
    mes = 'Какая <em>информация</em> Вас интересует?'
    await bot.send_message(chat_id, text=mes, reply_markup=markup, parse_mode='HTML')


@dp.callback_query_handler(func=lambda callback: callback.data == 'csu' or callback.data == 'it')
async def callback_mes(chat_id: int):
    if callback.data == 'csu':
        await bot.send_message(chat_id, text="""<b><em>Сайты, связанные с ЧелГУ</em></b>:
        <u>Мудл ЧелГУ</u>- супер сайт с курсами
        <u>Мудл ИИТ</u>-мега сайт с курсами всеми
        <u>Сайт ЧелГУ</u>
        <u>Научная Библиотека ЧелГУ</u>-мега библиотека
        <u>ЦТС(ЦентрТворчестваСтудентов)</u>
        <u>Профсоюзный Комитет(вк)</u>-не лезь,сожрет
        
        <em>Хочешь ссылки? Жми /links_csu</em>""", parse_mode='HTML')
        await bot.answer_callback_query(callback.id)
    elif callback.data == 'it':
        await bot.send_message(chat_id, text= """<b><em>Общие ресурсы (независимо от языка программирования)</em></b>:
        <u>Habr</u> - сайт, созданный для публикации новостей, аналитических статей, мыслей, связанных с информационными технологиями и интернетом.
        <u>GitHab</u> - крупнейший веб-сервис для хостинга IT-проектов и их совместной разработки. На сайте представлен свободный исходный код, с которым вы можете ознакомиться.
        <u>Metanit</u> - сайт посвящен различным языкам и технологиям программирования, компьютерам, мобильным платформам и ИТ-технологиям c различные руководства и учебные материалы, статьи и примеры
        <u>Открытый лекторий Летних школ от Яндекса</u> - более 150 лекций в онлайн-формате, общение с топовыми экспертами из Яндекса, прокачка знаний по востребованным IT‑специальностям и решение сложных бизнес‑кейсов
        <u>Киберфорум</u> - форум программистов и системных администраторов, помощь в решении задач по программированию, математике, физике и другим наукам, решение проблем с компьютером, операционными системами
        <u>Библиотека программиста</u> - материалы, которые научат и помогут программировать. Книги и лекции, видеоуроки и советы, тесты знаний и обсуждение горячих тем
        <u>Roadmap</u> - собрание дорожных карт, руководств и другого образовательного контента, которое поможет разработчикам выбрать правильный путь и направлять их обучение.
        
        <em>Заинтересовало? Жми /links_it для получения ссылок</em>""", parse_mode='HTML')
        await bot.answer_callback_query(callback.id)  # обработка команды закончена


@dp.message_handler(commands=['links_csu'])
async def csu(chat_id: int, bot: Bot):
    markup = types.InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Мудл ЧелГУ', url='https://moodle.uio.csu.ru/')
    btn2 = types.InlineKeyboardButton(text='Мудл ИИТ', url='https://eu.iit.csu.ru')
    btn3 = types.InlineKeyboardButton(text='Сайт ЧелГУ', url='https://www.csu.ru/')
    btn4 = types.InlineKeyboardButton(text='Научная Библиотека ЧелГУ', url='https://library.csu.ru/ru/')
    btn5 = types.InlineKeyboardButton(text='ЦТС (Центр Творчества Студентов)', url='https://ctsofficial.ru/')
    btn6 = types.InlineKeyboardButton(text='Профсоюзный Комитет (вк)', url='https://vk.com/profcomcsu')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5)
    markup.row(btn6)
    mes = 'Выберите <em>рессурс</em>, на который хотите перейти'
    await bot.send_message(chat_id, text=mes, reply_markup=markup.as_markup(), parse_mode='HTML')


@dp.message_handler(commands=['links_it'])
async def it(chat_id: int, bot: Bot):
    markup = types.InlineKeyboardBuider()
    btn1 = types.InlineKeyboardButton(text='Habr', url='https://habr.com/ru/')
    btn2 = types.InlineKeyboardButton(text='GitHab', url='https://github.com/')
    btn3 = types.InlineKeyboardButton(text='Metanit', url='https://metanit.com/')
    btn4 = types.InlineKeyboardButton(text='Открытый лекторий Летних школ от Яндекса', url='https://yandex.ru/yaintern/schools/open-lectures')
    btn5 = types.InlineKeyboardButton(text='Киберфорум', url='https://www.cyberforum.ru/')
    btn6 = types.InlineKeyboardButton(text='Библиотека программиста', url='https://proglib.io/')
    btn7 = types.InlineKeyboardButton(text='Roadmap', url='https://roadmap.sh/')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5, btn7)
    markup.row(btn6)
    mes = 'Выберите <em>рессурс</em>, на который хотите перейти'
    await bot.send_message(chat_id, text=mes, reply_markup=markup.as_markup(), parse_mode='HTML')


bot.polling(none_stop=True)  # бот работает бесконечно, процесс не завершается(bot.infinity_polling()-для бесконечн работы
