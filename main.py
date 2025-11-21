import os
import requests
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("terabox-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_direct_url(link):
    api = "https://terabox-api-hk.vercel.app/api?url=" + link
    r = requests.get(api).json()
    return r.get("direct_link")

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 Hi! Send a Terabox link.")

@app.on_message(filters.text)
async def download(_, msg):
    link = msg.text.strip()
    await msg.reply("⏳ Getting download link…")

    url = get_direct_url(link)
    if not url:
        return await msg.reply("❌ Unable to get direct link.")

    await msg.reply("⬆️ Uploading file…")
    await msg.reply_document(url)

app.run()
