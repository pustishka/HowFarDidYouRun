import asyncio
import menu
from database import insert_into_base, get_stats
from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardRemove
from haversine import haversine

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'  # Token from @BotFather
bot = Bot(TOKEN)
dp = Dispatcher(bot)

players = {}  # hashtable for accumulating members of bot
race_done_mark = False  # Mark using for access to second step (generate leader_board)
finished_players = {'Kat': [384713574, 150.0], 'ed': [384713574, 3500.0]}  # hashtable for players whom done first step
# fake data for imitate 3 and more players for display leaderboard


# main start handler for command in bot /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_full_name = message.from_user.full_name  # get full_name of user from message
    await message.answer(f'Hello, {user_full_name}', reply_markup=menu.mainMenu)  # bot sent 'Hello' to user


# handler for display top 10 players
@dp.message_handler(lambda message: message.text == '🏆 Top 10 🏆')
async def stats_handler(message: types.Message):
    data = get_stats().fetchall()[:10]
    sorted_data = sorted(data, key=lambda x: x[4], reverse=True)
    for pl in sorted_data:
        await message.answer(f'{pl[1]} | Mileage: {pl[2]} | Races: {pl[3]} | Rate: {pl[4]}')


# main handler for set location and make all calculation
@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def handle_location(message: types.Message):
    username = message.from_user.username
    full_name = message.from_user.full_name
    start_latitude = message.location.latitude  # get latitude and longitude from message location
    start_longitude = message.location.longitude

    # func for generate leaderboard and sent to every user in finished players
    async def generate_leaderboard(distance):
        global finished_players
        ids = message.from_user.id  # get id of user from message
        finished_players[username] = [ids, distance]  # contain key=user, value=id and distance in list
        # save data in database 'stats'
        insert_into_base(username, distance)
        del players[username]  # delete player if player now in finished hashtable
        leader_board = ''  # string of leader_board
        if 3 <= len(finished_players) <= 5:  # condition for limit players count in leader_board (3-5)
            await message.answer(f'Leaderboard:')  # sent to user title of leader_board
            for idx, pl in enumerate(
                    dict(sorted(finished_players.items(), key=lambda x: x[1][1], reverse=True)), start=1):
                # enumerate count and username to leader_board in decreasing order
                leader_board += f'{idx}. {pl} - {finished_players[pl][1]} meters\n'
            for ids in finished_players.values():
                await bot.send_message(chat_id=ids[0],
                                       text=leader_board)  # sent leader_board to every champion
            finished_players = {}  # clear for next race

    # function for limit timing of race
    async def set_timeouts():
        secs = 300
        timeout = secs / 5
        while secs > 0:
            await message.answer(f'Left {secs} second until the end of the race!')
            await asyncio.sleep(timeout)
            secs -= int(timeout)

    # func for calculation difference of lat and long and convert to meters
    async def calculate_distance():
        global race_done_mark
        if username in players and race_done_mark:  # condition for access to second step calc distance
            finish_latitude = message.location.latitude
            finish_longitude = message.location.longitude
            distance = round(haversine(players[username], (finish_latitude, finish_longitude)),
                             3) * 1000  # haversine can calculate distance
            await message.answer(f'{full_name}, you have walked {distance} meters',
                                 reply_markup=menu.mainMenu)  # sent to user passed distance
            await generate_leaderboard(distance)  # call function
        else:
            players[username] = [start_latitude, start_longitude]  # add player to all pool
            await message.answer(text='The race has begun!',
                                 reply_markup=ReplyKeyboardRemove())  # close button until race not finished
            await set_timeouts()
            race_done_mark = True
            await message.answer(f'The race is over')  # bot sent 'Race over' to user
            await message.answer(
                f'Click on the "Find out the result" button within 30 seconds or disqualification...',
                reply_markup=menu.mainMenuFinish)  # Forces user to set second point of his location

    await calculate_distance()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
