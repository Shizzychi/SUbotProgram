import os
import json
from telethon import TelegramClient, events
import re
import requests
from io import BytesIO
import threading
import signal
import sys
import asyncio

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
    pattern = r"^[\d+\-*/(). ]+$"
    return re.match(pattern, message)

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
        await client.start()
        print("Бот запущен!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")

def stop_bot():
    print("Остановка бота...")
    loop = asyncio.get_event_loop()
    loop.stop()
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
                                                                               
        """)
        print("\033[0m")
        print("1. Запустить бота")
        print("2. Остановить бота")
        print("3. Удалить сессию (сменить пользователя)")
        print("4. Выйти")
        
        choice = input("\nВыберите опцию: ")
