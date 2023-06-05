import time
import logging
import menu
from aiogram import Bot, Dispatcher, executor, types

from haversine import haversine, Unit

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await message.answer(f'Привет {user_full_name}', reply_markup=menu.mainMenu)
    # await message.s
    # print(user_id)


# @dp.message_handler()
# async def bot_message(message: types.Message):
#     print(message.text)
#     # location = message.location
#     # lat = location.latitude
#     # lon = location.longitude
#     # location_str = f"latitude: {lat}, longitude: {lon}"
#     # await message.answer(location_str)
#     if message.text == '🟢Start🟢':
#         # loc = message.location
#         # lat = loc.latitude
#         # long = loc.longitude
#         # await message.answer(f'{lat}')
#         print('Поехалииии')


# @dp.message_handler(content_types=types.ContentTypes.LOCATION)
# async def get_location(message: types.Message):
#     loc = message.location
#     lat = loc.latitude
#     long = loc.longitude
#     await message.reply(f'{lat}')
coords = []
@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    coords.append((latitude, longitude))
    if len(coords)>=2:
        distance = round(haversine(coords[-2], coords[-1]), 3) * 1000
        print(coords, str(distance) + ' метров')
        await message.reply(f'вы прошли {distance} метра')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
