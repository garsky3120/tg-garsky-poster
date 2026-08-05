import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("Ошибка: не найден TELEGRAM_TOKEN или CHANNEL_ID")
    sys.exit(1)

# Читаем список постов
with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Находим первый непубликованный пост
post_to_send = None
for post in posts:
    if not post.get("published", False):
        post_to_send = post
        break

if not post_to_send:
    print("Все посты уже опубликованы!")
    sys.exit(0)

# Отправляем сообщение в Telegram
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": post_to_send["text"],
    "parse_mode": "HTML",
    "disable_web_page_preview": False
}

data = urllib.parse.urlencode(payload).encode("utf-8")
req = urllib.request.Request(url, data=data)

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode("utf-8"))
        if res.get("ok"):
            print("Пост успешно опубликован!")
            post_to_send["published"] = True
        else:
            print(f"Ошибка от Telegram: {res}")
            sys.exit(1)
except Exception as e:
    print(f"Ошибка запроса: {e}")
    sys.exit(1)

# Сохраняем обновленный файл
with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
