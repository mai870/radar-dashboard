import requests
import datetime
import time

API_KEY = "5bdce32e40msh6d568ec820ed8fcp19fb9djsna203b995632f"
HOST = "tennis-api-atp-wta-itf.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

TELEGRAM_TOKEN = "8960085630:AAGtn8kHVbYL4UtTdVztSU-aogUcDHauOmY"
TELEGRAM_CHAT_ID = "8640013902"

def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        pass

today = datetime.datetime.now().strftime("%Y-%m-%d")
fixtures_url = f"https://{HOST}/tennis/v2/atp/fixtures/{today}"

try:
    response = requests.get(fixtures_url, headers=HEADERS)
    matches = response.json().get("data", [])
    
    if matches:
        found = 0
        for match in matches:
            event_id = match.get("id")
            p1 = match.get("player1", {}).get("name", "لاعب 1")
            p2 = match.get("player2", {}).get("name", "لاعب 2")
            
            odds_url = f"https://{HOST}/tennis/v2/extend/api/event/recent-odds/get/{event_id}"
            
            try:
                odds_res = requests.get(odds_url, headers=HEADERS)
                if odds_res.status_code == 200:
                    bet365 = odds_res.json().get("result", {}).get("Full Time Result", {}).get("Bet365", {})
                    if bet365:
                        od1 = float(bet365.get("od1", 0))
                        od2 = float(bet365.get("od2", 0))
                        
                        # المنطقة الذهبية 1.70 - 2.50
                        if (1.70 <= od1 <= 2.50) or (1.70 <= od2 <= 2.50):
                            msg = f"🚨 <b>فرصة استراتيجية تم رصدها (+EV)!</b>\n━━━━━━━━━━━━━━━\n🎾 <b>{p1}</b> ضد <b>{p2}</b>\n💰 عائد اللاعب الأول: {od1}\n💰 عائد اللاعب الثاني: {od2}\n🔗 ID: <code>{event_id}</code>"
                            send_telegram_alert(msg)
                            found += 1
                            if found >= 2: break
            except:
                pass
            time.sleep(1)
except Exception as e:
    pass
