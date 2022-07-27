import asyncio
import json
import time
from os import getenv
from sys import exit

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import hbold, hide_link

from main import collect_data

API_TOKEN = getenv("API_TOKEN")
if not API_TOKEN:
    exit("Error: no token provided")
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
flag = True


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Get miners', 'Stop', 'Get CSV', 'Get JSON']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    chat_id = message.chat.id
    await message.answer("Hi!\nI'm MainerBot!\nPowered by aiogram.")
    await message.answer('Select categories', reply_markup=keyboard)


@dp.message_handler(Text(equals='Stop'))
async def get_mainers(message: types.Message):
    await message.answer('<b>Bot</b> has been stopped')
    await exit()


@dp.message_handler(Text(equals='Get CSV'))
async def get_mainers(message: types.Message):
    await message.answer('Your CSV file ready: ')
    # await bot.send_document(message.chat.id, open(result.csv, 'rb'))


@dp.message_handler(Text(equals='Get JSON'))
async def get_mainers(message: types.Message):
    await message.answer('Your JSON file ready: ')


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


@dp.message_handler(Text(equals='Get miners'))
async def get_mainers(message: types.Message):
    await message.answer('Please waiting...')

    collect_data()

    with open('result.json') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hide_link(item.get("url_miner"))}' \
               f'Name miner: <a href="{item.get("url_miner")}">{hbold(item.get("miner_name"))}</a>\n' \
               f'Network: {hbold(item.get("network"))}\n' \
               f'Contract: {hbold(item.get("contract"))}\n' \
               f'Name Coin: {hbold(item.get("name_coin"))}\n ' \
               f'Symbol: {hbold(item.get("symbol"))}\n ' \
               f'Rate: {hbold(item.get("rate"))}\n ' \
               f'Fees: {hbold(item.get("fees"))}\n ' \
               f'Sell Fees: {hbold(item.get("sellFees"))}\n ' \
               f'Address: {hbold(item.get("address"))}\n ' \
               f'Telegram: {hbold(item.get("link_telegram"))}\n ' \
               f'Price: {hbold(item.get("price"))}\n ' \
               f'Balance now: {hbold(item.get("balance"))}\n ' \
               f'Balance for 7 days: {hbold(item.get("balance7d"))}\n ' \
               f'Balance for 24 days: {hbold(item.get("balance24"))}\n ' \
               f'Date create: {hbold(item.get("created_date"))}\n '

        await message.answer(card)

        await asyncio.sleep(5)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
