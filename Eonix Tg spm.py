# eonix_bot_multi.py
import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
"8580965508:AAGWJICvJObI2bgpokIfQyS87zeENImHgeQ",
                                                                            "8064172259:AAGNxN_wgvsrTfqwnjhLQrvBnWERnwUfbYI",
                                                                            "8498632361:AAEY_r5RlFqVt14uYb_mLuLjJ4vzLsE4Cyk",
                                                                            "8250301131:AAFLFLnA7a8JcQ6GE6o1oLqFWBSau-DADZY",     
                                                                            "8593096418:AAHtk3I0ncVdF1C_V8LS3feg6EG-cjQXUKo",    
                                                                            "7586866429:AAGf_45YOQI1NT5OZ3GowvZV91TvbrxVnZM",   
                                                                            "8312147463:AAFX1OzWCPIitKoqklG17fzybB0R8TZ4tfc",
                                                                            "8440409708:AAGbgS_SRUqalwnvsNRofHWyRHZxFO4BCjY",
                                                                            "8412261411:AAF9k2tSl3nn4nR0bArHs3QaGbI3x3zEObY",
                                                                            "8387211438:AAEGJvythFOiI2OrquuSj8ixc_j5i2HjixM",
                                                                            "8391748833:AAGeeRl5S5BcnDm_N6CwHNj4GMNUrrAGfHQ",
                                                                            "8490060490:AAFYyH5W7hRccroascWKFaXHzVQEwpGzCNM",
                                                                            "8340027113:AAG87EpJO-CLF30mcC8FBwxibmi8-DMa7tc",
                                                                            "8586866220:AAENx0J5eJzYkk-OJoKDYt9AuytRjyihF6w",
                                                                            "8286478935:AAEUTYar_1a68bB2HTPmqbv_nraPNicE4-E",
]                                                    
                                                                          
OWNER_ID = 7768926293
SUDO_FILE = "EONIX"

# ---------------------------
# RAID TEXTS
# ---------------------------
RAID_TEXTS = [
    "𝑮𝑪 𝑳𝑬𝑭𝑻 𝑳𝑬 लंगड़ी ᴍᴀᴀ ᴋᴇ ʙᴀᴄʜᴇ 🤮",
    "Tmkc pe chppl hi chppl marunga !! 🔥😂🩴 ",
    "𝐂ʜʟ 𝐇ᴀʀᴍᴢᴀᴅ𝐈 𝐊ᴇ लड़के 💛🤍🩵",
    "sort nhi krunga chud tu bina ruke 🤢🔥 ",
    "काले Doraemon रोता reh 🤣🤣 ",
    "Awaz neeche rndy k bacche 🤢🔥",
    "Ka Baap Eonix 🩷🩵🩶🩷🩵🩶🩷🩵🩶🩷🩵🩶",
    "𝙇𝙐𝙉𝘿 𝘾𝙃𝙐𝙎  🥶➿🩵 𝙈𝘼𝘿𝘼𝙍𝘾𝙃𝙊𝘿 ",
    "Sawal mt puch tery ma k bosda 😹🖕🏻",
    "Are try maa ka bosda 🤢᭄᭄᭄ 🌟 𝙇𝙐𝙉𝘿 𝘾𝙃𝙐𝙎 🤪᭄᭄",
    "fyter bnege langde madarchod 😂💥",
    "𝟏𝐱 𝐀ɴ𝐘 𝐂ʜ𝐋 𝐏ɪʟʟ𝐄 𝐍ᴏᴛ𝐈 𝐂ʟᴀɪ𝐌 𝐊ᴀ𝐑 🩷🩵🩶",
    "try maa > Mia Khalifa 🥵💯",
    "baap se fyt krega 😂😂 ?",
    "ATMKBFJ 🥀",
    "Mᴀᴀ Kᴇ Sᴀᴛʜ bhen ᗷᕼI ᥴᕼꪊ໓ ᭙ꫝꪶi 🤢🔥",
    "Teri maa ko Gachar Gachar codunga 😹❌🔥",
    "रंडीꪻ ♡︎ 🎀",
    "𝐓𝐆 𝐅𝐘𝐓𝐄𝐑 𝐁𝐍𝐄𝐆𝐀 ?? 𝐂𝐇𝐎𝐃𝐔 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 😂😂",
    "𝐓𝐎𝐓𝐋𝐄 𝐓𝐌𝐊𝐂 𝐌𝐄 𝐁𝐎𝐌𝐁 𝐅𝐄𝐊𝐃𝐔 💣💥",
    "Ｔᴏʜᴀʀ Ｍᴀɪʏᴀ Ｃʜᴀɪʏᴀ Ｃʜᴀɪʏᴀ 🤢🔥🤢🔥",
    " 𝙏𝙚𝙧𝙞 𝙢𝙖𝙖 𝙠𝙚 𝙗𝙝𝙤𝙨𝙙𝙚 𝙢𝙚 𝙡𝙖𝙩 𝙥𝙙𝙚𝙣𝙜𝙚 𝙗𝙝𝙤𝙩 𝙩𝙚𝙯 👻💥",
    "🦅🔥 Tᴇʀɪ 🦅🔥 Mᴀᴀ 🦅🔥 Rɴᴅɪ 🦅🔥",
    "कि बेहन 𝗧𝗔𝗞𝗟𝗜 💙",
    "𝗚𝗨𝗟𝗔𝗠 🥱👞",
    "ʙꪊʟʟꪗ केन्द्र ᥫ😂᭄",
    "तेरी माँ कि 𝘾ʜᴜᴛ में જ⁀➴🧨᭄",
    "𝘙𝘈𝘕𝘋 𝘽𝙃𝙀𝙀𝙆 𝙈𝘼𝙉𝙂 😹😹",
    "𝙎𝙐𝙋𝙋𝙊𝙍𝙏 𝙇𝘼 🤲🏿",
    "Bol 𝑬𝓸𝓷𝓲𝐗 ᴅꫝᴅᴅꪗ ❤‍🩹",
    "༆🤮꧂तेरी मांँ 売春婦 ᥫ😆᭄",
    "𝘽𝘼𝙐𝙉𝙀 मादरचोद ꧁🤮꧂",
    "𝐓𝐌𝐊𝐁 😹🔥😹🔥",
]

