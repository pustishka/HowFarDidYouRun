import time

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from main import race_done_mark

# --- Main Menu ---
btnStartGeo = KeyboardButton('🟢 Start 🟢', request_location=True)   # create start button
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartGeo)   # add to markup
btnFinishGeo = KeyboardButton('🏁 Узнать результат 🏁', request_location=True)   # create button for second point of location
mainMenuFinish = ReplyKeyboardMarkup(resize_keyboard=True).add(btnFinishGeo)  # add finishbutton to changing markup


