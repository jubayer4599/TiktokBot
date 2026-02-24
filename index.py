import os
import telebot
import requests
from flask import Flask, request
from telebot.types import InputMediaPhoto

# Environment variable থেকে টোকেন নেওয়া ভালো, তবে আপাতত আপনারটিই দিলাম
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8450856906:AAHO5RMn0fpmPJ78aZMFtToWHlXYLFyeqJQ')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

API_URL = "https://www.tikwm.com/api/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        welcome_text_bangla = (
            "👋 স্বাগতম! আমি একটি প্রিমিয়াম টিকটক ভিডিও অডিও ফটো কেপশন ডাউনলোডার বট।\n\n"
            "🚀 আমার ক্ষমতা বা ফিচারের তালিকা:\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ লোগো ছাড়া ফ্রেশ ভিডিও।\n"
            "📸 স্লাইডশো থেকে ছবি ডাউনলোড।\n"
            "🎵 ভিডিও থেকে MP3 সংগ্রহ।\n"
            "📊 লাইক এবং ভিউস সংখ্যা দেখা।\n"
            "⚡ সুপার ফাস্ট প্রসেসিং ও ডেলিভারি।\n"
            "📂 বড় সাইজ ভিডিও সাপোর্ট।\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💡 ব্যবহার নিয়ম: শুধু একটি TikTok ভিডিও লিংক পাঠান।\n\n"
            "➥ ᴘᴏᴡᴇʀ  ʙʏ  ᴊᴜʙᴀʏᴇʀ  ♡ جباير"
        )

        welcome_text_english = (
            "👋 Welcome! I am a premium TikTok video audio photo caption downloader bot.\n\n"
            "🚀 My capabilities or feature list:\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ Watermark Removed\n"
            "📸 Download photos from slideshow.\n"
            "🎵 Extract MP3 from video.\n"
            "📊 Real-time View like and view counts.\n"
            "⚡ Super fast processing and delivery.\n"
            "📂 Supports large size videos.\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💡 Usage Instructions: Just send a TikTok video link.\n\n"
            "➥ ᴘᴏᴡᴇʀ  ʙʏ  ᴊᴜʙᴀʏᴇʀ  ♡ جباير"
        )

        welcome_text = f"{welcome_text_bangla}\n\n{'━'*30}\n\n{welcome_text_english}"
        
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, welcome_text, parse_mode="Markdown")
    except Exception as e:
        pass

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    try:
        url = message.text.strip()

        if "tiktok.com" not in url:  
            bot.reply_to(message, "❌ সঠিক TikTok লিংক দিন।")  
            return  

        status_msg = bot.reply_to(message, "Wait... প্রসেসিং হচ্ছে ⏳")  
        bot.send_chat_action(message.chat.id, 'upload_video')  

        try:  
            response = requests.get(API_URL, params={"url": url}, headers=HEADERS, timeout=20)  
            data = response.json()  
        except Exception as e:  
            bot.edit_message_text("⚠️ সার্ভার এরর! আবার চেষ্টা করুন।", chat_id=message.chat.id, message_id=status_msg.message_id)  
            return  

        if data.get("code") == 0:  
            video_data = data.get("data")  
              
            title = video_data.get("title", "No Title")  
            likes = video_data.get("digg_count", 0)  
            views = video_data.get("play_count", 0)  
            author = video_data.get("author", {}).get("unique_id", "Unknown")  
            images = video_data.get("images")  

            if len(title) > 800:  
                title = title[:800] + "..."  

            caption_text = (  
                f"👤ᴛɪᴋᴛᴏᴋ: @{author}\n"  
                f"╔═══════════════╗\n"  
                f"╠ ʟɪᴋᴇ ❤️: {likes:,}\n"  
                f"║\n"  
                f"╠ ᴠɪᴇᴡs 👀: {views:,}\n"  
                f"╚═══════════════╝\n"  
                f"📝 {title}\n\n"  
                f"➥ ᴘᴏᴡᴇʀ  ʙʏ @jubayer3501"  
            )  

            if images and len(images) > 0:  
                bot.edit_message_text("📸 ছবি আপলোড হচ্ছে...", chat_id=message.chat.id, message_id=status_msg.message_id)  
                media_group = [InputMediaPhoto(img) for img in images[:10]]  
                media_group[0].caption = caption_text  
                bot.send_media_group(message.chat.id, media_group)  
                  
                if video_data.get("music"):  
                    try:
                        bot.send_audio(message.chat.id, video_data.get("music"), caption=f"🎵 Music for @{author}")  
                    except:
                        pass
                
                try: 
                    bot.delete_message(message.chat.id, status_msg.message_id)  
                except: 
                    pass  

            else:  
                video_url = video_data.get("play")  
                bot.edit_message_text("🚀 ভিডিও আপলোড হচ্ছে...", chat_id=message.chat.id, message_id=status_msg.message_id)  
                  
                try:  
                    bot.send_video(message.chat.id, video_url, caption=caption_text, timeout=150)  
                    try:
                        bot.delete_message(message.chat.id, status_msg.message_id)  
                    except:
                        pass
                except Exception as e:  
                    bot.edit_message_text(f"{caption_text}\n\n🔗 [Download Link]({video_url})", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")  

        else:  
            bot.edit_message_text("❌ ভিডিও পাওয়া যায়নি।", chat_id=message.chat.id, message_id=status_msg.message_id)  

    except Exception as e:  
        try: 
            bot.reply_to(message, "⚠️ সমস্যা হয়েছে, আবার চেষ্টা করুন।")  
        except: 
            pass

# Vercel-এর জন্য Webhook Route
@app.route('/', methods=['GET'])
def index():
    return "Bot is successfully running on Vercel!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Error', 403
