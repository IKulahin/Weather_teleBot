from config import API_WEATHER, TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import asyncio
import aiohttp
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class MyState(StatesGroup):
    """Class for state"""
    weather = State()


bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def starting(message: types.Message):
    """Starting the bot(default Telegram-bot function)"""
    await message.answer('Привіт! Я розкажу вам прогноз погоди за наданим містом! Напишіть /weather для початку')


@dp.message(MyState.weather)
async def get_weather(message: types.Message, state: FSMContext):
    """Sending request, and getting data from website"""
    await state.clear()
    async with aiohttp.ClientSession() as session1:
        url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={API_WEATHER}'
        async with session1.get(url1) as r1:
            data1 = await r1.json()
            city_name = data1[0]['name']
    async with aiohttp.ClientSession() as session2:
        url2 = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_WEATHER}&units=metric'
        async with session2.get(url2) as r2:
            data2 = await r2.json()
            temperature = data2['main']['temp']
            feels_like = data2['main']['feels_like']
            wind_speed = data2['wind']['speed']
        result_message = f'Ось погода за наданим містом:\n' \
                         f'\n' \
                         f'Дата і час: {datetime.now()}\n' \
                         f'\n' \
                         f'Температура: {temperature}⁰C\n' \
                         f'Відчувається як: {feels_like}⁰C\n' \
                         f'\n' \
                         f'Швидкість вітру: {wind_speed}м/с'
        await message.answer(result_message)


@dp.message(Command('weather'))
async def show_weather(message: types.Message, state: FSMContext):
    """Calling the get_weather function"""
    await state.set_state(MyState.weather)
    await message.answer('Введіть назву міста:')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
