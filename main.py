import os
import requests
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("terabox-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def get_direct_url(link):
    api = "https://mediabox.vercel.app/api?url=" + link

    try:
        response = requests.get(api, timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()
        return data.get("downloadUrl")

    except:
        return None


@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 ഏത് Terabox link ആണെങ്കിലും അയച്ചാൽ ഞാൻ download ചെയ്ത് തരാം (1GB+ OK).")


@app.on_message(filters.text)
async def download(_, msg):
    link = msg.text.strip()
    await msg.reply("⏳ ലിങ്ക് പരിശോധിക്കുന്നു...")

    direct = get_direct_url(link)

    if not direct:
        return await msg.reply("❌ Direct link എടുക്കാൻ പറ്റില്ല. API busy അല്ലെങ്കിൽ Terabox link തെറ്റാണ്.")

    await msg.reply("⬆️ Upload ചെയ്യുന്നു... (വലിയ ഫയലുകൾക്ക് സമയം എടുക്കും)")
    await msg.reply_document(direct)


app.run()
