from pyrogram import Client, filters as ay
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
from requests import get
import os

token = input("[~] Enter Bot Token : ") or '2146982601'
Sudo_id = input("[~] Enter Sudo id : ") or 944353237

opts = {
   "format": "best",
   "keepvideo": True,
   "prefer_ffmpeg": False,
   "geo_bypass": True,
   "outtmpl": "%(title)s.%(ext)s",
   "quite": True,
}

bot = Client(
   'youtube-bot',
   7720093,
   '51560d96d683932d1e68851e7f0fdea2',
   bot_token=token
)

@bot.on_message(~ay.private)
async def ahmed(client, message):
   try:
      await message.reply_text("انا اعمل في الخاص فقط")
   except Exception as e:
      pass
   await client.leave_chat(message.chat.id)

@bot.on_message(ay.command("start"))
async def start(client, message):
   await message.reply_text(
      "اهلا انا بوت تحميل من يوتيوب\nاستطيع رفع فيديوهات حتا 2GB\nفقط ارسل رابط التحميل وساقوم بالتحميل ورفعه لك",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("المطور", url=f"https://t.me/YYYBD"),
               InlineKeyboardButton("قناة البوت", url=f"https://t.me/YYYBR"),
            ]
         ]
      )
   )

@bot.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   msg = await message.reply_text("جاري معالجة الرابط")
   try:
      with YoutubeDL(opts) as ytdl:
         await msg.edit_text("جاري التحميل")
         ytdl_data = ytdl.extract_info(message.text, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await msg.edit_text(e)
      return
   await msg.edit_text("جاري الرفع")
   await message.reply_video(video_file,supports_streaming=True)
   await msg.delete()
   os.remove(video_file)

print("اشتغل يظميلي")
print("الملف بتاع @YYYBD")
bot.run()
