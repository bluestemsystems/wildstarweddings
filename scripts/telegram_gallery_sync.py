#!/usr/bin/env python3
"""Pull new photos from a Telegram bot into the Wildstar Weddings gallery.

Runs in GitHub Actions on a timer. Polls the bot's getUpdates, downloads any new
photos sent by the allowed Telegram account, saves them under assets/img/gallery/,
and prepends an entry (newest first) to gallery/gallery.json.

Caption format you send with each photo:
    Title | The caption you want under the photo
If there is no "|", the whole caption is used as the caption (no title).

Environment:
    TELEGRAM_BOT_TOKEN        (required)  bot token from @BotFather
    TELEGRAM_ALLOWED_CHAT_ID  (optional)  only accept photos from this numeric id;
                                          if unset, accepts everyone (and prints the
                                          ids it sees so you can find yours).
"""

import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(REPO, "gallery", "gallery.json")
OFFSET_FILE = os.path.join(REPO, "gallery", ".tg_offset")
IMG_DIR = os.path.join(REPO, "assets", "img", "gallery")
WEB_DIR = "/assets/img/gallery"

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ALLOWED = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()

API = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"
_CTX = ssl.create_default_context()


def api_get(method, **params):
    url = f"{API}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, context=_CTX, timeout=60) as r:
        data = json.load(r)
    if not data.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {data}")
    return data["result"]


def download(file_id):
    info = api_get("getFile", file_id=file_id)
    path = info["file_path"]
    ext = os.path.splitext(path)[1] or ".jpg"
    with urllib.request.urlopen(f"{FILE_API}/{path}", context=_CTX, timeout=120) as r:
        return r.read(), ext


def read_offset():
    try:
        with open(OFFSET_FILE) as f:
            return int(f.read().strip() or 0)
    except (FileNotFoundError, ValueError):
        return 0


def parse_caption(text):
    text = (text or "").strip()
    if "|" in text:
        title, caption = text.split("|", 1)
        return title.strip(), caption.strip()
    return "", text


def main():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not set; skipping.")
        return 0

    offset = read_offset()
    updates = api_get("getUpdates", offset=offset, timeout=0, allowed_updates=json.dumps(["message"]))
    if not updates:
        print("No new updates.")
        return 0

    with open(GALLERY_JSON) as f:
        gallery = json.load(f)
    items = gallery.setdefault("items", [])

    new_offset = offset
    added = 0
    os.makedirs(IMG_DIR, exist_ok=True)

    for upd in updates:
        new_offset = max(new_offset, upd["update_id"] + 1)
        msg = upd.get("message")
        if not msg:
            continue

        sender = msg.get("from", {}).get("id")
        chat = msg.get("chat", {}).get("id")
        if ALLOWED:
            if str(sender) != ALLOWED and str(chat) != ALLOWED:
                print(f"Ignoring message from non-allowed id (from={sender}, chat={chat}).")
                continue
        else:
            print(f"[no allow-list set] message from from={sender}, chat={chat}")

        # photos sent as photo, or as an image document
        file_id = None
        if msg.get("photo"):
            file_id = msg["photo"][-1]["file_id"]  # largest size
        elif msg.get("document", {}).get("mime_type", "").startswith("image/"):
            file_id = msg["document"]["file_id"]
        if not file_id:
            continue

        title, caption = parse_caption(msg.get("caption"))
        try:
            blob, ext = download(file_id)
        except Exception as e:  # noqa: BLE001
            print(f"Failed to download {file_id}: {e}")
            continue

        fname = f"tg-{upd['update_id']}-{int(time.time())}{ext}"
        with open(os.path.join(IMG_DIR, fname), "wb") as f:
            f.write(blob)

        items.insert(0, {
            "src": f"{WEB_DIR}/{fname}",
            "title": title,
            "caption": caption,
            "date": date.today().isoformat(),
        })
        added += 1
        print(f"Added {fname} (title={title!r})")

    with open(GALLERY_JSON, "w") as f:
        json.dump(gallery, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(OFFSET_FILE, "w") as f:
        f.write(str(new_offset) + "\n")

    print(f"Done. Added {added} photo(s). Offset now {new_offset}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
