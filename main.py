from pyrogram import Client, filters as ay
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from yt_dlp import YoutubeDL
from requests import get
import os, wget

def GetInfo():
   try:
      from info import token, Sudo_id, bot_id
   except:
      token, Sudo_id = False, False
      while not token:
         ayad = input("[~] Enter Bot Token : ")
         info = get(f"https://api.telegram.org/bot{ayad}/getme").json()
         if info.get('ok') == False:
            print("التوكن غلط يظميلي")
         else:
            print("توكن اخر في المصيدة")
            token = ayad
            bot_id = info.get("result").get("id")

      while not Sudo_id:
         ayad = input("[~] Enter Sudo id : ") or 944353237
         info = get(f"https://api.telegram.org/bot{token}/getchat?chat_id={ayad}").json()
         if info.get('ok') == False:
            print("الايدي غلط او صاحبه معملتش start ف البوت")
         else:
            print("تيجي انا وانت نلعب باليه")
            Sudo_id = ayad
      print("جاري حفظ البيانات")
      f = open("info.py", "w")
      f.write(f"token = '{token}'\nSudo_id = {Sudo_id}\nbot_id = {bot_id}")
      f.close()
      GetInfo()
   return token, Sudo_id, bot_id

token, Sudo_id, bot_id = GetInfo()

video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}

bot = Client(
   f'.{bot_id}-bot',
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
   await client.send_message(chat_id=Sudo_id,text=f"العضو : {message.from_user.mention()}\nضغط start في بوتك\nالايدي : `{message.from_user.id}`")

@bot.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"رابط المقطع : {message.text}",disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("تحميل صوت", callback_data="audio"),
               InlineKeyboardButton("تحميل فيديو", callback_data="video"),
            ]
         ]
      )
   )

@bot.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("انتظر")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text("جاري التحميل")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("جاري الرفع")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text("تم الارسال")
   os.remove(video_file)

@bot.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("انتظر")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text("جاري التحميل")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("جاري الرفع")
   await client.send_audio(
      callback_query.message.chat.id,
      audio=audio_file,
      duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})"
   )
   await callback_query.edit_message_text("تم الارسال")
   os.remove(audio_file)
   os.remove(thumb)


print("البوت اشتغل غور")
bot.run()
