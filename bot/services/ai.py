import json
import re
import anthropic
from bot.config import ANTHROPIC_API_KEY

_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
_MODEL = "claude-haiku-4-5-20251001"


async def generate_category(description: str, count: int = 20) -> tuple[str, list[str]]:
    message = await _client.messages.create(
        model=_MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": (
                f"Пользователь хочет категорию вопросов: «{description}»\n\n"
                f"Сгенерируй:\n"
                f"1. Короткое название категории (2-4 слова, добавь подходящий эмодзи в начало)\n"
                f"2. {count} уникальных вопросов для устного обсуждения\n"
                "   - Разнообразные: лёгкие, глубокие, философские, игривые\n"
                "   - Без повторений\n\n"
                "Верни ТОЛЬКО JSON без пояснений:\n"
                '{"name": "🎬 Название", "questions": ["Вопрос 1?", "Вопрос 2?", ...]}'
            ),
        }],
    )

    text = message.content[0].text.strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("Модель не вернула корректный JSON")

    data = json.loads(match.group())
    name: str = data["name"].strip()
    questions: list[str] = [
        q.strip() for q in data["questions"] if isinstance(q, str) and q.strip()
    ]
    if not name or not questions:
        raise ValueError("Модель вернула пустые данные")

    return name, questions
