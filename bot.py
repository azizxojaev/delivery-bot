import logging
import sqlite3 as sql
import requests
import datetime
import pytz

from states import UserStates, UserStates3
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from collections import Counter
from aiogram import Bot, Dispatcher, executor, types
from keyboards import *

BOT_TOKEN = "6145569761:AAFV2EacizdYIKLPLtc6AzVLMH4-IMQvbjw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# База данных
con = sql.connect("database.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS locations(
            location TEXT,
            id INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS korzina(
            products TEXT,
            cost INTEGER,
            id INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER,
            products TEXT,
            address TEXT,
            phone_number TEXT,
            price INTEGER,
            date TEXT,
            id INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS reviews(
            review TEXT,
            stars INTEGER,
            username TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS info_for_order(
            products TEXT,
            adress TEXT,
            phone_number TEXT,
            price INTEGER,
            date TEXT,
            id INTEGER
)""")


# Приниматель адресса
def get_address(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url).json()
    address = response['display_name']
    return address


# Команда start
@dp.message_handler(commands=["start"])
async def startBot_handler(message: types.Message):
    try:
        btn = await startBot_reply()
        await message.answer("*Добро пожаловать в службу доставки еды!*\n\nВыберите опцию ниже:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Ошибка {e}", reply_markup=btn)


# Кнопка Меню
@dp.message_handler(text="Меню 🍽")
async def menu_handler(message: types.Message):
    try:
        btn = await menu_inline()
        await message.answer("Выберите категорию", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)

# Кнопка Поддержки
@dp.message_handler(text="Поддержка 📞")
async def help_handler(message: types.Message):
    try:
        await message.answer("По всем вопросам пишите: @Wifenlof")
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


# Кнопка Отзывы
@dp.message_handler(text="Оставить отзыв ✍️")
async def reviews_handler(message: types.Message):
    try:
        btn = await starsBack_reply()
        await message.answer("Отзыв:", reply_markup=btn)
        btn = await stars_inline()
        await message.answer("На сколько звёзд вы бы оценили нас?", reply_markup=btn)
        await UserStates3.star.set()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Нажатие на звезду
@dp.callback_query_handler(text_contains="stars:", state=UserStates3.star)
async def stars_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        star = int(call.data.split(":")[1])
        await state.update_data(star=star)
        await call.message.edit_text("Напишите ваш отзыв")
        await UserStates3.review.set()
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(state=UserStates3.star, text="Нaзaд ⬅️")
async def review_handler(message: types.Message, state: FSMContext):
    try:
        btn = await startBot_reply()
        await message.answer("Выберите опцию ниже:", reply_markup=btn)
        await state.finish()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(state=UserStates3.review, text="Нaзaд ⬅️")
async def review_handler(message: types.Message, state: FSMContext):
    try:
        btn = await startBot_reply()
        await message.answer("Выберите опцию ниже:", reply_markup=btn)
        await state.finish()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(state=UserStates3.review)
async def review_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data(review=message.text)
        data = await state.get_data()
        username = message.from_user.username
        if username == None:
            username = message.from_user.id
        btn = await startBot_reply()
        await message.answer("Спасибо за отзыв!", reply_markup=btn)
        cur.execute("INSERT INTO reviews VALUES (?, ?, ?)", (data["review"], data["star"], username))
        con.commit()
        await state.finish()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


# Кнопка Корзины
@dp.message_handler(text="Корзина 🛒")
async def basket_handler(message: types.Message):
    try:
        global showProducts
        global sum
        global final_sum
        global allProducts
        cur.execute(f"DELETE FROM info_for_order WHERE id = {message.from_user.id}")
        con.commit()
        if cur.execute(f"SELECT products FROM korzina WHERE id = {message.from_user.id}").fetchone() != None:
            allProducts = []
            allCosts = []
            sum = 0
            showProducts = ""
            for i in cur.execute(f"SELECT products FROM korzina WHERE id = {message.from_user.id}").fetchall():
                allProducts.append(i[0])
            counter = Counter(allProducts)
            for value, count in counter.items():
                showProducts = showProducts + f"▪️{value} {count}x\n"
            for i in cur.execute(f"SELECT cost FROM korzina WHERE id = {message.from_user.id}").fetchall():
                allCosts.append(int(i[0]))
            for i in range(len(allCosts)):
                sum = sum + allCosts[i]
            final_sum = sum + 10000
            final_sum = str(final_sum)
            final_sum = final_sum[:-3]
            sum = str(sum)
            sum = sum[:-3]
            btn = await basket_inline()
            await message.answer(f"*В корзине:*\n\n_{showProducts}_\n*Товары:* `{sum} 000 сум`\n*Доставка:* `10 000 сум`\n*Итого:* `{final_sum} 000`", reply_markup=btn)
            sumForDB = int(final_sum) * 1000
            cur.execute("INSERT INTO info_for_order VALUES (?, ?, ?, ?, ?, ?)", (str(allProducts), None, None, sumForDB, None, message.from_user.id))
            con.commit()
        else:
            await message.answer("У вас нету никакого товара в корзине")
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


# Инлайн кнопки заказов
@dp.callback_query_handler(text_contains="order:")
async def myorders_handler(call: types.CallbackQuery):
    try:
        call_id = call.data.split(":")[1]
        allData = cur.execute(f"SELECT * FROM orders WHERE order_id = {call_id}").fetchone()
        orderId = allData[0]
        all_products = str(allData[1])
        all_products = all_products.split(",")
        for i in range(len(all_products)):
            all_products[i] = all_products[i].lstrip()
        result = ""
        for i in range(len(all_products)):
            result = result + f"▪️ {all_products[i]}\n"
        result = result.replace("'", "")
        result = result.replace("[", "")
        result = result.replace("]", "")
        adress_result = allData[2]
        phoneNumber_result = allData[3]
        price_result = str(allData[4])[:-3]
        date_result = allData[5]
        btn = await back_inline()
        await call.message.edit_text(f"*Заказ № {orderId}:*\n\n_{result}_\n*Адрес: *`{adress_result}`\n*Номер телефона:* `{phoneNumber_result}`\n*Цена:* `{price_result} 000`\n*Дата:* `{date_result}`", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Назад к заказам
@dp.callback_query_handler(text="backToOrders")
async def backToOrders_handler(call: types.CallbackQuery):
    try:
        orders = cur.execute(f"SELECT * FROM orders WHERE id = {call.from_user.id}").fetchall()
        idList = []
        for i in range(len(orders)):
            idList.append(orders[i][0])
        btn = await orders_inline(idList)
        await call.message.edit_text("Выберите ваши заказы:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Кнопка Мои заказы
@dp.message_handler(text="Мои заказы 🛍")
async def myorders_handler(message: types.Message):
    try:
        if cur.execute(f"SELECT * FROM orders WHERE id = {message.from_user.id}").fetchone() != None:
            orders = cur.execute(f"SELECT * FROM orders WHERE id = {message.from_user.id}").fetchall()
            idList = []
            for i in range(len(orders)):
                idList.append(orders[i][0])
            btn = await orders_inline(idList)
            await message.answer("Выберите ваши заказы:", reply_markup=btn)
        else:
            await message.answer("Вы еще ничего не заказывали!")
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


# Товары
@dp.callback_query_handler(text="back")
async def back_products(call: types.CallbackQuery):
    try:
        btn = await menu_inline()
        await call.message.edit_text("Выберите категорию", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Назад в меню
@dp.callback_query_handler(text_contains="bac:")
async def back_products(call: types.CallbackQuery):
    try:
        msg = call.data.split(":")[1]
        await call.message.delete()
        btn = await product_inline(msg)
        await call.message.answer("Выберите товар", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Меню
@dp.callback_query_handler(text_contains="c:")
async def menu_product1(call: types.CallbackQuery):
    try:
        global category
        msg = call.data.split(":")[1]
        category = msg
        btn = await product_inline(msg)
        await call.message.delete()
        await call.message.answer_photo(types.InputFile(f"main_images/{msg}.jpg"), caption="Выберите товар", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Карта продукта
@dp.callback_query_handler(text_contains="p:")
async def check_product(call: types.CallbackQuery):
    try:
        global num
        global product
        global cost
        num = 1
        msg = call.data.split(":")[1]
        if True:
            if msg == "1":
                product = "Лаваш с курицей "
                cost = 26000
            elif msg == "2":
                product = "Лаваш с говядиной и сыром "
                cost = 31000
            elif msg == "3":
                product = "Лаваш острый с говядиной "
                cost = 28000
            elif msg == "4":
                product = "Лаваш острый с курицей "
                cost = 26000
            elif msg == "5":
                product = "Лаваш с курицей и сыром "
                cost = 29000
            elif msg == "6":
                product = "Фиттер "
                cost = 24000
            elif msg == "7":
                product = "Триндвич с курицей "
                cost = 24000
            elif msg == "8":
                product = "Триндвич с говядиной "
                cost = 26000
            elif msg == "9":
                product = "Шаурма острая с говядиной "
                cost = 26000
            elif msg == "10":
                product = "Шаурма с курицей "
                cost = 26000
            elif msg == "11":
                product = "Шаурма острая c курицей "
                cost = 24000
            elif msg == "12":
                product = "Шаурма с говядиной "
                cost = 26000
            elif msg == "13":
                product = "Гамбургер "
                cost = 22000
            elif msg == "14":
                product = "Чизбургер "
                cost = 24000
            elif msg == "15":
                product = "Даблбургер "
                cost = 33000
            elif msg == "16":
                product = "Даблчизбургер "
                cost = 37000
            elif msg == "17":
                product = "Саб с курицей  "
                cost = 17000
            elif msg == "18":
                product = "Саб с курицей и сыром "
                cost = 19000
            elif msg == "19":
                product = "Саб с говядиной и сыром "
                cost = 21000
            elif msg == "20":
                product = "Саб с говядиной "
                cost = 19000
            elif msg == "21":
                product = "Картофель по-деревенски "
                cost = 15000
            elif msg == "22":
                product = "Картофель Фри "
                cost = 14000
            elif msg == "23":
                product = "Хот-дог "
                cost = 14000
            elif msg == "24":
                product = "ДаблХот-дог "
                cost = 21000
            elif msg == "25":
                product = "Хот-дог детский "
                cost = 8000
            elif msg == "26":
                product = "Хот-дог Мини "
                cost = 8000
            elif msg == "27":
                product = "Смайлики "
                cost = 14000
            elif msg == "28":
                product = "Стрипсы "
                cost = 19000
            elif msg == "29":
                product = "Рис "
                cost = 7000
            elif msg == "30":
                product = "Лепешка "
                cost = 3000
            elif msg == "31":
                product = "Салат "
                cost = 7000
            elif msg == "32":
                product = "Салат Цезарь "
                cost = 24000
            elif msg == "33":
                product = "Салат Греческий "
                cost = 22000
            elif msg == "34":
                product = "Кисло-сладкий соус 25 мл "
                cost = 3000
            elif msg == "35":
                product = "Томатный кетчуп 25 мл "
                cost = 3000
            elif msg == "36":
                product = "Барбекю 25 мл "
                cost = 3000
            elif msg == "37":
                product = "Майонезно-сырный соус 25 мл "
                cost = 3000
            elif msg == "38":
                product = "Комбо Плюс "
                cost = 17000
            elif msg == "39":
                product = "Комбо плюс горячий (зеленый чай) "
                cost = 17000
            elif msg == "40":
                product = "Донар с говядиной "
                cost = 43000
            elif msg == "41":
                product = "ФитКомбо "
                cost = 31000
            elif msg == "42":
                product = "Донар c курицей "
                cost = 41000
            elif msg == "43":
                product = "Комбо плюс горячий (чёрный чай) "
                cost = 17000
            elif msg == "44":
                product = "Детское комбо "
                cost = 17000
            elif msg == "45":
                product = "Донар-бокс с курицей "
                cost = 34000
            elif msg == "46":
                product = "Донар-бокс с говядиной "
                cost = 36000
            elif msg == "47":
                product = "Донат карамельный "
                cost = 15000
            elif msg == "48":
                product = "Медовик "
                cost = 16000
            elif msg == "49":
                product = "Чизкейк "
                cost = 16000
            elif msg == "50":
                product = "Донат ягодный "
                cost = 15000
            elif msg == "51":
                product = "Кофе Глясе "
                cost = 13000
            elif msg == "52":
                product = "Чай зеленый с лимоном "
                cost = 5000
            elif msg == "53":
                product = "Латте "
                cost = 13000
            elif msg == "54":
                product = "Чай черный с лимоном "
                cost = 5000
            elif msg == "55":
                product = "Чай черный "
                cost = 4000
            elif msg == "56":
                product = "Чай зеленый "
                cost = 4000
            elif msg == "57":
                product = "Капучино "
                cost = 13000
            elif msg == "58":
                product = "Американо "
                cost = 11000
            elif msg == "59":
                product = "Сок Яблочный без сахара, 0,33л. "
                cost = 10000
            elif msg == "60":
                product = "Вода без газа 0,5л "
                cost = 4000
            elif msg == "61":
                product = "Сок Блисс "
                cost = 16000
            elif msg == "62":
                product = "Пепси, бутылка 0,5л "
                cost = 9000
            elif msg == "63":
                product = "Пепси, бутылка 1,5л "
                cost = 17000
            elif msg == "64":
                product = "Пепси, стакан 0,4л "
                cost = 8000
            elif msg == "65":
                product = "Мохито "
                cost = 11000
            elif msg == "66":
                product = "Пина колада "
                cost = 11000
        btn = await howMuch_inline(num, category)
        await call.message.delete()
        await call.message.answer_photo(types.InputFile(f"products/p.{msg}.jpg"), caption=f"Сколько {product}желаете?\nЦена: {cost} сум", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Добавить товвра
@dp.callback_query_handler(text="+")
async def plus_product(call: types.CallbackQuery):
    try:
        global num
        num = num + 1
        btn = await howMuch_inline(num, category)
        await call.message.edit_reply_markup(btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Убавить товар
@dp.callback_query_handler(text="-")
async def minus_product(call: types.CallbackQuery):
    try:
        global num
        if num > 1:
            num = num - 1
            btn = await howMuch_inline(num, category)
            await call.message.edit_reply_markup(btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Добавить товар в корзину
@dp.callback_query_handler(text="add")
async def add_product(call: types.CallbackQuery):
    try:
        for i in range(num):
            cur.execute(f"INSERT INTO korzina VALUES (?, ?, ?)", (product, cost, call.from_user.id))
            con.commit()
        await call.answer("Товар добавлен в корзину", show_alert=True)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


# Корзина
@dp.callback_query_handler(text="clear")
async def clear_products(call: types.CallbackQuery):
    try:
        cur.execute(f"DELETE FROM korzina WHERE id = {call.from_user.id}")
        con.commit()
        await call.message.edit_text("Корзина очищена")
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Кнопки назад
@dp.message_handler(text="Назaд ⬅️", state=UserStates.contact)
async def back_products(message: types.Message, state: FSMContext):
    try:
        cur.execute(f"DELETE FROM info_for_order WHERE id = {message.from_user.id}")
        con.commit()
        await state.finish()
        btn = await startBot_reply()
        await message.answer("Корзина:", reply_markup=btn)
        global showProducts
        global sum
        global final_sum
        global allProducts
        cur.execute(f"DELETE FROM info_for_order WHERE id = {message.from_user.id}")
        con.commit()
        if cur.execute(f"SELECT products FROM korzina WHERE id = {message.from_user.id}").fetchone() != None:
            allProducts = []
            allCosts = []
            sum = 0
            showProducts = ""
            for i in cur.execute(f"SELECT products FROM korzina WHERE id = {message.from_user.id}").fetchall():
                allProducts.append(i[0])
            counter = Counter(allProducts)
            for value, count in counter.items():
                showProducts = showProducts + f"▪️{value} {count}x\n"
            for i in cur.execute(f"SELECT cost FROM korzina WHERE id = {message.from_user.id}").fetchall():
                allCosts.append(int(i[0]))
            for i in range(len(allCosts)):
                sum = sum + allCosts[i]
            final_sum = sum + 10000
            final_sum = str(final_sum)
            final_sum = final_sum[:-3]
            sum = str(sum)
            sum = sum[:-3]
            btn = await basket_inline()
            await message.answer(f"*В корзине:*\n\n_{showProducts}_\n*Товары:* `{sum} 000 сум`\n*Доставка:* `10 000 сум`\n*Итого:* `{final_sum} 000`", reply_markup=btn)
            sumForDB = int(final_sum) * 1000
            cur.execute("INSERT INTO info_for_order VALUES (?, ?, ?, ?, ?, ?)", (str(allProducts), None, None, sumForDB, None, message.from_user.id))
            con.commit()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Кнопка назад
@dp.message_handler(text="Нaзад ⬅️", state=UserStates.location)
async def back_products(message: types.Message, state: FSMContext):
    try:
        btn = await order_reply()
        await message.answer("Отправьте ваш номер телефона через кнопку или в формате: +998 \*\* \*\*\* \*\* \*\*", reply_markup=btn)
        await UserStates.contact.set()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)

# Запрос номера телефона
@dp.callback_query_handler(text="order")
async def clear_products(call: types.CallbackQuery):
    try:
        btn = await order_reply()
        await call.message.delete()
        await call.message.answer("Отправьте ваш номер телефона через кнопку или в формате: +998 \*\* \*\*\* \*\* \*\*", reply_markup=btn)
        await UserStates.contact.set()
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Запрос адреса
@dp.message_handler(content_types=["text", "contact"], state=UserStates.contact)
async def contact_sended(message: types.Message, state: FSMContext):
    try:
        global phoneNumber
        if message.content_type == "contact":
            phoneNumber = "+" + message.contact.phone_number
            cur.execute(f"UPDATE info_for_order SET phone_number = {phoneNumber} WHERE id = {message.from_user.id}")
            con.commit()
            btn = await adress_reply()
            await message.answer("Выберите адресс для доставки:", reply_markup=btn)
            await state.finish()
            await UserStates.location.set()
        elif message.content_type == "text":
            if "+998" in message.text and len(message.text) == 17:
                phoneNumber = message.text
                cur.execute(f"UPDATE info_for_order SET phone_number = '{phoneNumber}' WHERE id = {message.from_user.id}")
                con.commit()
                btn = await adress_reply()
                await message.answer("Выберите адресс для доставки:", reply_markup=btn)
                await state.finish()
                await UserStates.location.set()
            else:
                await message.answer("Вы неверно ввели номер телефона")
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Получение локации
@dp.message_handler(content_types=["location"], state=UserStates.location)
async def location_check(message: types.Message, state: FSMContext):
    try:
        global address
        latitude = message.location.latitude
        longitude = message.location.longitude
        address1 = get_address(latitude, longitude)
        address1 = str(address1)
        address1 = address1.split(", Toshkent")[0]
        address = ""
        for i in range(len(address1)):
            if address1[i] != "`":
                address = address + address1[i]
        btn = await adressCheck_reply()
        await message.answer(f"Ваш адрес: {address}?", reply_markup=btn)
        cur.execute(f"UPDATE info_for_order SET adress = '{address}' WHERE id = {message.from_user.id}")
        con.commit()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Сохраненные адреса
@dp.message_handler(text="Сохраненные адреса 🗺", state=UserStates.location)
async def savedLocations_check(message: types.Message, state: FSMContext):
    try:
        if cur.execute(f"SELECT location FROM locations WHERE id = {message.from_user.id}").fetchone() != None:
            addresses = []
            for i in cur.execute(f"SELECT location FROM locations WHERE id = {message.from_user.id}").fetchall():
                addresses.append(i[0])
            btn = await chooseAddress_reply(addresses)
            await message.answer("Выберите адресс", reply_markup=btn)
            await UserStates.location2.set()
        else:
            await message.answer("У вас нет сохраненных адресов")
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Подтверждение локации
@dp.message_handler(text="Нет ❌", state=UserStates.location)
async def locationNo_check(message: types.Message, state: FSMContext):
    try:
        btn = await adress_reply()
        await message.answer("Выберите адресс для доставки:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(text="Назад ⬅️", state=UserStates.location)
async def locationBack2_check(message: types.Message, state: FSMContext):
    try:
        btn = await adress_reply()
        await message.answer("Выберите адресс для доставки:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(text="Да ✅", state=UserStates.location)
async def locationYes_check(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        if cur.execute(f"SELECT location FROM locations WHERE id = {message.from_user.id}").fetchone() == None:
            cur.execute("INSERT INTO locations VALUES (?, ?)", (address, message.from_user.id))
            con.commit()
        btn = await orderDone_reply()
        await message.answer(f"*Ваш заказ:*\n\n*Aдрес:* `{address}`\n\n_{showProducts}_\n*Товары:* `{sum} 000 сум`\n*Доставка:* `10 000 сум`\n*Итого:* `{final_sum} 000`", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Кнопка назад
@dp.message_handler(text="Назад ↩️", state=UserStates.location2)
async def locationBack_check(message: types.Message, state: FSMContext):
    try:
        btn = await adress_reply()
        await message.answer("Выберите адресс для доставки:", reply_markup=btn)
        await UserStates.location.set()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Локация в виде текста
@dp.message_handler(state=UserStates.location2)
async def savedLocationsWait_check(message: types.Message, state: FSMContext):
    try:
        global address
        address = message.text
        if cur.execute(f"SELECT location FROM locations WHERE id = {message.from_user.id}").fetchone() == None:
            cur.execute("INSERT INTO locations VALUES (?, ?)", (address, message.from_user.id))
            con.commit()
        btn = await orderDone_reply()
        await message.answer(f"*Ваш заказ:*\n\n*Aдрес:* `{address}`\n\n_{showProducts}_\n*Товары:* `{sum} 000 сум`\n*Доставка:* `10 000 сум`\n*Итого:* `{final_sum} 000`", reply_markup=btn)
        cur.execute(f"UPDATE info_for_order SET adress = '{address}' WHERE id = {message.from_user.id}")
        con.commit()
        await UserStates.state1.set()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
# Подтверждение заказа
@dp.message_handler(text="Подтвердить ✅", state=UserStates.state1)
async def locationDone_check(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        tz = pytz.timezone('Asia/Tashkent')
        now_date = datetime.datetime.now(tz)
        date = now_date.strftime("%H:%M/%d.%m.%y")
        last_id = 1
        if cur.execute("SELECT order_id FROM orders").fetchone() != None:
            last_id = cur.execute("SELECT order_id FROM orders").fetchall()[-1][0] + 1
        cur.execute(f"UPDATE info_for_order SET date = '{date}' WHERE id = {message.from_user.id}")
        con.commit()
        data = cur.execute(f"SELECT * FROM info_for_order WHERE id = {message.from_user.id}").fetchone()
        cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)", (last_id, data[0], data[1], data[2], data[3], data[4], message.from_user.id))
        cur.execute(f"DELETE FROM korzina WHERE id = {message.from_user.id}")
        cur.execute(f"DELETE FROM info_for_order WHERE id = {message.from_user.id}")
        con.commit()
        btn = await startBot_reply()
        await message.answer("Ваш заказ выполняется. Спасибо за покупку!", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.message_handler(text="Назад ⬅️", state=UserStates.state1)
async def back_products(message: types.Message, state: FSMContext):
    try:
        btn = await adress_reply()
        await message.answer("Выберите адресс для доставки:", reply_markup=btn)
        await UserStates.location.set()
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)

# Режим администратора
@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):
    try:
        if message.from_user.id == 735815568:
            btn = await admin_inline()
            await message.answer("Выберите данные:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text="view_review")
async def view_review(call: types.CallbackQuery):
    try:
        data = cur.execute("SELECT * FROM reviews").fetchall()
        result = ""
        for i in range(len(data)):
            result = result + f"*Отзыв:* `{data[i][0]}`, *Звезды:* `{data[i][1]}`, *Пользователь:* `{data[i][2]}`.\n"
        btn = await adminBack_inline()
        await call.message.edit_text(result, reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text="back_review")
async def back_review(call: types.CallbackQuery):
    try:
        btn = await admin_inline()
        await call.message.edit_text("Выберите данные:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)

@dp.callback_query_handler(text="view_orders")
async def view_orders(call: types.CallbackQuery):
    try:
        if cur.execute(f"SELECT * FROM orders").fetchone() != None:
            orders = cur.execute(f"SELECT * FROM orders").fetchall()
            idList = []
            for i in range(len(orders)):
                idList.append(orders[i][0])
            btn = await adminOrders_inline(idList)
            await call.message.edit_text("Выберите заказы:", reply_markup=btn)
        else:
            btn = await adminBack_inline()
            await call.message.edit_text("Нету никаких заказов!", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text_contains="order2:")
async def myorders_handler(call: types.CallbackQuery):
    try:
        call_id = call.data.split(":")[1]
        allData = cur.execute(f"SELECT * FROM orders WHERE order_id = {call_id}").fetchone()
        orderId = allData[0]
        all_products = str(allData[1])
        all_products = all_products.split(",")
        for i in range(len(all_products)):
            all_products[i] = all_products[i].lstrip()
        result = ""
        for i in range(len(all_products)):
            result = result + f"▪️ {all_products[i]}\n"
        result = result.replace("'", "")
        result = result.replace("[", "")
        result = result.replace("]", "")
        adress_result = allData[2]
        phoneNumber_result = allData[3]
        price_result = str(allData[4])[:-3]
        date_result = allData[5]
        btn = await back2_inline()
        await call.message.edit_text(f"*Заказ № {orderId}:*\n\n_{result}_\n*Адрес: *`{adress_result}`\n*Номер телефона:* `{phoneNumber_result}`\n*Цена:* `{price_result} 000`\n*Дата:* `{date_result}`", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text="backToOrders2")
async def myordersBack_handler(call: types.CallbackQuery):
    try:
        orders = cur.execute(f"SELECT * FROM orders").fetchall()
        idList = []
        for i in range(len(orders)):
            idList.append(orders[i][0])
        btn = await adminOrders_inline(idList)
        await call.message.edit_text("Выберите заказы:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text="delete_order")
async def myOrdersDelete_handler(call: types.CallbackQuery):
    try:
        order_id = call.message.text.split(" № ")[1]
        order_id = int(order_id.split(":")[0])
        cur.execute(f"DELETE FROM orders WHERE order_id = {order_id}")
        con.commit()
        orders = cur.execute(f"SELECT * FROM orders").fetchall()
        idList = []
        for i in range(len(orders)):
            idList.append(orders[i][0])
        btn = await adminOrders_inline(idList)
        await call.message.edit_text("Выберите заказы:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)
@dp.callback_query_handler(text="backToAdminMenu")
async def adminMenuBack_handler(call: types.CallbackQuery):
    try:
        if call.from_user.id == 735815568:
            btn = await admin_inline()
            await call.message.edit_text("Выберите данные:", reply_markup=btn)
    except Exception as e:
        btn = await startBot_reply()
        await call.message.answer(f"Произошла ошибка: {e}", reply_markup=btn)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)