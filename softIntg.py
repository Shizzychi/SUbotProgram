import re
import requests
from io import BytesIO
from telethon import TelegramClient, events
import os
import signal
import sys

api_id = "23286444"
api_hash = "f56caed4076eaba4deda000795a42589"
your_user_id = 123456789

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
    if event.sender_id == your_user_id:
        message = event.raw_text.strip()
        if message.startswith(".P "):
            query = message[3:].strip()
            image_data = fetch_image(query)
            if image_data:
                await client.send_file(event.chat_id, file=image_data, caption=f"Вот ваш запрос: {query}")
            return
        if is_math_expression(message):
            try:
                result = eval(message)
                await event.reply(f"Ответ: {result}")
            except Exception:
                pass

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
            try:
                client.start()
                print("Бот запущен!")
                client.run_until_disconnected()
            except Exception as e:
                print(f"Ошибка запуска: {e}")
                input("Нажмите Enter для возврата в меню...")
        
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