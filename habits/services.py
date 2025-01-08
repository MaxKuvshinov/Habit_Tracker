import requests
from config import settings


def send_message_telegram(chat_id, message):
    """Функция для отправки сообщения через телеграм бота"""
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    url = f"{settings.TELEGRAM_URL}{settings.BOT_TOKEN}/sendMessage"
    response = requests.get(url=url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Ошибка отправки сообщения в телеграм: {response.text}")
