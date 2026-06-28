# Telegram → Gallery setup

Forward a photo to your bot and it appears in the website gallery automatically.
A GitHub Action checks the bot every ~10 minutes, downloads new photos, and commits
them to the site.

## One-time setup

1. **Create the bot**
   - In Telegram, message **@BotFather** → `/newbot` → follow prompts.
   - Copy the **bot token** it gives you (looks like `123456:ABC-DEF...`).

2. **Find your numeric Telegram ID**
   - Message **@userinfobot** in Telegram; it replies with your `Id` (a number).
   - This locks the gallery to only accept photos from you.

3. **Add both as repository secrets** (GitHub → repo **Settings → Secrets and variables → Actions → New repository secret**):
   - `TELEGRAM_BOT_TOKEN` = the bot token from step 1
   - `TELEGRAM_ALLOWED_CHAT_ID` = your numeric id from step 2

4. **Say hi to the bot** in Telegram (send it any message once) so it's allowed to see your messages.

That's it. The workflow (`.github/workflows/gallery-sync.yml`) runs on a timer; you can
also trigger it manually under the repo's **Actions** tab → *Gallery sync (Telegram)* → *Run workflow*.

## How to post a photo

Send (or forward) a photo **to your bot** with a caption in this format:

```
Title | The caption you want under the photo
```

- Text **before** the `|` becomes the bold title.
- Text **after** the `|` becomes the caption.
- No `|`? The whole caption is used as the caption, with no title.
- No caption at all? The photo still posts, with no title/caption.

New photos appear at the **top** of the gallery within ~10–15 minutes.

## Notes

- Photos are saved to `assets/img/gallery/` and listed in `gallery/gallery.json`
  (newest first). You can hand-edit that JSON anytime to change titles/captions,
  reorder, or remove photos.
- The 10 original photos are seeded in `gallery.json` with blank titles/captions —
  edit them there if you want to add text.
- Send photos as a **photo** or as an image **file**; both work.
