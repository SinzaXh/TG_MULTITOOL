import asyncio
import time
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded

API_ID = 24428848
API_HASH = "8bd8a034ef548cd8408610a7f9905441"

async def login():
    app = Client("user_session", api_id=API_ID, api_hash=API_HASH)
    await app.start()

    if await app.get_me():
        print(f"✅ Logged in as: {(await app.get_me()).first_name}")
    return app

async def send_message(app, chat_ids, message, repeat=1, delay=1):
    for i in range(repeat):
        for chat_id in chat_ids:
            try:
                await app.send_message(chat_id, message)
                print(f"✅ Message sent to {chat_id}")
            except Exception as e:
                print(f"❌ Failed to send message to {chat_id}: {e}")
        if i != repeat - 1:
            await asyncio.sleep(delay)

async def delete_messages(app, chat_ids, limit=None):
    for chat_id in chat_ids:
        try:
            async for message in app.get_chat_history(chat_id, limit=limit):
                await app.delete_messages(chat_id, message.id)
                print(f"🗑️ Deleted message {message.id} from {chat_id}")
        except Exception as e:
            print(f"❌ Failed to delete messages from {chat_id}: {e}")

async def main():
    app = await login()

    print("""
🤖 Welcome to MultiTool Bot
✨ By: @SINZAxh (AJAY)
Features:
- 💬 Spam message to multiple users/groups
- 🗑️ Delete message history (all or limited)
- 🕒 Delay & repeat control
Use with caution. Don't abuse 🙏
""")

    while True:
        print("\nSelect Action:")
        print("1. 🚀 Send Message")
        print("2. 🧹 Delete Messages")
        print("3. ❌ Exit")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            chats = input("Enter usernames or chat IDs (comma-separated): ").strip().split(",")
            chats = [c.strip() for c in chats if c.strip()]
            message = input("Enter the message (emoji allowed 😎): ").strip()
            repeat = int(input("How many times to send message?: ").strip())
            delay = float(input("Delay between rounds (in seconds)?: ").strip())
            await send_message(app, chats, message, repeat, delay)

        elif choice == "2":
            chats = input("Enter chat IDs/usernames (comma separated): ").strip().split(",")
            chats = [c.strip() for c in chats if c.strip()]
            limit_str = input("Enter number of messages to delete (or 'all'): ").strip().lower()
            limit = None if limit_str == "all" else int(limit_str)
            await delete_messages(app, chats, limit)

        elif choice == "3":
            print("👋 Exiting. Bye!")
            await app.stop()
            break
        else:
            print("❗ Invalid choice, try again.")

if __name__ == "__main__":
    asyncio.run(main())
