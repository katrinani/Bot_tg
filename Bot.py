import sqlite3 as sq
import aiogram
import asyncio
import json

from db_map import db_start, create_profile, edit_profile, check_group_of_student, check_role, output_all_id

from aiogram import F, Bot, types, Dispatcher
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode

with open('data.json', 'r') as json_file:
    mes_data = json.load(json_file)

bot = Bot(token='6401248215:AAHb1ieiU5malll9Hga3-eqTsQgwLCZjXow')
dp = Dispatcher(storage=MemoryStorage())

group_name = ['ПРИ101', 'ПРИ102', 'ПРИ103', 'БИ101', 'ПИ101']
callback_map = ['0fl', '1fl', '2fl', '3fl', '4fl']
callback_mater = ['mat1', 'mat2', 'mat3', 'mat4', 'mat5', 'mat6', 'mat7', 'mat8', 'mat9', 'mat10',]
callback_timetable = ['1_1d', '1_2d', '1_3d', '1_4d', '1_5d', '1_6d', '2_1d', '2_2d', '2_3d', '2_4d', '2_5d', '2_6d']
callback_info = ['csu', 'it']
callback_week = ['n1', 'n2']
callback_questions = ['que1', 'que2', 'que3', 'que4', 'que5', 'que6', 'que7', 'que8']


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
    await message.answer("Welcome! For the beginning let's create your profile for functions\
like timetable and mailing list. Push /create",
                         reply_markup=get_kb())
    await create_profile(user_id=message.from_user.id)


@dp.message(F.text, Command('create'))
async def cmd_create(message: Message, state: FSMContext):
    await message.reply(
        text="To start work let's clarify your group and \
group number (For example: 'ПИ101')\nIf you want to finish creating of profile push cancel",
        reply_markup=get_cancel_kb())
    await state.set_state(ProfileStatesGroup.choosing_group)  # установили состояние ожидания группы


