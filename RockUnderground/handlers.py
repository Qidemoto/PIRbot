import asyncio
from cgitb import text
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.types.callback_query import CallbackQuery
from main import rock, dp
import time
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,MessageToDeleteNotFound)
from keyboards import main_menu, exitor_menu, work_menu, group_menu
from aiogram.types import Message, message, user
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from contextlib import suppress
from aiogram import Dispatcher
import requests
from bs4 import BeautifulSoup
import re

# База данных для анализа
database = {
    'одежда': {
        'единственное': ['платье', 'рубашка', 'брюки', 'юбка', 'шапка', 'пальто', 'пиджак', 'свитер', 'футболка', 'ботинок', 'штаны', 'куртка', 'жилет', 'жилетка', 'джинсы', 'кед', 'галстук', 'майка', 'кофта', 'комбинезон', 'туфля', 'кроссовок', 'блуза', 'плащ', 'косуха', 'корсет', 'носок', 'сапог', 'шорты', 'бриджи'],
        'множественное': ['платья', 'рубашки', 'брюки', 'юбки', 'шапки', 'пальто', 'пиджаки', 'свитера', 'футболки', 'ботинки', 'штаны', 'куртки', 'жилеты', 'жилетки', 'джинсы', 'кеды', 'галстуки', 'майки', 'кофты', 'комбинезоны', 'туфли', 'кроссовки', 'блузы', 'плащи', 'косухи', 'корсеты', 'носки', 'сапоги', 'шорты', 'бриджи']
    },
    'прически': {
        'единственное': ['коса', 'хвост', 'пучок', 'завиток', 'кудряшка', 'прическа', 'локон', 'приподнятые волосы', 'пучок на затылке', 'косичка', 'хвостик', 'длинные волосы', 'зачесанные назад волосы', 'пышно-уложенные волосы', 'начес', 'начёс', 'ирокез', 'выбритый висок', 'распущенные волосы', 'прядь', 'челка', 'чёлка', 'укладка', 'короткие волосы', 'взъерошенные волосы'],
        'множественное': ['косы', 'хвосты', 'пучки', 'завитки', 'кудряшки', 'прически', 'локоны', 'приподнятые волосы', 'пучки на затылке', 'косички', 'хвостики', 'длинные волосы', 'зачесанные назад волосы ', 'пышно-уложенные волосы ', 'начесы', 'начёсы', 'ирокезы', 'выбритые виски', ' распущенные волосы', 'пряди', 'челки', 'чёлки', 'укладки', 'короткие волосы', 'взъерошенные волосы']
    },
    'украшения': {
        'единственное': ['браслет', 'кольцо', 'подвеска', 'зажим для галстука', 'запонка', 'брошь', 'цепочка', 'часы', 'пирсинг', 'мужской браслет', 'очки', 'солнцезащитные очки', 'очки-авиаторы', 'имиджевые очки', 'очки с диоптриями', 'золотой браслет', 'серебряный браслет', 'золотые часы', 'серебряные часы', 'кожаный браслет', 'ремень', 'кожаный ремень', 'тонкий ремень', 'толстый ремень', 'ремень с большой пряжкой', 'цепь', 'цепочка', 'золотая цепь', 'серебряная цепь', 'золотая цепочка', 'золотая цепь', 'тонкая цепь', 'тонкая цепочка', 'толстая цепь', 'толстая цепочка', 'фенечка', 'крест', 'медальон', 'кулон', 'галстук', 'бабочка', 'шип', 'клепка', 'заклепка', 'клёпка', 'заклёпка', 'чокер', 'бусы', 'бандажная лента', 'повязка', 'золотое кольцо', 'серебряное кольцо', 'перстень', 'серебряный перстень', 'золотой перстень', 'серьга', 'золотая серьга', 'серебряная серьга', 'сережка', 'золотая сережка', 'серебряная сережка', 'серёжка', 'золотая серёжка', 'серебряная серёжка', 'золотая подвеска', 'серебряная подвеска', 'золотой крест', 'серебряный крест', 'сережка-цепь', 'серебряная сережка-цепь', 'золотая сережка-цепь', 'серёжка-цепь', 'серебряная серёжка-цепь', 'золотая серёжка-цепь', 'шарф', 'ободок', 'резинка', 'бант', 'заколка', 'перчатка', 'перчатка с открытыми пальцами', 'кожаная перчатка', 'кожаная перчатка с открытыми пальцами', 'ожерелье', 'жемчужное ожерелье', 'ремень с металлической пряжкой', 'ремешок', 'кожаный ремешок', 'ремешок с пряжкой', 'ремешок с металлической пряжкой', 'металлическая заклепка', 'металлическая заклёпка', 'гетры', 'гольфы', 'кепка', 'бандана', 'платок', 'косынка', 'узкие очки', 'узкие солнцезащитные очки', 'шапка', 'вязаная шапка', 'тонкая шапка', 'берет', 'беретка', 'кафф', 'клатч', 'бананка', 'поясная сумка', 'сумка', 'почтальонка', 'рюкзак', 'портфель', 'шляпа', 'шляпка', 'пояс', 'булавка', 'чулок', 'подтяжка', 'палантин', 'массивная цепь', 'высокая перчатка', 'парео', 'панамка', 'бейсболка', 'колье', 'клипса', 'веер', 'трость', 'тросточка', 'зонт', 'зонтик', 'портмоне', 'кошелек', 'кошелёк', 'обруч', 'зажим', 'брелок', 'головной убор', 'жабо', 'пуговица', 'пуговка', 'молния', 'замок', 'аксессуар', 'украшение', 'бижутерия', 'ювелирное изделие'],
        'множественное': ['браслеты', 'кольца', 'подвески', 'зажимы для галстука', 'запонки', 'броши', 'цепочки', 'часы', 'пирсинги', 'мужские браслеты', 'очки', 'солнцезащитные очки', 'очки-авиаторы', 'имиджевые очки', 'очки с диоптриями', 'золотые браслеты', 'серебряные браслеты', 'золотые часы', 'серебряные часы', 'кожаные браслеты', 'ремни', 'кожаные ремни', 'тонкие ремни', 'толстые ремни', 'ремни с большими пряжками', 'цепи', 'цепочки', 'золотые цепи', 'серебряные цепи', 'золотые цепочки', 'золотые цепи', 'тонкие цепи', 'тонкие цепочки', 'толстые цепи', 'толстые цепочки', 'фенечки', 'кресты', 'медальоны', 'кулоны', 'галстуки', 'бабочки', 'шипы', 'клепки', 'заклепки', 'клёпки', 'заклёпки', 'чокеры', 'бусы', 'бандажные ленты', 'повязки', 'золотые кольца', 'серебряные кольца', 'перстни', 'серебряные перстни', 'золотые перстни', 'серьги', 'золотые серьги', 'серебряные серьги', 'сережки', 'золотые сережки', 'серебряные сережки', 'серёжки', 'золотые серёжки', 'серебряные серёжки', 'золотые подвески', 'серебряные подвески', 'золотые кресты', 'серебряные кресты', 'сережки-цепи', 'серебряные сережки-цепи', 'золотые сережки-цепи', 'серёжки-цепи', 'серебряные серёжки-цепи', 'золотые серёжки-цепи', 'шарфы', 'ободки', 'резинки', 'банты', 'заколки', 'перчатки', 'перчатки с открытыми пальцами', 'кожаные перчатки', 'кожаные перчатки с открытыми пальцами', 'ожерелья', 'жемчужные ожерелья', 'ремни с металлическими пряжками', 'ремешки', 'кожаные ремешки', 'ремешки с пряжкой', 'ремешки с металлическими пряжками', 'металлические заклепки', 'металлические заклёпки', 'кепки', 'банданы', 'платки', 'косынки', 'узкие очки', 'узкие солнцезащитные очки', 'шапки', 'вязаные шапки', 'тонкие шапки', 'береты', 'беретки', 'каффы', 'клатчи', 'бананки', 'поясные сумки', 'сумки', 'почтальонки', 'рюкзаки', 'портфели', 'шляпы', 'шляпки', 'пояса', 'булавки', 'подтяжки', 'палантины', 'массивные цепи', 'высокие перчатки', 'парео', 'панамки', 'бейсболки', 'колье', 'клипсы', 'веера', 'трости', 'тросточки', 'зонты', 'зонтики', 'портмоне', 'кошельки', 'обручи', 'зажимы', 'брелоки', 'головные уборы', 'жабо', 'пуговицы', 'пуговки', 'молнии', 'замки', 'аксессуары', 'украшения', 'бижутерии', 'ювелирные изделия']
    }
}

