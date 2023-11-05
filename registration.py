# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State

#
# # storage = MemoryStorage()
# dp = Dispatcher(bot,
#                 storage=storage)


# class ProfileStatesGroup(StatesGroup):
#     group = State()  # статус ожидания на group


# @dp.message_handler(commands=['start'])
# async def cmd_start(message: types.Message) -> None:
#     await message.answer('Welcome! So as to create profile - type /create',
#                          reply_markup=get_kb())
#
#     await create_profile(user_id=message.from_user.id)
#
#
# def get_kb() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)
#     kb.add(KeyboardButton('/create'))
#
#     return kb
#
#
# @dp.message_handler(commands=['create'])
# async def cmd_create(message: types.Message) -> None:
#     await message.reply("Для начала раоты даате сначала уточним вашу группу. Введите ее в формате 'ПИ'",
#                         reply_markup=get_cancel_kb())
#     await ProfileStatesGroup.group.set()  # установили состояние ожидания группы
#
#
# def get_cancel_kb() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)
#     kb.add(KeyboardButton('/cancel'))
#
#     return kb
#
#
# @dp.message_handler(commands=['cancel'], state='*')  # * - любое состояние
# async def cmd_cancel(message: types.Message, state: FSMContext):
#     if state is None:
#         return
#
#     await state.finish()
#     await message.reply('Вы прервали ввод группы',
#                         reply_markup=get_kb())
#
#
# @dp.message_handler(content_types=['text'], state=ProfileStatesGroup.group)
# async def load_group(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:  # открыть локальное хранилище данных
#         data['group'] = message.text
#         await message.answer(chat_id=message.from_user.id, mes=f"Ваша группа :{data['text']}")
#
#     await message.answer('Запомню! Теперь можно продолжить')
#     await state.finish()
#
#
# @dp.message_handler(
#     lambda message: message.text != message.text.upper(),
#     state=ProfileStatesGroup.group
# )  # если сообщение не в верхнем регистре и в состоянии ожидания
# async def check_age(message: types.Message):
#     await message.reply('Введите группу в верхнем регистре (пр. ПИ)')
#
#


#

