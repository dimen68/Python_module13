# Задача "Меньше текста, больше кликов"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncio

api = '*************************************'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
kb_start.add(KeyboardButton('Рассчитать калории'))
kb_start.add(KeyboardButton('Информация'))


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=kb_start)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(
        'Информация о боте: Это бот, который помогает рассчитать количество необходимых калорий на основе данных пользователя',
        reply_markup=kb_start)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Рассчитать калории', 'Colories', 'Калории', 'калори'])
async def set_age(message):
    await message.answer('Введите свой возраст: ')
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
    colories = 5 * int(data['age']) + 6.25 * int(data['growth']) + 10 * int(data['weight'])
    await message.answer(f'Ваша норма калорий: {colories}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
