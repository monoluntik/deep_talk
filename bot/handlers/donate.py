from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from bot.db import queries
from bot.i18n import t
from bot.keyboards import donate_keyboard

router = Router()


@router.message(Command("donate"))
async def handle_donate(message: Message) -> None:
    lang = await queries.get_language(message.chat.id)
    await message.answer(t(lang, "donate_intro"), reply_markup=donate_keyboard())


@router.callback_query(F.data.startswith("donate:"))
async def handle_donate_amount(callback: CallbackQuery, bot: Bot) -> None:
    amount = int(callback.data.split(":")[1])
    lang = await queries.get_language(callback.message.chat.id)
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=t(lang, "donate_title"),
        description=f"{t(lang, 'donate_description')} {'⭐' * min(amount, 10)}",
        payload=f"donate_{amount}",
        currency="XTR",
        prices=[LabeledPrice(label="Telegram Stars", amount=amount)],
    )


@router.pre_checkout_query()
async def handle_pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def handle_successful_payment(message: Message) -> None:
    lang = await queries.get_language(message.chat.id)
    stars = message.successful_payment.total_amount
    word = t(lang, "donate_stars_one") if stars == 1 else t(lang, "donate_stars_many")
    await message.answer(t(lang, "donate_thanks", stars=stars, word=word))
