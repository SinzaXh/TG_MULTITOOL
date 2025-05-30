import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
import time
import os

SPAM_WORDS = ["buy now", "free", "porn", "http", "www", "t.me/"]

# ---------- Feature 1: Spam Messages ----------
async def spam_messages(app):
    os.system('clear')
    print("===== Message Spammer =====")
    chat = input("🗂️ Enter target chat username or ID: ").strip()
    message = input("✉️ Enter message to spam: ").strip()
    count = input("🔢 Number of times to send: ").strip()
    try:
        count = int(count)
    except:
        print("❌ Invalid number. Aborting spam.")
        time.sleep(2)
        return

    print(f"\n🚀 Spamming message {count} times to {chat}...")
    for i in range(count):
        try:
            await app.send_message(chat, message)
            print(f"✔️ Sent message {i+1}/{count}")
            await asyncio.sleep(1)
        except FloodWait as e:
            wait = e.value
            print(f"⏳ Flood wait: Sleeping for {wait} seconds")
            time.sleep(wait)
        except Exception as e:
            print(f"❌ Error sending message {i+1}: {str(e)}")
    print("\n✅ Spam complete! Press Enter to continue...")
    input()

# ---------- Feature 2: Scrape Users ----------
async def scrape_users(app):
    os.system('clear')
    print("===== User Scraper =====")
    target = input("🗂️ Enter target chat username or ID: ").strip()
    print(f"\n🔍 Fetching members from {target}...")

    try:
        count = 0
        with open("scraped_users.txt", "w", encoding="utf-8") as f:
            async for member in app.get_chat_members(target):
                user = member.user
                username = user.username if user.username else "NoUsername"
                line = f"{username},{user.id}\n"
                f.write(line)
                count += 1
                if count % 50 == 0:
                    print(f"➡️ {count} members scraped...")
        print(f"\n✅ Done! Total {count} members saved to scraped_users.txt")
    except Exception as e:
        print(f"❌ Failed to get members: {str(e)}")
    print("\nPress Enter to continue...")
    input()

# ---------- Feature 3: Delete Messages ----------
async def delete_messages(app):
    os.system('clear')
    print("===== Message Deleter =====")
    chats_input = input("🗂️ Enter target chat usernames or IDs (comma separated): ").strip()
    users_input = input("👤 Enter usernames/user IDs to delete from (comma separated, leave empty for ALL): ").strip()
    max_del_input = input("🔢 Max messages to delete per user/chat (leave empty for ALL): ").strip()

    chats = [c.strip() for c in chats_input.split(",") if c.strip()]
    users = [u.strip().replace("@", "") for u in users_input.split(",")] if users_input else []
    max_del = int(max_del_input) if max_del_input.isdigit() else None

    if not chats:
        print("❌ No chats specified!")
        time.sleep(2)
        return

    confirm = input("\n⚠️ Confirm delete messages? Type 'yes' to proceed: ").strip().lower()
    if confirm != "yes":
        print("❌ Delete cancelled.")
        time.sleep(2)
        return

    for chat in chats:
        print(f"\n🧹 Processing chat: {chat}")
        count_total = 0

        try:
            if users:
                for user in users:
                    count = 0
                    async for message in app.get_chat_history(chat):
                        if max_del is not None and count >= max_del:
                            break
                        if message.from_user:
                            from_id = str(message.from_user.id)
                            from_username = str(message.from_user.username).lower() if message.from_user.username else ""
                            if user == from_id or user.lower() == from_username:
                                try:
                                    await app.delete_messages(chat_id=chat, message_ids=message.id)
                                    count += 1
                                    count_total += 1
                                    print(f"🗑️ Deleted message {count} from user {user}")
                                except Exception as e:
                                    print(f"❌ Could not delete message: {str(e)}")
                    print(f"✅ Deleted {count} messages from user {user}")
            else:
                count = 0
                async for message in app.get_chat_history(chat):
                    if max_del is not None and count >= max_del:
                        break
                    try:
                        await app.delete_messages(chat_id=chat, message_ids=message.id)
                        count += 1
                        count_total += 1
                        print(f"🗑️ Deleted message {count}")
                    except Exception as e:
                        print(f"❌ Could not delete message: {str(e)}")
                print(f"✅ Deleted {count} messages in chat")
            
            print(f"✅ Finished deleting total {count_total} messages in {chat}")
        except Exception as e:
            print(f"❌ Error processing chat {chat}: {str(e)}")
    
    print("\n✅ All requested deletions done. Press Enter to continue...")
    input()

# ---------- Feature 4: Broadcast Message ----------
async def broadcast_message(app):
    os.system('clear')
    print("===== Message Broadcaster =====")
    chats_input = input("🗂️ Enter target chats (comma separated): ").strip()
    message = input("✉️ Enter broadcast message: ").strip()
    
    if not chats_input:
        print("❌ No chats specified!")
        time.sleep(2)
        return
        
    chats = [c.strip() for c in chats_input.split(",") if c.strip()]
    success = 0
    fail = 0
    
    for chat in chats:
        try:
            await app.send_message(chat, message)
            print(f"✅ Broadcasted to {chat}")
            success += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            wait = e.value
            print(f"⏳ Flood wait: Sleeping for {wait} seconds")
            time.sleep(wait)
        except Exception as e:
            print(f"❌ Failed to send to {chat}: {str(e)}")
            fail += 1
    
    print(f"\n✅ Broadcast complete! Success: {success}, Failed: {fail}")
    print("Press Enter to continue...")
    input()

