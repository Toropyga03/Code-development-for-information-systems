import requests
from typing import Dict, Any

API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def fetch_rates() -> Dict[str, Any]:
    """
    Получение данных о курсе валют через API-запрос

    Returns:
        dict: Словарь с данными о курсах валют

    Raises:
        requests.RequestException: Если произошла ошибка при запросе
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Проверяем статус ответа
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"Ошибка при запросе к API: {e}")
    except ValueError as e:
        raise ValueError(f"Ошибка при обработке JSON: {e}")