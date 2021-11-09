import re sub

from Maxrobot import pbot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


repmark = InlineKeyboardMarkup(
      [
        [
        InlineKeyboardButton(text="➕ Add me to your group ➕", url=f"http://t.me/Max123Robot?startgroup=botstart") 
        ],
        [
         InlineKeyboardButton(text="🗣️Join my updates ", url=f"https://t.me/MaxRobot_updates") 
        ]
      ]      
    )

def nospace(s):

    s = re.sub(r"\s+", '%20', s)

    return s
@pbot.on_message(filters.command(["logo", f"logo@Max123Robot"]))
async def make_logo(_, message):
    await AddUserToDatabase(_, message)
    FSub = await ForceSub(_, message)
    if FSub == 400:
        return
    imgcaption = f"""
☘️** Logo Created Successfully**✅

"""
    name = nospace(message.text.strip().split(None, 1)[1].lower())
    m = await message.reply_text("🛠️**Crating your logo**.....")
    await m.edit("📤**Uploading**...")
    try:
        await message.reply_photo(
            photo=f"https://api.singledevelopers.net/logo?name={name}",
            caption=imgcaption,
            reply_markup = repmark
        )
        await m.delete()
    except Exception as e:
        await message.reply_text(f"⭕ ** Logo Creation Error ** ⭕\n\n★ It's may be API Error or name can't open 😶\n★ Try  Different name 🤗",
            reply_markup = repmark
        )
        await m.delete()

@pbot.on_message(filters.command(["logohq", f"logohq@Max123Robot"]))
async def make_logo(_, message):
    await AddUserToDatabase(_, message)
    FSub = await ForceSub(_, message)
    if FSub == 400:
        return
    imgcaption = f"""
☘️** Logo Created Successfully**✅

"""
    name = nospace(message.text.strip().split(None, 1)[1].lower())
    m = await message.reply_text("🛠️**Crating your logo**.....")
    await m.edit("📤**Uploading**...")
    try:
        await message.reply_photo(
            photo=f"https://single-developers.herokuapp.com/logohq?name={name}",
            caption=imgcaption,
            reply_markup = repmark
        )
        await m.delete()
    except Exception as e:
        await message.reply_text(f"⭕ ** Logo Creation Error ** ⭕\n\n★ It's may be API Error or name can't open 😶\n★ Try  Different name 🤗",
            reply_markup = repmark
        )
        await m.delete()
