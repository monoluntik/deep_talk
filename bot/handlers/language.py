from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.i18n import t
from bot.keyboards import language_keyboard

router = Router()


@router.message(Command("language"))
async def handle_language(message: Message) -> None:
    lang = await queries.get_language(message.chat.id)
    await message.answer(t(lang, "choose_language"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def handle_language_select(callback: CallbackQuery) -> None:
    new_lang = callback.data.split(":")[1]
    if new_lang not in ("ru", "en"):
        await callback.answer()
        return

    await queries.set_language(callback.message.chat.id, new_lang)
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await callback.message.answer(t(new_lang, "language_set"))
