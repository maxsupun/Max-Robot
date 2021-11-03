#@supunmabot

from pyrogram import filters, Client 
from szbot import sz
import psutil
import shutil
import traceback
import os
from pyrogram.types import  Message
from helpers.database.access_db import db
from helpers.broadcast import main_broadcast_handler
from helpers.humanbytes import humanbytes
from config import BOT_OWNER
from helpers.database import db


# broadcast improved now we can broadcast messages for groups and all users
# Broadcast message to users (This will Broadcast using Bot with Db)
@sz.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)



#stats user
@sz.on_message(filters.private & filters.command("stats"))
async def show_status_count(_, bot: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()    
    await bot.reply_text(
        text=f"""
❤️Hey{Message.from_user.mention}  Your Bot Users Count
& Disk/cpu/ram Usage

😊😇`{total_users}` Promote me {Message.from_user.mention}

**Total Disk Space:** {total} 
**Used Space:** {used}({disk_usage}%) 
**Free Space:** {free} 
**CPU Usage:** {cpu_usage}% 
**RAM Usage:** {ram_usage}%
**Total Users in DB:** `{total_users}`

☬─────────────☬
🤟 **ᗪᙓᐯᙓᒪOᑭᙓᖇ** :- [OғғɪᴄɪᴀʟBᴏᴛs](https://t.me/szteambots)
🦅 **Powered By** :- `【SZ™】`
☬─────────────☬

©2021[ 【SZ™】 team ](https://t.me/szteambots) **All Right Reserved**.⚠️       
        """,
        parse_mode="Markdown",
        quote=True
    )


# Ban User
@sz.on_message(filters.private & filters.command("ban") & filters.user(BOT_OWNER))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban Users from using this bot 🤒",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"`Banning User 🗑...` \nUser ID: `{user_id}` \nDuration: `{ban_duration}` \nReason: `{ban_reason}`"
        try:
            await c.send_message(
                user_id,
                f" You are **Banned 😂!** \n\nReason: `{ban_reason}` \nDuration: `{ban_duration}` day(s). \n\n**Message From The Owner! Ask in **@slbotzone** or **@supunmabot** if you think this was an mistake."
            )
            ban_log_text += '\n\nSuccessfully Notified About This Ban to that **Dumb User** 😅'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nI can't Notify About This Ban to That **Dumb User** 🤯 \n\n`{traceback.format_exc()}`"
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"An Error Occoured ❌! Traceback is given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


# Unban User
@sz.on_message(filters.private & filters.command("unban") & filters.user(BOT_OWNER))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban Users from using this bot 🤒! ",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        unban_log_text = f"`Unbanning user...` /n**User ID:**{user_id}"
        try:
            await c.send_message(
                user_id,
                f"Good News! **You are Unbanned** 😊!"
            )
            unban_log_text += '\n\nSuccessfully Notified About This to that **Good User** 😅'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\n I can't Notify About This to That **Dumb User** 🤯 \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"An Error Occoured ❌! Traceback is given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


# Banned User List
@sz.on_message(filters.private & filters.command("banlist") & filters.user(BOT_OWNER))
async def _banned_usrs(_, m: Message):
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"➬ **User ID**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned Date**: `{banned_on}`, **Ban Reason**: `{ban_reason}`\n\n"
    reply_text = f"**Total Banned:** `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-user-list.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-user-list.txt', True)
        os.remove('banned-user-list.txt')
        return
    await m.reply_text(reply_text, True)

