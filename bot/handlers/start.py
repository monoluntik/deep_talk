from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! 👋\n\n"
        "<b>Deep Talk</b> — бот для живых разговоров. Не «как дела» и «нормально», а настоящих.\n\n"
        "Бот присылает вопрос — вы обсуждаете его голосом или текстом прямо в чате. "
        "Никаких правил, никакого таймера. Подходит для любой компании.\n\n"
        "<b>Команды:</b>\n"
        "🗂 /menu — выбрать категорию вопросов\n"
        "⏭ Кнопка под вопросом — следующий вопрос\n"
        "💬 /current — показать текущий вопрос снова\n"
        "✨ /generate — создать свою категорию через ИИ\n"
        "❤️ /donate — поддержать бота\n\n"
        "<b>Базовые категории:</b>\n"
        "🎭 <b>То или Это</b> — дилеммы и выборы\n"
        "💬 <b>Узнай меня лучше</b> — открытые вопросы\n\n"
        "Начните с /menu 👇"
    )
