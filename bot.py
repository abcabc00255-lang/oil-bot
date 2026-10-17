import time, feedparser, requests
from deep_translator import GoogleTranslator

# --- FINAL CONFIG - Sab fill hai ---
TELEGRAM_BOT_TOKEN = "8703081151:AAGaIQu3yX8FAdDrLA6aPV_CUPyOiYRhIwg"
TELEGRAM_CHAT_ID = "8814220350"
FB_SYSTEM_TOKEN = "EAAXUYhX94UEBS2fOVXSkzqSIhjWYJZCoDhvp6ZB6VZA3JNhQqSR2x8oimwyZCmcr5FvmepTr0sK6A4tWZAzhe7nwWNyQL3wK1gZCjcBEWUZCX5dyxcQR5gGvUxbp7XvE30CgPQdKboTV3fSt6iO5tE9BscUSVeYbOYZAzhrL7lVdBwUUYB7ooffZAQKV8ejHGxTuQZDZD"
TWITTER_USER = "MarioNawfal"
RSS_URL = f"https://rsshub.app/twitter/user/{TWITTER_USER}"

print("Bot Starting...")

def get_page_token():
    try:
        r = requests.get(f"https://graph.facebook.com/v19.0/me/accounts?access_token={FB_SYSTEM_TOKEN}").json()
        print(f"Facebook Response: {r}")
        page = r['data'][0]
        return page['id'], page['access_token']
    except Exception as e:
        print(f"Page nahi mila, saare pages check karo: {e}")
        return None, None

PAGE_ID, PAGE_TOKEN = get_page_token()

if PAGE_ID:
    print(f"Page Found: {PAGE_ID} - Bot Ready!")
else:
    print("Page ID nahi mila, aapka token pages permission nahi de raha. Pages_show_list add karna hoga.")

translator = GoogleTranslator(source='en', target='ur')
last_tweet_id = ""

while True:
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            latest = feed.entries[0]
            if latest.id != last_tweet_id and last_tweet_id != "":
                original_text = latest.title
                print(f"New Tweet Found: {original_text}")

                # Translate
                urdu_text = translator.translate(original_text)

                # Aapka Format
                final_format = f"🚨 بریکنگ نیوز 🚨\n\n{urdu_text}\n\nاصل خبر: {original_text}\n\nSource: @{TWITTER_USER}"

                # 1. Telegram par
                requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params={"chat_id": TELEGRAM_CHAT_ID, "text": final_format})
                
                # 2. Facebook par
                if PAGE_ID:
                    requests.post(f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed", data={"message": final_format, "access_token": PAGE_TOKEN})
                
                print("Posted Successfully!")
            
            last_tweet_id = latest.id

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(300) # 5 minute
