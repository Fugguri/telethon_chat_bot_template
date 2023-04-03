import json
import asyncio
from helpers import DB
from telethon import TelegramClient, events, types
from time import sleep
import openai
with open("config.json", "rb") as file:
    data = json.load(file)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    phone = data["phone"]

client = TelegramClient(phone, api_id, api_hash)
# db = DB("bot.db")
# db.create()

async def message(event):
    sender = await event.get_sender()
 

async def main():
    async with client:
        if not await client.is_user_authorized():
            await client.send_code_request(phone, force_sms=False)
            code = input("Enter login code: ")
            try:
                me = await client.sign_in(phone, code=code)
            except telethon.errors.SessionPasswordNeededError:
                password = input("Enter password: ")
                me = await client.sign_in(password=password)
        try:
            client.add_event_handler(message, events.NewMessage)
            await client.run_until_disconnected()
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    asyncio.run(main())
