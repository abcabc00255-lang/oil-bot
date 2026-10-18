import time, feedparser, requests, threading
from deep_translator import GoogleTranslator
from PIL import Image, ImageDraw, ImageFont
import textwrap
from flask import Flask

# --- Keep Render Alive ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running!"
def run_flask():
    app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_flask).start()

# --- BOT CONFIG ---
TWITTER_USER = "MarioNawfal"
RSS_URL = f"https://rsshub.app/twitter/user/{TWITTER_USER}"
TELEGRAM_TOKEN = "8703081151:AAGaIQu3yX8FAdDrLA6aPV_CUPyOiYRhIwg"
TELEGRAM_CHAT_ID = "8814220350"
translator = GoogleTranslator(source='en', target='ur')

def get_latest_tweet():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries: return None, None, None
    e = feed.entries[0]
    return e.title, e.link, e.id

def make_thumbnail(urdu_hook, output="/tmp/thumbnail.jpg"):
    img = Image.new('RGB', (1080, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    try:
        font_big = ImageFont.truetype("arial.ttf", 80)
        font_urdu = ImageFont.truetype("arial.ttf", 60)
    except:
        font_big = ImageFont.load_default()
        font_urdu = font_big
    draw.rectangle([(0,0),(1080, 160)], fill=(180, 20, 20))
    draw.text((40, 40), "BREAKING NEWS", fill="white", font=font_big)
    wrapped = textwrap.wrap(urdu_hook, width=22)
    y = 450
    for line in wrapped:
        draw.text((50, y), line, fill="white", font=font_urdu)
        y += 80
    img.save(output)
    return output

def send_to_telegram(photo_path, caption):
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as f:
        requests.post(url_photo, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"photo": f})

last_id = ""
while True:
    try:
        eng, link, tweet_id = get_latest_tweet()
        if eng and tweet_id != last_id:
            last_id = tweet_id
            urdu = translator.translate(eng)
            caption = f"🚨🇸🇦 {urdu}\n\nSource: @{TWITTER_USER}\n{link}\n#Breaking"
            thumb = make_thumbnail(urdu[:80])
            send_to_telegram(thumb, caption)
            print("✅ Sent to Telegram!")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(300)
