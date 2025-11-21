import os
import requests
import re
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Memory session → FloodWait ഇല്ല
app = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def get_direct_url(link):
    try:
        if "www" not in link:
            link = link.replace("terabox.com", "www.terabox.com")

        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(link, headers=headers, timeout=10).text

        # First pattern (most common)
        match1 = re.search(r'"downloadUrl":"(https:[^"]+)"', html)
        if match1:
            url = match1.group(1).replace("\\u002F", "/").replace("\\", "")
            return url

        # Second pattern (fallback)
        match2 = re.search(r'"direct_link":"(https:[^"]+)"', html)
        if match2:
            url = match2.group(1).replace("\\u002F", "/").replace("\\", "")
            return url

        return None

    except:
        return None


@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 Terabox link അയക്കൂ! ഞാൻ download ചെയ്ത് നൽകാം.")


@app.on_message(filters.text)
async def dl(_, msg):
    link = msg.text.strip()
    await msg.reply("🔍 Link പരിശോധിക്കുന്നു...")

    url = get_direct_url(link)

    if not url:
        return await msg.reply("❌ Direct link കിട്ടിയില്ല.\n➡ Link public ആണോ എന്ന് check ചെയ്യൂ.")

    await msg.reply("⬆️ Upload ചെയ്യുന്നു... കുറച്ചു സമയം എടുക്കും.")
    await msg.reply_document(url)


app.run()
