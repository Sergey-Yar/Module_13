from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
button_cal = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
kb_start.row(button_cal, button_info)
kb_start.row(button_buy)

kb_cal = InlineKeyboardMarkup()
button_norma = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_cal.add(button_norma, button_formula)

kb_buy = InlineKeyboardMarkup()
button_buy_1 = InlineKeyboardButton(text='Каша 1', callback_data='product_buying')
button_buy_2 = InlineKeyboardButton(text='Каша 2', callback_data='product_buying')
button_buy_3 = InlineKeyboardButton(text='Каша 3', callback_data='product_buying')
button_buy_4 = InlineKeyboardButton(text='Каша 4', callback_data='product_buying')
kb_buy.add(button_buy_1, button_buy_2, button_buy_3, button_buy_4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb_start)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_call = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {result_call}')
    await state.finish()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_cal)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 х вес в кг) + (6,25 х рост в см) – (5 х возраст в г) – 161')
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in crud_functions.get_all_product():
        await message.answer(f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}')
        with open(f'img/{i[0]}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_buy)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    # crud_functions.get_all_product()
    executor.start_polling(dp, skip_updates=True)