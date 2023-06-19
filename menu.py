from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Main Menu ---
btnStartGeo = KeyboardButton('🟢 Start 🟢', request_location=True)   # create start button
btnStats = KeyboardButton('🏆 Топ 10 🏆')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartGeo).add(btnStats)   # add to markup
btnFinishGeo = KeyboardButton('🏁 Узнать результат 🏁', request_location=True)   # create button for second location
mainMenuFinish = ReplyKeyboardMarkup(resize_keyboard=True).add(btnFinishGeo)  # add finish button to changing markup