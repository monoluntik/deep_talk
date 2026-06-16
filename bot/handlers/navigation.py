from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.keyboards import exhausted_keyboard
from bot.utils import send_question

router = Router()

_EXHAUSTED = "exhausted"
_NO_CATEGORY = "no_category"


async def _do_next(bot: Bot, chat_id: int, old_message_id: int | None) -> str | None:
    state = await queries.get_chat_state(chat_id)
    category_id = state["current_category_id"]
    cursor = state["history_cursor"]

    next_cursor = await queries.get_next_cursor(chat_id, cursor)

    if next_cursor is None:
        if not category_id:
            return _NO_CATEGORY

        q_raw = await queries.pick_next_question(chat_id, category_id)
        if not q_raw:
            return _EXHAUSTED

        next_cursor = await queries.add_to_history(chat_id, q_raw["id"])

    q = await queries.get_question_at_cursor(chat_id, next_cursor)
    if not q:
        return "Ошибка навигации."

    msg_id = await send_question(bot, chat_id, q["category_name"], q["text"], old_message_id)
    await queries.set_history_cursor(chat_id, next_cursor, msg_id)
    return None


async def _send_exhausted(bot: Bot, chat_id: int, old_message_id: int | None, category_id: int) -> None:
    category = await queries.get_category(category_id)
    cat_name = category["name"] if category else "этой категории"

    if old_message_id:
        try:
            await bot.edit_message_reply_markup(
                chat_id=chat_id, message_id=old_message_id, reply_markup=None
            )
        except Exception:
            pass

    await bot.send_message(
        chat_id=chat_id,
        text=f"🎉 Все вопросы из «{cat_name}» пройдены!",
        reply_markup=exhausted_keyboard(category_id),
    )


@router.callback_query(F.data == "nav:next")
async def handle_next_callback(callback: CallbackQuery, bot: Bot) -> None:
    chat_id = callback.message.chat.id
    state = await queries.get_chat_state(chat_id)

    result = await _do_next(bot, chat_id, state["question_message_id"])
    await callback.answer()

    if result == _EXHAUSTED:
        await _send_exhausted(bot, chat_id, state["question_message_id"], state["current_category_id"])
    elif result == _NO_CATEGORY:
        await bot.send_message(chat_id, "Выберите категорию через /menu")
    elif result:
        await bot.send_message(chat_id, result)


@router.message(Command("next"))
async def handle_next_command(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    state = await queries.get_chat_state(chat_id)

    try:
        await message.delete()
    except Exception:
        pass

    result = await _do_next(bot, chat_id, state["question_message_id"])

    if result == _EXHAUSTED:
        await _send_exhausted(bot, chat_id, state["question_message_id"], state["current_category_id"])
    elif result:
        await bot.send_message(chat_id, result)


@router.message(Command("current"))
async def handle_current(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    state = await queries.get_chat_state(chat_id)

    try:
        await message.delete()
    except Exception:
        pass

    if state["history_cursor"] < 0 or state["current_category_id"] is None:
        await bot.send_message(chat_id, "Нет активного вопроса. Используйте /menu чтобы начать.")
        return

    q = await queries.get_question_at_cursor(chat_id, state["history_cursor"])
    if not q:
        await bot.send_message(chat_id, "Не удалось найти текущий вопрос.")
        return

    msg_id = await send_question(bot, chat_id, q["category_name"], q["text"], state["question_message_id"])
    await queries.set_history_cursor(chat_id, state["history_cursor"], msg_id)
