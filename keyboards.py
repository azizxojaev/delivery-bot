from aiogram.types import *


async def startBot_reply():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.row("Меню 🍽", "Корзина 🛒")
    btn.row("Мои заказы 🛍", "Оставить отзыв ✍️", "Поддержка 📞")
    return btn

async def order_reply():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn.add(
        KeyboardButton("Мой номер 📞", request_contact=True),
        KeyboardButton("Назaд ⬅️")
    )
    return btn

async def adress_reply():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("Моя геолокация 📍", request_location=True),
        KeyboardButton("Сохраненные адреса 🗺")
    )
    btn.add(
        KeyboardButton("Нaзад ⬅️")
    )
    return btn
async def adressCheck_reply():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("Да ✅"),
        KeyboardButton("Нет ❌")
    )
    btn.add(
        KeyboardButton("Назад ⬅️")
    )
    return btn

async def chooseAddress_reply(addresses):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in range(len(addresses)):
        btn.add(
            KeyboardButton(f"{addresses[i]}")
        )
    btn.add(
        KeyboardButton("Назад ↩️")
    )
    return btn

async def orderDone_reply():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("Подтвердить ✅"),
        KeyboardButton("Назад ⬅️")
    )
    return btn


async def stars_inline():
    btn = InlineKeyboardMarkup(row_width=5)
    btn.add(
        InlineKeyboardButton("1⭐️", callback_data="stars:1"),
        InlineKeyboardButton("2⭐️", callback_data="stars:2"),
        InlineKeyboardButton("3⭐️", callback_data="stars:3"),
        InlineKeyboardButton("4⭐️", callback_data="stars:4"),
        InlineKeyboardButton("5⭐️", callback_data="stars:5")
    )
    return btn
async def starsBack_reply():
    btn = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    btn.add(
        KeyboardButton("Нaзaд ⬅️")
    )
    return btn

async def orders_inline(id):
    btn = InlineKeyboardMarkup(row_width=2)
    for i in range(len(id)):
        btn.add(
            InlineKeyboardButton(f"Заказ № {id[i]}", callback_data=f"order:{id[i]}")
        )
    return btn
async def back_inline():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("Назад ⬅️", callback_data="backToOrders")
    )
    return btn
async def menu_inline():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Лаваш 🌯", callback_data="c:1"),
        InlineKeyboardButton("Триндвич 🥪", callback_data="c:2"),
        InlineKeyboardButton("Шаурма 🫓", callback_data="c:3"),
        InlineKeyboardButton("Бургеры 🍔", callback_data="c:4"),
        InlineKeyboardButton("Саб 🌮", callback_data="c:5"),
        InlineKeyboardButton("Картошка 🍟", callback_data="c:6"),
        InlineKeyboardButton("Хот-Доги 🌭", callback_data="c:7"),
        InlineKeyboardButton("Снэки 🍗", callback_data="c:8"),
        InlineKeyboardButton("Гарниры, салаты, хлеб 🥗", callback_data="c:9"),
        InlineKeyboardButton("Соусы, добавки 🥫", callback_data="c:10"),
        InlineKeyboardButton("Наборы (Сеты) 🍱", callback_data="c:11"),
        InlineKeyboardButton("Десерты 🍰", callback_data="c:12"),
        InlineKeyboardButton("Горячие напитки ☕️", callback_data="c:13"),
        InlineKeyboardButton("Холодные напитки 🥤", callback_data="c:14"),
    )
    return btn

