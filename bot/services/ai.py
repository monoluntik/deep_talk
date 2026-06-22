import json
import asyncio
import anthropic
from bot.config import ANTHROPIC_API_KEY

_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
_MODEL = "claude-haiku-4-5-20251001"


async def generate_category(description: str, count: int = 20) -> tuple[str, list[str]]:
    prompt = (
        f"Пользователь хочет категорию вопросов: «{description}»\n\n"
        f"Сгенерируй:\n"
        f"1. Короткое название категории (2-4 слова, добавь подходящий эмодзи в начало)\n"
        f"2. {count} уникальных вопросов для устного обсуждения\n"
        "   - Разнообразные: лёгкие, глубокие, философские, игривые\n"
        "   - Без повторений\n\n"
        "Верни ТОЛЬКО JSON в формате:\n"
        '{"name": "🎬 Название", "questions": ["Вопрос 1?", "Вопрос 2?"]}'
    )

    last_err: Exception | None = None
    for attempt in range(3):
        try:
            message = await _client.messages.create(
                model=_MODEL,
                max_tokens=4096,
                temperature=1.0,
                messages=[
                    {"role": "user", "content": prompt},
                    # префилл: заставляет модель начать ответ с "{" — никакой преамбулы
                    {"role": "assistant", "content": "{"},
                ],
            )
            text = "{" + "".join(
                block.text for block in message.content if block.type == "text"
            )
            data = json.loads(text)

            name = str(data["name"]).strip()
            questions = [
                q.strip() for q in data.get("questions", [])
                if isinstance(q, str) and q.strip()
            ]
            if not name or not questions:
                raise ValueError("модель вернула пустые данные")
            return name, questions[:count]

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            last_err = e
        except (anthropic.RateLimitError, anthropic.APIStatusError) as e:
            last_err = e
            await asyncio.sleep(2 ** attempt)

    raise RuntimeError(f"Не удалось сгенерировать категорию: {last_err}")
