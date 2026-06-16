from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db import queries
from bot.keyboards import nav_keyboard, switch_keyboard
from bot.services.ai import generate_category

router = Router()

_HINT = (
    "✍️ Опишите, какую категорию вопросов вы хотите.\n\n"
    "Можно указать <b>тему, характер и сложность</b> — чем подробнее, тем точнее результат.\n\n"
    "<b>Простые примеры:</b>\n"
    "• Про наши любимые фильмы и сериалы\n"
    "• Детство и школьные воспоминания\n\n"
    "<b>С характером:</b>\n"
    "• Смешные и абсурдные гипотетические ситуации\n"
    "• Глубокие философские вопросы про смысл жизни\n"
    "• Лёгкие игривые вопросы про еду и вкусы\n\n"
    "<b>Со сложностью:</b>\n"
    "• Простые вопросы про повседневные привычки\n"
    "• Сложные вопросы про ценности и жизненные выборы\n\n"
    "<b>Комбинированные:</b>\n"
    "• Лёгкие смешные вопросы про путешествия и странные места\n"
    "• Глубокие вопросы про страхи и то, что нас формирует\n"
    "• Провокационные вопросы-дилеммы в стиле «то или это»\n\n"
    "Я придумаю название и сгенерирую вопросы!"
)


@router.message(Command("generate"))
async def handle_generate_start(message: Message) -> None:
    await queries.set_awaiting_generate(message.chat.id, True)
    await message.answer(_HINT)


@router.message(F.text & ~F.text.startswith("/"))
async def handle_description_input(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    state = await queries.get_chat_state(chat_id)
    if not state.get("awaiting_generate"):
        return

    description = message.text.strip()
    await queries.set_awaiting_generate(chat_id, False)

    status = await message.reply("⏳ Генерирую категорию...")

    try:
        name, questions = await generate_category(description)

        if await queries.category_exists(name, chat_id):
            name = f"{name} 2"

        category_id = await queries.create_category(name, chat_id=chat_id, is_custom=True)
        await queries.bulk_insert_questions(category_id, questions)

        await status.edit_text(
            f"✅ Создана категория <b>{name}</b> — {len(questions)} вопросов.\n\n"
            "Переключиться на неё прямо сейчас?",
            reply_markup=switch_keyboard(category_id),
        )
    except Exception as exc:
        await queries.set_awaiting_generate(chat_id, False)
        await status.edit_text(f"❌ Ошибка: {exc}")


@router.callback_query(F.data.startswith("cat:extend:"))
async def handle_extend_category(callback: CallbackQuery, bot: Bot) -> None:
    category_id = int(callback.data.split(":")[2])
    category = await queries.get_category(category_id)
    if not category:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    status = await callback.message.answer(f"⏳ Генерирую ещё вопросы для «{category['name']}»...")

    try:
        _, questions = await generate_category(category["name"])
        await queries.bulk_insert_questions(category_id, questions)
        await status.edit_text(
            f"✅ Добавлено {len(questions)} новых вопросов в «{category['name']}»!",
            reply_markup=nav_keyboard(),
        )
    except Exception as exc:
        await status.edit_text(f"❌ Ошибка: {exc}")


@router.callback_query(F.data == "gen:stay")
async def handle_gen_stay(callback: CallbackQuery) -> None:
    await callback.answer("Продолжаем текущую категорию!")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
