from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def nav_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⏭ Следующий вопрос", callback_data="nav:next"),
    ]])


def category_keyboard(categories: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for cat in categories:
        row = [InlineKeyboardButton(text=cat["name"], callback_data=f"cat:{cat['id']}")]
        if cat.get("is_custom"):
            row.append(InlineKeyboardButton(text="🗑", callback_data=f"cat:delete:{cat['id']}"))
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_delete_keyboard(category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Удалить", callback_data=f"cat:delete:confirm:{category_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cat:delete:cancel"),
    ]])


def exhausted_keyboard(category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Дополнить вопросами", callback_data=f"cat:extend:{category_id}")],
        [InlineKeyboardButton(text="📂 Сменить категорию", callback_data="menu:show")],
    ])


def donate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⭐ 1", callback_data="donate:1"),
        InlineKeyboardButton(text="⭐ 5", callback_data="donate:5"),
        InlineKeyboardButton(text="⭐ 10", callback_data="donate:10"),
        InlineKeyboardButton(text="⭐ 25", callback_data="donate:25"),
    ]])


def switch_keyboard(category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Переключиться", callback_data=f"cat:{category_id}"),
        InlineKeyboardButton(text="❌ Остаться", callback_data="gen:stay"),
    ]])
