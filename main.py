import os
import json
from telethon import TelegramClient, events
import re
import asyncio
import sys

config_file = "config.json"


def get_config():
    if os.path.exists(config_file):
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
    try:
        eval(message)
        return True
    except:
        return False


@client.on(events.NewMessage)
async def handle_message(event):
    if event.sender_id == your_user_id:
        message = event.raw_text.strip()

        if is_math_expression(message):
            try:
                result = eval(message)
                await event.reply(f"Ответ: {result}")
            except Exception:
                await event.reply("Ошибка при вычислении.")


async def start_bot():
    try:
        print("Попытка запуска бота...")
        await client.start()
        print("Бот успешно запущен!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")


def stop_bot():
    print("Остановка бота...")
    asyncio.create_task(client.disconnect())
    print("Бот остановлен.")


def menu():
    while True:
        os.system("clear")
        print("\033[1;32m")
        print("""
     ___      .______       _______       ___       __       __       ___      
    /   \     |   _  \     |       \     /   \     |  |     |  |     /   \     
   /  ^  \    |  |_)  |    |  .--.  |   /  ^  \    |  |     |  |    /  ^  \    
  /  /_\  \   |      /     |  |  |  |  /  /_\  \   |  |     |  |   /  /_\  \   
 /  _____  \  |  |\  \----.|  '--'  | /  _____  \  |  `----.|  |  /  _____  \  
/__/     \__\ | _| `._____||_______/ /__/     \__\ |_______||__| /__/     \__\ 
                     version: 0w2.1b                                                          
        """)
        print("\033[0m")
        print("1. Запустить бота")
        print("2. Остановить бота")
        print("3. Удалить сессию (сменить пользователя)")
        print("4. Выйти")

        choice = input("\nВыберите опцию: ")

        if choice == "1":
            asyncio.run(start_bot())
        elif choice == "2":
            stop_bot()
        elif choice == "3":
            if os.path.exists("userbot_session.session"):
                os.remove("userbot_session.session")
                print("Сессия удалена.")
            else:
                print("Сессия не найдена.")
        elif choice == "4":
            print("Выход из программы.")
            sys.exit()
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    menu()