async def product_inline(msg):
    btn = InlineKeyboardMarkup(row_width=2)
    if msg == "1":
        btn.add(
            InlineKeyboardButton("Лаваш с курицей 🌯", callback_data="p:1"),
            InlineKeyboardButton("Лаваш с говядиной и сыром 🌯", callback_data="p:2"),
            InlineKeyboardButton("Лаваш острый с говядиной 🌯", callback_data="p:3"),
            InlineKeyboardButton("Лаваш острый с курицей 🌯", callback_data="p:4"),
            InlineKeyboardButton("Лаваш с курицей и сыром 🌯", callback_data="p:5"),
            InlineKeyboardButton("Фиттер 🌯", callback_data="p:6")
        )
    elif msg == "2":
        btn.add(
        InlineKeyboardButton("Триндвич с курицей 🥪", callback_data="p:7"),
        InlineKeyboardButton("Триндвич с говядиной 🥪", callback_data="p:8")
        )
    elif msg == "3":
        btn.add(
        InlineKeyboardButton("Шаурма острая с говядиной 🫓", callback_data="p:9"),
        InlineKeyboardButton("Шаурма с курицей 🫓", callback_data="p:10"),
        InlineKeyboardButton("Шаурма острая с курицей 🫓", callback_data="p:11"),
        InlineKeyboardButton("Шаурма с говядиной 🫓", callback_data="p:12")
        )
    elif msg == "4":
        btn.add(
        InlineKeyboardButton("Гамбургер 🍔", callback_data="p:13"),
        InlineKeyboardButton("Чизбургер 🍔", callback_data="p:14"),
        InlineKeyboardButton("Даблбургер 🍔", callback_data="p:15"),
        InlineKeyboardButton("Даблчизбургер 🍔", callback_data="p:16")
        )
    elif msg == "5":
        btn.add(
        InlineKeyboardButton("Саб с курицей 🌮", callback_data="p:17"),
        InlineKeyboardButton("Саб с курицей и сыром 🌮", callback_data="p:18"),
        InlineKeyboardButton("Саб с говядиной и сыром 🌮", callback_data="p:19"),
        InlineKeyboardButton("Саб с говядиной 🌮", callback_data="p:20")
        )
    elif msg == "6":
        btn.add(
        InlineKeyboardButton("Картофель по-деревенски 🍟", callback_data="p:21"),
        InlineKeyboardButton("Картофель Фри 🍟", callback_data="p:22")
        )
    elif msg == "7":
        btn.add(
        InlineKeyboardButton("Хот-дог 🌭", callback_data="p:23"),
        InlineKeyboardButton("ДаблХот-дог 🌭", callback_data="p:24"),
        InlineKeyboardButton("Хот-дог детский 🌭", callback_data="p:25"),
        InlineKeyboardButton("Хот-дог Мини 🌭", callback_data="p:26")
        )
    elif msg == "8":
        btn.add(
        InlineKeyboardButton("Смайлики 🍗", callback_data="p:27"),
        InlineKeyboardButton("Стрипсы 🍗", callback_data="p:28")
        )
    elif msg == "9":
        btn.add(
        InlineKeyboardButton("Рис 🥗", callback_data="p:29"),
        InlineKeyboardButton("Лепешка 🥗", callback_data="p:30"),
        InlineKeyboardButton("Салат 🥗", callback_data="p:31"),
        InlineKeyboardButton("Салат Цезарь 🥗", callback_data="p:32"),
        InlineKeyboardButton("Салат Греческий 🥗", callback_data="p:33")
        )
    elif msg == "10":
        btn.add(
        InlineKeyboardButton("Кисло-сладкий соус 25 мл 🥫", callback_data="p:34"),
        InlineKeyboardButton("Томатный кетчуп 25 мл 🥫", callback_data="p:35"),
        InlineKeyboardButton("Барбекю 25 мл 🥫", callback_data="p:36"),
        InlineKeyboardButton("Майонезно-сырный соус 25 мл 🥫", callback_data="p:37")
        )
    elif msg == "11":
        btn.add(
        InlineKeyboardButton("Комбо Плюс 🍱", callback_data="p:38"),
        InlineKeyboardButton("Комбо плюс горячий (зеленый чай) 🍱", callback_data="p:39"),
        InlineKeyboardButton("Донар с говядиной 🍱", callback_data="p:40"),
        InlineKeyboardButton("ФитКомбо 🍱", callback_data="p:41"),
        InlineKeyboardButton("Донар с курицей 🍱", callback_data="p:42"),
        InlineKeyboardButton("Комбо плюс горячий (черный чай) 🍱", callback_data="p:43"),
        InlineKeyboardButton("Детское комбо 🍱", callback_data="p:44"),
        InlineKeyboardButton("Донар-бокс с курицей 🍱", callback_data="p:45"),
        InlineKeyboardButton("Донар-бокс с говядиной 🍱", callback_data="p:46")
        )
    elif msg == "12":
        btn.add(
        InlineKeyboardButton("Донат карамельный 🍰", callback_data="p:47"),
        InlineKeyboardButton("Медовик 🍰", callback_data="p:48"),
        InlineKeyboardButton("Чизкейк 🍰", callback_data="p:49"),
        InlineKeyboardButton("Донат ягодный 🍰", callback_data="p:50")
        )
    elif msg == "13":
        btn.add(
        InlineKeyboardButton("Кофе Глясе ☕️", callback_data="p:51"),
        InlineKeyboardButton("Чай зеленый с лимоном ☕️", callback_data="p:52"),
        InlineKeyboardButton("Латте ☕️", callback_data="p:53"),
        InlineKeyboardButton("Чай черный с лимоном ☕️", callback_data="p:54"),
        InlineKeyboardButton("Чай черный ☕️", callback_data="p:55"),
        InlineKeyboardButton("Чай зеленый ☕️", callback_data="p:56"),
        InlineKeyboardButton("Капучино ☕️", callback_data="p:57"),
        InlineKeyboardButton("Американо ☕️", callback_data="p:58")
        )
    elif msg == "14":
        btn.add(
        InlineKeyboardButton("Сок Яблочный без сахара, 0,33л. 🥤", callback_data="p:59"),
        InlineKeyboardButton("Вода без газа 0,5л 🥤", callback_data="p:60"),
        InlineKeyboardButton("Сок Блисс 🥤", callback_data="p:61"),
        InlineKeyboardButton("Пепси, бутылка 0,5л 🥤", callback_data="p:62"),
        InlineKeyboardButton("Пепси, бутылка 1,5л 🥤", callback_data="p:63"),
        InlineKeyboardButton("Пепси, стакан 0,4л 🥤", callback_data="p:64"),
        InlineKeyboardButton("Мохито 🥤", callback_data="p:65"),
        InlineKeyboardButton("Пина колада 🥤", callback_data="p:66")
        )
    btn.add(
        InlineKeyboardButton("Назад ⬅️", callback_data="back")
    )
    return btn

