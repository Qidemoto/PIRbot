from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание начального меню
main_menu = InlineKeyboardMarkup(row_width=8)
btn_1 = InlineKeyboardButton(text="Начать работу с ботом",callback_data ="k1")
main_menu.add(btn_1)

work_menu = InlineKeyboardMarkup(row_width=8)
btn_2 = InlineKeyboardButton(text="Прочитать описания",callback_data ="k2")
btn_3 = InlineKeyboardButton(text="Просмотреть фотографии",callback_data ="k3")
btn_4 = InlineKeyboardButton(text="Составить описания",callback_data ="k4")
work_menu.add(btn_2)
work_menu.add(btn_3)
work_menu.add(btn_4)

# Создание меню выхода
exitor_menu = InlineKeyboardMarkup(row_width=5)
btn_exit = InlineKeyboardButton(text="Назад", callback_data ="k5")
exitor_menu.add(btn_exit)

# Создание меню с группами
group_menu = InlineKeyboardMarkup(row_width=8)
grp_1 = InlineKeyboardButton(text="Кино",callback_data ="g1")
grp_2 = InlineKeyboardButton(text="Объект Насмешек",callback_data ="g2")
grp_3 = InlineKeyboardButton(text="Аквариум",callback_data ="g3")
grp_4 = InlineKeyboardButton(text="Диалог",callback_data ="g4")
grp_5 = InlineKeyboardButton(text="Алиса",callback_data ="g5")
grp_6 = InlineKeyboardButton(text="Дурное Влияние",callback_data ="g6")
grp_7 = InlineKeyboardButton(text="Зоопарк",callback_data ="g7")
grp_8 = InlineKeyboardButton(text="Пикник",callback_data ="g8")
grp_9 = InlineKeyboardButton(text="Телевизор",callback_data ="g9")
grp_10 = InlineKeyboardButton(text="Другие фото",callback_data ="g10")
group_menu.add(grp_1)
group_menu.add(grp_2)
group_menu.add(grp_3)
group_menu.add(grp_4)
group_menu.add(grp_5)
group_menu.add(grp_6)
group_menu.add(grp_7)
group_menu.add(grp_8)
group_menu.add(grp_9)
group_menu.add(grp_10)

'''
buttons = []
if p_index > 0:
    buttons.append(InlineKeyboardButton("Назад", callback_data="back"))
if p_index < len(photos[0]) - (photos[0]).count(None) - 1:
    buttons.append(InlineKeyboardButton("Вперед", callback_data="forward"))
buttons.append(InlineKeyboardButton("Вернуться", callback_data="return"))
photo_menu = InlineKeyboardMarkup().add(*buttons)

photo_menu = InlineKeyboardMarkup(row_width=8)
ph_1 = InlineKeyboardButton(text="Назад", callback_data="back")
ph_2 = InlineKeyboardButton(text="Вперед", callback_data="forward")
ph_3 = InlineKeyboardButton(text="Вернуться", callback_data="return")
if p_index > 0:
    photo_menu.add(ph_1)
if p_index < len(photos[0]) - (photos[0]).count(None) - 1:
    photo_menu.add(ph_2)
photo_menu.add(ph_3)
'''