from __future__ import annotations

from typing import Optional
import aiosqlite
from bot.config import DATABASE_PATH


# ── categories ───────────────────────────────────────────────────────────────

async def get_categories(chat_id: int, lang: str = "ru") -> list[dict]:
    """Return global base categories for this language + custom categories for this chat."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, name, is_custom FROM categories "
            "WHERE (is_custom = 0 AND language = ?) OR (is_custom = 1 AND chat_id = ?) "
            "ORDER BY is_custom ASC, id ASC",
            (lang, chat_id),
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_category(category_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, name FROM categories WHERE id = ?", (category_id,)
        ) as cur:
            row = await cur.fetchone()
    return dict(row) if row else None


async def category_exists(name: str, chat_id: Optional[int]) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        if chat_id is None:
            async with db.execute(
                "SELECT 1 FROM categories WHERE name = ? AND chat_id IS NULL", (name,)
            ) as cur:
                return await cur.fetchone() is not None
        else:
            async with db.execute(
                "SELECT 1 FROM categories WHERE name = ? AND chat_id = ?",
                (name, chat_id),
            ) as cur:
                return await cur.fetchone() is not None


async def delete_category(category_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE chat_state SET current_category_id = NULL WHERE current_category_id = ?",
            (category_id,),
        )
        await db.execute("DELETE FROM categories WHERE id = ? AND is_custom = 1", (category_id,))
        await db.commit()


async def create_category(
    name: str,
    chat_id: Optional[int] = None,
    is_custom: bool = True,
    language: str = "ru",
) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "INSERT INTO categories (name, is_custom, chat_id, language) VALUES (?, ?, ?, ?)",
            (name, 1 if is_custom else 0, chat_id, language),
        ) as cur:
            category_id = cur.lastrowid
        await db.commit()
    return category_id


async def bulk_insert_questions(category_id: int, texts: list[str]) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executemany(
            "INSERT INTO questions (category_id, text) VALUES (?, ?)",
            [(category_id, t) for t in texts],
        )
        await db.commit()


# ── chat state ───────────────────────────────────────────────────────────────

async def get_chat_state(chat_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT current_category_id, history_cursor, question_message_id, "
            "awaiting_generate, language "
            "FROM chat_state WHERE chat_id = ?",
            (chat_id,),
        ) as cur:
            row = await cur.fetchone()
    return dict(row) if row else {
        "current_category_id": None,
        "history_cursor": -1,
        "question_message_id": None,
        "awaiting_generate": 0,
        "language": "ru",
    }


async def _ensure_state(db: aiosqlite.Connection, chat_id: int) -> None:
    await db.execute(
        "INSERT OR IGNORE INTO chat_state (chat_id, history_cursor) VALUES (?, -1)",
        (chat_id,),
    )


async def get_language(chat_id: int) -> str:
    state = await get_chat_state(chat_id)
    return state.get("language") or "ru"


async def set_language(chat_id: int, lang: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await _ensure_state(db, chat_id)
        await db.execute(
            "UPDATE chat_state SET language = ? WHERE chat_id = ?",
            (lang, chat_id),
        )
        await db.commit()


async def set_awaiting_generate(chat_id: int, value: bool) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await _ensure_state(db, chat_id)
        await db.execute(
            "UPDATE chat_state SET awaiting_generate = ? WHERE chat_id = ?",
            (1 if value else 0, chat_id),
        )
        await db.commit()


async def set_chat_category(chat_id: int, category_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await _ensure_state(db, chat_id)
        await db.execute(
            "UPDATE chat_state SET current_category_id = ? WHERE chat_id = ?",
            (category_id, chat_id),
        )
        await db.commit()


async def set_history_cursor(
    chat_id: int, cursor: int, message_id: Optional[int] = None
) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await _ensure_state(db, chat_id)
        if message_id is not None:
            await db.execute(
                "UPDATE chat_state SET history_cursor = ?, question_message_id = ? "
                "WHERE chat_id = ?",
                (cursor, message_id, chat_id),
            )
        else:
            await db.execute(
                "UPDATE chat_state SET history_cursor = ? WHERE chat_id = ?",
                (cursor, chat_id),
            )
        await db.commit()


# ── history navigation ────────────────────────────────────────────────────────

async def get_question_at_cursor(chat_id: int, cursor: int) -> Optional[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT q.id, q.text, c.name AS category_name
            FROM chat_history h
            JOIN questions q ON q.id = h.question_id
            JOIN categories c ON c.id = q.category_id
            WHERE h.chat_id = ? AND h.seq = ?
            """,
            (chat_id, cursor),
        ) as cur:
            row = await cur.fetchone()
    return dict(row) if row else None


async def get_next_cursor(chat_id: int, current: int) -> Optional[int]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT MIN(seq) FROM chat_history WHERE chat_id = ? AND seq > ?",
            (chat_id, current),
        ) as cur:
            row = await cur.fetchone()
    return row[0] if row and row[0] is not None else None


async def add_to_history(chat_id: int, question_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COALESCE(MAX(seq), -1) + 1 FROM chat_history WHERE chat_id = ?",
            (chat_id,),
        ) as cur:
            seq: int = (await cur.fetchone())[0]
        await db.execute(
            "INSERT INTO chat_history (chat_id, question_id, seq) VALUES (?, ?, ?)",
            (chat_id, question_id, seq),
        )
        await db.commit()
    return seq


async def pick_next_question(chat_id: int, category_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT id, text FROM questions
            WHERE category_id = ?
              AND id NOT IN (
                  SELECT question_id FROM chat_history WHERE chat_id = ?
              )
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (category_id, chat_id),
        ) as cur:
            row = await cur.fetchone()
    return dict(row) if row else None
