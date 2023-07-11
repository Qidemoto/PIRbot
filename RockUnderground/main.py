import aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.helper import Helper, HelperMode, ListItem

#Token (индивидуальны номер) бота
BOT_TOKEN = '6061317414:AAE-IoOn0DIgbViciP2DM4JFiEkA-oJAXsU'    

#Инициализация бота
rock = Bot(BOT_TOKEN,parse_mode="HTML")

#Инициализация обработчика запросов
dp = Dispatcher(rock, storage = MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

#Запуск бота
if __name__=="__main__":
    from handlers import dp
    executor.start_polling(dp)