# ---------------------------
# NCEMO EMOJIS
# ---------------------------
NCEMO_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡","😠","😤",
    "😮‍💨","🙄","😒","🥶","🥵","🤢","🫠","😎","🥸","🕯","🫧","🦄","🌺","☘","🌊","🎀","♠","🧸","🌼","🌻","🌵","🌴","🌳","🌷","🌸",
    "😹","💫","😼","😽","🙀","😿","😾",
    "🙈","🙉","🙊",
    "⭐","🌟","✨","⚡","💥","💨",
    "💛","💙","💜","🤎","🤍","💘","💝"
]

# ---------------------------
# GLOBAL STATE
# ---------------------------
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}
with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

group_tasks = {}         
slide_targets = set()    
slidespam_targets = set()
swipe_mode = {}
apps, bots = [], []
delay = 1

logging.basicConfig(level=logging.INFO)

# ---------------------------
# DECORATORS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            return await update.message.reply_text("औकात बना बना बिहारी मादरचोद 👞🐕😹.")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("Aʙᴇ Cʜᴀʟ Tᴇʀɪ Mᴀᴀ Kᴀ Bʜᴏsᴅᴀ〽️👞.")
        return await func(update, context)
    return wrapper

# ---------------------------
# LOOP FUNCTION
# ---------------------------
async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raid":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"[WARN] Bot error in chat {chat_id}: {e}")
            await asyncio.sleep(2)

# ---------------------------
# COMMANDS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💗 Welcome to 𝐄𝐨𝐧𝐢𝐱  Bot!\nUse /help to see all commands.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 ༒𝐄𝐎𝐍𝐈𝐗 𝑀𝑈𝐿𝑇𝐼 𝐵𝑂𝑇 𝑀𝐸𝑁𝑈 2.0༒🎀👑\n\n"
        "⚡ GC Loops:\n"
        "/gcnc <text>\n/ncemo <text>\n/stopgcnc\n/stopall\n/delay <sec>\n/status\n\n"
        "🎯 Slide & Spam:\n"
        "/targetslide (reply)\n/stopslide (reply)\n/slidespam (reply)\n/stopslidespam (reply)\n\n"
        "⚡ Swipe Mode:\n"
        "/swipe <name>\n/stopswipe\n\n"
        "👑 SUDO:\n"
        "/addsudo (reply)\n/delsudo (reply)\n/listsudo\n\n"
        "🛠 Misc:\n/myid\n/ping"
    )

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"🏓 Pong! ✅ {latency} ms")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# --- GC Loops ---
@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /gcnc <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "raid"))
            group_tasks[chat_id][bot.id] = task
    await update.message.reply_text("Isᴋɪ Mᴀᴀ Cʜᴏᴅɴᴀ Sᴛᴀʀᴛ Kᴀʀ Dɪʏᴀ✔️☢️.")

