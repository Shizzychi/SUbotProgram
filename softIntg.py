import os
import json
from telethon import TelegramClient, events
import re
import requests
from io import BytesIO

config_file = "config.json"

def get_config():
    if os.path.exists(config_file)
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    else:
        print("Конфигурация не найдена. Пожалуйста, введите данные.")
        api_id = input("Введите ваш API ID: ")
        api_hash = input("Введите ваш API Hash: ")
        user_id = input("Введите ваш User ID: ")

        config = {
            "api_id": api_id,
            "api_hash": api_hash,
            "user_id": user_id
        }

        with open(config_file, 'w') as file:
            json.dump(config, file)

        return config

config = get_config()
api_id = config["api_id"]
api_hash = config["api_hash"]
your_user_id = int(config["user_id"])

client = TelegramClient("userbot_session", api_id, api_hash)

def is_math_expression(message):
    pattern = r"^[\d+\-*/(). ]+$"
    return re.match(pattern, message)

def fetch_image(query):
    url = f"https://source.unsplash.com/600x400/?{query}"
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

@client.on(events.NewMessage)
async def handle_message(event):
    if event.sender_id == your_user_id:  # Реагирует только на ваши сообщения
        message = event.raw_text.strip()
message):
            try:
                result = eval(message)  # Решаем уравнение
                await event.reply(f"Ответ: {result}")
            except Exception:
                await event.reply("Ошибка при вычислении.")

        if message.startswith(".P "):
            query = message[3:].strip()
            image_data = fetch_image(query)
            if image_data:
                await client.send_file(event.chat_id, file=image_data, caption=f"Вот ваш запрос: {query}")
            else:
                await event.reply("Изображение не найдено.")

def start_bot():
    try:
        client.start()
        print("Бот запущен!")
        client.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")

def menu():
    while True:
        os.system("clear")
        print("\033[1;32m")
        print("""
  _   _ _     _    
 | | | (_)   | |   
 | |_| |_  __| | __
 |  _  | |/ _` |/ /
 | | | | | (_|   < 
 \_| |_/_|\__,_|\_\
        """)
        print("\033[0m")
        print("1. Запустить бота")
        print("2. Остановить бота")
        print("3. Удалить сессию (сменить пользователя)")
        print("4. Выйти")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            print("Запуск бота...")
            bot_thread = threading.Thread(target=start_bot)
            bot_thread.start()
            input("Бот запущен! Нажмите Enter для возврата в меню...")
        
        elif choice == "2":
            print("Остановка бота...")
            os.kill(os.getpid(), signal.SIGTERM)
        
        elif choice == "3":
            print("Удаление сессии...")
            try:
                os.remove("userbot_session.session")
                print("Сессия удалена.")
            except FileNotFoundError:
                print("Сессия не найдена.")
            input("Нажмите Enter для возврата в меню...")
        
        elif choice == "4":
            print("Выход...")
            sys.exit(0)
        
        else:
            print("Неверная опция!")
            input("Нажмите Enter для возврата в меню...")

if __name__ == "__main__":
    menu()
