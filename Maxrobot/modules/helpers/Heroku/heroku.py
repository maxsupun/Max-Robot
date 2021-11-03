#del vars is not included yet -:(

import asyncio
import os
import sys

import heroku3
from szbot import sz
from config import BOT_OWNER, HEROKU_API_KEY, HEROKU_APP_NAME 
from pyrogram import filters, Client
from pyrogram.types import Message

heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)

#set vars
@sz.on_message(filters.command("set") & filters.user(BOT_OWNER))
async def variable(var):
    if var.fwd_from:
        return
    if var.sender_id == BOT_OWNER:
        pass
    else:
        return
    """
    Manage most of ConfigVars setting, set new var, get current var,
    or delete var...
    """
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        return await var.reply("`[HEROKU]:" "\nPlease setup your` **HEROKU_APP_NAME**")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "see":
        k = await var.reply("`Getting information...`")
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await k.edit(
                    "**ConfigVars**:" f"\n\n`{variable} = {heroku_var[variable]}`\n"
                )
            else:
                return await k.edit(
                    "**ConfigVars**:" f"\n\n`Error:\n-> {variable} don't exists`"
                )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await k.edit(
                        "`[HEROKU]` ConfigVars:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        s = await var.reply("`Setting information...weit ser`")
        variable = var.pattern_match.group(2)
        if not variable:
            return await s.edit(">`.set var <ConfigVars-name> <value>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await s.edit(">`/set  <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await s.edit(
                f"**{variable}**  `successfully changed to`  ->  **{value}**"
            )
        else:
            await s.edit(
                f"**{variable}**  `successfully added with value`  ->  **{value}**"
            )
        heroku_var[variable] = value
    elif exe == "del":
        m = await var.edit("`Getting information to deleting variable...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await m.edit("`Please specify ConfigVars you want to delete`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await m.edit(f"**{variable}**  `successfully deleted`")
            del heroku_var[variable]
        else:
            return await m.edit(f"**{variable}**  `is not exists`")


#Restart your bot
@sz.on_message(filters.command("restart") & filters.user(BOT_OWNER))
async def restart_bot(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == BOT_OWNER:
        pass
    else:
        return await dyno.replybot( """
        ================================
        will be restarted...
        ================================
        """
         )
    args = [sys.executable, "-m", "bot"]
    os.execl(sys.executable, *args)

#update your bot
@sz.on_message(filters.command("update") & filters.user(BOT_OWNER))
async def upgrade(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == BOT_OWNER:
        pass
    else:
        return await dyno.reply(
            "`Checking for updates, please wait....`"
        )
    m = await dyno.reply("""
    ================================
    **Your bot is being deployed,
     please wait for it to complete.
     It may take upto 5 minutes **
    ================================
    """)
    proc = await asyncio.create_subprocess_shell(
        "git pull --no-edit",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout = (await proc.communicate())[0]
    if proc.returncode == 0:
        if "Already up to date." in stdout.decode():
            await m.edit_text("There's nothing to upgrade.")
        else:
            await m.edit_text("Restarting...")
            args = [sys.executable, "-m", "bot"]
            os.execl(sys.executable, *args)
    else:
        await m.edit_text(
            f"Upgrade failed (process exited with {proc.returncode}):\n{stdout.decode()}"
        )
        proc = await asyncio.create_subprocess_shell("git merge --abort")
        await proc.communicate()
        
# Heroku logs        
@sz.on_message(filters.command("logs") & filters.user(BOT_OWNER))
async def _(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == BOT_OWNER:
        pass
    else:
        return
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except:
        return await dyno.reply(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    v = await dyno.reply("================================ \nGetting Logs....\n================================")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await v.edit("Got the logs wait a sec")
    await dyno.client.send_file(
        dyno.chat_id,
        "logs.txt",
        reply_to=dyno.id,
        caption=" ================================\nBot Logz.\n================================",        
    )

    await asyncio.sleep(5)
    await v.delete()
    return os.remove("logs.txt")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)
