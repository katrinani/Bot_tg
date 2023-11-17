import sqlite3 as sq
import aiogram
import asyncio
from aiogram import F, Bot, types, Dispatcher
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton, Message
from db_map import db_start, create_profile, edit_profile, check_group_of_student, check_role, output_all_id
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode


scheduler = AsyncIOScheduler()
bot = Bot(token='6401248215:AAHb1ieiU5malll9Hga3-eqTsQgwLCZjXow')
dp = Dispatcher(storage=MemoryStorage())

group_name = ['ПРИ101', 'ПРИ102', 'ПРИ103', 'БИ101', 'ПИ101']
callback_map = ['0fl', '1fl', '2fl', '3fl', '4fl']
callback_timetable = ['1_1d', '1_3d', '1_4d', '1_5d', '1_6d', '2_1d', '2_2d', '2_3d', '2_4d', '2_5d', '2_6d']
tg_user_id = ''


async def on_startup():
    await db_start()


class ProfileStatesGroup(StatesGroup):  # cоздаем класс  насследующийся от StatesGroup
    choosing_group = State()  # статус ожидания на group
    input_text = State()


def get_cancel_kb() -> ReplyKeyboardMarkup:
    bt = [types.KeyboardButton(text='/cancel')]
    kb = ReplyKeyboardMarkup(
        keyboard=[bt],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb


def get_kb() -> ReplyKeyboardMarkup:
    bt = [types.KeyboardButton(text='/create')]
    kb = types.ReplyKeyboardMarkup(
        keyboard=[bt],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb


@dp.message(F.text, Command('start'))
async def cmd_start(message: Message) -> None:
    await message.answer('Добро пожаловать! Для начала давайте создадим профиль. Нажмите /create',
                         reply_markup=get_kb())

    global tg_user_id
    tg_user_id = str(message.from_user.id)
    await create_profile(user_id=message.from_user.id)


@dp.message(F.text, Command('create'))
async def cmd_create(message: Message, state: FSMContext):
    await message.reply(
        text="Для начала работы давате сначала уточним вашу группу и номер группы. Введите их в формате 'ПИ101'\
    \nЕсли хотите прекратить создание профиля нажмите cancel",
        reply_markup=get_cancel_kb())
    await state.set_state(ProfileStatesGroup.choosing_group)  # установили состояние ожидания группы


@dp.message(F.text, Command(commands='cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    if state is None:
        return
    await state.clear()
    await message.answer(text='Действие отменено', reply_markup=get_kb())


@dp.message(
    F.text.in_(group_name),
    ProfileStatesGroup.choosing_group
)  # состояние ожидания группы и текст из списка
async def load_group(message: Message, state: FSMContext) -> None:
    user_group = message.text
    await message.reply(text=f"Ваша группа : {user_group}\nТеперь можно продолжить!")
    await edit_profile(user_group, user_id=message.from_user.id)
    await state.clear()


@dp.message(StateFilter('ProfileStatesGroup:choosing_group'))  # то же состояние, но на вход пришли другие данные
async def check_group(message: Message):
    await message.reply('Нет такой группы. Попробуйте ещё раз ввести группу и номер в верхнем регистре (пр. ПИ101)')


# ----------------------------------------------------------------------


@dp.callback_query(F.data.in_(callback_map))
async def callback_message(callback: types.CallbackQuery):
    first_char = str(callback.data)[0]  # 1 число поступающего колбэка
    file = FSInputFile(f'floor/Этаж {first_char}.png')
    await callback.message.answer(text=f'{first_char} этаж')  # вызов 0 этажа пока не возможен, jpg формат
    await callback.message.answer_photo(file)


@dp.callback_query(F.data.in_(callback_timetable))
async def step(callback: types.CallbackQuery):
    user_group = await check_group_of_student(tg_user_id)
    first_char = str(callback.data)[0:3]
    file = FSInputFile(f'{user_group}/day{first_char}.jpg')  # вместо папки будет подключаться информаци о группе из бд
    await callback.message.answer_photo(file)


@dp.message(F.text, Command('help'))
async def help_ph(message: types.Message):
    mess = """<b><em>Вот, с чем я могу тебе помочь</em></b>:
    <em>/map</em> - выведу карты всех этажей главного корпуса и помогу найти дорогу до 4 корпуса
    <em>/timetable</em> - покажу актуальное рассписание на конкретный день
    <em>/info</em> - дам описание полезной информации о учёбе
    <em>/links_csu</em> - выведу ссылки, связанные с ЧелГУ и деятелностью его студентов
    <em>/links_it</em> - выведу полезные ссылки, помогающие в освоении it профессии
    <em>/help</em> - расскажу ещё раз про свои функции"""
    await message.answer(
        text=mess,
        parse_mode=ParseMode.HTML
        )


@dp.message(F.text, Command('map'))
async def map_csu(message: types.Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='0 этаж', callback_data='0fl')
    btn2 = types.InlineKeyboardButton(text='1 этаж', callback_data='1fl')
    btn3 = types.InlineKeyboardButton(text='2 этаж', callback_data='2fl')
    btn4 = types.InlineKeyboardButton(text='3 этаж', callback_data='3fl')
    btn5 = types.InlineKeyboardButton(text='4 этаж', callback_data='4fl')
    btn6 = types.InlineKeyboardButton(
        text='Расположение 4 корпуса',
        url='https://maps.google.com/maps?q=55.180035,61.335219&ll=55.180035,61.335219&z=16'
        )
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6)
    await message.answer(
        text='Какой <em>этаж/корпус</em> Вас интересует?',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.message(F.text, Command('timetable'))
async def timetable(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Нечетная неделя (1)', callback_data='n1')
    btn2 = types.InlineKeyboardButton(text='Четная неделя (2)', callback_data='n2')
    markup.row(btn1)
    markup.row(btn2)
    await message.answer(
        text='Выберите <em> неделю </em>',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(F.data == 'n1' or F.data == 'n2')
async def one_step(callback: types.CallbackQuery):
    if callback.data == 'n1':
        markup2 = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(text='Понедельник', callback_data='1_1d')
        btn2 = types.InlineKeyboardButton(text='Вторник', callback_data='1_2d')
        btn3 = types.InlineKeyboardButton(text='Среда', callback_data='1_3d')
        btn4 = types.InlineKeyboardButton(text='Четверг', callback_data='1_4d')
        btn5 = types.InlineKeyboardButton(text='Пятница', callback_data='1_5d')
        btn6 = types.InlineKeyboardButton(text='Суббота', callback_data='1_6d')
        markup2.row(btn1, btn2)
        markup2.row(btn3, btn4)
        markup2.row(btn5, btn6)
        await callback.message.answer(
            text='Выберите <em>день недели</em>',
            reply_markup=markup2.as_markup(),
            parse_mode='HTML'
        )
    elif callback.data == 'n2':
        markup3 = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(text='Понедельник', callback_data='2_1d')
        btn2 = types.InlineKeyboardButton(text='Вторник', callback_data='2_2d')
        btn3 = types.InlineKeyboardButton(text='Среда', callback_data='2_3d')
        btn4 = types.InlineKeyboardButton(text='Четверг', callback_data='2_4d')
        btn5 = types.InlineKeyboardButton(text='Пятница', callback_data='2_5d')
        btn6 = types.InlineKeyboardButton(text='Суббота', callback_data='2_6d')
        markup3.row(btn1, btn2)
        markup3.row(btn3, btn4)
        markup3.row(btn5, btn6)
        await callback.message.answer(
            text='Выберите <em>день недели</em>',
            reply_markup=markup3.as_markup(),
            parse_mode='HTML'
        )


@dp.message(F.text, Command('info'))
async def info(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Информация о интернет-ресурсах ЧелГУ', callback_data='csu')
    btn2 = types.InlineKeyboardButton(text='Ресурсы для программистов', callback_data='it')
    markup.row(btn1)
    markup.row(btn2)
    await message.answer(
        text='Какая <em>информация</em> Вас интересует?',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(F.data == 'csu' or F.data == 'it')
async def callback_mes(callback: types.CallbackQuery):
    if callback.data == 'csu':
        await callback.message.answer(
            text="""<b><em>Сайты, связанные с ЧелГУ</em></b>:
            <u>Мудл ЧелГУ</u> - система управления электронными образовательными курсами (здесь ты можешь\
        найти курсы от преподавателей с различных факультетов)
            <u>Мудл ИИТ</u> - здесь ты можешь найти курсы от преподавателей из ИИТ
            <u>Сайт ЧелГУ</u> - новостной сайт, где ты можешь найти информацию о ЧелГУ в целом\
        (структура, расписание и многое другое)
            <u>Научная Библиотека ЧелГУ</u> - огромный каталог электронных книг и прочих информационных ресурсов
            <u>ЦТС(ЦентрТворчестваСтудентов)</u> - здесь можно узнать о творческой внеучебной жизни вуза\
        (информация по мероприятиям, ссылки на кружки по пению, танцам и т.д.)
            <u>Профсоюзный Комитет(вк)</u> - информация для участников профсоюза (о мероприятиях,\
        льготах, как вступить и т.п.)
        
            <em>Хочешь ссылки? Жми /links_csu</em>""",
            parse_mode='HTML'
        )
    else:  # callback.data == 'it':
        await callback.message.answer(
            text="""<b><em>Общие ресурсы (независимо от языка программирования)</em></b>:
            <u>Habr</u> - сайт, созданный для публикации новостей, аналитических статей, мыслей, \
            связанных с информационными технологиями и интернетом.
            <u>GitHub</u> - крупнейший веб-сервис для хостинга IT-проектов и их совместной разработки. \
            На сайте представлен свободный исходный код, с которым вы можете ознакомиться.
            <u>Metanit</u> - сайт посвящен различным языкам и технологиям программирования, компьютерам,\
             мобильным платформам и ИТ-технологиям c различные руководства и учебные материалы, статьи и примеры
            <u>Открытый лекторий Летних школ от Яндекса</u> - более 150 лекций в онлайн-формате, общение с топовыми\
             экспертами из Яндекса, прокачка знаний по востребованным IT‑специальностям и решение сложных бизнес‑кейсов
            <u>Киберфорум</u> - форум программистов и системных администраторов, помощь в решении задач по \
            программированию, математике, физике и другим наукам, решение проблем с компьютером, операционными системами
            <u>Библиотека программиста</u> - материалы, которые научат и помогут программировать. Книги и лекции,\
             видеоуроки и советы, тесты знаний и обсуждение горячих тем
            <u>Roadmap</u> - собрание дорожных карт, руководств и другого образовательного контента, которое\
             поможет разработчикам выбрать правильный путь и направлять их обучение.
        
        <em>Заинтересовало? Жми /links_it для получения ссылок</em>""",
            parse_mode='HTML'
        )


@dp.message(F.text, Command('links_csu'))
async def csu(message: Message):
    markup = InlineKeyboardBuilder()
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
    await message.answer(
        text='Выберите <em>рессурс</em>, на который хотите перейти',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.message(F.text, Command('links_it'))
async def it(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Habr', url='https://habr.com/ru/')
    btn2 = types.InlineKeyboardButton(text='GitHub', url='https://github.com/')
    btn3 = types.InlineKeyboardButton(text='Metanit', url='https://metanit.com/')
    btn4 = types.InlineKeyboardButton(text='Открытый лекторий Летних школ от Яндекса',
                                      url='https://yandex.ru/yaintern/schools/open-lectures')
    btn5 = types.InlineKeyboardButton(text='Киберфорум', url='https://www.cyberforum.ru/')
    btn6 = types.InlineKeyboardButton(text='Библиотека программиста', url='https://proglib.io/')
    btn7 = types.InlineKeyboardButton(text='Roadmap', url='https://roadmap.sh/')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5, btn7)
    markup.row(btn6)
    await message.answer(
        text='Выберите <em>рессурс</em>, на который хотите перейти',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.message(F.text, Command('spam'))
async def can_spam(message: Message, state: FSMContext):
    user_role = await check_role(message.from_user.id)
    if user_role == 'ADMIN':
        await message.answer('Введите текст рассылки')
        await state.set_state(ProfileStatesGroup.input_text)
    else:
        await message.answer('У вас нет прав администратора для этой функции')


@dp.message(F.text, ProfileStatesGroup.input_text)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('Действие отменено')
        await state.clear()
    else:
        spam_base = await output_all_id()
        for num in range(len(spam_base)):
            await bot.send_message(chat_id=spam_base[num][0], text=message.text)
            await message.answer('Рассылка завершена!')
            await state.clear()


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
