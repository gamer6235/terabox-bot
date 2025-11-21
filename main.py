import os
import requests
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("terabox-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# List of fallback APIs — biri try ചെയ്ത് success link കിട്ടാത്തുവേള്‍ മറ്റൊന്ന് try ചെയ്യും
API_LIST = [
    "https://mediabox.vercel.app/api?url=",
    "https://terabox-api-hk.vercel.app/api?url="
]

def get_direct_url(link):
    # Try each API in list with retries and return debug info on failure
    for base in API_LIST:
        api = base + link
        try:
            resp = requests.get(api, timeout=10)
        except Exception as e:
            # network/DNS error — return tuple (None, debug_string)
            debug = f"REQUEST-ERROR for {base}: {repr(e)}"
            return None, debug

        debug = f"API={base} STATUS={resp.status_code} LEN={len(resp.text)}"

        # Try parse json safely
        try:
            data = resp.json()
        except Exception as e:
            # non-json response — include first 400 chars for debug
            snippet = resp.text[:400].replace("\n"," ")
            debug += f" JSON-DECODE-ERR: {repr(e)} SNIPPET='{snippet}'"
            # continue to next API instead of immediate fail
            continue

        # try known keys (different apis use different keys)
        for key in ("downloadUrl", "direct_link", "direct_link", "directLink", "download_url"):
            if isinstance(data, dict) and key in data and data[key]:
                return data[key], debug + f" -> FOUND key={key}"
        # if API returned a string directly
        if isinstance(data, str) and data.startswith("http"):
            return data, debug + " -> FOUND string"
        # else continue trying next API
        debug += " -> key-not-found"
    return None, debug

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 Send Terabox share link. I'll try fetch direct url (debug enabled).")

@app.on_message(filters.text)
async def download(_, msg):
    link = msg.text.strip()
    await msg.reply("⏳ Trying to fetch direct url...")

    url, debug = get_direct_url(link)
    # send debug info so you can see what went wrong
    if not url:
        await msg.reply(f"❌ Unable to get direct link.\nDebug: {debug}")
        return

    await msg.reply(f"✅ Direct link found. {debug}\nUploading...")
    await msg.reply_document(url)

app.run()