# Результирующая база данных
print_database = {
    'одежда': {
        'единственное': [],
        'множественное': []
    },
    'прически': {
        'единственное': [],
        'множественное': []
    },
    'украшения': {
        'единственное': [],
        'множественное': []
    }
}

# Индексы групп и фото
g_index = 0
p_index = 0

comment = []
for i in range(10):
    comment.append(f"<b>Описание группы:</b>")

# Инициализация меню под фотографией
photo_menu = InlineKeyboardMarkup(row_width=8)
num = InlineKeyboardButton(text="1 фото", callback_data="k3")
ph_1 = InlineKeyboardButton(text="Назад", callback_data="back")
ph_2 = InlineKeyboardButton(text="Вперед", callback_data="forward")
ph_3 = InlineKeyboardButton(text="Вернуться", callback_data="return")
photo_menu.add(num)
photo_menu.add(ph_2)
photo_menu.add(ph_3)

# Обновление кнопок для меню под фото
def update_photo_menu():
    global p_index
    global g_index
    photo_menu = InlineKeyboardMarkup(row_width=8)
    num = InlineKeyboardButton(text=f"{p_index+1} фото", callback_data="k3")
    photo_menu.add(num)
    if p_index > 0:
        photo_menu.add(ph_1)
    if p_index < len(photos[g_index]) - (photos[g_index]).count(None) - 1:
        photo_menu.add(ph_2)
    photo_menu.add(ph_3)
    return photo_menu

