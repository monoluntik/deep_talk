from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.keyboards import category_keyboard, confirm_delete_keyboard
from bot.utils import send_question

router = Router()


async def _show_menu(chat_id: int, bot: Bot) -> None:
    categories = await queries.get_categories(chat_id)
    if not categories:
        await bot.send_message(chat_id, "Пока нет категорий.\nИспользуйте /generate чтобы создать первую!")
        return
    await bot.send_message(chat_id, "Выберите категорию:", reply_markup=category_keyboard(categories))


@router.message(Command("menu"))
async def handle_menu(message: Message, bot: Bot) -> None:
    await _show_menu(message.chat.id, bot)


@router.callback_query(F.data == "menu:show")
async def handle_menu_callback(callback: CallbackQuery, bot: Bot) -> None:
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await _show_menu(callback.message.chat.id, bot)


@router.callback_query(F.data.regexp(r"^cat:\d+$"))
async def handle_category_select(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[1])
    chat_id = callback.message.chat.id

    category = await queries.get_category(category_id)
    if not category:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    await queries.set_chat_category(chat_id, category_id)

    q = await queries.pick_next_question(chat_id, category_id)
    if not q:
        await callback.answer()
        await callback.message.edit_text(
            f"🎉 Вы прошли все вопросы из «{category['name']}»!\n\n"
            "Используйте /generate чтобы создать новые вопросы,\n"
            "или /menu чтобы выбрать другую категорию."
        )
        return

    seq = await queries.add_to_history(chat_id, q["id"])
    state = await queries.get_chat_state(chat_id)

    try:
        await callback.message.delete()
    except Exception:
        pass

    msg_id = await send_question(bot, chat_id, category["name"], q["text"], state["question_message_id"])
    await queries.set_history_cursor(chat_id, seq, msg_id)
    await callback.answer()


@router.callback_query(F.data.regexp(r"^cat:delete:\d+$"))
async def handle_delete_request(callback: CallbackQuery) -> None:
    category_id = int(callback.data.split(":")[2])
    category = await queries.get_category(category_id)
    if not category:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    await callback.answer()
    await callback.message.edit_text(
        f"Удалить категорию «{category['name']}»?\n"
        "Все вопросы и история просмотров будут сохранены.",
        reply_markup=confirm_delete_keyboard(category_id),
    )


@router.callback_query(F.data.regexp(r"^cat:delete:confirm:\d+$"))
async def handle_delete_confirm(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[3])
    category = await queries.get_category(category_id)
    cat_name = category["name"] if category else "категория"

    await queries.delete_category(category_id)
    await callback.answer(f"«{cat_name}» удалена.")

    try:
        await callback.message.delete()
    except Exception:
        pass
    await _show_menu(callback.message.chat.id, bot)


@router.callback_query(F.data == "cat:delete:cancel")
async def handle_delete_cancel(callback: CallbackQuery, bot: Bot) -> None:
    await callback.answer("Отменено.")
    try:
        await callback.message.delete()
    except Exception:
        pass
    await _show_menu(callback.message.chat.id, bot)
