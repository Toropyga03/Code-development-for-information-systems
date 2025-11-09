import sqlite3
from datetime import datetime

DB_NAME = 'exchange_rates.db'


def init_db():
    """
    Инициализация БД. Создаёт таблицу со столбцами:
    id, имя валюты, курс, дата обновления
    """
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT UNIQUE NOT NULL,
                rate REAL NOT NULL,
                fetched_at TEXT NOT NULL
            )
        """)


def save_rate(target_currency: str, rate: float):
    """
    Сохранение данных о курсе валют в БД

    Args:
        target_currency: код валюты (например, 'USD', 'EUR')
        rate: курс валюты
    """
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        fetched_at = datetime.now().isoformat()

        cur.execute("""
            INSERT INTO rates (currency, rate, fetched_at)
            VALUES (?, ?, ?)
            ON CONFLICT(currency) DO UPDATE SET
                rate = excluded.rate,
                fetched_at = excluded.fetched_at
        """, (target_currency, rate, fetched_at))


def get_saved_rate(target_currency: str) -> float:
    """
    Получение курса по имени валюты из БД

    Args:
        target_currency: код валюты (например, 'USD', 'EUR')

    Returns:
        float: курс валюты

    Raises:
        ValueError: если валюта не найдена в БД
    """
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT rate FROM rates
            WHERE currency = ?
            ORDER BY fetched_at DESC
            LIMIT 1
        """, (target_currency,))

        result = cur.fetchone()

        if result:
            return result[0]
        else:
            raise ValueError(f"Курс для валюты {target_currency} не найден в базе данных")


# Инициализируем базу данных при импорте модуля
init_db()