# Создание массива для фото
photos = [[None]] * 10
for i in range(10):
    photos[i] = [None] * 10
# Ссылки для парсинга групповых фото
directory_urls = [
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%9A%D0%B8%D0%BD%D0%BE",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%20%D0%9D%D0%B0%D1%81%D0%BC%D0%B5%D1%88%D0%B5%D0%BA",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%90%D0%BA%D0%B2%D0%B0%D1%80%D0%B8%D1%83%D0%BC",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%94%D0%B8%D0%B0%D0%BB%D0%BE%D0%B3",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%90%D0%BB%D0%B8%D1%81%D0%B0",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%94%D1%83%D1%80%D0%BD%D0%BE%D0%B5%20%D0%92%D0%BB%D0%B8%D1%8F%D0%BD%D0%B8%D0%B5",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%97%D0%BE%D0%BE%D0%BF%D0%B0%D1%80%D0%BA",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%9F%D0%B8%D0%BA%D0%BD%D0%B8%D0%BA",
    "https://github.com/Qidemoto/PIRbot/raw/main/Foto/%D0%A2%D0%B5%D0%BB%D0%B5%D0%B2%D0%B8%D0%B7%D0%BE%D1%80"
]

count = 0
# Проход по каждой директории
for directory_url in directory_urls:
    # Получение HTML-кода страницы директории
    response = requests.get(directory_url)
    html_content = response.content
    
    # Создание объекта BeautifulSoup для анализа HTML-кода
    soup = BeautifulSoup(html_content, "html.parser")
    i = 0
    # Нахождение всех ссылок на файлы в директории
    for link in soup.find_all("a", {"class": "js-navigation-open"}):
        file_url = link.get("href")
        if file_url.endswith(".jpg") or file_url.endswith(".jpeg") or file_url.endswith(".png"):
            file_url = file_url.replace('/blob/', '/raw/')
            photos[count][i] = 'https://github.com/'+file_url
            i += 1
    count += 1

# Функция вызова начального меню
@dp.message_handler(commands=['start'], state = "*")
async def start(message: types.Message):
    msg1 = await message.answer(text="Привет, я RockUnderground_bot!")
    await rock.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    time.sleep(1)
    # Вызов начального с группами
    msg2 = await message.answer(text=f"Вы можете:\
        <b>\n• Прочитать описания групп\n• Просмотреть фотографии групп\n• Составить описания групп по фотографиям</b>\n\n<i>Для работы с ботом пропиши команду /groups\n(или просто нажмите на кнопку)</i>", reply_markup= main_menu)
    await asyncio.sleep(17)
    await msg2.delete()
    await asyncio.sleep(0.5)
    await msg1.delete()

# Функция вызова меню с группами по команде
@dp.message_handler(commands=['groups'], state = "*")
async def groups(message: types.CallbackQuery):
    msg = await message.answer(text = "<b>Выберите группу, фотографии которой вы хотели бы посмотреть:</b>", reply_markup = group_menu)

# Функция вызова меню с группами по кнопке
@dp.callback_query_handler(text = "k1")
async def groups_button(callback: types.CallbackQuery):
    await callback.message.answer(text = "<b>Выберите группу, фотографии которой вы хотели бы посмотреть:</b>", reply_markup = group_menu)
    # await callback.message.delete_reply_markup()

# Функция вызова описания группы
@dp.callback_query_handler(text="k2")
async def comments_dropper(message: types.CallbackQuery):
    await message.message.answer(text=comment[g_index])
    await message.message.delete_reply_markup()
    print(print_database)
    

