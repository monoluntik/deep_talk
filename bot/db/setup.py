import aiosqlite
from bot.config import DATABASE_PATH


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS categories (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                is_custom INTEGER DEFAULT 0,
                chat_id   INTEGER
            );

            CREATE TABLE IF NOT EXISTS questions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                text        TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chat_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     INTEGER NOT NULL,
                question_id INTEGER NOT NULL REFERENCES questions(id),
                seq         INTEGER NOT NULL,
                UNIQUE(chat_id, seq)
            );

            CREATE TABLE IF NOT EXISTS chat_state (
                chat_id             INTEGER PRIMARY KEY,
                current_category_id INTEGER REFERENCES categories(id),
                history_cursor      INTEGER DEFAULT -1,
                question_message_id INTEGER
            );
        """)

        # Migrations: add missing columns if upgrading from older schema
        async with db.execute("PRAGMA table_info(categories)") as cur:
            cat_cols = [row[1] for row in await cur.fetchall()]
        if "chat_id" not in cat_cols:
            await db.execute("ALTER TABLE categories ADD COLUMN chat_id INTEGER")

        async with db.execute("PRAGMA table_info(chat_state)") as cur:
            state_cols = [row[1] for row in await cur.fetchall()]
        if "awaiting_generate" not in state_cols:
            await db.execute(
                "ALTER TABLE chat_state ADD COLUMN awaiting_generate INTEGER DEFAULT 0"
            )

        await db.commit()