@only_sudo
async def ncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /ncemo <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "emoji"))
            group_tasks[chat_id][bot.id] = task
    await update.message.reply_text("Eᴍᴏᴊɪ K Sᴀᴛʜ Mᴀᴀ Cʜᴜᴅᴇɢɪ Aʙ Isᴋɪ.")

@only_sudo
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
        await update.message.reply_text("⏹ 𝑅𝑂𝐾 𝐷𝐼𝑌𝐴 🙈💋")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id in list(group_tasks.keys()):
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
    await update.message.reply_text("⏹ 𝑅𝑂𝐾 𝐷𝐼𝑌𝐴 🙈💋")

@only_sudo
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args: return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    try:
        delay = max(0.5, float(context.args[0]))
        await update.message.reply_text(f"✔️ Oᴋ. Aʙ Isᴋɪ Mᴀᴀ Iᴛɴᴇ Sᴇᴄᴏɴᴅs Mᴇ Cʜᴜᴅᴇɢɪ {delay}s")
    except: await update.message.reply_text("⚠️ Invalid number.")

@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 Active Loops:\n"
    for chat_id, tasks in group_tasks.items():
        msg += f"Chat {chat_id}: {len(tasks)} bots running\n"
    await update.message.reply_text(msg)

# --- SUDO ---
@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        SUDO_USERS.add(uid); save_sudo()
        await update.message.reply_text(f"✅ {uid} Bɴᴀᴅɪʏᴀ Is Mᴄ Kᴏ Sᴜᴅᴏ.")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        if uid in SUDO_USERS:
            SUDO_USERS.remove(uid); save_sudo()
            await update.message.reply_text(f"🗑 {uid} Hᴀᴛ Bʜᴇɴ Kᴇ Lᴏᴅᴇ👞😹.")

@only_sudo
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 SUDO USERS:\n" + "\n".join(map(str, SUDO_USERS)))

# --- Slide / Spam / Swipe ---
@only_sudo
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Aʙ Isᴋɪ Cʜᴜᴅᴀɪ Sᴛᴀʀᴛ😹😹☢️👞.")

@only_sudo
async def stopslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        slide_targets.discard(uid)
        await update.message.reply_text("Bᴀᴄʜ Gʏᴀ Gᴀʀᴇᴇʙ👞👑 .")

@only_sudo
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Sʟɪᴅᴇ Sᴇ Isᴋɪ Bᴜᴀ Cʜᴜᴅᴇɢɪ Aʙ.")

@only_sudo
async def stopslidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.discard(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🛑 sʟɪᴅᴇ sᴘᴀᴍ ʀᴏᴋᴅɪʏᴀ.")

@only_sudo
async def swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /swipe <name>")
    swipe_mode[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"⚡ Sᴡɪᴘᴇ Sᴇ Mᴀᴀ Cʜᴜᴅᴇɢɪ Isᴋɪ🤪: {swipe_mode[update.message.chat_id]}")

@only_sudo
async def stopswipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    swipe_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 Sᴡɪᴘᴇ Sᴘᴀᴍ Rᴏᴋᴅɪʏᴀ.")

# --- Auto Replies ---
async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, chat_id = update.message.from_user.id, update.message.chat_id
    if uid in slide_targets:
        for text in RAID_TEXTS: await update.message.reply_text(text)
    if uid in slidespam_targets:
        for text in RAID_TEXTS: await update.message.reply_text(text)
    if chat_id in swipe_mode:
        for text in RAID_TEXTS: await update.message.reply_text(f"{swipe_mode[chat_id]} {text}")

# ---------------------------
# BUILD APP & RUN
# ---------------------------
def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(CommandHandler("ncemo", ncemo))
    app.add_handler(CommandHandler("stopgcnc", stopgcnc))
    app.add_handler(CommandHandler("stopall", stopall))
    app.add_handler(CommandHandler("delay", delay_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("listsudo", listsudo))
    app.add_handler(CommandHandler("targetslide", targetslide))
    app.add_handler(CommandHandler("stopslide", stopslide))
    app.add_handler(CommandHandler("slidespam", slidespam))
    app.add_handler(CommandHandler("stopslidespam", stopslidespam))
    app.add_handler(CommandHandler("swipe", swipe))
    app.add_handler(CommandHandler("stopswipe", stopswipe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    return app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if token.strip():
            try:
                app = build_app(token)
                apps.append(app); bots.append(app.bot)
            except Exception as e:
                print("Failed building app:", e)

    for app in apps:
        try:
            await app.initialize(); await app.start(); await app.updater.start_polling()
        except Exception as e:
            print("Failed starting app:", e)

    print("🚀 Eonix Bot is running (all bots started).")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_all_bots())
