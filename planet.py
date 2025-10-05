import swisseph as swe
from datetime import datetime
import requests

# --- Telegram Bot Config ---
BOT_TOKEN = '7718468355:AAEQc0dSgLjTYVWGrmPRZAY0VshGXxsJCFU'  # 🔁 Replace with your bot token
CHAT_ID = '-4716730270'      # 🔁 Replace with your Telegram chat ID

# --- Swiss Ephemeris Setup ---
swe.set_ephe_path('.')  # If eph files are in current directory
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri Ayanamsa

# --- Zodiac Signs & Symbols ---
ZODIAC_SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
ZODIAC_SYMBOLS = ['♈', '♉', '♊', '♋', '♌', '♍',
                  '♎', '♏', '♐', '♑', '♒', '♓']

# --- Planets and their Symbols ---
PLANETS = {
    '☉ Sun': swe.SUN,
    '☽ Moon': swe.MOON,
    '☿ Mercury': swe.MERCURY,
    '♀ Venus': swe.VENUS,
    '♂ Mars': swe.MARS,
    '♃ Jupiter': swe.JUPITER,
    '♄ Saturn': swe.SATURN,
    '♅ Uranus': swe.URANUS,
    '♆ Neptune': swe.NEPTUNE,
    '♇ Pluto': swe.PLUTO,
    '☊ Rahu': swe.MEAN_NODE
}

def get_rashi(deg):
    index = int(deg // 30)
    return ZODIAC_SIGNS[index], ZODIAC_SYMBOLS[index], index  # include index for sorting

def get_planet_positions():
    now = datetime.now()
    jd = swe.julday(now.year, now.month, now.day, 0.0)
    positions = []

    for name, pid in PLANETS.items():
        lon, _ = swe.calc_ut(jd, pid)
        deg = lon[0] % 360

        if name == '☊ Rahu':
            # Ketu position
            ketu_deg = (deg + 180) % 360
            ketu_rashi, ketu_symbol, ketu_index = get_rashi(ketu_deg)
            positions.append(("☋ Ketu", ketu_deg, ketu_rashi, ketu_symbol, ketu_index))

        rashi, symbol, rashi_index = get_rashi(deg)
        positions.append((name, deg, rashi, symbol, rashi_index))

    # Sort by zodiac sign (index) and degree within sign
    sorted_positions = sorted(positions, key=lambda x: (x[4], x[1] % 30))

    # Build formatted message
    message = f"🌌 *Planetary Positions* — `{now.strftime('%Y-%m-%d')}`\n📍 *Sidereal Zodiac* (Lahiri)\n\n"
    for name, deg, rashi, symbol, _ in sorted_positions:
        message += f"{name}: `{round(deg, 2)}°` — {rashi} {symbol}\n"

    return message

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Sent to Telegram")
    else:
        print("❌ Failed to send:", response.text)

# --- Run Script ---
msg = get_planet_positions()
send_to_telegram(msg)