@dp.message(F.text, Command(commands='cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    if state is None:
        return
    await state.clear()
    await message.answer(text='Action canceled', reply_markup=get_kb())


@dp.message(
    F.text.in_(group_name),
    ProfileStatesGroup.choosing_group
)  # состояние ожидания группы и текст из списка
async def load_group(message: Message, state: FSMContext) -> None:
    user_group = message.text
    await message.reply(text=f"Your group : {user_group}\nNow you can continue!\
\nPush /help to view bot capabilities")
    await edit_profile(user_group, user_id=message.from_user.id)
    await state.clear()


@dp.message(StateFilter('ProfileStatesGroup:choosing_group'))  # то же состояние, но на вход пришли другие данные
async def check_group(message: Message):
    await message.reply("Such group doesn't exist. Try to enter group and number in uppercase again (example: 'ПИ101')")


# ----------------------------------------------------------------------


@dp.callback_query(F.data.in_(callback_map))
async def callback_message(callback: types.CallbackQuery):
    first_char = str(callback.data)[0]  # 1 число поступающего колбэка
    file = FSInputFile(f'floor/Этаж {first_char}.png')
    await callback.message.answer(text=f'{first_char} flour')  # вызов 0 этажа пока не возможен, jpg формат
    await callback.message.answer_photo(file)


@dp.callback_query(F.data.in_(callback_timetable))
async def step(callback: types.CallbackQuery):
    user_group = await check_group_of_student(tg_user_id)
    first_char = str(callback.data)[0:3]
    file = FSInputFile(f'{user_group}/day{first_char}.jpg')  # вместо папки будет подключаться информаци о группе из бд
    await callback.message.answer_photo(file)


@dp.message(F.text, Command('help'))
async def help_ph(message: types.Message):
    await message.answer(
        text=mes_data['help'],
        parse_mode=ParseMode.HTML
        )


@dp.message(F.text, Command('map'))
async def map_csu(message: types.Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='0 flour', callback_data='0fl')
    btn2 = types.InlineKeyboardButton(text='1 flour', callback_data='1fl')
    btn3 = types.InlineKeyboardButton(text='2 flour', callback_data='2fl')
    btn4 = types.InlineKeyboardButton(text='3 flour', callback_data='3fl')
    btn5 = types.InlineKeyboardButton(text='4 flour', callback_data='4fl')
    btn6 = types.InlineKeyboardButton(
        text='location of building 4',
        url='https://maps.google.com/maps?q=55.180035,61.335219&ll=55.180035,61.335219&z=16'
        )
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6)
    await message.answer(
        text='Which <em>flour/</em>building are you interested in?',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.message(F.text, Command('timetable'))
async def timetable(message: Message):
    group = await check_group_of_student(message.from_user.id)
    if group == '':
        await message.answer('To access this feature, first go through the regime! For this go through /create')
    else:
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(text='Odd week (1)', callback_data='n1')
        btn2 = types.InlineKeyboardButton(text='Even week (2)', callback_data='n2')
        markup.row(btn1)
        markup.row(btn2)
        await message.answer(
            text='Choose <em> a week </em>',
            reply_markup=markup.as_markup(),
            parse_mode=ParseMode.HTML
        )
        global tg_user_id
        tg_user_id = str(message.from_user.id)


@dp.callback_query(F.data.in_(callback_week))
async def one_step(callback: types.CallbackQuery):
    if callback.data == 'n1':
        markup2 = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(text='Mondey', callback_data='1_1d')
        btn2 = types.InlineKeyboardButton(text='Tuesday', callback_data='1_2d')
        btn3 = types.InlineKeyboardButton(text='Wednesday', callback_data='1_3d')
        btn4 = types.InlineKeyboardButton(text='Thursday', callback_data='1_4d')
        btn5 = types.InlineKeyboardButton(text='Friday', callback_data='1_5d')
        btn6 = types.InlineKeyboardButton(text='Saturday', callback_data='1_6d')
        markup2.row(btn1, btn2)
        markup2.row(btn3, btn4)
        markup2.row(btn5, btn6)
        await callback.message.answer(
            text='Choose <em>day of the week</em>',
            reply_markup=markup2.as_markup(),
            parse_mode='HTML'
        )
    elif callback.data == 'n2':
        markup3 = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(text='Monday', callback_data='2_1d')
        btn2 = types.InlineKeyboardButton(text='Tuesday', callback_data='2_2d')
        btn3 = types.InlineKeyboardButton(text='Wednesday', callback_data='2_3d')
        btn4 = types.InlineKeyboardButton(text='Thursday', callback_data='2_4d')
        btn5 = types.InlineKeyboardButton(text='Friday', callback_data='2_5d')
        btn6 = types.InlineKeyboardButton(text='Saturday', callback_data='2_6d')
        markup3.row(btn1, btn2)
        markup3.row(btn3, btn4)
        markup3.row(btn5, btn6)
        await callback.message.answer(
            text='Choose <em>the day of the week</em>',
            reply_markup=markup3.as_markup(),
            parse_mode='HTML'
        )


@dp.message(F.text, Command('info'))
async def info(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(
        text='Information about internet-sources CSU',
        callback_data='csu'
    )
    btn2 = types.InlineKeyboardButton(
        text='Sources for programmers',
        callback_data='it'
    )
    markup.row(btn1)
    markup.row(btn2)
    await message.answer(
        text='Which <em>information</em> are you interested in?',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(F.data.in_(callback_info))
async def callback_mes(callback: types.CallbackQuery):
    if callback.data == 'csu':
        await callback.message.answer(
            text=mes_data['csu'],
            parse_mode='HTML'
        )
    elif callback.data == 'it':
        await callback.message.answer(
            text=mes_data['it'],
            parse_mode='HTML'
        )


@dp.message(F.text, Command('links_csu'))
async def csu(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Moodle CSU', url='https://moodle.uio.csu.ru/')
    btn2 = types.InlineKeyboardButton(text='Moodle IIT', url='https://eu.iit.csu.ru')
    btn3 = types.InlineKeyboardButton(text='CSU site', url='https://www.csu.ru/')
    btn4 = types.InlineKeyboardButton(text='Scientific library CSU', url='https://library.csu.ru/ru/')
    btn5 = types.InlineKeyboardButton(text='SCC (Student Creativity Center)', url='https://ctsofficial.ru/')
    btn6 = types.InlineKeyboardButton(text='Trade union committee (vk)', url='https://vk.com/profcomcsu')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5)
    markup.row(btn6)
    await message.answer(
        text='Choose <em>source</em>, to which you want to switch',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.message(F.text, Command('links_it'))
async def it(message: Message):
    markup = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text='Habr', url='https://habr.com/ru/')
    btn2 = types.InlineKeyboardButton(text='GitHub', url='https://github.com/')
    btn3 = types.InlineKeyboardButton(text='Metanit', url='https://metanit.com/')
    btn4 = types.InlineKeyboardButton(text='Summer Schools Open Lecture Hall from Yandex',
                                      url='https://yandex.ru/yaintern/schools/open-lectures')
    btn5 = types.InlineKeyboardButton(text='Cyberforum', url='https://www.cyberforum.ru/')
    btn6 = types.InlineKeyboardButton(text='Programmer library, url='https://proglib.io/')
    btn7 = types.InlineKeyboardButton(text='Roadmap', url='https://roadmap.sh/')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4)
    markup.row(btn5, btn7)
    markup.row(btn6)
    await message.answer(
        text='Choose <em>source</em>, to which you want to switch',
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


# команда, генерирующая сначала вопросы, а потом ответы на них
@dp.message(F.text, Command('questions'))
async def questions(message: Message):
    markup = InlineKeyboardBuilder()
    for num in range(1, 9):
        btn = types.InlineKeyboardButton(text=f'№{num}', callback_data=f'que{num}')
        markup.add(btn)
    await message.answer(
        text=mes_data['que'],
        reply_markup=markup.as_markup(),
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(F.data.in_(callback_questions))
async def answer(callback: types.CallbackQuery):
    for num in range(1, 9):
        if callback.data == f'que{num}':
            await callback.message.answer(
                text=mes_data[f'answ{num}'],
                parse_mode=ParseMode.HTML
            )


# функция, высылающая спам рассылки от админа
@dp.message(F.text, Command('spam'))
async def can_spam(message: Message, state: FSMContext):
    user_role = await check_role(message.from_user.id)
    if user_role == 'ADMIN':
        await message.answer('Enter text for mailing')
        await state.set_state(ProfileStatesGroup.input_text)
    else:
        await message.answer('You do not have administrator rights for this feature or you are not registered')


@dp.message(F.text, ProfileStatesGroup.input_text)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'назад':
        await message.answer('Action canceled')
        await state.clear()
    else:
        spam_base = await output_all_id()
        for num in range(len(spam_base)):
            await bot.send_message(chat_id=spam_base[num][0], text=message.text)
            await message.answer('Emailing is finished!')
            await state.clear()


@dp.message(F.text, Command('materials'))
async def start_materials(message: Message):
    markup = InlineKeyboardBuilder()
    for num in range(1, 11):
        btn = types.InlineKeyboardButton(text=f'№{num}', callback_data=f'mat{num}')
        markup.add(btn)
    await message.answer(
        text=mes_data['materials'],
        parse_mode=ParseMode.HTML,
        reply_markup=markup.as_markup()
    )


@dp.callback_query(F.data.in_(callback_mater))
async def answer(callback: types.CallbackQuery):

    if callback.data == 'mat1':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Muller’s English-Russian Dictionary',
            url='https://gufo.me/dict/enru_muller')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Duolingo - The world’s best way to learn languages',
            url='https://www.duolingo.com/')
        markup.row(btn2)
        btn3 = types.InlineKeyboardButton(
            text='Free English Grammar Lessons and Tests',
            url='https://www.grammar-monster.com/')
        markup.row(btn3)
        await callback.message.answer(
            text='Materials for English',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat2':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Fundamentals of discrete mathematics',
            url='https://habr.com/ru/companies/otus/articles/529600/')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Discrete mathematics. Course of lectures',
            url='https://siblec.ru/informatika-i-vychislitelnaya-tekhnika/diskretnaya-matematika?ysclid=lp87bv0d2p745216383')
        markup.row(btn2)
        await callback.message.answer(
            text='Materials for Discrete Mathematics',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat3':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Programmer school',
            url='https://acmp.ru/?ysclid=lp87fqd34f765284201')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Main page in ulearn.me',
            url='https://ulearn.me/')
        markup.row(btn2)
        await callback.message.answer(
            text='Materials for Computer Science and Programming',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat4':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Arzamas',
            url='https://arzamas.academy/?ysclid=lp87k0ru38913824207')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Arzamas - YouTube',
            url='https://www.youtube.com/channel/UCVgvnGSFU41kIhEc09aztEg')
        markup.row(btn2)
        await callback.message.answer(
            text='МатериалыMaterials for Russian History',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat5':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Linear algebra and analytic geometry, YouTube',
            url='https://www.youtube.com/playlist?list=PLaX3n04-uUZoTu4DcD2Eqgq-h5wimh_uT')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Analytical geometry for «teapots»',
            url='https://mathter.pro/angem/index.html')
        markup.row(btn2)
        await callback.message.answer(
            text='Materials for Linear algebra and analytic geometry',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat6':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='N Eliseeva - YouTube',
            url='https://www.youtube.com/@NEliseeva/featured')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Advanced mathematics for part-time students and not only',
            url='http://www.mathprofi.ru/')
        markup.row(btn2)
        await callback.message.answer(
            text='Materials for Mathematical Analysis',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat7' or callback.data == 'mat8':
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(
            text='Link to bot',
            url='https://t.me/Trezz_bot'
        ))
        await callback.message.answer(
            text='Bot of our colleagues',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat9':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Examples of bibliographic descriptions',
            url='https://library.csu.ru//media/files/i-culture/primery_new-gost-2018.pdf')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='bibliographic description',
            url='https://library.csu.ru//media/files/i-culture/gosty.pdf')
        markup.row(btn2)
        await callback.message.answer(
            text='Materials for Modern Information Retrieval and Processing Technologies',
            reply_markup=markup.as_markup()
        )

    elif callback.data == 'mat10':
        markup = InlineKeyboardBuilder()
        btn1 = types.InlineKeyboardButton(
            text='Wikipedia - a free encyclopedia',
            url='https://ru.wikipedia.org/wiki/Заглавная_страница')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton(
            text='Summary of lectures on mechanics',
            url='https://teachmen.csu.ru/methods/konspect_mech.pdf')
        markup.row(btn2)
        btn3 = types.InlineKeyboardButton(
            text='Ogurtsov A.N. Physics for students. Part 1. Mechanics',
            url='https://smindolin.ucoz.ru/Lectures/TTP_21_TTP_22/1103880_4A1DC_ogurcov_a_n_fizika_dlya_studentov_ch.pdf')
        markup.row(btn3)
        await callback.message.answer(
            text='Materials for physics',
            reply_markup=markup.as_markup()
        )


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
