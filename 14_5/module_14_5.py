# Задача "Регистрация покупателей"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import get_all_products, is_included, add_user

api = '**************************************'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
kb_start.add(KeyboardButton('Рассчитать'), KeyboardButton('Информация'))
kb_start.add(KeyboardButton('Регистрация'), KeyboardButton('Купить'))

kb_calories = InlineKeyboardMarkup()
kb_calories.add(
    InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
    InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
)

kb_products = InlineKeyboardMarkup()
kb_products.add(
    InlineKeyboardButton(text='Витамин А', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамин В', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамин С', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамин D', callback_data='product_buying'),
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=kb_start)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(
        'Информация о боте: Это бот, который помогает рассчитать количество необходимых калорий на основе данных пользователя',
        reply_markup=kb_start)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_calories)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    i = 1
    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        photo = f'{i}.jpg'
        i += 1
        with open(photo, 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_products)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()
    await call.message.answer('Выберите опцию:', reply_markup=kb_calories)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    colories = 5 * int(data['age']) + 6.25 * int(data['growth']) + 10 * int(data['weight']) + 5
    await message.answer(f'Ваша норма калорий {colories}')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя: ')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email: ')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст: ')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    add_user(user_data['username'], user_data['email'], user_data['age'])
    await message.answer('Регистрация прошла успешно', reply_markup=kb_start)
    await state.finish()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
