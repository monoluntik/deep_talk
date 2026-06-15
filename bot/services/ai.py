import json
import re
from openai import AsyncOpenAI
from bot.config import OPENROUTER_API_KEY

_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

_MODEL = "openrouter/free"


async def generate_category(description: str, count: int = 20) -> tuple[str, list[str]]:
    """Ask AI to invent a category name and questions based on user description."""
    response = await _client.chat.completions.create(
        model=_MODEL,
        max_tokens=8192,
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

    text = response.choices[0].message.content.strip()
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