async def howMuch_inline(num, categ):
    btn = InlineKeyboardMarkup(row_width=3)
    btn.add(
        InlineKeyboardButton("-", callback_data="-"),
        InlineKeyboardButton(f"{num}", callback_data="n"),
        InlineKeyboardButton("+", callback_data="+"),
        InlineKeyboardButton("Добавить в корзину 🛒", callback_data="add"),
        InlineKeyboardButton("Назад ⬅️", callback_data=f"bac:{categ}")
    )
    return btn

async def basket_inline():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("Очистить корзину 🗑", callback_data="clear"),
        InlineKeyboardButton("Оформить заказ 🚖", callback_data="order"),
    )
    return btn

async def admin_inline():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Отзывы", callback_data="view_review"),
        InlineKeyboardButton("Все заказы", callback_data="view_orders"),
    )
    return btn
async def adminBack_inline():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Назад ⬅️", callback_data="back_review")
    )
    return btn
async def adminOrders_inline(id):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Назад ⬅️", callback_data="backToAdminMenu")
    )
    for i in range(len(id)):
        btn.add(
            InlineKeyboardButton(f"Заказ № {id[i]}", callback_data=f"order2:{id[i]}")
        )
    return btn
async def back2_inline():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("Назад ⬅️", callback_data="backToOrders2")
    )
    btn.add(
        InlineKeyboardButton("Удалить заказ 🗑", callback_data="delete_order")
    )
    return btn