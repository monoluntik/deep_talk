from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.i18n import t
from bot.keyboards import category_keyboard, language_keyboard

router = Router()

_FLAG = {"ru": "🇷🇺", "en": "🇬🇧"}
_LABEL = {"ru": "Русский", "en": "English"}


@router.message(Command("language"))
async def handle_language(message: Message) -> None:
    lang = await queries.get_language(message.chat.id)
    current = f"{_FLAG[lang]} {_LABEL[lang]}"
    await message.answer(
        f"{t(lang, 'choose_language')}\n<i>Current / Текущий: {current}</i>",
        reply_markup=language_keyboard(),
    )


@router.callback_query(F.data.startswith("lang:"))
async def handle_language_select(callback: CallbackQuery, bot: Bot) -> None:
    new_lang = callback.data.split(":")[1]
    if new_lang not in ("ru", "en"):
        await callback.answer()
        return

    chat_id = callback.message.chat.id
    await queries.set_language(chat_id, new_lang)
    await queries.reset_category(chat_id)

    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.message.answer(t(new_lang, "language_set"))

    # Show menu in new language right away
    categories = await queries.get_categories(chat_id, new_lang)
    if categories:
        await bot.send_message(
            chat_id,
            t(new_lang, "menu_title"),
            reply_markup=category_keyboard(categories, new_lang),
        )
    else:
        await bot.send_message(chat_id, t(new_lang, "menu_empty"))
