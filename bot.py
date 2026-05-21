import os
import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔑 
BOT_TOKEN = "8360325799:AAFCaB25P3EJBywTz3wZr-LN28ftN8TdMf0"
MOSCOW_TZ = ZoneInfo("Europe/Moscow")  # Часовой пояс, чтобы день менялся в полночь по МСК

def load_messages():
    messages = []
    for file_name in ["personal.txt", "internet.txt"]:
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        messages.append(line)
    if not messages:
        messages = ["📝 Добавь свои фразы в файлы personal.txt или internet.txt и перезапусти бота."]
    return messages

# Загружаем сообщения один раз при старте
ALL_MESSAGES = load_messages()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Берём номер дня в году (от 1 до 366) по МСК
    day_of_year = int(datetime.datetime.now(MOSCOW_TZ).strftime("%j"))
    # Выбираем сообщение. Одинаковый номер дня = одинаковое сообщение весь день.
    # Завтра номер изменится → придёт новое сообщение.
    idx = (day_of_year - 1) % len(ALL_MESSAGES)
    await update.message.reply_text(ALL_MESSAGES[idx])

def main():
    print("✅ Бот запущен! Жду команды /start...")
    # Создаём приложение бота
    app = Application.builder().token(BOT_TOKEN).build()
    # Привязываем команду /start к нашей функции
    app.add_handler(CommandHandler("start", start))
    # Запускаем постоянный опрос Telegram
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

