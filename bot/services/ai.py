from __future__ import annotations

import json
import re
from openai import AsyncOpenAI
from bot.config import OPENROUTER_API_KEY
from bot.i18n import t

_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

_MODEL = "openrouter/free"


async def generate_category(
    description: str, count: int = 20, lang: str = "ru"
) -> tuple[str, list[str]]:
    """Ask AI to invent a category name and questions based on user description."""
    prompt = t(lang, "ai_prompt", description=description, count=count)

    response = await _client.chat.completions.create(
        model=_MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content.strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("Model did not return valid JSON" if lang == "en" else "Модель не вернула корректный JSON")

    data = json.loads(match.group())
    name: str = data["name"].strip()
    questions: list[str] = [
        q.strip() for q in data["questions"] if isinstance(q, str) and q.strip()
    ]
    if not name or not questions:
        raise ValueError("Model returned empty data" if lang == "en" else "Модель вернула пустые данные")

    return name, questions
