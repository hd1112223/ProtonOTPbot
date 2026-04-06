import time
import requests
import logging
import json
import os
import re
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut
import asyncio

# === CONFIG ===
BOT_TOKEN = '8515176529:AAGqHoinX-3DlDhL-d1NtCT1mIBiXfYyIPA'
CHAT_ID = '-1003212961512'
USERNAME = 'otpbot16'
PASSWORD = 'otpbot16'
BASE_URL = "http://109.236.84.81/"
LOGIN_PAGE_URL = BASE_URL + "/ints/login"
LOGIN_POST_URL = BASE_URL + "/ints/signin"
DATA_URL = BASE_URL + "/ints/client/res/data_smscdr.php"

bot = Bot(token=BOT_TOKEN)
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
logging.basicConfig(level=logging.INFO, format='%(message)s')

# === Country Code Map ===
COUNTRY_MAP = {
    '1': '🇺🇸 USA / Canada',
    '7': '🇷🇺 Russia / Kazakhstan',
    '20': '🇪🇬 Egypt',
    '27': '🇿🇦 South Africa',
    '30': '🇬🇷 Greece',
    '31': '🇳🇱 Netherlands',
    '32': '🇧🇪 Belgium',
    '33': '🇫🇷 France',
    '34': '🇪🇸 Spain',
    '36': '🇭🇺 Hungary',
    '39': '🇮🇹 Italy',
    '40': '🇷🇴 Romania',
    '41': '🇨🇭 Switzerland',
    '43': '🇦🇹 Austria',
    '44': '🇬🇧 United Kingdom',
    '45': '🇩🇰 Denmark',
    '46': '🇸🇪 Sweden',
    '47': '🇳🇴 Norway',
    '48': '🇵🇱 Poland',
    '49': '🇩🇪 Germany',
    '51': '🇵🇪 Peru',
    '52': '🇲🇽 Mexico',
    '53': '🇨🇺 Cuba',
    '54': '🇦🇷 Argentina',
    '55': '🇧🇷 Brazil',
    '56': '🇨🇱 Chile',
    '57': '🇨🇴 Colombia',
    '58': '🇻🇪 Venezuela',
    '60': '🇲🇾 Malaysia',
    '61': '🇦🇺 Australia',
    '62': '🇮🇩 Indonesia',
    '63': '🇵🇭 Philippines',
    '64': '🇳🇿 New Zealand',
    '65': '🇸🇬 Singapore',
    '66': '🇹🇭 Thailand',
    '81': '🇯🇵 Japan',
    '82': '🇰🇷 South Korea',
    '84': '🇻🇳 Vietnam',
    '86': '🇨🇳 China',
    '90': '🇹🇷 Turkey',
    '91': '🇮🇳 India',
    '92': '🇵🇰 Pakistan',
    '93': '🇦🇫 Afghanistan',
    '94': '🇱🇰 Sri Lanka',
    '95': '🇲🇲 Myanmar',
    '98': '🇮🇷 Iran',
    '211': '🇸🇸 South Sudan',
    '212': '🇲🇦 Morocco',
    '213': '🇩🇿 Algeria',
    '216': '🇹🇳 Tunisia',
    '218': '🇱🇾 Libya',
    '220': '🇬🇲 Gambia',
    '221': '🇸🇳 Senegal',
    '222': '🇲🇷 Mauritania',
    '223': '🇲🇱 Mali',
    '224': '🇬🇳 Guinea',
    '225': '🇨🇮 Côte d\'Ivoire',
    '226': '🇧🇫 Burkina Faso',
    '227': '🇳🇪 Niger',
    '228': '🇹🇬 Togo',
    '229': '🇧🇯 Benin',
    '230': '🇲🇺 Mauritius',
    '231': '🇱🇷 Liberia',
    '232': '🇸🇱 Sierra Leone',
    '233': '🇬🇭 Ghana',
    '234': '🇳🇬 Nigeria',
    '235': '🇹🇩 Chad',
    '236': '🇨🇫 Central African Republic',
    '237': '🇨🇲 Cameroon',
    '238': '🇨🇻 Cape Verde',
    '239': '🇸🇹 Sao Tome & Principe',
    '240': '🇬🇶 Equatorial Guinea',
    '241': '🇬🇦 Gabon',
    '242': '🇨🇬 Congo',
    '243': '🇨🇩 DR Congo',
    '244': '🇦🇴 Angola',
    '249': '🇸🇩 Sudan',
    '250': '🇷🇼 Rwanda',
    '251': '🇪🇹 Ethiopia',
    '252': '🇸🇴 Somalia',
    '253': '🇩🇯 Djibouti',
    '254': '🇰🇪 Kenya',
    '255': '🇹🇿 Tanzania',
    '256': '🇺🇬 Uganda',
    '257': '🇧🇮 Burundi',
    '258': '🇲🇿 Mozambique',
    '260': '🇿🇲 Zambia',
    '261': '🇲🇬 Madagascar',
    '263': '🇿🇼 Zimbabwe',
    '264': '🇳🇦 Namibia',
    '265': '🇲🇼 Malawi',
    '266': '🇱🇸 Lesotho',
    '267': '🇧🇼 Botswana',
    '268': '🇸🇿 Eswatini',
    '269': '🇰🇲 Comoros',
    '290': '🇸🇭 Saint Helena',
    '291': '🇪🇷 Eritrea',
    '297': '🇦🇼 Aruba',
    '298': '🇫🇴 Faroe Islands',
    '299': '🇬🇱 Greenland',
    '350': '🇬🇮 Gibraltar',
    '351': '🇵🇹 Portugal',
    '352': '🇱🇺 Luxembourg',
    '353': '🇮🇪 Ireland',
    '354': '🇮🇸 Iceland',
    '355': '🇦🇱 Albania',
    '356': '🇲🇹 Malta',
    '357': '🇨🇾 Cyprus',
    '358': '🇫🇮 Finland',
    '359': '🇧🇬 Bulgaria',
    '370': '🇱🇹 Lithuania',
    '371': '🇱🇻 Latvia',
    '372': '🇪🇪 Estonia',
    '373': '🇲🇩 Moldova',
    '374': '🇦🇲 Armenia',
    '375': '🇧🇾 Belarus',
    '376': '🇦🇩 Andorra',
    '377': '🇲🇨 Monaco',
    '378': '🇸🇲 San Marino',
    '380': '🇺🇦 Ukraine',
    '381': '🇷🇸 Serbia',
    '382': '🇲🇪 Montenegro',
    '383': '🇽🇰 Kosovo',
    '385': '🇭🇷 Croatia',
    '386': '🇸🇮 Slovenia',
    '387': '🇧🇦 Bosnia & Herzegovina',
    '389': '🇲🇰 North Macedonia',
    '420': '🇨🇿 Czech Republic',
    '421': '🇸🇰 Slovakia',
    '423': '🇱🇮 Liechtenstein',
    '852': '🇭🇰 Hong Kong',
    '853': '🇲🇴 Macau',
    '855': '🇰🇭 Cambodia',
    '856': '🇱🇦 Laos',
    '880': '🇧🇩 Bangladesh',
    '886': '🇹🇼 Taiwan',
    '960': '🇲🇻 Maldives',
    '961': '🇱🇧 Lebanon',
    '962': '🇯🇴 Jordan',
    '963': '🇸🇾 Syria',
    '964': '🇮🇶 Iraq',
    '965': '🇰🇼 Kuwait',
    '966': '🇸🇦 Saudi Arabia',
    '967': '🇾🇪 Yemen',
    '968': '🇴🇲 Oman',
    '970': '🇵🇸 Palestine',
    '971': '🇦🇪 UAE',
    '972': '🇮🇱 Israel',
    '973': '🇧🇭 Bahrain',
    '974': '🇶🇦 Qatar',
    '975': '🇧🇹 Bhutan',
    '976': '🇲🇳 Mongolia',
    '977': '🇳🇵 Nepal',
    '992': '🇹🇯 Tajikistan',
    '993': '🇹🇲 Turkmenistan',
    '994': '🇦🇿 Azerbaijan',
    '995': '🇬🇪 Georgia',
    '996': '🇰🇬 Kyrgyzstan',
    '998': '🇺🇿 Uzbekistan'
}

