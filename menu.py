from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Main Menu ---
btnStartGeo = KeyboardButton('🟢 Start 🟢', request_location=True)
btnCountDist = KeyboardButton('🏁 Узнать результат 🏁', request_location=True)
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartGeo).add(btnCountDist)