# ---------- Feature 5: Join Groups ----------
async def join_groups(app):
    os.system('clear')
    print("===== Group Joiner =====")
    groups_input = input("🗂️ Enter group usernames or invite links (comma separated): ").strip()
    
    if not groups_input:
        print("❌ No groups specified!")
        time.sleep(2)
        return
        
    groups = [g.strip() for g in groups_input.split(",") if g.strip()]
    success = 0
    fail = 0
    
    for group in groups:
        try:
            await app.join_chat(group)
            print(f"✅ Joined group {group}")
            success += 1
            await asyncio.sleep(3)
        except FloodWait as e:
            wait = e.value
            print(f"⏳ Flood wait: Sleeping for {wait} seconds")
            time.sleep(wait)
        except Exception as e:
            print(f"❌ Failed to join {group}: {str(e)}")
            fail += 1
    
    print(f"\n✅ Join complete! Success: {success}, Failed: {fail}")
    print("Press Enter to continue...")
    input()

# ---------- Feature 6: Mass Add Members ----------
async def mass_add_members(app):
    os.system('clear')
    print("===== Mass Member Adder =====")
    source_chat = input("👥 Source group username or ID: ").strip()
    target_chat = input("🎯 Target group username or ID: ").strip()
    limit = input("🔢 How many members to add? ").strip()
    
    try:
        limit = int(limit)
    except:
        print("❌ Invalid number. Aborting.")
        time.sleep(2)
        return

    try:
        members = []
        print("\n🔍 Finding members...")
        async for user in app.get_chat_members(source_chat):
            if len(members) >= limit:
                break
            if not user.user.is_bot and user.user.username:
                members.append(user.user.username)
                if len(members) % 10 == 0:
                    print(f"👥 Found {len(members)} members...")

        print(f"\n👥 Found {len(members)} members. Starting to add...")
        success = 0
        fail = 0
        
        for username in members:
            try:
                await app.add_chat_members(target_chat, username)
                print(f"✅ Added: @{username}")
                success += 1
                await asyncio.sleep(10)
            except FloodWait as e:
                wait = e.value
                print(f"⏳ Flood wait: Sleeping for {wait} seconds")
                time.sleep(wait)
            except Exception as e:
                print(f"❌ Failed to add @{username}: {str(e)}")
                fail += 1
                
        print(f"\n✅ Add complete! Success: {success}, Failed: {fail}")
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    
    print("\nPress Enter to continue...")
    input()

# ---------- Feature 7: User Info Lookup ----------
async def user_info(app):
    os.system('clear')
    print("===== User Info Lookup =====")
    user_input = input("🔎 Enter username or user ID: ").strip()
    try:
        user = await app.get_users(user_input)
        print(f"""
👤 Name: {user.first_name or 'N/A'} {user.last_name or ''}
🆔 ID: {user.id}
🔗 Username: @{user.username if user.username else 'N/A'}
🤖 Is Bot: {user.is_bot}
📞 Phone Public?: {'Yes' if user.phone_number else 'No'}
""")
    except Exception as e:
        print(f"⚠️ Error fetching user info: {str(e)}")
    print("\nPress Enter to continue...")
    input()

# ---------- Feature 8: Anti-Spam Shield ----------
async def anti_spam(client, message):
    if message.chat and message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if message.text and any(word in message.text.lower() for word in SPAM_WORDS):
            try:
                await message.delete()
                print(f"\n🗑️ Deleted spam message from {message.from_user.id}")
            except Exception as e:
                print(f"\n❌ Failed to delete spam: {str(e)}")

def add_handlers(app):
    app.add_handler(filters.group & filters.incoming, anti_spam)

# ---------- Menu System ----------
def show_menu():
    os.system('clear')
    print("""======================================
🤖 Telegram MultiTool - Termux Edition
⚙️  Use number keys to select options
======================================\n""")
    
    options = [
        "[1] Spam Messages",
        "[2] Scrape Users",
        "[3] Delete Messages",
        "[4] Broadcast Message",
        "[5] Join Groups",
        "[6] Mass Add Members",
        "[7] User Info Lookup",
        "[8] Exit"
    ]
    
    for option in options:
        print(option)
    
    print("\nSelect option (1-8): ", end='')
    try:
        choice = input().strip()
        if choice.isdigit():
            return int(choice)
        return -1
    except:
        return -1

# ---------- Main Program ----------
async def main():
    print("="*50)
    print("🤖 Welcome to TG MultiTool")
    print("⚙️ Termux-optimized Telegram automation toolkit")
    print("="*50)

    api_id = input("\n🔑 Enter your API ID: ").strip()
    api_hash = input("🧬 Enter your API HASH: ").strip()

    if not api_id.isdigit():
        print("❌ API ID must be a number!")
        return
        
    app = Client("tg_multitool", api_id=int(api_id), api_hash=api_hash)
    add_handlers(app)

    try:
        await app.start()
        me = await app.get_me()
        print(f"\n✅ Logged in as: {me.first_name} ({me.id})")
        print("🛡️ Anti-Spam Shield activated in background\n")
        time.sleep(2)
        
        while True:
            choice = show_menu()
            
            if choice == 1:
                await spam_messages(app)
            elif choice == 2:
                await scrape_users(app)
            elif choice == 3:
                await delete_messages(app)
            elif choice == 4:
                await broadcast_message(app)
            elif choice == 5:
                await join_groups(app)
            elif choice == 6:
                await mass_add_members(app)
            elif choice == 7:
                await user_info(app)
            elif choice == 8:
                print("\n👋 Exiting... Goodbye!")
                break
            else:
                print("❌ Invalid choice. Try again.")
                time.sleep(1)
                
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
    finally:
        await app.stop()
        print("\nSession closed.")

if __name__ == "__main__":
    asyncio.run(main())
