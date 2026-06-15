from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from bot.keyboards import donate_keyboard

router = Router()


@router.message(Command("donate"))
async def handle_donate(message: Message) -> None:
    await message.answer(
        "❤️ Спасибо, что хотите поддержать <b>Deep Talk</b>!\n\n"
        "Бот работает бесплатно — ваша поддержка помогает оплачивать сервер "
        "и развивать новые функции.\n\n"
        "Выберите количество Stars:",
        reply_markup=donate_keyboard(),
    )


@router.callback_query(F.data.startswith("donate:"))
async def handle_donate_amount(callback: CallbackQuery, bot: Bot) -> None:
    amount = int(callback.data.split(":")[1])
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Поддержать Deep Talk",
        description=f"Спасибо! Ваш вклад помогает боту работать и развиваться {'⭐' * min(amount, 10)}",
        payload=f"donate_{amount}",
        currency="XTR",
        prices=[LabeledPrice(label="Telegram Stars", amount=amount)],
    )


@router.pre_checkout_query()
async def handle_pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def handle_successful_payment(message: Message) -> None:
    stars = message.successful_payment.total_amount
    await message.answer(
        f"⭐ Получено {stars} {'Star' if stars == 1 else 'Stars'} — огромное спасибо!\n"
        "Это очень мотивирует развивать Deep Talk дальше ❤️"
    )
