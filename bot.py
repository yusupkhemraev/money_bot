import requests
import logging
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from bs4 import BeautifulSoup as soup




try:
    url = 'https://finca.tj/'

    headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.4.143 Yowser/2.5 Safari/537.36'}
    full_page = requests.get(url , headers = headers)
    html_page = soup(full_page.content, 'html.parser')

    rub = html_page.findAll('td', {})[2].text
    usd = html_page.findAll('td', {})[6].text
    eur = html_page.findAll('td', {})[10].text

    rub = float(rub)
    usd = round(float(usd), 2)
    eur = float(eur)

except requests.exceptions.ConnectionError:
    requests.status_code = "Connection refused"
    rub = 'В соединени отказано!'
    usd = 'В соединени отказано!'
    eur = 'В соединени отказано!'

TOKEN = '1925943055:AAHbhbEc17hcrhYIoBRb66N92Zu0B1iAc2Y'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Курс рубля ₽', 'Курс доллара 💵', 'Курс евро 💶', 'Бросить кубик']
    keyboard.add(*buttons)

    await message.answer(f'Привет  {message.from_user.first_name} !\nЗдесь ты можешь узнать курс \nРубля ₽\nДоллара 💲\nЕвро 💶 !\nЕщё этот бот может бросить кубик 🎲', reply_markup=keyboard)


@dp.message_handler(Text(equals='Бросить кубик')) # Можно и так lambda message: message.text == "Послать"
async def process_dice_command(message: types.Message):
    await message.answer_dice(emoji="🎲")

@dp.message_handler(Text(equals='Курс рубля ₽'))
async def process_rub_command(message: types.Message):
    await message.answer(f'1 000 российский рубль (RUB) равняется {rub * 1000} таджикский сомони (TJS)')

@dp.message_handler(Text(equals='Курс доллара 💵'))
async def process_usd_command(message: types.Message):
    await message.answer(f'100 доллар США (USD) равняется {usd * 100} таджикский сомони (TJS)')

@dp.message_handler(Text(equals='Курс евро 💶'))
async def process_eur_command(message: types.Message):
    await message.answer(f'100 евро (EUR) равняется {eur * 100} таджикский сомони (TJS)')


if __name__ == '__main__':
    executor.start_polling(dp)