# Функция вызова альбома группы
@dp.callback_query_handler(text="k3", state = '*')
async def photosend(callback: types.CallbackQuery):
    global p_index
    global g_index
    current_photo = photos[g_index][p_index]
    photo_number = p_index + 1
    # Отправляем текущую фотографию
    sent_message = await rock.send_photo(chat_id=callback.message.chat.id, photo=current_photo)

    # Обновляем сообщение с клавиатурой
    await rock.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=sent_message.message_id, reply_markup=photo_menu)

# Функция приема сообщения
@dp.callback_query_handler(text="k4", state='*')
async def comments_taker(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text="Введите описание группы по просмотренным фотографиям:")
    await NewComments(callback_query.message.text)

# Функция обработки сообщения
async def NewComments(group_description: str):
    # Разделение на отдельные слова
    words = re.findall(r'\b\w+\b', group_description)
    # Отфильтровать знаки пунктуации
    filtered_words = [word for word in words if word.isalpha()]
    print(filtered_words)

    # Анализ по одному слову и парам слов
    for i in range(len(filtered_words)):
        word1 = filtered_words[i]
        if i < len(filtered_words) - 1:
            word2 = filtered_words[i + 1]
        else:
            word2 = "q"

        for category in database:
            for number in database[category]:
                if word1.lower() in database[category][number]:
                    print_database[category][number].append(word1.lower())

                if (word1.lower()+" "+word2.lower()) in database[category][number]:
                    print_database[category][number].append(word1.lower()+" "+word2.lower())

# Функции смены индекса группы и вызова меню действий
@dp.callback_query_handler(text="g1")
async def photosend1(callback: types.CallbackQuery):
    global g_index
    g_index = 0
    await actions(callback)
@dp.callback_query_handler(text="g2")
async def photosend2(callback: types.CallbackQuery):
    global g_index
    g_index = 1
    await actions(callback)
@dp.callback_query_handler(text="g3")
async def photosend3(callback: types.CallbackQuery):
    global g_index
    g_index = 2
    await actions(callback)
@dp.callback_query_handler(text="g4")
async def photosend4(callback: types.CallbackQuery):
    global g_index
    g_index = 3
    await actions(callback)
@dp.callback_query_handler(text="g5")
async def photosend5(callback: types.CallbackQuery):
    global g_index
    g_index = 4
    await actions(callback)
@dp.callback_query_handler(text="g6")
async def photosend6(callback: types.CallbackQuery):
    global g_index
    g_index = 5
    await actions(callback)
@dp.callback_query_handler(text="g7")
async def photosend7(callback: types.CallbackQuery):
    global g_index
    g_index = 6
    await actions(callback)
@dp.callback_query_handler(text="g8")
async def photosend8(callback: types.CallbackQuery):
    global g_index
    g_index = 7
    await actions(callback)
@dp.callback_query_handler(text="g9")
async def photosend9(callback: types.CallbackQuery):
    global g_index
    g_index = 8
    await actions(callback)
@dp.callback_query_handler(text="g10")
async def photosend10(callback: types.CallbackQuery):
    global g_index
    g_index = 9
    await actions(callback)

# Функция промотки на фото назад
@dp.callback_query_handler(text = "back")
async def p_back(callback: types.CallbackQuery):
    global p_index
    global photo_menu
    p_index -= 1
    # Обновление меню с фото
    photo_menu = update_photo_menu()
    # Вызов меню с фото заново
    await photosend(callback)
    await callback.message.delete_reply_markup()

# Функция промотки на фото вперед
@dp.callback_query_handler(text = "forward")
async def p_forward(callback: types.CallbackQuery):
    global p_index
    global photo_menu
    p_index += 1
    # Обновление меню с фото
    photo_menu = update_photo_menu()
    # Вызов меню с фото заново
    await photosend(callback)
    await callback.message.delete_reply_markup()

# Функция возврата в каталог с группами
@dp.callback_query_handler(text = "return")
async def p_return(callback: types.CallbackQuery):
    global p_index
    global g_index
    global photo_menu
    p_index = 0
    g_index = 0
    # Обновление меню с фото
    photo_menu = update_photo_menu()
    # Вызов меню с каталогом
    await groups_button(callback)
    await callback.message.delete_reply_markup()

# Фцнкция вызова рабочего меню
@dp.callback_query_handler()
async def actions(callback: types.CallbackQuery):
    msg = await callback.message.answer(text = "<b>Выберите необходимое действие:</b>", reply_markup = work_menu)
    await callback.message.delete_reply_markup()