def get_country_from_number(number: str) -> str:
    for code in sorted(COUNTRY_MAP.keys(), key=lambda x: -len(x)):
        if number.startswith(code):
            return COUNTRY_MAP[code]
    return '🌍 Unknown'

def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def save_already_sent(already_sent):
    with open("already_sent.json", "w") as f:
        json.dump(list(already_sent), f)

def load_already_sent():
    if os.path.exists("already_sent.json"):
        with open("already_sent.json", "r") as f:
            return set(json.load(f))
    return set()

def login():
    try:
        resp = session.get(LOGIN_PAGE_URL)
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            logging.error("Captcha not found.")
            return False
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2

        payload = {"username": USERNAME, "password": PASSWORD, "capt": captcha_answer}
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": LOGIN_PAGE_URL}

        resp = session.post(LOGIN_POST_URL, data=payload, headers=headers)
        if "dashboard" in resp.text.lower() or "logout" in resp.text.lower():
            logging.info("Login successful ✅")
            return True
        else:
            logging.error("Login failed ❌")
            return False
    except Exception as e:
        logging.error(f"Login error: {e}")
        return False

def build_api_url():
    start_date = "2026-01-01"
    end_date = "2027-01-01"
    return (
        f"{DATA_URL}?fdate1={start_date}%2000:00:00&fdate2={end_date}%2023:59:59&"
        "frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&"
        "sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&"
        "mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&"
        "mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&"
        "mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&"
        "mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&"
        "mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&"
        "mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&"
        "mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&"
        "sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1"
    )

