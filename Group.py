from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import re
from Group_manager import app




PROHIBITED_CONTENT = ["porn", "18+", "nudes", "xxx"]
WARN_LIMIT = 3
warns = {}


def contains_prohibited_content(message: Message):
    if message.text:
        return any(word in message.text.lower() for word in PROHIBITED_CONTENT)
    elif message.photo or message.video or message.sticker or message.animation:
        caption = message.caption or ""
        return any(word in caption.lower() for word in PROHIBITED_CONTENT)
    return False


def add_warning(user_id, chat_id):
    warns.setdefault(chat_id, {}).setdefault(user_id, 0)
    warns[chat_id][user_id] += 1
    return warns[chat_id][user_id]


@app.on_message(filters.group & ~filters.edited)
def warn_user(client, message):
    if contains_prohibited_content(message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.mention

        
        message.delete()

        
        warn_count = add_warning(user_id, chat_id)
        message.reply_text(
            f"🚫 {user_name}, your message contains prohibited content. Warning {warn_count}/{WARN_LIMIT}."
        )

        
        if warn_count >= WARN_LIMIT:
            client.kick_chat_member(chat_id, user_id)
            message.reply_text(f"🚨 {user_name} has been banned for exceeding the warning limit.")


@app.on_message(filters.group & ~filters.edited)
def anti_spam(client, message):
    
    user_id = message.from_user.id
    chat_id = message.chat.id

    


@app.on_message(filters.command("ban", prefixes=["/"]) & filters.group)
def ban_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        client.kick_chat_member(chat_id, user_id)
        message.reply_text(f"🚫 User {message.reply_to_message.from_user.mention} has been banned.")


@app.on_message(filters.command("unban", prefixes=["/"]) & filters.group)
def unban_user(client, message):
    if len(message.command) > 1:
        user_id = int(message.command[1])
        chat_id = message.chat.id
        client.unban_chat_member(chat_id, user_id)
        message.reply_text(f"✅ User {user_id} has been unbanned.")


@app.on_message(filters.command("settitle", prefixes=["/"]) & filters.group)
def set_group_title(client, message):
    if len(message.command) > 1:
        new_title = " ".join(message.command[1:])
        client.set_chat_title(message.chat.id, new_title)
        message.reply_text(f"✅ Group title has been changed to: {new_title}")


@app.on_message(filters.command("setpic", prefixes=["/"]) & filters.group)
def set_group_pic(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
        client.set_chat_photo(message.chat.id, photo=file_id)
        message.reply_text("✅ Group picture has been updated.")


@app.on_message(filters.command("adminlist", prefixes=["/"]) & filters.group)
def admin_list(client, message):
    admins = client.get_chat_members(message.chat.id, filter="administrators")
    admin_names = [f"{admin.user.first_name}" for admin in admins]
    message.reply_text(f"👮 Admins:\n" + "\n".join(admin_names))

# Start the bot
print("Bot is running...")
app.run()
