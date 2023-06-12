import time

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from main import race_done_mark

# --- Main Menu ---
if race_done_mark is False:
    btnStartGeo = KeyboardButton('🟢 Start 🟢', request_location=True)
    mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartGeo)
btnFinishGeo = KeyboardButton('🏁 Узнать результат 🏁', request_location=True)
mainMenuFinish = ReplyKeyboardMarkup(resize_keyboard=True).add(btnFinishGeo)
# hideMenu = ReplyKeyboardMarkup(resize_keyboard=True)


