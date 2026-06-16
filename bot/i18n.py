from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "welcome": (
            "Привет! 👋\n\n"
            "<b>Deep Talk</b> — бот для живых разговоров. Не «как дела» и «нормально», а настоящих.\n\n"
            "Бот присылает вопрос — вы обсуждаете его голосом или текстом прямо в чате. "
            "Никаких правил, никакого таймера. Подходит для любой компании.\n\n"
            "<b>Команды:</b>\n"
            "🗂 /menu — выбрать категорию вопросов\n"
            "⏭ Кнопка под вопросом — следующий вопрос\n"
            "💬 /current — показать текущий вопрос снова\n"
            "✨ /generate — создать свою категорию через ИИ\n"
            "🌐 /language — сменить язык\n"
            "❤️ /donate — поддержать бота\n\n"
            "<b>Базовые категории:</b>\n"
            "🎭 <b>То или Это</b> — дилеммы и выборы\n"
            "💬 <b>Узнай меня лучше</b> — открытые вопросы\n\n"
            "Начните с /menu 👇"
        ),
        "menu_empty": "Пока нет категорий.\nИспользуйте /generate чтобы создать первую!",
        "menu_title": "Выберите категорию:",
        "cat_not_found": "Категория не найдена.",
        "cat_all_done": (
            "🎉 Вы прошли все вопросы из «{name}»!\n\n"
            "Используйте /generate чтобы создать новые вопросы,\n"
            "или /menu чтобы выбрать другую категорию."
        ),
        "delete_confirm": (
            "Удалить категорию «{name}»?\n"
            "Все вопросы и история просмотров будут сохранены."
        ),
        "deleted": "«{name}» удалена.",
        "cancelled": "Отменено.",
        "no_category": "Выберите категорию через /menu",
        "no_active_question": "Нет активного вопроса. Используйте /menu чтобы начать.",
        "question_not_found": "Не удалось найти текущий вопрос.",
        "exhausted": "🎉 Все вопросы из «{name}» пройдены!",
        "nav_error": "Ошибка навигации.",
        "generate_hint": (
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
        ),
        "generate_status": "⏳ Генерирую категорию...",
        "generate_success": "✅ Создана категория <b>{name}</b> — {count} вопросов.\n\nПереключиться на неё прямо сейчас?",
        "generate_error": "❌ Ошибка: {error}",
        "extend_status": "⏳ Генерирую ещё вопросы для «{name}»...",
        "extend_success": "✅ Добавлено {count} новых вопросов в «{name}»!",
        "gen_stay": "Продолжаем текущую категорию!",
        "donate_intro": (
            "❤️ Спасибо, что хотите поддержать <b>Deep Talk</b>!\n\n"
            "Бот работает бесплатно — ваша поддержка помогает оплачивать сервер "
            "и развивать новые функции.\n\n"
            "Выберите количество Stars:"
        ),
        "donate_title": "Поддержать Deep Talk",
        "donate_description": "Спасибо! Ваш вклад помогает боту работать и развиваться",
        "donate_thanks": "⭐ Получено {stars} {word} — огромное спасибо!\nЭто очень мотивирует развивать Deep Talk дальше ❤️",
        "donate_stars_one": "Star",
        "donate_stars_many": "Stars",
        "choose_language": "🌐 Выберите язык / Choose language:",
        "language_set": "🇷🇺 Язык изменён на <b>русский</b>.",
        # keyboard buttons
        "btn_next": "⏭ Следующий вопрос",
        "btn_delete_confirm": "✅ Удалить",
        "btn_cancel": "❌ Отмена",
        "btn_extend": "➕ Дополнить вопросами",
        "btn_change_cat": "📂 Сменить категорию",
        "btn_switch": "✅ Переключиться",
        "btn_stay": "❌ Остаться",
        "ai_prompt": (
            "Пользователь хочет категорию вопросов: «{description}»\n\n"
            "Сгенерируй:\n"
            "1. Короткое название категории (2-4 слова, добавь подходящий эмодзи в начало)\n"
            "2. {count} уникальных вопросов для устного обсуждения\n"
            "   - Разнообразные: лёгкие, глубокие, философские, игривые\n"
            "   - Без повторений\n\n"
            "Верни ТОЛЬКО JSON без пояснений:\n"
            '{{\"name\": \"🎬 Название\", \"questions\": [\"Вопрос 1?\", \"Вопрос 2?\", ...]}}'
        ),
    },
    "en": {
        "welcome": (
            "Hi! 👋\n\n"
            "<b>Deep Talk</b> — a bot for real conversations. Not just \"how are you\" and \"fine\", but genuine ones.\n\n"
            "The bot sends a question — you discuss it by voice or text right in the chat. "
            "No rules, no timer. Works for any group.\n\n"
            "<b>Commands:</b>\n"
            "🗂 /menu — choose a question category\n"
            "⏭ Button below question — next question\n"
            "💬 /current — show the current question again\n"
            "✨ /generate — create your own category with AI\n"
            "🌐 /language — change language\n"
            "❤️ /donate — support the bot\n\n"
            "<b>Base categories:</b>\n"
            "🎭 <b>This or That</b> — dilemmas and choices\n"
            "💬 <b>Get to Know Me</b> — open-ended questions\n\n"
            "Start with /menu 👇"
        ),
        "menu_empty": "No categories yet.\nUse /generate to create the first one!",
        "menu_title": "Choose a category:",
        "cat_not_found": "Category not found.",
        "cat_all_done": (
            "🎉 You've gone through all questions in «{name}»!\n\n"
            "Use /generate to create new questions,\n"
            "or /menu to choose another category."
        ),
        "delete_confirm": (
            "Delete category «{name}»?\n"
            "All questions and view history will be preserved."
        ),
        "deleted": "«{name}» deleted.",
        "cancelled": "Cancelled.",
        "no_category": "Choose a category via /menu",
        "no_active_question": "No active question. Use /menu to start.",
        "question_not_found": "Could not find the current question.",
        "exhausted": "🎉 All questions from «{name}» completed!",
        "nav_error": "Navigation error.",
        "generate_hint": (
            "✍️ Describe the question category you want.\n\n"
            "You can specify the <b>topic, tone, and difficulty</b> — the more detail, the better.\n\n"
            "<b>Simple examples:</b>\n"
            "• Our favorite movies and shows\n"
            "• Childhood and school memories\n\n"
            "<b>With tone:</b>\n"
            "• Funny and absurd hypothetical situations\n"
            "• Deep philosophical questions about the meaning of life\n"
            "• Light playful questions about food and tastes\n\n"
            "<b>With difficulty:</b>\n"
            "• Easy questions about everyday habits\n"
            "• Hard questions about values and life choices\n\n"
            "<b>Combined:</b>\n"
            "• Light funny questions about travel and weird places\n"
            "• Deep questions about fears and what shaped us\n"
            "• Provocative dilemma-style \"this or that\" questions\n\n"
            "I'll come up with a name and generate the questions!"
        ),
        "generate_status": "⏳ Generating category...",
        "generate_success": "✅ Category <b>{name}</b> created — {count} questions.\n\nSwitch to it right now?",
        "generate_error": "❌ Error: {error}",
        "extend_status": "⏳ Generating more questions for «{name}»...",
        "extend_success": "✅ Added {count} new questions to «{name}»!",
        "gen_stay": "Continuing with the current category!",
        "donate_intro": (
            "❤️ Thank you for wanting to support <b>Deep Talk</b>!\n\n"
            "The bot is free — your support helps pay for the server "
            "and develop new features.\n\n"
            "Choose the number of Stars:"
        ),
        "donate_title": "Support Deep Talk",
        "donate_description": "Thank you! Your contribution helps the bot run and grow",
        "donate_thanks": "⭐ Received {stars} {word} — thank you so much!\nThis really motivates us to keep developing Deep Talk ❤️",
        "donate_stars_one": "Star",
        "donate_stars_many": "Stars",
        "choose_language": "🌐 Выберите язык / Choose language:",
        "language_set": "🇬🇧 Language changed to <b>English</b>.",
        # keyboard buttons
        "btn_next": "⏭ Next question",
        "btn_delete_confirm": "✅ Delete",
        "btn_cancel": "❌ Cancel",
        "btn_extend": "➕ Add more questions",
        "btn_change_cat": "📂 Change category",
        "btn_switch": "✅ Switch",
        "btn_stay": "❌ Stay",
        "ai_prompt": (
            "The user wants a question category: \"{description}\"\n\n"
            "Generate:\n"
            "1. A short category name (2-4 words, add a fitting emoji at the start)\n"
            "2. {count} unique questions for verbal discussion\n"
            "   - Varied: easy, deep, philosophical, playful\n"
            "   - No repetitions\n\n"
            "Return ONLY JSON with no explanation:\n"
            '{{\"name\": \"🎬 Name\", \"questions\": [\"Question 1?\", \"Question 2?\", ...]}}'
        ),
    },
}


def t(lang: str, key: str, **kwargs: object) -> str:
    strings = STRINGS.get(lang, STRINGS["ru"])
    text = strings.get(key) or STRINGS["ru"].get(key, key)
    return text.format(**kwargs) if kwargs else text
