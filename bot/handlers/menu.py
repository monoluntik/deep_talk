from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.i18n import t
from bot.keyboards import category_keyboard, confirm_delete_keyboard
from bot.utils import send_question

router = Router()


async def _show_menu(chat_id: int, bot: Bot, lang: str) -> None:
    categories = await queries.get_categories(chat_id, lang)
    if not categories:
        await bot.send_message(chat_id, t(lang, "menu_empty"))
        return
    await bot.send_message(chat_id, t(lang, "menu_title"), reply_markup=category_keyboard(categories, lang))


@router.message(Command("menu"))
async def handle_menu(message: Message, bot: Bot) -> None:
    lang = await queries.get_language(message.chat.id)
    await _show_menu(message.chat.id, bot, lang)


@router.callback_query(F.data == "menu:show")
async def handle_menu_callback(callback: CallbackQuery, bot: Bot) -> None:
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    lang = await queries.get_language(callback.message.chat.id)
    await _show_menu(callback.message.chat.id, bot, lang)


@router.callback_query(F.data.regexp(r"^cat:\d+$"))
async def handle_category_select(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[1])
    chat_id = callback.message.chat.id
    lang = await queries.get_language(chat_id)

    category = await queries.get_category(category_id)
    if not category:
        await callback.answer(t(lang, "cat_not_found"), show_alert=True)
        return

    await queries.set_chat_category(chat_id, category_id)

    q = await queries.pick_next_question(chat_id, category_id)
    if not q:
        await callback.answer()
        await callback.message.edit_text(t(lang, "cat_all_done", name=category["name"]))
        return

    seq = await queries.add_to_history(chat_id, q["id"])
    state = await queries.get_chat_state(chat_id)

    try:
        await callback.message.delete()
    except Exception:
        pass

    msg_id = await send_question(bot, chat_id, category["name"], q["text"], state["question_message_id"], lang)
    await queries.set_history_cursor(chat_id, seq, msg_id)
    await callback.answer()


@router.callback_query(F.data.regexp(r"^cat:delete:\d+$"))
async def handle_delete_request(callback: CallbackQuery) -> None:
    category_id = int(callback.data.split(":")[2])
    lang = await queries.get_language(callback.message.chat.id)
    category = await queries.get_category(category_id)
    if not category:
        await callback.answer(t(lang, "cat_not_found"), show_alert=True)
        return

    await callback.answer()
    await callback.message.edit_text(
        t(lang, "delete_confirm", name=category["name"]),
        reply_markup=confirm_delete_keyboard(category_id, lang),
    )


@router.callback_query(F.data.regexp(r"^cat:delete:confirm:\d+$"))
async def handle_delete_confirm(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[3])
    lang = await queries.get_language(callback.message.chat.id)
    category = await queries.get_category(category_id)
    cat_name = category["name"] if category else ""

    await queries.delete_category(category_id)
    await callback.answer(t(lang, "deleted", name=cat_name))

    try:
        await callback.message.delete()
    except Exception:
        pass
    await _show_menu(callback.message.chat.id, bot, lang)


@router.callback_query(F.data == "cat:delete:cancel")
async def handle_delete_cancel(callback: CallbackQuery, bot: Bot) -> None:
    lang = await queries.get_language(callback.message.chat.id)
    await callback.answer(t(lang, "cancelled"))
    try:
        await callback.message.delete()
    except Exception:
        pass
    await _show_menu(callback.message.chat.id, bot, lang)