def fetch_data():
    url = build_api_url()
    headers = {"X-Requested-With": "XMLHttpRequest"}

    try:
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 or "login" in response.text.lower():
            logging.warning("Session expired. Re-logging...")
            if login():
                return fetch_data()
            return None
        else:
            logging.error(f"Unexpected error: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return None

already_sent = load_already_sent()

async def sent_messages():
    logging.info("🔍 Checking for messages...\n")
    data = fetch_data()

    if data and 'aaData' in data:
        for row in data['aaData']:
            date = str(row[0]).strip()
            number = str(row[2]).strip()
            service = str(row[3]).strip()
            message = str(row[4]).strip()

            match = re.search(r'\d{3}-\d{3}|\d{4,6}', message)
            otp = match.group() if match else None

            if otp:
                unique_key = f"{number}|{otp}"
                if unique_key not in already_sent:
                    already_sent.add(unique_key)

                    country = get_country_from_number(number)

                    text = (
                        "✨ <b>OTP Received</b> ✨\n\n"
                        f"⏰ <b>Time:</b> {escape_html(date)}\n"
                        f"📞 <b>Number:</b> {escape_html(number)}\n"
                        f"🌍 <b>Country:</b> {country}\n"
                        f"🔧 <b>Service:</b> {escape_html(service)}\n"
                        f"🔐 <b>OTP Code:</b> <code>{escape_html(otp)}</code>\n"
                        f"📝 <b>Msg:</b> <i>{escape_html(message)}</i>\n\n"
                        "<b>P0WERED BY</b> Ruku Vai "
                    )

                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("👨‍💻 Bot Owner", url="https://t.me/rikton16")],
                        [InlineKeyboardButton("🔁 Number Channel", url="")]
                    ])

                    try:
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text,
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                            reply_markup=keyboard
                        )
                        save_already_sent(already_sent)
                        logging.info(f"[+] Sent OTP: {otp}")
                    except TimedOut:
                        logging.error("Telegram TimedOut")
                    except Exception as e:
                        logging.error(f"Telegram error: {e}")
            else:
                logging.info(f"No OTP found in: {message}")
    else:
        logging.info("No data or invalid response.")

async def main():
    if login():
        while True:
            await sent_messages()
            await asyncio.sleep(3)
    else:
        logging.error("Initial login failed. Exiting...")

# Run bot
asyncio.run(main())
