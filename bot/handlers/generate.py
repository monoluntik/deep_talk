from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.i18n import t
from bot.keyboards import nav_keyboard, switch_keyboard
from bot.services.ai import generate_category

router = Router()


@router.message(Command("generate"))
async def handle_generate_start(message: Message) -> None:
    lang = await queries.get_language(message.chat.id)
    await queries.set_awaiting_generate(message.chat.id, True)
    await message.answer(t(lang, "generate_hint"))


@router.message(F.text & ~F.text.startswith("/"))
async def handle_description_input(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    state = await queries.get_chat_state(chat_id)
    if not state.get("awaiting_generate"):
        return

    lang = state.get("language") or "ru"
    description = message.text.strip()
    await queries.set_awaiting_generate(chat_id, False)

    status = await message.reply(t(lang, "generate_status"))

    try:
        name, questions = await generate_category(description, lang=lang)

        if await queries.category_exists(name, chat_id):
            name = f"{name} 2"

        category_id = await queries.create_category(name, chat_id=chat_id, is_custom=True, language=lang)
        await queries.bulk_insert_questions(category_id, questions)

        await status.edit_text(
            t(lang, "generate_success", name=name, count=len(questions)),
            reply_markup=switch_keyboard(category_id, lang),
        )
    except Exception as exc:
        await queries.set_awaiting_generate(chat_id, False)
        await status.edit_text(t(lang, "generate_error", error=exc))


@router.callback_query(F.data.startswith("cat:extend:"))
async def handle_extend_category(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[2])
    lang = await queries.get_language(callback.message.chat.id)
    category = await queries.get_category(category_id)
    if not category:
        await callback.answer(t(lang, "cat_not_found"), show_alert=True)
        return

    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    status = await callback.message.answer(t(lang, "extend_status", name=category["name"]))

    try:
        _, questions = await generate_category(category["name"], lang=lang)
        await queries.bulk_insert_questions(category_id, questions)
        await status.edit_text(
            t(lang, "extend_success", count=len(questions), name=category["name"]),
            reply_markup=nav_keyboard(lang),
        )
    except Exception as exc:
        await status.edit_text(t(lang, "generate_error", error=exc))


@router.callback_query(F.data == "gen:stay")
async def handle_gen_stay(callback: CallbackQuery) -> None:
    lang = await queries.get_language(callback.message.chat.id)
    await callback.answer(t(lang, "gen_stay"))
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
