import sqlite3

DB_NAME = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT NOT NULL,
                            role TEXT NOT NULL,
                            content TEXT NOT NULL
                        )
                        ''')

def save_message(session_id: str, role: str, content: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)',
                     (session_id, role, content))
        conn.commit()

def get_history(session_id: str) -> list[dict]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY id ASC',
                              (session_id,))
        history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    return history

def delete_history(session_id: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM chat_history WHERE session_id = ?', (session_id,))
        conn.commit()


if __name__ == "__main__":
    init_db()
    save_message("test_session", "user", "Hello, this is a test message.")
    save_message("test_session", "assistant", "Hello, this is a test reply.")
    print("sau Khi luu", get_history("test_session"))
    delete_history("test_session")
    print("sau Khi xoa", get_history("test_session"))

    