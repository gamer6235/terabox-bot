import os
import requests
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client(":memory:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_direct_url(link):
    try:
        api = f"https://api.sparky.biz.id/api/downloader/terrabox?url={link}"
        res = requests.get(api, timeout=20).json()

        # Success result
        if res.get("status") and res.get("data") and res["data"].get("dlink"):
            return res["data"]["dlink"], res["data"].get("title"), res["data"].get("size")

        return None, None, None
    except:
        return None, None, None


@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 *Terabox link അയയ്ക്കൂ*, ഞാൻ download link പിടിച്ചു തരാം!")


@app.on_message(filters.text)
async def download(_, msg):
    link = msg.text.strip()
    await msg.reply("🔍 Processing Terabox link...")

    dlink, title, size = get_direct_url(link)

    if not dlink:
        return await msg.reply("❌ Direct link കിട്ടിയില്ല.\n🔸 Link ശരിയായതാണോ check ചെയ്യൂ.")

    # Info message
    await msg.reply(f"📥 **File:** `{title}`\n📦 **Size:** {size}\n\n⬆️ Upload ചെയ്യുന്നു...")

    # Upload to Telegram
    await msg.reply_document(dlink, file_name=title)


app.run()
