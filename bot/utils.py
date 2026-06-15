from typing import Optional
from aiogram import Bot
from bot.keyboards import nav_keyboard


def format_question(category_name: str, question_text: str) -> str:
    return f"<b>{category_name}</b>\n\n{question_text}"


async def send_question(
    bot: Bot,
    chat_id: int,
    category_name: str,
    question_text: str,
    old_message_id: Optional[int] = None,
) -> int:
    # Remove buttons from the previous question message
    if old_message_id:
        try:
            await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=old_message_id,
                reply_markup=None,
            )
        except Exception:
            pass

    msg = await bot.send_message(
        chat_id=chat_id,
        text=format_question(category_name, question_text),
        reply_markup=nav_keyboard(),
    )
    return msg.message_id
