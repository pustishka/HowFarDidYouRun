from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Main Menu ---
btnStartGeo = KeyboardButton('Начать гонку🟢')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartGeo)