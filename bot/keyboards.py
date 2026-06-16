from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.i18n import t


def nav_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "btn_next"), callback_data="nav:next"),
    ]])


def category_keyboard(categories: list[dict], lang: str = "ru") -> InlineKeyboardMarkup:
    rows = []
    for cat in categories:
        row = [InlineKeyboardButton(text=cat["name"], callback_data=f"cat:{cat['id']}")]
        if cat.get("is_custom"):
            row.append(InlineKeyboardButton(text="🗑", callback_data=f"cat:delete:{cat['id']}"))
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_delete_keyboard(category_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "btn_delete_confirm"), callback_data=f"cat:delete:confirm:{category_id}"),
        InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="cat:delete:cancel"),
    ]])


def exhausted_keyboard(category_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_extend"), callback_data=f"cat:extend:{category_id}")],
        [InlineKeyboardButton(text=t(lang, "btn_change_cat"), callback_data="menu:show")],
    ])


def donate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⭐ 1", callback_data="donate:1"),
        InlineKeyboardButton(text="⭐ 5", callback_data="donate:5"),
        InlineKeyboardButton(text="⭐ 10", callback_data="donate:10"),
        InlineKeyboardButton(text="⭐ 25", callback_data="donate:25"),
    ]])


def switch_keyboard(category_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "btn_switch"), callback_data=f"cat:{category_id}"),
        InlineKeyboardButton(text=t(lang, "btn_stay"), callback_data="gen:stay"),
    ]])


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
    ]])
