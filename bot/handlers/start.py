from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db import queries
from bot.i18n import t

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    chat_id = message.chat.id
    state = await queries.get_chat_state(chat_id)

    # Auto-detect language for new chats
    if not state.get("language"):
        user_lang = (message.from_user.language_code or "ru")[:2]
        lang = "en" if user_lang == "en" else "ru"
        await queries.set_language(chat_id, lang)
    else:
        lang = state["language"]

    await message.answer(t(lang, "welcome"))
