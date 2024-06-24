# bot.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay import *
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = '6804114220:AAHITURjgcBYYLn0nb4o03DQvXSJCD5c-14'
# Настройка логирования
logging.basicConfig(level=logging.INFO)

session = AiohttpSession(proxy="socks5://@47.242.34.249:33888")

crypto = AioCryptoPay(token='215084:AAyrwoP5mKQYQyXDwiCyWVIXk1OnK992t50', network=Networks.MAIN_NET)


# Создание экземпляров бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command('start'))
async def start_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доступ в чат", callback_data="buy")],
        [InlineKeyboardButton(text="Сапорт", callback_data="help")]
    ])
    await message.answer("Оплата подписки ниже:", reply_markup=keyboard)

# Обработка нажатий на инлайн-кнопки
@dp.callback_query()
async def handle_callback_query(callback_query: CallbackQuery):
    if callback_query.data == "buy":

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="CryptoBot", callback_data="buycryptobot")],
            [InlineKeyboardButton(text="Картой (РФ)", callback_data="buycard")]
            ])
        await callback_query.message.answer("Выберите способ: ", reply_markup = keyboard)

    elif callback_query.data == "buycryptobot":

        fiat_invoice = await crypto.create_invoice(amount=30, fiat='USD', currency_type='fiat')
        invoice_url = fiat_invoice.bot_invoice_url

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Оплата", url=f"{invoice_url}")]
        ])

        old_invoice = await crypto.get_invoices(invoice_ids=fiat_invoice.invoice_id)

        await callback_query.message.answer("Оплатите по кнопке ниже", reply_markup=keyboard)

        while old_invoice.status == 'active':
            await asyncio.sleep(10)  # Проверяем статус каждые 10 секунд
            old_invoice = await crypto.get_invoices(invoice_ids=fiat_invoice.invoice_id)  # Обновляем статус инвойса
            if old_invoice.status != 'active':
                break

        await bot.send_message(user_id, "<b>🥳 Бот получил оплату\n\n⏳ Отправка ссылки...</b>")
        # Добавьте сюда код для обработки платежа через CryptoBot API

    elif callback_query.data == "buycard":
        # Логика для оплаты картой РФ
        await callback_query.message.answer("Вы выбрали оплату картой (РФ).")
        # Добавьте сюда код для обработки платежа через API платежной системы для карт РФ

    elif callback_query.data == "help":
        await callback_query.message.answer("Вы выбрали Помощь.")
    await callback_query.answer()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
