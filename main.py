import os
import json
import gspread
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from oauth2client.service_account import ServiceAccountCredentials

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из Railway
TOKEN = os.getenv("TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(GOOGLE_SHEETS_KEY)  # Преобразуем строку в JSON
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
menu_buttons = [
    [types.KeyboardButton("Число судьбы"), types.KeyboardButton("Число имени")],
    [types.KeyboardButton("Число дня"), types.KeyboardButton("Совместимость")],
    [types.KeyboardButton("Ежедневный прогноз"), types.KeyboardButton("О боте")],
]
keyboard = types.ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)

# Команда /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот по нумерологии. Выбери нужный пункт:", reply_markup=keyboard)

# Команда "О боте"
@dp.message_handler(lambda message: message.text == "О боте")
async def about_bot(message: types.Message):
    await message.answer("Я бот, который помогает с расчетами в нумерологии. Выбери нужную функцию в меню.")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
