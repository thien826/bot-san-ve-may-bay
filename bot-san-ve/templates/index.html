bash

cat > /mnt/user-data/outputs/app_full.py << 'ENDOFFILE'
"""
Flight Hunter Pro — Full System
Trang chủ đẹp + Auth + Dashboard + Đặt khách sạn + Khu du lịch + Đa ngôn ngữ
"""
import os, json, time, logging, threading, random
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, render_template_string, redirect, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "flighthunter-pro-2026-secret")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATA_FILE = "fh_data.json"

# ─── DATA ───
DOMESTIC_AIRPORTS = [
    {"code":"SGN","name_vi":"SGN — TP. Hồ Chí Minh","name_en":"SGN — Ho Chi Minh City"},
    {"code":"HAN","name_vi":"HAN — Hà Nội","name_en":"HAN — Hanoi"},
    {"code":"DAD","name_vi":"DAD — Đà Nẵng","name_en":"DAD — Da Nang"},
    {"code":"CXR","name_vi":"CXR — Nha Trang","name_en":"CXR — Nha Trang"},
    {"code":"PQC","name_vi":"PQC — Phú Quốc","name_en":"PQC — Phu Quoc"},
    {"code":"VCA","name_vi":"VCA — Cần Thơ","name_en":"VCA — Can Tho"},
    {"code":"HPH","name_vi":"HPH — Hải Phòng","name_en":"HPH — Hai Phong"},
    {"code":"HUI","name_vi":"HUI — Huế","name_en":"HUI — Hue"},
    {"code":"VII","name_vi":"VII — Vinh","name_en":"VII — Vinh"},
    {"code":"BMV","name_vi":"BMV — Buôn Ma Thuột","name_en":"BMV — Buon Ma Thuot"},
    {"code":"UIH","name_vi":"UIH — Quy Nhơn","name_en":"UIH — Quy Nhon"},
    {"code":"VCL","name_vi":"VCL — Chu Lai","name_en":"VCL — Chu Lai"},
]
INTERNATIONAL_AIRPORTS = [
    {"code":"BKK","name_vi":"BKK — Bangkok, Thái Lan","name_en":"BKK — Bangkok, Thailand"},
    {"code":"SIN","name_vi":"SIN — Singapore","name_en":"SIN — Singapore"},
    {"code":"KUL","name_vi":"KUL — Kuala Lumpur, Malaysia","name_en":"KUL — Kuala Lumpur, Malaysia"},
    {"code":"HKG","name_vi":"HKG — Hồng Kông","name_en":"HKG — Hong Kong"},
    {"code":"NRT","name_vi":"NRT — Tokyo, Nhật Bản","name_en":"NRT — Tokyo, Japan"},
    {"code":"ICN","name_vi":"ICN — Seoul, Hàn Quốc","name_en":"ICN — Seoul, South Korea"},
    {"code":"CDG","name_vi":"CDG — Paris, Pháp","name_en":"CDG — Paris, France"},
    {"code":"LHR","name_vi":"LHR — London, Anh","name_en":"LHR — London, UK"},
    {"code":"SYD","name_vi":"SYD — Sydney, Úc","name_en":"SYD — Sydney, Australia"},
    {"code":"LAX","name_vi":"LAX — Los Angeles, Mỹ","name_en":"LAX — Los Angeles, USA"},
    {"code":"DXB","name_vi":"DXB — Dubai, UAE","name_en":"DXB — Dubai, UAE"},
    {"code":"PEK","name_vi":"PEK — Bắc Kinh, Trung Quốc","name_en":"PEK — Beijing, China"},
    {"code":"TPE","name_vi":"TPE — Đài Bắc, Đài Loan","name_en":"TPE — Taipei, Taiwan"},
    {"code":"MNL","name_vi":"MNL — Manila, Philippines","name_en":"MNL — Manila, Philippines"},
]
AIRLINES = [
    {"code":"ALL","name_vi":"Tất cả hãng bay","name_en":"All Airlines","logo":"✈"},
    {"code":"VJ","name_vi":"VietJet Air","name_en":"VietJet Air","logo":"🔴"},
    {"code":"VN","name_vi":"Vietnam Airlines","name_en":"Vietnam Airlines","logo":"🟡"},
    {"code":"QH","name_vi":"Bamboo Airways","name_en":"Bamboo Airways","logo":"🟢"},
    {"code":"BL","name_vi":"Pacific Airlines","name_en":"Pacific Airlines","logo":"🔵"},
    {"code":"TG","name_vi":"Thai Airways","name_en":"Thai Airways","logo":"🟣"},
    {"code":"SQ","name_vi":"Singapore Airlines","name_en":"Singapore Airlines","logo":"⭐"},
    {"code":"CX","name_vi":"Cathay Pacific","name_en":"Cathay Pacific","logo":"🌐"},
    {"code":"EK","name_vi":"Emirates","name_en":"Emirates","logo":"🏅"},
    {"code":"JL","name_vi":"Japan Airlines","name_en":"Japan Airlines","logo":"🎌"},
    {"code":"KE","name_vi":"Korean Air","name_en":"Korean Air","logo":"🇰🇷"},
]
TRIP_SUGGESTIONS = [
    {"from":"SGN","to":"DAD","price":890000,"label_vi":"Đà Nẵng - Hội An","label_en":"Da Nang - Hoi An","img":"🌊","desc_vi":"Biển xanh, phố cổ, ẩm thực tuyệt vời","desc_en":"Blue sea, ancient town, amazing cuisine"},
    {"from":"HAN","to":"PQC","price":1200000,"label_vi":"Phú Quốc - Đảo Ngọc","label_en":"Phu Quoc - Pearl Island","img":"🏝","desc_vi":"Thiên đường nhiệt đới, snorkeling tuyệt đỉnh","desc_en":"Tropical paradise, top snorkeling"},
    {"from":"SGN","to":"NRT","price":7500000,"label_vi":"Tokyo - Nhật Bản","label_en":"Tokyo - Japan","img":"🗼","desc_vi":"Hoa anh đào, ẩm thực Nhật, văn hóa độc đáo","desc_en":"Cherry blossoms, Japanese cuisine, unique culture"},
    {"from":"HAN","to":"BKK","price":3200000,"label_vi":"Bangkok - Thái Lan","label_en":"Bangkok - Thailand","img":"🛕","desc_vi":"Chợ đêm, chùa vàng, ẩm thực đường phố","desc_en":"Night markets, golden temples, street food"},
    {"from":"SGN","to":"SIN","price":2800000,"label_vi":"Singapore","label_en":"Singapore","img":"🦁","desc_vi":"Gardens by the Bay, Marina Bay Sands","desc_en":"Gardens by the Bay, Marina Bay Sands"},
    {"from":"DAD","to":"HAN","price":750000,"label_vi":"Hà Nội - Thủ Đô","label_en":"Hanoi - Capital","img":"🏛","desc_vi":"Hồ Hoàn Kiếm, phố cổ, bún chả","desc_en":"Hoan Kiem Lake, old quarter, bun cha"},
]
HOTELS = [
    {"name":"Vinpearl Resort & Spa","city_vi":"Nha Trang","city_en":"Nha Trang","stars":5,"price":2800000,"img":"🏨","tag_vi":"Nghỉ dưỡng","tag_en":"Resort"},
    {"name":"InterContinental Danang","city_vi":"Đà Nẵng","city_en":"Da Nang","stars":5,"price":4200000,"img":"🌅","tag_vi":"Sang trọng","tag_en":"Luxury"},
    {"name":"Mường Thanh Grand","city_vi":"Hà Nội","city_en":"Hanoi","stars":4,"price":1200000,"img":"🏙","tag_vi":"Kinh doanh","tag_en":"Business"},
    {"name":"Fusion Maia Resort","city_vi":"Đà Nẵng","city_en":"Da Nang","stars":5,"price":3500000,"img":"🌊","tag_vi":"Spa","tag_en":"Spa"},
    {"name":"La Siesta Hoi An","city_vi":"Hội An","city_en":"Hoi An","stars":4,"price":1800000,"img":"🏮","tag_vi":"Boutique","tag_en":"Boutique"},
    {"name":"Rex Hotel Saigon","city_vi":"TP.HCM","city_en":"Ho Chi Minh","stars":4,"price":1500000,"img":"🌃","tag_vi":"Trung tâm","tag_en":"Central"},
    {"name":"Alma Resort Cam Ranh","city_vi":"Nha Trang","city_en":"Nha Trang","stars":5,"price":3800000,"img":"🏖","tag_vi":"Gia đình","tag_en":"Family"},
    {"name":"Ninh Van Bay Hideaway","city_vi":"Nha Trang","city_en":"Nha Trang","stars":5,"price":8500000,"img":"⛵","tag_vi":"Bungalow","tag_en":"Bungalow"},
]
ATTRACTIONS = [
    {"name_vi":"Vịnh Hạ Long","name_en":"Ha Long Bay","city_vi":"Quảng Ninh","city_en":"Quang Ninh","price":850000,"img":"⛰","type_vi":"Di sản UNESCO","type_en":"UNESCO Heritage","rating":4.9},
    {"name_vi":"Phố Cổ Hội An","name_en":"Hoi An Ancient Town","city_vi":"Hội An","city_en":"Hoi An","price":120000,"img":"🏮","type_vi":"Di sản văn hóa","type_en":"Cultural Heritage","rating":4.8},
    {"name_vi":"Bà Nà Hills","name_en":"Ba Na Hills","city_vi":"Đà Nẵng","city_en":"Da Nang","price":750000,"img":"🎡","type_vi":"Khu vui chơi","type_en":"Theme Park","rating":4.7},
    {"name_vi":"VinWonders Phú Quốc","name_en":"VinWonders Phu Quoc","city_vi":"Phú Quốc","city_en":"Phu Quoc","price":950000,"img":"🎢","type_vi":"Công viên giải trí","type_en":"Amusement Park","rating":4.8},
    {"name_vi":"Cố Đô Huế","name_en":"Hue Imperial City","city_vi":"Huế","city_en":"Hue","price":200000,"img":"🏰","type_vi":"Di tích lịch sử","type_en":"Historical Site","rating":4.6},
    {"name_vi":"Mũi Né - Phan Thiết","name_en":"Mui Ne - Phan Thiet","city_vi":"Bình Thuận","city_en":"Binh Thuan","price":0,"img":"🏜","type_vi":"Thiên nhiên","type_en":"Nature","rating":4.5},
    {"name_vi":"Safari Phú Quốc","name_en":"Phu Quoc Safari","city_vi":"Phú Quốc","city_en":"Phu Quoc","price":600000,"img":"🦁","type_vi":"Động vật hoang dã","type_en":"Wildlife","rating":4.7},
    {"name_vi":"Sun World Hạ Long","name_en":"Sun World Ha Long","city_vi":"Quảng Ninh","city_en":"Quang Ninh","price":400000,"img":"🎠","type_vi":"Khu vui chơi","type_en":"Theme Park","rating":4.6},
]

def load_data():
    default = {
        "users": {"admin": {"password":"123456","email":"admin@example.com"}},
        "config": {"origin":"SGN","destination":"DAD","fly_date":(datetime.now()+timedelta(days=7)).strftime("%Y-%m-%d"),
                   "threshold":2500000,"interval":15,"is_active":False,"airline":"ALL","route_type":"domestic",
                   "hotel_city":"Đà Nẵng","hotel_threshold":1000000},
        "stats": {"scan_count":0,"alert_count":0,"last_scan":"—","cheapest":"—"},
        "results":[],"hotel_results":[],"logs":[]
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f: d=json.load(f)
            d.setdefault("users",default["users"]); d.setdefault("config",default["config"])
            # migrate old user format
            for u,v in d["users"].items():
                if isinstance(v, str): d["users"][u] = {"password":v,"email":""}
            return d
        except: pass
    return default

def save_data():
    try:
        with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(state,f,ensure_ascii=False,indent=2)
    except Exception as e: logger.error(e)

state = load_data()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN","123:FAKE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID","123")

def add_log(msg, t="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    state["logs"].insert(0,{"time":ts,"text":msg,"type":t})
    if len(state["logs"])>50: state["logs"].pop()
    save_data()

def run_flight_scan(cfg):
    flights=[]
    base = 900000
    if cfg.get("route_type","domestic") == "international": base = 4000000
    airlines_pool = [a for a in AIRLINES[1:] if cfg["airline"]=="ALL" or a["code"]==cfg["airline"]]
    if not airlines_pool: airlines_pool = AIRLINES[1:4]
    random.seed(int(time.time()))
    for a in airlines_pool[:5]:
        price = int(base + random.randint(100000, base*0.6))
        if a["code"]=="VN": price = int(price*1.15)
        if a["code"]=="SQ" or a["code"]=="EK": price = int(price*1.3)
        h=random.randint(5,22); m=random.choice([0,15,30,45])
        flights.append({"id":f"{a['code']}-{random.randint(100,999)}","airline":a["name_vi"],"airline_logo":a["logo"],
            "time_window":f"{h:02d}:{m:02d} → {(h+2)%24:02d}:{m:02d}","price":price,
            "link":f"https://www.traveloka.com/vi-vn/flight/search?ap={cfg['origin']}.{cfg['destination']}"})
    flights.sort(key=lambda x:x["price"])
    return flights

def execute_scan(force=False):
    cfg=state["config"]; state["stats"]["scan_count"]+=1; state["stats"]["last_scan"]=datetime.now().strftime("%H:%M")
    try:
        flights=run_flight_scan(cfg); state["results"]=flights
        if flights:
            c=flights[0]; state["stats"]["cheapest"]=f"{c['price']:,} ₫"
            add_log(f"Quét thành công! Vé {cfg['origin']}→{cfg['destination']}: {c['price']:,} ₫","success")
            if c["price"]<=int(cfg["threshold"]) or force:
                state["stats"]["alert_count"]+=1
                msg=f"✈️ <b>FLIGHT HUNTER</b>\n📍 {cfg['origin']}→{cfg['destination']}\n📅 {cfg['fly_date']}\n💵 <b>{c['price']:,} ₫</b>\n👉 <a href='{c['link']}'>ĐẶT VÉ</a>"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",json={"chat_id":TELEGRAM_CHAT_ID,"text":msg,"parse_mode":"HTML"},timeout=8)
    except Exception as e: add_log(f"Lỗi: {e}","error")
    save_data()

# ════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════
LANDING_HTML = r"""<!DOCTYPE html>
<html lang="vi" id="html-root">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flight Hunter Pro — Săn Vé Thông Minh</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --emerald:#10b981;--emerald-light:#34d399;--emerald-dark:#059669;
  --gold:#f59e0b;--navy:#0a1628;--navy2:#0d2137;
  --white:#ffffff;--gray:#f8fafc;--text:#1e293b;--muted:#64748b;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Be Vietnam Pro',sans-serif;color:var(--text);overflow-x:hidden}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 40px;display:flex;align-items:center;justify-content:space-between;transition:all 0.3s;background:transparent}
nav.scrolled{background:rgba(10,22,40,0.95);backdrop-filter:blur(12px);padding:12px 40px;box-shadow:0 2px 20px rgba(0,0,0,0.3)}
.nav-brand{display:flex;align-items:center;gap:10px;text-decoration:none}
.nav-logo{width:36px;height:36px;background:linear-gradient(135deg,var(--emerald),var(--emerald-light));border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.nav-name{font-family:'Playfair Display',serif;font-size:1.25rem;font-weight:700;color:white}
.nav-name span{color:var(--emerald-light)}
.nav-links{display:flex;align-items:center;gap:8px}
.nav-link{color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.85rem;font-weight:500;padding:6px 14px;border-radius:20px;transition:all 0.2s}
.nav-link:hover{color:white;background:rgba(255,255,255,0.1)}
.nav-lang{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:white;padding:6px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;cursor:pointer;border:none;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.2s}
.nav-lang:hover{background:rgba(255,255,255,0.2)}
.btn-nav-login{background:transparent;border:1.5px solid rgba(255,255,255,0.5);color:white;padding:8px 20px;border-radius:22px;font-size:0.85rem;font-weight:600;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.2s}
.btn-nav-login:hover{border-color:var(--emerald-light);color:var(--emerald-light)}
.btn-nav-register{background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));color:white;border:none;padding:8px 20px;border-radius:22px;font-size:0.85rem;font-weight:700;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.2s}
.btn-nav-register:hover{transform:translateY(-1px);box-shadow:0 4px 15px rgba(16,185,129,0.4)}

/* HERO */
.hero{height:100vh;position:relative;overflow:hidden;display:flex;align-items:center}
.hero-slides{position:absolute;inset:0}
.slide{position:absolute;inset:0;opacity:0;transition:opacity 1.5s ease;background-size:cover;background-position:center}
.slide.active{opacity:1}
/* Vietnam landscape SVG backgrounds */
.slide-1{background:linear-gradient(135deg,#0a2e1a 0%,#1a5c3a 30%,#0d4a6b 70%,#061528 100%)}
.slide-2{background:linear-gradient(135deg,#1a0a2e 0%,#2d1b69 30%,#1e3a5f 70%,#0a1628 100%)}
.slide-3{background:linear-gradient(135deg,#2e1a0a 0%,#8b4513 30%,#d4691e 60%,#0a1628 100%)}
.slide-4{background:linear-gradient(135deg,#0a2e2e 0%,#1a6b5c 40%,#0d6b4a 70%,#0a1628 100%)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(10,22,40,0.5) 0%,rgba(10,22,40,0.3) 50%,rgba(10,22,40,0.8) 100%)}
.hero-scene{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden}
.landscape-svg{width:100%;height:100%;position:absolute}

.hero-content{position:relative;z-index:10;text-align:center;padding:0 24px;max-width:800px;margin:0 auto}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:20px;padding:6px 16px;font-size:0.78rem;font-weight:600;color:var(--emerald-light);letter-spacing:0.08em;margin-bottom:24px;animation:fadeUp 0.8s ease 0.2s both}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(2.5rem,6vw,4.5rem);font-weight:900;color:white;line-height:1.1;margin-bottom:20px;animation:fadeUp 0.8s ease 0.4s both}
.hero-title .em{color:var(--emerald-light)}
.hero-sub{font-size:1.05rem;color:rgba(255,255,255,0.75);line-height:1.7;margin-bottom:36px;animation:fadeUp 0.8s ease 0.6s both}
.hero-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;animation:fadeUp 0.8s ease 0.8s both}
.btn-hero-primary{background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));color:white;border:none;padding:15px 36px;border-radius:50px;font-size:0.95rem;font-weight:700;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.3s;box-shadow:0 8px 25px rgba(16,185,129,0.4)}
.btn-hero-primary:hover{transform:translateY(-3px);box-shadow:0 14px 35px rgba(16,185,129,0.5)}
.btn-hero-sec{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);color:white;border:1.5px solid rgba(255,255,255,0.3);padding:15px 36px;border-radius:50px;font-size:0.95rem;font-weight:600;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.3s}
.btn-hero-sec:hover{background:rgba(255,255,255,0.2);border-color:white}

.slide-dots{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:10}
.dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.4);cursor:pointer;transition:all 0.3s}
.dot.active{background:var(--emerald-light);width:24px;border-radius:3px}
.scroll-hint{position:absolute;bottom:60px;right:40px;z-index:10;display:flex;flex-direction:column;align-items:center;gap:6px;color:rgba(255,255,255,0.5);font-size:0.72rem;letter-spacing:0.1em}
.scroll-line{width:1px;height:40px;background:linear-gradient(to bottom,transparent,rgba(255,255,255,0.4));animation:scrollPulse 2s ease infinite}
@keyframes scrollPulse{0%,100%{transform:scaleY(1);opacity:0.5}50%{transform:scaleY(1.3);opacity:1}}

/* STATS BAR */
.stats-bar{background:white;padding:28px 40px;display:flex;justify-content:center;gap:60px;box-shadow:0 4px 20px rgba(0,0,0,0.06);position:relative;z-index:5}
.stat-item{text-align:center}
.stat-num{font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:var(--emerald)}
.stat-desc{font-size:0.78rem;color:var(--muted);font-weight:500;margin-top:2px}

/* SECTIONS */
section{padding:80px 40px}
.container{max-width:1200px;margin:0 auto}
.section-label{font-size:0.75rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--emerald);margin-bottom:12px}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(1.8rem,3vw,2.6rem);font-weight:700;color:var(--navy);line-height:1.2;margin-bottom:14px}
.section-sub{font-size:0.95rem;color:var(--muted);line-height:1.7;max-width:560px}

/* DESTINATIONS */
.dest-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin-top:40px}
.dest-card{border-radius:20px;overflow:hidden;background:white;box-shadow:0 4px 20px rgba(0,0,0,0.08);transition:all 0.3s;cursor:pointer;text-decoration:none;display:block;border:1px solid #f0f4f8}
.dest-card:hover{transform:translateY(-6px);box-shadow:0 16px 40px rgba(0,0,0,0.14)}
.dest-img{height:180px;position:relative;display:flex;align-items:center;justify-content:center;font-size:4rem;overflow:hidden}
.dest-img.d1{background:linear-gradient(135deg,#0d7a5f,#1bb38a,#059669)}
.dest-img.d2{background:linear-gradient(135deg,#1a3a6b,#2563eb,#1d4ed8)}
.dest-img.d3{background:linear-gradient(135deg,#7c2d12,#dc2626,#ef4444)}
.dest-img.d4{background:linear-gradient(135deg,#713f12,#d97706,#f59e0b)}
.dest-img.d5{background:linear-gradient(135deg,#1e1b4b,#4f46e5,#6366f1)}
.dest-img.d6{background:linear-gradient(135deg,#064e3b,#047857,#10b981)}
.dest-badge{position:absolute;top:12px;right:12px;background:rgba(255,255,255,0.95);border-radius:20px;padding:4px 10px;font-size:0.7rem;font-weight:700;color:var(--emerald)}
.dest-body{padding:18px}
.dest-name{font-weight:700;font-size:1rem;color:var(--navy);margin-bottom:4px}
.dest-desc{font-size:0.8rem;color:var(--muted);margin-bottom:12px}
.dest-price{display:flex;align-items:center;justify-content:space-between}
.dest-from{font-size:0.72rem;color:var(--muted)}
.dest-amount{font-weight:800;font-size:1rem;color:var(--emerald)}
.dest-book{background:var(--emerald);color:white;border:none;padding:7px 16px;border-radius:20px;font-size:0.75rem;font-weight:700;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif}

/* AIRLINES */
.airlines-bg{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 100%)}
.airlines-bg .section-title{color:white}
.airlines-bg .section-label{color:var(--emerald-light)}
.airlines-bg .section-sub{color:rgba(255,255,255,0.6)}
.airline-scroll{display:flex;gap:16px;margin-top:36px;overflow-x:auto;padding-bottom:12px;-webkit-overflow-scrolling:touch}
.airline-scroll::-webkit-scrollbar{height:4px}
.airline-scroll::-webkit-scrollbar-track{background:rgba(255,255,255,0.05)}
.airline-scroll::-webkit-scrollbar-thumb{background:var(--emerald);border-radius:2px}
.airline-card{flex-shrink:0;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 24px;text-align:center;min-width:140px;transition:all 0.3s;cursor:pointer}
.airline-card:hover,.airline-card.selected{background:rgba(16,185,129,0.15);border-color:var(--emerald);transform:translateY(-4px)}
.airline-logo{font-size:2rem;margin-bottom:8px}
.airline-name{font-size:0.8rem;font-weight:600;color:white;line-height:1.3}

/* HOW IT WORKS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;margin-top:48px}
.step-card{background:white;border-radius:20px;padding:28px 24px;border:1px solid #f0f4f8;box-shadow:0 4px 16px rgba(0,0,0,0.05);position:relative}
.step-num{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));color:white;font-weight:800;font-size:1rem;display:flex;align-items:center;justify-content:center;margin-bottom:16px;font-family:'Playfair Display',serif}
.step-icon{font-size:1.8rem;margin-bottom:12px}
.step-title{font-weight:700;color:var(--navy);margin-bottom:8px}
.step-desc{font-size:0.85rem;color:var(--muted);line-height:1.6}
.connector{position:absolute;right:-12px;top:50%;transform:translateY(-50%);color:var(--emerald);font-size:1.2rem;z-index:2}

/* HOTELS PREVIEW */
.hotels-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:40px}
.hotel-card{background:white;border-radius:18px;overflow:hidden;border:1px solid #f0f4f8;box-shadow:0 4px 16px rgba(0,0,0,0.06);transition:all 0.3s}
.hotel-card:hover{transform:translateY(-5px);box-shadow:0 14px 36px rgba(0,0,0,0.12)}
.hotel-img{height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem;position:relative}
.hotel-img.h1{background:linear-gradient(135deg,#0d4a6b,#0891b2)}
.hotel-img.h2{background:linear-gradient(135deg,#1e3a5f,#2563eb)}
.hotel-img.h3{background:linear-gradient(135deg,#1a3a6b,#7c3aed)}
.hotel-img.h4{background:linear-gradient(135deg,#064e3b,#10b981)}
.hotel-stars{position:absolute;bottom:10px;left:12px;display:flex;gap:2px}
.hotel-star{font-size:0.7rem;color:#fbbf24}
.hotel-body{padding:16px}
.hotel-tag{display:inline-block;background:var(--gray);color:var(--muted);font-size:0.68rem;font-weight:600;padding:3px 10px;border-radius:10px;margin-bottom:8px;letter-spacing:0.04em}
.hotel-name{font-weight:700;color:var(--navy);font-size:0.9rem;margin-bottom:4px}
.hotel-city{font-size:0.78rem;color:var(--muted);margin-bottom:10px}
.hotel-price{display:flex;align-items:center;justify-content:space-between}
.hotel-amount{font-weight:800;color:var(--emerald);font-size:0.95rem}
.hotel-per{font-size:0.7rem;color:var(--muted)}
.btn-book-hotel{background:transparent;border:1.5px solid var(--emerald);color:var(--emerald);padding:6px 14px;border-radius:20px;font-size:0.73rem;font-weight:700;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all 0.2s}
.btn-book-hotel:hover{background:var(--emerald);color:white}

/* HELP SECTION */
.help-bg{background:var(--gray)}
.faq-list{margin-top:36px;display:flex;flex-direction:column;gap:12px}
.faq-item{background:white;border-radius:14px;border:1px solid #e8eef4;overflow:hidden}
.faq-q{padding:18px 22px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:color 0.2s;font-size:0.92rem}
.faq-q:hover{color:var(--emerald)}
.faq-q .arrow{font-size:0.8rem;transition:transform 0.3s;color:var(--emerald)}
.faq-item.open .arrow{transform:rotate(180deg)}
.faq-a{padding:0 22px;max-height:0;overflow:hidden;transition:all 0.3s;font-size:0.87rem;color:var(--muted);line-height:1.7}
.faq-item.open .faq-a{padding:0 22px 18px 22px;max-height:300px}

.guide-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:36px}
.guide-card{background:white;border-radius:16px;padding:22px;border:1px solid #e8eef4;display:flex;gap:14px;align-items:flex-start}
.guide-icon{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0}
.guide-text h4{font-weight:700;color:var(--navy);margin-bottom:6px;font-size:0.9rem}
.guide-text p{font-size:0.8rem;color:var(--muted);line-height:1.6}

/* FOOTER */
footer{background:var(--navy);color:rgba(255,255,255,0.6);padding:48px 40px 28px}
.footer-top{display:flex;justify-content:space-between;flex-wrap:wrap;gap:32px;margin-bottom:36px}
.footer-brand .nav-name{font-size:1.4rem}
.footer-tagline{font-size:0.82rem;color:rgba(255,255,255,0.4);margin-top:8px;max-width:260px}
.footer-col h4{font-size:0.8rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:14px}
.footer-col a{display:block;font-size:0.85rem;color:rgba(255,255,255,0.6);text-decoration:none;margin-bottom:8px;transition:color 0.2s}
.footer-col a:hover{color:var(--emerald-light)}
.footer-bottom{border-top:1px solid rgba(255,255,255,0.07);padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.footer-email{display:flex;align-items:center;gap:8px;font-size:0.82rem;color:var(--emerald-light)}
.copyright{font-size:0.78rem;color:rgba(255,255,255,0.3)}

/* MODAL */
.modal-overlay{position:fixed;inset:0;background:rgba(10,22,40,0.85);backdrop-filter:blur(8px);z-index:1000;display:none;align-items:center;justify-content:center;padding:20px}
.modal-overlay.open{display:flex}
.modal-box{background:white;border-radius:24px;width:100%;max-width:420px;overflow:hidden;animation:modalIn 0.35s cubic-bezier(0.34,1.56,0.64,1)}
@keyframes modalIn{from{opacity:0;transform:scale(0.85) translateY(20px)}to{opacity:1;transform:scale(1) translateY(0)}}
.modal-header{background:linear-gradient(135deg,var(--navy),var(--navy2));padding:28px;text-align:center}
.modal-logo{width:52px;height:52px;background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 12px}
.modal-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:white}
.modal-sub{font-size:0.78rem;color:rgba(255,255,255,0.5);margin-top:4px}
.modal-body{padding:28px}
.modal-tabs{display:flex;background:#f8fafc;border-radius:12px;padding:4px;margin-bottom:22px}
.modal-tab{flex:1;padding:9px;text-align:center;font-size:0.82rem;font-weight:600;border-radius:9px;cursor:pointer;color:var(--muted);transition:all 0.2s;border:none;background:transparent;font-family:'Be Vietnam Pro',sans-serif}
.modal-tab.active{background:white;color:var(--navy);box-shadow:0 2px 8px rgba(0,0,0,0.08)}
.modal-alert{padding:10px 14px;border-radius:10px;font-size:0.82rem;font-weight:600;margin-bottom:16px;text-align:center}
.modal-alert.err{background:#fee2e2;color:#dc2626}
.modal-alert.ok{background:#dcfce7;color:#16a34a}
.field{background:#f8fafc;border:1.5px solid #e8ecf0;border-radius:12px;padding:11px 14px;margin-bottom:12px;transition:border-color 0.2s}
.field:focus-within{border-color:var(--emerald)}
.field label{font-size:0.68rem;font-weight:700;color:#94a3b8;letter-spacing:0.06em;text-transform:uppercase;display:block;margin-bottom:2px}
.field input{background:transparent;border:none;outline:none;width:100%;font-family:'Be Vietnam Pro',sans-serif;font-size:0.92rem;font-weight:500;color:var(--navy)}
.field input::placeholder{color:#b0bec5}
.btn-modal{width:100%;padding:14px;background:linear-gradient(135deg,var(--emerald),var(--emerald-dark));color:white;font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;border:none;border-radius:13px;cursor:pointer;margin-top:4px;transition:all 0.2s}
.btn-modal:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(16,185,129,0.35)}
.modal-close{position:absolute;top:16px;right:16px;background:rgba(255,255,255,0.1);border:none;color:white;width:32px;height:32px;border-radius:50%;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center}
.modal-wrap{position:relative}

/* ANIM */
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.reveal{opacity:0;transform:translateY(30px);transition:all 0.7s cubic-bezier(0.22,1,0.36,1)}
.reveal.visible{opacity:1;transform:translateY(0)}

/* MOBILE */
@media(max-width:768px){
  nav{padding:14px 20px}
  nav.scrolled{padding:10px 20px}
  .nav-links .nav-link{display:none}
  section{padding:60px 20px}
  .stats-bar{gap:30px;flex-wrap:wrap;padding:24px 20px}
  .hero-title{font-size:2rem}
  footer{padding:40px 20px 24px}
  .footer-top{flex-direction:column;gap:24px}
  .footer-bottom{flex-direction:column;text-align:center}
}
</style>
</head>
<body>

<!-- NAV -->
<nav id="main-nav">
  <a href="/" class="nav-brand">
    <div class="nav-logo">✈</div>
    <div class="nav-name">Flight<span>Hunter</span></div>
  </a>
  <div class="nav-links">
    <a href="#destinations" class="nav-link" data-vi="Điểm đến" data-en="Destinations">Điểm đến</a>
    <a href="#airlines" class="nav-link" data-vi="Hãng bay" data-en="Airlines">Hãng bay</a>
    <a href="#hotels" class="nav-link" data-vi="Khách sạn" data-en="Hotels">Khách sạn</a>
    <a href="#help" class="nav-link" data-vi="Trợ giúp" data-en="Help">Trợ giúp</a>
    <button class="nav-lang" onclick="toggleLang()" id="lang-btn">EN</button>
    <button class="btn-nav-login" onclick="openModal('login')" data-vi="Đăng nhập" data-en="Login">Đăng nhập</button>
    <button class="btn-nav-register" onclick="openModal('register')" data-vi="Đăng ký" data-en="Sign Up">Đăng ký</button>
  </div>
</nav>

<!-- HERO -->
<section class="hero" id="home">
  <div class="hero-slides">
    <div class="slide slide-1 active">
      <div class="hero-scene">
        <svg class="landscape-svg" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice">
          <!-- Ha Long Bay scene -->
          <defs>
            <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0a3d62"/><stop offset="100%" stop-color="#0d7a5f"/></linearGradient>
            <linearGradient id="water1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1bb38a" stop-opacity="0.6"/><stop offset="100%" stop-color="#064e3b"/></linearGradient>
          </defs>
          <rect width="1400" height="700" fill="url(#sky1)"/>
          <!-- Moon/Sun -->
          <circle cx="1100" cy="120" r="60" fill="#fef3c7" opacity="0.3"/>
          <circle cx="1100" cy="120" r="45" fill="#fef9c3" opacity="0.4"/>
          <!-- Stars -->
          <circle cx="200" cy="80" r="2" fill="white" opacity="0.6"/><circle cx="400" cy="50" r="1.5" fill="white" opacity="0.5"/>
          <circle cx="600" cy="100" r="2" fill="white" opacity="0.4"/><circle cx="800" cy="60" r="1.5" fill="white" opacity="0.7"/>
          <circle cx="300" cy="150" r="1" fill="white" opacity="0.5"/><circle cx="700" cy="40" r="2" fill="white" opacity="0.3"/>
          <!-- Karst mountains - Ha Long -->
          <ellipse cx="100" cy="420" rx="180" ry="280" fill="#0a4a3a"/>
          <ellipse cx="250" cy="400" rx="150" ry="260" fill="#0d5c48"/>
          <ellipse cx="450" cy="380" rx="200" ry="300" fill="#085940"/>
          <ellipse cx="700" cy="350" rx="220" ry="320" fill="#0a6b4e"/>
          <ellipse cx="950" cy="390" rx="170" ry="275" fill="#085c45"/>
          <ellipse cx="1150" cy="410" rx="190" ry="285" fill="#0a4f3c"/>
          <ellipse cx="1350" cy="440" rx="160" ry="260" fill="#085040"/>
          <!-- Water -->
          <ellipse cx="700" cy="680" rx="900" ry="120" fill="url(#water1)" opacity="0.8"/>
          <rect x="0" y="560" width="1400" height="140" fill="url(#water1)" opacity="0.7"/>
          <!-- Boat silhouette -->
          <path d="M620 520 L780 520 L760 550 L640 550 Z" fill="#0a2e1a"/>
          <rect x="690" y="470" width="4" height="52" fill="#0a2e1a"/>
          <path d="M694 470 L740 490 L694 510 Z" fill="#1bb38a" opacity="0.6"/>
          <!-- Reflections on water -->
          <rect x="0" y="560" width="1400" height="2" fill="rgba(27,179,138,0.3)"/>
          <path d="M100 580 Q350 570 600 585 Q850 600 1100 580 Q1300 570 1400 582" stroke="rgba(27,179,138,0.2)" stroke-width="1.5" fill="none"/>
          <path d="M0 610 Q300 600 700 615 Q1000 625 1400 610" stroke="rgba(27,179,138,0.15)" stroke-width="1" fill="none"/>
        </svg>
      </div>
    </div>
    <div class="slide slide-2">
      <div class="hero-scene">
        <svg class="landscape-svg" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice">
          <!-- Da Nang beach -->
          <defs>
            <linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0c2340"/><stop offset="60%" stop-color="#1e4480"/><stop offset="100%" stop-color="#0d3060"/></linearGradient>
            <linearGradient id="sea2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1d4ed8" stop-opacity="0.8"/><stop offset="100%" stop-color="#1e3a8a"/></linearGradient>
          </defs>
          <rect width="1400" height="700" fill="url(#sky2)"/>
          <!-- City lights reflection -->
          <ellipse cx="700" cy="700" rx="800" ry="200" fill="#1e3a8a" opacity="0.4"/>
          <!-- Building skyline -->
          <rect x="50" y="350" width="60" height="300" fill="#0d2137"/><rect x="60" y="320" width="40" height="40" fill="#0d2137"/>
          <rect x="130" y="280" width="80" height="380" fill="#0f2d4a"/><rect x="145" y="260" width="50" height="30" fill="#0f2d4a"/>
          <rect x="240" y="310" width="70" height="350" fill="#0d2137"/>
          <rect x="340" y="250" width="100" height="420" fill="#10345c"/><rect x="355" y="230" width="70" height="30" fill="#10345c"/>
          <rect x="470" y="200" width="120" height="470" fill="#0f2d4a"/>
          <rect x="620" y="180" width="90" height="490" fill="#0d2137"/>
          <rect x="740" y="220" width="110" height="450" fill="#10345c"/>
          <rect x="880" y="260" width="85" height="410" fill="#0d2137"/>
          <rect x="990" y="290" width="100" height="380" fill="#0f2d4a"/>
          <rect x="1120" y="310" width="80" height="360" fill="#0d2137"/>
          <rect x="1230" y="340" width="90" height="330" fill="#10345c"/>
          <rect x="1340" y="370" width="60" height="300" fill="#0d2137"/>
          <!-- Windows (city lights) -->
          <rect x="145" y="285" width="6" height="4" fill="#fbbf24" opacity="0.7"/><rect x="158" y="295" width="6" height="4" fill="#fbbf24" opacity="0.5"/>
          <rect x="355" y="255" width="8" height="5" fill="#60a5fa" opacity="0.8"/><rect x="370" y="270" width="8" height="5" fill="#fbbf24" opacity="0.6"/>
          <rect x="490" y="210" width="10" height="6" fill="#60a5fa" opacity="0.7"/><rect x="510" y="230" width="10" height="6" fill="#fbbf24" opacity="0.5"/>
          <rect x="635" y="190" width="8" height="5" fill="#fbbf24" opacity="0.6"/><rect x="655" y="210" width="8" height="5" fill="#60a5fa" opacity="0.7"/>
          <!-- Sea -->
          <rect x="0" y="540" width="1400" height="160" fill="url(#sea2)"/>
          <!-- Beach sand -->
          <ellipse cx="700" cy="560" rx="900" ry="60" fill="#d4a853" opacity="0.5"/>
          <!-- Waves -->
          <path d="M0 555 Q175 545 350 560 Q525 575 700 558 Q875 545 1050 562 Q1225 575 1400 558" stroke="rgba(255,255,255,0.4)" stroke-width="2" fill="none"/>
          <path d="M0 575 Q200 565 400 578 Q600 591 800 575 Q1000 562 1200 578 Q1350 588 1400 580" stroke="rgba(255,255,255,0.25)" stroke-width="1.5" fill="none"/>
          <!-- Dragon Bridge -->
          <path d="M380 450 Q700 400 1020 450" stroke="#2563eb" stroke-width="6" fill="none" opacity="0.7"/>
          <path d="M380 450 L390 540" stroke="#1d4ed8" stroke-width="4" fill="none"/>
          <path d="M580 420 L590 540" stroke="#1d4ed8" stroke-width="4" fill="none"/>
          <path d="M780 408 L790 540" stroke="#1d4ed8" stroke-width="4" fill="none"/>
          <path d="M980 420 L990 540" stroke="#1d4ed8" stroke-width="4" fill="none"/>
          <path d="M1020 450 L1030 540" stroke="#1d4ed8" stroke-width="4" fill="none"/>
        </svg>
      </div>
    </div>
    <div class="slide slide-3">
      <div class="hero-scene">
        <svg class="landscape-svg" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice">
          <!-- Hoi An lanterns scene -->
          <defs>
            <linearGradient id="sky3" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1a0a00"/><stop offset="50%" stop-color="#7c3a00"/><stop offset="100%" stop-color="#4a1a00"/></linearGradient>
          </defs>
          <rect width="1400" height="700" fill="url(#sky3)"/>
          <!-- Full moon -->
          <circle cx="700" cy="150" r="80" fill="#fef9c3" opacity="0.2"/>
          <circle cx="700" cy="150" r="60" fill="#fef3c7" opacity="0.35"/>
          <!-- Ancient buildings -->
          <rect x="0" y="380" width="200" height="320" fill="#3d1a00"/><rect x="20" y="360" width="160" height="30" fill="#4a2000"/>
          <rect x="220" y="340" width="180" height="360" fill="#4a2000"/><rect x="235" y="320" width="150" height="30" fill="#5a2800"/>
          <rect x="420" y="360" width="160" height="340" fill="#3d1a00"/>
          <rect x="600" y="320" width="200" height="380" fill="#4a2000"/>
          <rect x="820" y="350" width="170" height="350" fill="#3d1a00"/>
          <rect x="1010" y="330" width="190" height="370" fill="#4a2000"/>
          <rect x="1220" y="360" width="180" height="340" fill="#3d1a00"/>
          <!-- Roof curves -->
          <path d="M0 380 Q100 360 200 380" fill="#6b3a00" stroke="none"/>
          <path d="M220 340 Q310 318 400 340" fill="#7a4500" stroke="none"/>
          <path d="M600 320 Q700 296 800 320" fill="#6b3a00" stroke="none"/>
          <!-- Lanterns -->
          <ellipse cx="300" cy="260" rx="18" ry="24" fill="#f59e0b" opacity="0.9"/>
          <rect x="297" y="236" width="6" height="10" fill="#92400e"/>
          <ellipse cx="300" cy="260" rx="18" ry="24" fill="none" stroke="#d97706" stroke-width="2"/>
          
          <ellipse cx="500" cy="200" rx="20" ry="28" fill="#ef4444" opacity="0.85"/>
          <rect x="497" y="172" width="6" height="12" fill="#7f1d1d"/>
          
          <ellipse cx="700" cy="240" rx="22" ry="30" fill="#f59e0b" opacity="0.9"/>
          <rect x="697" y="210" width="6" height="12" fill="#92400e"/>
          
          <ellipse cx="900" cy="210" rx="18" ry="26" fill="#ef4444" opacity="0.85"/>
          <rect x="897" y="184" width="6" height="10" fill="#7f1d1d"/>
          
          <ellipse cx="1100" cy="250" rx="20" ry="28" fill="#f59e0b" opacity="0.9"/>
          <rect x="1097" y="222" width="6" height="12" fill="#92400e"/>
          
          <ellipse cx="150" cy="300" rx="15" ry="20" fill="#ef4444" opacity="0.8"/>
          <ellipse cx="1250" cy="290" rx="16" ry="22" fill="#f59e0b" opacity="0.85"/>
          
          <!-- Lantern strings -->
          <path d="M150 280 Q300 240 500 172 Q700 210 900 184 Q1100 222 1250 268" stroke="rgba(255,200,0,0.3)" stroke-width="1" fill="none"/>
          
          <!-- River Thu Bon reflection -->
          <rect x="0" y="560" width="1400" height="140" fill="#1a0800" opacity="0.9"/>
          <!-- Lantern reflections in water -->
          <ellipse cx="300" cy="600" rx="15" ry="25" fill="#f59e0b" opacity="0.3"/>
          <ellipse cx="500" cy="590" rx="12" ry="22" fill="#ef4444" opacity="0.3"/>
          <ellipse cx="700" cy="595" rx="14" ry="28" fill="#f59e0b" opacity="0.3"/>
          <ellipse cx="900" cy="590" rx="12" ry="20" fill="#ef4444" opacity="0.3"/>
          <ellipse cx="1100" cy="600" rx="15" ry="25" fill="#f59e0b" opacity="0.3"/>
        </svg>
      </div>
    </div>
    <div class="slide slide-4">
      <div class="hero-scene">
        <svg class="landscape-svg" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice">
          <!-- Mekong Delta rice fields -->
          <defs>
            <linearGradient id="sky4" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0a2e1a"/><stop offset="40%" stop-color="#065f3a"/><stop offset="100%" stop-color="#047857"/></linearGradient>
            <linearGradient id="rice" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#15803d"/><stop offset="100%" stop-color="#166534"/></linearGradient>
          </defs>
          <rect width="1400" height="700" fill="url(#sky4)"/>
          <!-- Sun setting -->
          <circle cx="200" cy="200" r="100" fill="#fef9c3" opacity="0.15"/>
          <circle cx="200" cy="200" r="70" fill="#fef3c7" opacity="0.25"/>
          <circle cx="200" cy="200" r="50" fill="#fde68a" opacity="0.4"/>
          <!-- Sun rays -->
          <path d="M200 150 L195 80" stroke="#fde68a" stroke-width="2" opacity="0.3"/>
          <path d="M235 165 L280 110" stroke="#fde68a" stroke-width="2" opacity="0.3"/>
          <path d="M165 165 L120 110" stroke="#fde68a" stroke-width="2" opacity="0.3"/>
          <!-- Rice terrace layers -->
          <path d="M0 320 Q350 300 700 320 Q1050 340 1400 315 L1400 700 L0 700 Z" fill="url(#rice)"/>
          <path d="M0 380 Q350 360 700 375 Q1050 392 1400 370 L1400 700 L0 700 Z" fill="#166534" opacity="0.9"/>
          <path d="M0 440 Q350 420 700 435 Q1050 450 1400 428 L1400 700 L0 700 Z" fill="#14532d" opacity="0.95"/>
          <path d="M0 500 Q350 480 700 495 Q1050 510 1400 488 L1400 700 L0 700 Z" fill="#052e16"/>
          <!-- Rice stalks -->
          <path d="M100 320 Q102 310 100 300" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.6"/>
          <path d="M200 315 Q202 305 200 295" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.5"/>
          <path d="M400 310 Q402 300 400 290" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.6"/>
          <path d="M700 318 Q702 308 700 298" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.5"/>
          <path d="M1000 313 Q1002 303 1000 293" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.6"/>
          <path d="M1300 316 Q1302 306 1300 296" stroke="#4ade80" stroke-width="1.5" fill="none" opacity="0.5"/>
          <!-- Canal/water channel -->
          <path d="M0 430 Q400 415 700 428 Q1000 441 1400 425" stroke="rgba(27,179,138,0.5)" stroke-width="8" fill="none"/>
          <!-- Palm trees -->
          <rect x="450" cy="260" width="8" height="120" fill="#422006" transform="translate(450,260)"/>
          <path d="M454 260 Q420 230 390 240" stroke="#15803d" stroke-width="8" fill="none" stroke-linecap="round"/>
          <path d="M454 260 Q488 225 515 235" stroke="#15803d" stroke-width="8" fill="none" stroke-linecap="round"/>
          <path d="M454 260 Q454 218 454 200" stroke="#166534" stroke-width="7" fill="none" stroke-linecap="round"/>
          <!-- Farmer silhouette -->
          <ellipse cx="750" cy="480" rx="10" ry="24" fill="#052e16"/>
          <circle cx="750" cy="452" r="10" fill="#052e16"/>
          <!-- Conical hat -->
          <path d="M740 453 L750 435 L760 453 Z" fill="#1a0a00"/>
        </svg>
      </div>
    </div>
  </div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-badge" data-vi="⚡ Tự động quét 24/7 • Thông báo Telegram tức thì" data-en="⚡ Auto scan 24/7 • Instant Telegram alerts">⚡ Tự động quét 24/7 • Thông báo Telegram tức thì</div>
    <h1 class="hero-title">
      Săn Vé <span class="em">Thông Minh</span><br>Khám Phá Việt Nam
    </h1>
    <p class="hero-sub" data-vi="Cấu hình một lần — bot tự động quét giá vé từ tất cả hãng bay và gửi cảnh báo ngay khi giá chạm mức kỳ vọng của bạn." data-en="Set up once — our bot automatically scans prices from all airlines and alerts you instantly when prices hit your target.">Cấu hình một lần — bot tự động quét giá vé từ tất cả hãng bay và gửi cảnh báo ngay khi giá chạm mức kỳ vọng của bạn.</p>
    <div class="hero-btns">
      <button class="btn-hero-primary" onclick="openModal('register')" data-vi="🚀 Bắt đầu miễn phí" data-en="🚀 Get Started Free">🚀 Bắt đầu miễn phí</button>
      <button class="btn-hero-sec" onclick="document.getElementById('help').scrollIntoView({behavior:'smooth'})" data-vi="📖 Cách sử dụng" data-en="📖 How it works">📖 Cách sử dụng</button>
    </div>
  </div>
  <div class="slide-dots">
    <div class="dot active" onclick="goSlide(0)"></div>
    <div class="dot" onclick="goSlide(1)"></div>
    <div class="dot" onclick="goSlide(2)"></div>
    <div class="dot" onclick="goSlide(3)"></div>
  </div>
  <div class="scroll-hint">
    <div class="scroll-line"></div>
    <span data-vi="CUỘN" data-en="SCROLL">CUỘN</span>
  </div>
</section>

<!-- STATS BAR -->
<div class="stats-bar reveal">
  <div class="stat-item"><div class="stat-num">50+</div><div class="stat-desc" data-vi="Hãng bay kết nối" data-en="Airlines connected">Hãng bay kết nối</div></div>
  <div class="stat-item"><div class="stat-num">200+</div><div class="stat-desc" data-vi="Điểm đến trong nước & QT" data-en="Domestic & International">Điểm đến trong & ngoài nước</div></div>
  <div class="stat-item"><div class="stat-num">24/7</div><div class="stat-desc" data-vi="Tự động quét giá" data-en="Auto price scanning">Tự động quét giá</div></div>
  <div class="stat-item"><div class="stat-num">98%</div><div class="stat-desc" data-vi="Khách hài lòng" data-en="Customer satisfaction">Khách hài lòng</div></div>
</div>

<!-- DESTINATIONS -->
<section id="destinations">
<div class="container">
  <div class="reveal">
    <div class="section-label" data-vi="✈ GỢI Ý CHUYẾN ĐI" data-en="✈ TRIP SUGGESTIONS">✈ GỢI Ý CHUYẾN ĐI</div>
    <h2 class="section-title" data-vi="Điểm Đến Nổi Bật" data-en="Top Destinations">Điểm Đến Nổi Bật</h2>
    <p class="section-sub" data-vi="Những hành trình được yêu thích nhất — từ bãi biển nhiệt đới đến cố đô ngàn năm lịch sử." data-en="Most loved journeys — from tropical beaches to ancient imperial cities.">Những hành trình được yêu thích nhất — từ bãi biển nhiệt đới đến cố đô ngàn năm lịch sử.</p>
  </div>
  <div class="dest-grid reveal">
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d1"><span>🌊</span><div class="dest-badge" data-vi="Phổ biến" data-en="Popular">Phổ biến</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Đà Nẵng - Hội An" data-en="Da Nang - Hoi An">Đà Nẵng - Hội An</div><div class="dest-desc" data-vi="Biển xanh, phố cổ, ẩm thực tuyệt vời" data-en="Blue sea, ancient town, amazing cuisine">Biển xanh, phố cổ, ẩm thực tuyệt vời</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ TP.HCM" data-en="From HCMC">Từ TP.HCM</div><div class="dest-amount">890.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d2"><span>🏝</span><div class="dest-badge" data-vi="Thiên đường" data-en="Paradise">Thiên đường</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Phú Quốc - Đảo Ngọc" data-en="Phu Quoc - Pearl Island">Phú Quốc - Đảo Ngọc</div><div class="dest-desc" data-vi="Nhiệt đới trong lành, snorkeling tuyệt đỉnh" data-en="Tropical paradise, top snorkeling">Nhiệt đới trong lành, snorkeling tuyệt đỉnh</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ Hà Nội" data-en="From Hanoi">Từ Hà Nội</div><div class="dest-amount">1.200.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d3"><span>🗼</span><div class="dest-badge" data-vi="Quốc tế" data-en="International">Quốc tế</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Tokyo - Nhật Bản" data-en="Tokyo - Japan">Tokyo - Nhật Bản</div><div class="dest-desc" data-vi="Hoa anh đào, ẩm thực Nhật, văn hóa độc đáo" data-en="Cherry blossoms, Japanese cuisine, unique culture">Hoa anh đào, ẩm thực Nhật, văn hóa độc đáo</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ TP.HCM" data-en="From HCMC">Từ TP.HCM</div><div class="dest-amount">7.500.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d4"><span>🛕</span><div class="dest-badge" data-vi="Quốc tế" data-en="International">Quốc tế</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Bangkok - Thái Lan" data-en="Bangkok - Thailand">Bangkok - Thái Lan</div><div class="dest-desc" data-vi="Chợ đêm, chùa vàng, ẩm thực đường phố" data-en="Night markets, golden temples, street food">Chợ đêm, chùa vàng, ẩm thực đường phố</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ Hà Nội" data-en="From Hanoi">Từ Hà Nội</div><div class="dest-amount">3.200.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d5"><span>🦁</span><div class="dest-badge" data-vi="Quốc tế" data-en="International">Quốc tế</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Singapore" data-en="Singapore">Singapore</div><div class="dest-desc" data-vi="Gardens by the Bay, Marina Bay Sands huyền thoại" data-en="Gardens by the Bay, legendary Marina Bay Sands">Gardens by the Bay, Marina Bay Sands huyền thoại</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ TP.HCM" data-en="From HCMC">Từ TP.HCM</div><div class="dest-amount">2.800.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
    <a class="dest-card" href="#" onclick="openModal('login');return false;">
      <div class="dest-img d6"><span>🏛</span><div class="dest-badge" data-vi="Di sản" data-en="Heritage">Di sản</div></div>
      <div class="dest-body"><div class="dest-name" data-vi="Hà Nội - Thủ Đô" data-en="Hanoi - Capital">Hà Nội - Thủ Đô</div><div class="dest-desc" data-vi="Hồ Hoàn Kiếm, phố cổ 36 phường, bún chả" data-en="Hoan Kiem Lake, 36 old streets, bun cha">Hồ Hoàn Kiếm, phố cổ 36 phường, bún chả</div><div class="dest-price"><div><div class="dest-from" data-vi="Từ Đà Nẵng" data-en="From Da Nang">Từ Đà Nẵng</div><div class="dest-amount">750.000 ₫</div></div><button class="dest-book" data-vi="Săn vé" data-en="Hunt">Săn vé</button></div></div>
    </a>
  </div>
</div>
</section>

<!-- AIRLINES -->
<section id="airlines" style="padding:60px 40px">
<div class="airlines-bg" style="border-radius:28px;padding:60px 40px">
<div class="container">
  <div class="reveal">
    <div class="section-label" data-vi="✈ CÁC HÃNG BAY" data-en="✈ AIRLINES">✈ CÁC HÃNG BAY</div>
    <h2 class="section-title" data-vi="Ưu Tiên Hãng Bay Của Bạn" data-en="Choose Your Preferred Airline">Ưu Tiên Hãng Bay Của Bạn</h2>
    <p class="section-sub" data-vi="Chọn hãng bay yêu thích để bot ưu tiên tìm kiếm và cảnh báo giá theo sở thích." data-en="Select your preferred airlines so our bot prioritizes searching and alerting based on your preferences.">Chọn hãng bay yêu thích để bot ưu tiên tìm kiếm và cảnh báo giá theo sở thích.</p>
  </div>
  <div class="airline-scroll reveal">
    <div class="airline-card selected" onclick="selectAirline(this,'ALL')"><div class="airline-logo">✈</div><div class="airline-name" data-vi="Tất cả hãng" data-en="All Airlines">Tất cả hãng</div></div>
    <div class="airline-card" onclick="selectAirline(this,'VJ')"><div class="airline-logo">🔴</div><div class="airline-name">VietJet Air</div></div>
    <div class="airline-card" onclick="selectAirline(this,'VN')"><div class="airline-logo">🟡</div><div class="airline-name">Vietnam Airlines</div></div>
    <div class="airline-card" onclick="selectAirline(this,'QH')"><div class="airline-logo">🟢</div><div class="airline-name">Bamboo Airways</div></div>
    <div class="airline-card" onclick="selectAirline(this,'BL')"><div class="airline-logo">🔵</div><div class="airline-name">Pacific Airlines</div></div>
    <div class="airline-card" onclick="selectAirline(this,'TG')"><div class="airline-logo">🟣</div><div class="airline-name">Thai Airways</div></div>
    <div class="airline-card" onclick="selectAirline(this,'SQ')"><div class="airline-logo">⭐</div><div class="airline-name">Singapore Airlines</div></div>
    <div class="airline-card" onclick="selectAirline(this,'CX')"><div class="airline-logo">🌐</div><div class="airline-name">Cathay Pacific</div></div>
    <div class="airline-card" onclick="selectAirline(this,'EK')"><div class="airline-logo">🏅</div><div class="airline-name">Emirates</div></div>
    <div class="airline-card" onclick="selectAirline(this,'JL')"><div class="airline-logo">🎌</div><div class="airline-name">Japan Airlines</div></div>
    <div class="airline-card" onclick="selectAirline(this,'KE')"><div class="airline-logo">🇰🇷</div><div class="airline-name">Korean Air</div></div>
  </div>
</div>
</div>
</section>

<!-- HOTELS PREVIEW -->
<section id="hotels">
<div class="container">
  <div class="reveal">
    <div class="section-label" data-vi="🏨 KHÁCH SẠN NỔI BẬT" data-en="🏨 FEATURED HOTELS">🏨 KHÁCH SẠN NỔI BẬT</div>
    <h2 class="section-title" data-vi="Đặt Phòng Tốt Nhất" data-en="Best Hotel Deals">Đặt Phòng Tốt Nhất</h2>
    <p class="section-sub" data-vi="Từ resort 5 sao đến boutique hotel — tìm phòng phù hợp ngân sách và phong cách." data-en="From 5-star resorts to boutique hotels — find the room that fits your budget and style.">Từ resort 5 sao đến boutique hotel — tìm phòng phù hợp ngân sách và phong cách.</p>
  </div>
  <div class="hotels-grid reveal">
    <div class="hotel-card"><div class="hotel-img h1"><span>🏨</span><div class="hotel-stars">★★★★★</div></div><div class="hotel-body"><div class="hotel-tag" data-vi="Nghỉ dưỡng" data-en="Resort">Nghỉ dưỡng</div><div class="hotel-name">Vinpearl Resort & Spa</div><div class="hotel-city" data-vi="📍 Nha Trang" data-en="📍 Nha Trang">📍 Nha Trang</div><div class="hotel-price"><div><div class="hotel-amount">2.800.000 ₫</div><div class="hotel-per" data-vi="/đêm" data-en="/night">/đêm</div></div><button class="btn-book-hotel" onclick="openModal('login')" data-vi="Đặt phòng" data-en="Book">Đặt phòng</button></div></div></div>
    <div class="hotel-card"><div class="hotel-img h2"><span>🌅</span><div class="hotel-stars">★★★★★</div></div><div class="hotel-body"><div class="hotel-tag" data-vi="Sang trọng" data-en="Luxury">Sang trọng</div><div class="hotel-name">InterContinental Danang</div><div class="hotel-city" data-vi="📍 Đà Nẵng" data-en="📍 Da Nang">📍 Đà Nẵng</div><div class="hotel-price"><div><div class="hotel-amount">4.200.000 ₫</div><div class="hotel-per" data-vi="/đêm" data-en="/night">/đêm</div></div><button class="btn-book-hotel" onclick="openModal('login')" data-vi="Đặt phòng" data-en="Book">Đặt phòng</button></div></div></div>
    <div class="hotel-card"><div class="hotel-img h3"><span>🏮</span><div class="hotel-stars">★★★★</div></div><div class="hotel-body"><div class="hotel-tag" data-vi="Boutique" data-en="Boutique">Boutique</div><div class="hotel-name">La Siesta Hoi An</div><div class="hotel-city" data-vi="📍 Hội An" data-en="📍 Hoi An">📍 Hội An</div><div class="hotel-price"><div><div class="hotel-amount">1.800.000 ₫</div><div class="hotel-per" data-vi="/đêm" data-en="/night">/đêm</div></div><button class="btn-book-hotel" onclick="openModal('login')" data-vi="Đặt phòng" data-en="Book">Đặt phòng</button></div></div></div>
    <div class="hotel-card"><div class="hotel-img h4"><span>🌊</span><div class="hotel-stars">★★★★★</div></div><div class="hotel-body"><div class="hotel-tag" data-vi="Spa" data-en="Spa">Spa</div><div class="hotel-name">Fusion Maia Resort</div><div class="hotel-city" data-vi="📍 Đà Nẵng" data-en="📍 Da Nang">📍 Đà Nẵng</div><div class="hotel-price"><div><div class="hotel-amount">3.500.000 ₫</div><div class="hotel-per" data-vi="/đêm" data-en="/night">/đêm</div></div><button class="btn-book-hotel" onclick="openModal('login')" data-vi="Đặt phòng" data-en="Book">Đặt phòng</button></div></div></div>
  </div>
  <div style="text-align:center;margin-top:32px" class="reveal">
    <button class="btn-hero-primary" onclick="openModal('login')" data-vi="Xem tất cả khách sạn →" data-en="View all hotels →">Xem tất cả khách sạn →</button>
  </div>
</div>
</section>

<!-- HOW IT WORKS -->
<section style="background:var(--gray)">
<div class="container">
  <div class="reveal">
    <div class="section-label" data-vi="⚙ CÁCH SỬ DỤNG" data-en="⚙ HOW TO USE">⚙ CÁCH SỬ DỤNG</div>
    <h2 class="section-title" data-vi="Đơn Giản - Nhanh Chóng - Hiệu Quả" data-en="Simple - Fast - Effective">Đơn Giản - Nhanh Chóng - Hiệu Quả</h2>
  </div>
  <div class="steps-grid reveal">
    <div class="step-card"><div class="step-num">1</div><div class="step-icon">👤</div><div class="step-title" data-vi="Tạo tài khoản" data-en="Create account">Tạo tài khoản</div><div class="step-desc" data-vi="Đăng ký miễn phí chỉ 30 giây. Không cần thẻ tín dụng." data-en="Register free in 30 seconds. No credit card needed.">Đăng ký miễn phí chỉ 30 giây. Không cần thẻ tín dụng.</div><div class="connector">→</div></div>
    <div class="step-card"><div class="step-num">2</div><div class="step-icon">⚙️</div><div class="step-title" data-vi="Cấu hình chuyến đi" data-en="Configure your trip">Cấu hình chuyến đi</div><div class="step-desc" data-vi="Chọn điểm đi, điểm đến, ngày bay, hãng ưu tiên và giá mong muốn." data-en="Select origin, destination, date, preferred airline and target price.">Chọn điểm đi, điểm đến, ngày bay, hãng ưu tiên và giá mong muốn.</div><div class="connector">→</div></div>
    <div class="step-card"><div class="step-num">3</div><div class="step-icon">🤖</div><div class="step-title" data-vi="Bật theo dõi tự động" data-en="Enable auto tracking">Bật theo dõi tự động</div><div class="step-desc" data-vi="Bot quét giá vé mỗi 5–60 phút tùy chu kỳ bạn đặt." data-en="Bot scans prices every 5–60 minutes based on your schedule.">Bot quét giá vé mỗi 5–60 phút tùy chu kỳ bạn đặt.</div><div class="connector">→</div></div>
    <div class="step-card"><div class="step-num">4</div><div class="step-icon">📱</div><div class="step-title" data-vi="Nhận cảnh báo Telegram" data-en="Get Telegram alerts">Nhận cảnh báo Telegram</div><div class="step-desc" data-vi="Khi giá rớt xuống dưới ngưỡng kỳ vọng, Telegram báo ngay lập tức." data-en="When price drops below your target, Telegram notifies you instantly.">Khi giá rớt xuống dưới ngưỡng kỳ vọng, Telegram báo ngay lập tức.</div></div>
  </div>
</div>
</section>

<!-- HELP / FAQ -->
<section id="help">
<div class="container">
  <div class="reveal">
    <div class="section-label" data-vi="❓ TRỢ GIÚP" data-en="❓ HELP">❓ TRỢ GIÚP</div>
    <h2 class="section-title" data-vi="Câu Hỏi Thường Gặp" data-en="Frequently Asked Questions">Câu Hỏi Thường Gặp</h2>
  </div>
  <div class="guide-grid reveal">
    <div class="guide-card"><div class="guide-icon">🔔</div><div class="guide-text"><h4 data-vi="Cài đặt Telegram Bot" data-en="Setup Telegram Bot">Cài đặt Telegram Bot</h4><p data-vi="Vào BotFather trên Telegram, tạo bot mới, lấy Token và Chat ID điền vào biến môi trường TELEGRAM_TOKEN và TELEGRAM_CHAT_ID." data-en="Go to BotFather on Telegram, create a new bot, get Token and Chat ID, fill in TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables.">Vào BotFather trên Telegram, tạo bot mới, lấy Token và Chat ID điền vào biến môi trường.</p></div></div>
    <div class="guide-card"><div class="guide-icon">✈</div><div class="guide-text"><h4 data-vi="Chọn chuyến bay" data-en="Select flights">Chọn chuyến bay</h4><p data-vi="Chọn điểm đi & đến từ danh sách sân bay nội địa hoặc quốc tế. Chọn hãng ưu tiên hoặc tất cả." data-en="Choose origin & destination from domestic or international airports. Select preferred airline or all.">Chọn điểm đi & đến từ danh sách nội địa hoặc quốc tế. Có thể ưu tiên hãng bay.</p></div></div>
    <div class="guide-card"><div class="guide-icon">💰</div><div class="guide-text"><h4 data-vi="Đặt giá kỳ vọng" data-en="Set target price">Đặt giá kỳ vọng</h4><p data-vi="Nhập giá tối đa bạn muốn trả. Bot chỉ gửi cảnh báo khi tìm được vé thấp hơn mức này." data-en="Enter the maximum price you want to pay. Bot only alerts when it finds tickets below this amount.">Nhập giá tối đa bạn muốn trả. Bot chỉ cảnh báo khi tìm được vé thấp hơn mức này.</p></div></div>
    <div class="guide-card"><div class="guide-icon">🏨</div><div class="guide-text"><h4 data-vi="Đặt khách sạn & khu vui chơi" data-en="Book hotels & attractions">Đặt khách sạn & khu vui chơi</h4><p data-vi="Sau khi đăng nhập, vào tab Khách Sạn và Du Lịch để xem danh sách khách sạn và khu vui chơi kèm link đặt." data-en="After login, go to the Hotels and Tourism tab to see hotels and attractions with booking links.">Sau đăng nhập vào tab Khách Sạn & Du Lịch để xem danh sách kèm link đặt trực tiếp.</p></div></div>
  </div>
  <div class="faq-list reveal">
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)" data-vi="Bot có quét giá thực tế từ hãng bay không?" data-en="Does the bot scan real prices from airlines?">Bot có quét giá thực tế từ hãng bay không? <span class="arrow">▼</span></div>
      <div class="faq-a" data-vi="Trong phiên bản demo, bot tạo giá mô phỏng để minh họa cơ chế hoạt động. Phiên bản production sẽ kết nối API thực tế từ các hãng bay và nền tảng vé máy bay." data-en="In demo version, the bot generates simulated prices to illustrate the mechanism. Production version will connect to real APIs from airlines and ticketing platforms.">Trong phiên bản demo, bot tạo giá mô phỏng để minh họa cơ chế hoạt động. Phiên bản production sẽ kết nối API thực tế từ các hãng bay và nền tảng vé máy bay.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)" data-vi="Tôi có thể theo dõi nhiều chặng bay cùng lúc không?" data-en="Can I track multiple routes at the same time?">Tôi có thể theo dõi nhiều chặng bay cùng lúc không? <span class="arrow">▼</span></div>
      <div class="faq-a" data-vi="Hiện tại mỗi tài khoản theo dõi một chặng bay. Tính năng đa chặng đang được phát triển và sẽ ra mắt trong phiên bản tiếp theo." data-en="Currently each account tracks one route. Multi-route feature is in development and will launch in the next version.">Hiện tại mỗi tài khoản theo dõi một chặng bay. Tính năng đa chặng đang được phát triển.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)" data-vi="Chu kỳ quét tối thiểu là bao nhiêu?" data-en="What is the minimum scan interval?">Chu kỳ quét tối thiểu là bao nhiêu? <span class="arrow">▼</span></div>
      <div class="faq-a" data-vi="Chu kỳ quét tối thiểu là 5 phút. Bạn có thể chọn 5, 15, 30 hoặc 60 phút tùy nhu cầu. Quét thường xuyên hơn sẽ phát hiện vé rẻ sớm hơn." data-en="The minimum scan interval is 5 minutes. You can choose 5, 15, 30, or 60 minutes. More frequent scanning detects cheap tickets earlier.">Chu kỳ quét tối thiểu là 5 phút. Bạn có thể chọn 5, 15, 30 hoặc 60 phút tùy nhu cầu.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)" data-vi="Làm sao nhận cảnh báo qua Telegram?" data-en="How do I receive Telegram alerts?">Làm sao nhận cảnh báo qua Telegram? <span class="arrow">▼</span></div>
      <div class="faq-a" data-vi="Bạn cần: (1) Tạo bot Telegram qua @BotFather, (2) Lấy API Token, (3) Tìm Chat ID của bạn, (4) Điền vào biến môi trường TELEGRAM_TOKEN và TELEGRAM_CHAT_ID khi deploy ứng dụng." data-en="You need: (1) Create a Telegram bot via @BotFather, (2) Get API Token, (3) Find your Chat ID, (4) Fill in TELEGRAM_TOKEN and TELEGRAM_CHAT_ID env vars when deploying.">Bạn cần tạo bot qua @BotFather → lấy Token & Chat ID → điền vào biến môi trường khi deploy.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)" data-vi="Dữ liệu cấu hình có được lưu không?" data-en="Is my configuration data saved?">Dữ liệu cấu hình có được lưu không? <span class="arrow">▼</span></div>
      <div class="faq-a" data-vi="Có, tất cả cấu hình (điểm đi/đến, ngày bay, giá kỳ vọng, hãng ưu tiên) được lưu vào file JSON trên server và được giữ nguyên khi bạn đăng xuất rồi đăng nhập lại." data-en="Yes, all configurations (origin/destination, dates, target prices, preferred airlines) are saved to a JSON file on the server and persist across login sessions.">Có, tất cả cấu hình được lưu vào file JSON và giữ nguyên giữa các phiên đăng nhập.</div>
    </div>
  </div>
</div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <div class="nav-brand" style="text-decoration:none;display:flex;align-items:center;gap:10px">
        <div class="nav-logo" style="width:36px;height:36px;background:linear-gradient(135deg,#10b981,#059669);border-radius:10px;display:flex;align-items:center;justify-content:center">✈</div>
        <div class="nav-name" style="font-family:Playfair Display,serif;font-weight:700;font-size:1.3rem;color:white">Flight<span style="color:#34d399">Hunter</span></div>
      </div>
      <div class="footer-tagline" data-vi="Săn vé thông minh — Khám phá Việt Nam và thế giới với giá tốt nhất." data-en="Smart ticket hunting — Explore Vietnam and the world at the best prices.">Săn vé thông minh — Khám phá Việt Nam và thế giới với giá tốt nhất.</div>
    </div>
    <div class="footer-col">
      <h4 data-vi="Sản phẩm" data-en="Product">Sản phẩm</h4>
      <a href="#destinations" data-vi="Điểm đến" data-en="Destinations">Điểm đến</a>
      <a href="#airlines" data-vi="Hãng bay" data-en="Airlines">Hãng bay</a>
      <a href="#hotels" data-vi="Khách sạn" data-en="Hotels">Khách sạn</a>
      <a href="#help" data-vi="Trợ giúp" data-en="Help">Trợ giúp</a>
    </div>
    <div class="footer-col">
      <h4 data-vi="Điểm đến hot" data-en="Hot destinations">Điểm đến hot</h4>
      <a href="#">Đà Nẵng</a><a href="#">Phú Quốc</a><a href="#">Hội An</a><a href="#">Bangkok</a><a href="#">Tokyo</a>
    </div>
    <div class="footer-col">
      <h4 data-vi="Liên hệ" data-en="Contact">Liên hệ</h4>
      <a href="mailto:thienpun826@gmail.com">✉ thienpun826@gmail.com</a>
      <a href="#">Telegram Bot</a>
      <a href="#">GitHub</a>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-email">✉ thienpun826@gmail.com</div>
    <div class="copyright">© 2026 Flight Hunter Pro. Made with ❤ in Việt Nam</div>
  </div>
</footer>

<!-- AUTH MODAL -->
<div class="modal-overlay" id="authModal" onclick="closeModalOutside(event)">
  <div class="modal-box">
    <div class="modal-wrap">
      <div class="modal-header">
        <div class="modal-logo">✈</div>
        <div class="modal-title">Flight<span style="color:#34d399">Hunter</span></div>
        <div class="modal-sub" id="modal-sub-txt">Đăng nhập để tiếp tục</div>
        <button class="modal-close" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="modal-tabs">
          <button class="modal-tab active" id="tab-login" onclick="switchModalTab('login')" data-vi="Đăng nhập" data-en="Login">Đăng nhập</button>
          <button class="modal-tab" id="tab-register" onclick="switchModalTab('register')" data-vi="Đăng ký" data-en="Sign Up">Đăng ký</button>
        </div>
        <div id="modal-alert" style="display:none" class="modal-alert"></div>
        <!-- Login -->
        <div id="form-login">
          <div class="field"><label data-vi="TÊN TÀI KHOẢN" data-en="USERNAME">TÊN TÀI KHOẢN</label><input type="text" id="l-user" placeholder="Nhập tên tài khoản..."></div>
          <div class="field"><label data-vi="MẬT KHẨU" data-en="PASSWORD">MẬT KHẨU</label><input type="password" id="l-pass" placeholder="Nhập mật khẩu..." onkeydown="if(event.key==='Enter')doLogin()"></div>
          <button class="btn-modal" onclick="doLogin()" data-vi="XÁC THỰC ĐĂNG NHẬP" data-en="LOGIN">XÁC THỰC ĐĂNG NHẬP</button>
        </div>
        <!-- Register -->
        <div id="form-register" style="display:none">
          <div class="field"><label data-vi="TÊN TÀI KHOẢN" data-en="USERNAME">TÊN TÀI KHOẢN</label><input type="text" id="r-user" placeholder="Nhập tên tài khoản..."></div>
          <div class="field"><label data-vi="EMAIL" data-en="EMAIL">EMAIL</label><input type="email" id="r-email" placeholder="email@example.com..."></div>
          <div class="field"><label data-vi="MẬT KHẨU" data-en="PASSWORD">MẬT KHẨU</label><input type="password" id="r-pass" placeholder="Tạo mật khẩu..." onkeydown="if(event.key==='Enter')doRegister()"></div>
          <button class="btn-modal" onclick="doRegister()" data-vi="TẠO TÀI KHOẢN" data-en="CREATE ACCOUNT">TẠO TÀI KHOẢN</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// Lang
let lang = 'vi';
function toggleLang() {
  lang = lang==='vi'?'en':'vi';
  document.getElementById('lang-btn').textContent = lang==='vi'?'EN':'VI';
  document.querySelectorAll('[data-vi]').forEach(el => {
    if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') return;
    el.textContent = el.getAttribute('data-'+lang);
  });
}

// Slides
let curSlide=0; const slides=document.querySelectorAll('.slide'); const dots=document.querySelectorAll('.dot');
function goSlide(n){slides[curSlide].classList.remove('active');dots[curSlide].classList.remove('active');curSlide=n;slides[curSlide].classList.add('active');dots[curSlide].classList.add('active');}
setInterval(()=>goSlide((curSlide+1)%slides.length),5000);

// Nav scroll
window.addEventListener('scroll',()=>{document.getElementById('main-nav').classList.toggle('scrolled',window.scrollY>60)});

// Reveal on scroll
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:0.1});
document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));

// Airline select
function selectAirline(el, code) {
  document.querySelectorAll('.airline-card').forEach(c=>c.classList.remove('selected'));
  el.classList.add('selected');
}

// FAQ
function toggleFaq(el){el.parentElement.classList.toggle('open')}

// Modal
function openModal(tab){document.getElementById('authModal').classList.add('open');switchModalTab(tab);}
function closeModal(){document.getElementById('authModal').classList.remove('open');}
function closeModalOutside(e){if(e.target===document.getElementById('authModal'))closeModal();}
function switchModalTab(t){
  document.getElementById('tab-login').classList.toggle('active',t==='login');
  document.getElementById('tab-register').classList.toggle('active',t==='register');
  document.getElementById('form-login').style.display=t==='login'?'block':'none';
  document.getElementById('form-register').style.display=t==='register'?'block':'none';
  document.getElementById('modal-alert').style.display='none';
  document.getElementById('modal-sub-txt').textContent=t==='login'?'Đăng nhập để tiếp tục':'Tạo tài khoản mới';
}
function showAlert(msg,type){let a=document.getElementById('modal-alert');a.textContent=msg;a.className='modal-alert '+(type||'err');a.style.display='block';}
function doLogin(){
  let u=document.getElementById('l-user').value.trim(),p=document.getElementById('l-pass').value.trim();
  if(!u||!p){showAlert('Vui lòng điền đủ thông tin!','err');return;}
  fetch('/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})})
    .then(r=>r.json()).then(d=>{if(d.ok){window.location.href='/dashboard';}else{showAlert(d.msg,'err');}});
}
function doRegister(){
  let u=document.getElementById('r-user').value.trim(),e=document.getElementById('r-email').value.trim(),p=document.getElementById('r-pass').value.trim();
  if(!u||!p){showAlert('Vui lòng điền đủ thông tin!','err');return;}
  fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,email:e,password:p})})
    .then(r=>r.json()).then(d=>{if(d.ok){showAlert('Đăng ký thành công! Đang chuyển hướng...','ok');setTimeout(()=>window.location.href='/dashboard',1200);}else{showAlert(d.msg,'err');}});
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});
</script>
</body>
</html>"""

# ════════════════════════════════════════════════
# DASHBOARD HTML
# ════════════════════════════════════════════════
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="vi" id="html-root">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Flight Hunter — Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--g:#10b981;--gd:#059669;--gl:#34d399;--navy:#0a1628;--navy2:#0d2137;--page:#f0f4f8;--card:#ffffff;--border:#e8eef4;--text:#1e293b;--muted:#64748b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--page);font-family:'Be Vietnam Pro',sans-serif;color:var(--text);min-height:100vh}

/* SIDEBAR */
.sidebar{position:fixed;left:0;top:0;bottom:0;width:72px;background:var(--navy);display:flex;flex-direction:column;align-items:center;padding:16px 0;gap:4px;z-index:50}
.s-logo{width:44px;height:44px;background:linear-gradient(135deg,var(--g),var(--gd));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:20px;cursor:pointer;text-decoration:none}
.s-item{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;cursor:pointer;transition:all 0.2s;position:relative}
.s-item:hover,.s-item.active{background:rgba(16,185,129,0.15)}
.s-item.active::before{content:'';position:absolute;left:-4px;top:50%;transform:translateY(-50%);width:4px;height:24px;background:var(--g);border-radius:0 4px 4px 0}
.s-tooltip{position:absolute;left:58px;background:var(--navy2);color:white;font-size:0.72rem;font-weight:600;padding:5px 10px;border-radius:8px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity 0.2s;z-index:100}
.s-item:hover .s-tooltip{opacity:1}
.s-bottom{margin-top:auto;display:flex;flex-direction:column;align-items:center;gap:8px}
.s-avatar{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--g),var(--gd));display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:700;color:white;cursor:pointer}

/* MAIN */
.main{margin-left:72px;padding:28px 28px 60px}

/* TOP BAR */
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:28px}
.page-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:var(--navy)}
.page-sub{font-size:0.82rem;color:var(--muted);margin-top:2px}
.topbar-right{display:flex;align-items:center;gap:12px}
.lang-sw{background:var(--card);border:1.5px solid var(--border);color:var(--text);padding:6px 12px;border-radius:20px;font-size:0.78rem;font-weight:600;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif}
.live-badge{display:flex;align-items:center;gap:6px;background:var(--card);border:1.5px solid var(--border);padding:8px 16px;border-radius:20px;font-size:0.78rem;font-weight:600;color:var(--muted)}
.ldot{width:7px;height:7px;border-radius:50%;background:#d1d5db}
.ldot.on{background:var(--g);box-shadow:0 0 6px var(--g);animation:p 2s infinite}
@keyframes p{0%,100%{opacity:1}50%{opacity:0.4}}

/* TABS */
.tabs{display:flex;gap:4px;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:4px;margin-bottom:24px;overflow-x:auto}
.tab{padding:9px 18px;border-radius:12px;font-size:0.82rem;font-weight:600;cursor:pointer;color:var(--muted);white-space:nowrap;transition:all 0.2s;border:none;background:transparent;font-family:'Be Vietnam Pro',sans-serif}
.tab.active{background:var(--navy);color:white}

/* STATS */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}
.sc{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}
.sv{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:var(--navy);margin-bottom:4px}
.sv.g{color:var(--g)}
.sv.sm{font-size:1.1rem}
.sl{font-size:0.75rem;color:var(--muted);font-weight:500}
.st-icon{font-size:1.4rem;margin-bottom:8px}

/* STATUS CARD */
.status-card{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:16px 22px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}
.st-lbl{font-size:0.82rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:flex;align-items:center;gap:8px}
.st-badge{display:flex;align-items:center;gap:7px;background:#f3f4f6;border-radius:20px;padding:7px 16px;font-size:0.78rem;font-weight:700;color:var(--muted)}
.st-badge.on{background:rgba(16,185,129,0.12);color:var(--g)}

/* CONFIG CARD */
.cfg{background:var(--card);border:1px solid var(--border);border-radius:22px;padding:24px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}
.cfg-head{font-size:0.8rem;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.07em;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.fi{background:#f8fafc;border:1.5px solid var(--border);border-radius:14px;padding:10px 14px;transition:border-color .2s}
.fi:focus-within{border-color:var(--g)}
.fl{font-size:.68rem;font-weight:700;color:#94a3b8;letter-spacing:.06em;text-transform:uppercase;margin-bottom:3px;display:block}
.fi select,.fi input{background:transparent;border:none;outline:none;width:100%;font-family:'Be Vietnam Pro',sans-serif;font-size:.92rem;font-weight:600;color:var(--text);-webkit-appearance:none}
.price-hint{font-size:.75rem;color:var(--g);font-weight:600;margin-top:-8px;margin-bottom:12px;padding-left:2px}

/* route type */
.route-tabs{display:flex;gap:8px;margin-bottom:12px}
.rt{padding:8px 16px;border-radius:10px;font-size:.8rem;font-weight:600;cursor:pointer;border:1.5px solid var(--border);background:var(--card);color:var(--muted);font-family:'Be Vietnam Pro',sans-serif;transition:all .2s}
.rt.active{background:var(--g);color:white;border-color:var(--g)}

/* range */
.irow{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.ilbl{font-size:.82rem;color:var(--muted)}
.ival{font-size:.9rem;font-weight:700;color:var(--g)}
input[type=range]{width:100%;-webkit-appearance:none;height:4px;border-radius:4px;background:linear-gradient(to right,var(--g) 20%,#e5e7eb 20%);outline:none;margin-bottom:6px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:white;border:2.5px solid var(--g);box-shadow:0 2px 8px rgba(16,185,129,.25);cursor:pointer}
.ticks{display:flex;justify-content:space-between;font-size:.7rem;color:#9ca3af;margin-bottom:12px}

/* toggle */
.tog-row{background:#f9fafb;border:1px solid var(--border);border-radius:16px;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.tog-title{font-size:.9rem;font-weight:700;color:var(--navy)}
.tog-sub{font-size:.73rem;color:var(--muted);margin-top:2px}
.tog-sw{position:relative;width:52px;height:30px;flex-shrink:0}
.tog-sw input{opacity:0;width:0;height:0}
.tog-tr{position:absolute;inset:0;background:#d1d5db;border-radius:30px;cursor:pointer;transition:background .25s}
.tog-tr::after{content:'';position:absolute;left:4px;top:4px;width:22px;height:22px;border-radius:50%;background:white;box-shadow:0 2px 5px rgba(0,0,0,.15);transition:transform .25s}
.tog-sw input:checked + .tog-tr{background:var(--g)}
.tog-sw input:checked + .tog-tr::after{transform:translateX(22px)}

/* btns */
.btn-p{width:100%;padding:15px;background:linear-gradient(135deg,var(--g),var(--gd));color:white;font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;border:none;border-radius:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;transition:all .2s}
.btn-p:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(16,185,129,.35)}
.btn-row{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:9px}
.btn-s{padding:12px;background:var(--page);color:var(--text);font-size:.8rem;font-weight:600;border:1.5px solid var(--border);border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;font-family:'Be Vietnam Pro',sans-serif;transition:all .2s}
.btn-s:hover{background:var(--border)}
.btn-d{padding:11px;background:#fff1f2;color:#ef4444;font-size:.8rem;font-weight:600;border:1.5px solid #fecdd3;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;width:100%;font-family:'Be Vietnam Pro',sans-serif}

/* Results */
.rbox{margin-bottom:20px}
.rhead{font-size:.8rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.empty{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:40px;text-align:center}
.empty-ico{font-size:2.5rem;opacity:.25;display:block;margin-bottom:14px;filter:grayscale(1)}
.empty-txt{font-size:.85rem;color:#9ca3af}
.flight-c{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.fn{font-weight:700;font-size:.9rem;color:var(--navy)}
.ft{font-size:.75rem;color:var(--muted);margin-top:3px}
.fp{font-family:'Playfair Display',serif;font-weight:800;font-size:1rem;color:var(--g);text-align:right}
.bk{display:inline-block;margin-top:5px;background:#eff6ff;color:#2563eb;font-size:.7rem;font-weight:700;padding:5px 11px;border-radius:8px;text-decoration:none}

/* Hotel cards */
.hotel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-bottom:20px}
.hc{background:var(--card);border:1px solid var(--border);border-radius:18px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.05);transition:all .3s}
.hc:hover{transform:translateY(-4px);box-shadow:0 10px 28px rgba(0,0,0,.1)}
.hi{height:130px;display:flex;align-items:center;justify-content:center;font-size:2.5rem;position:relative}
.hi.h1{background:linear-gradient(135deg,#0d4a6b,#0891b2)}
.hi.h2{background:linear-gradient(135deg,#1e3a5f,#2563eb)}
.hi.h3{background:linear-gradient(135deg,#064e3b,#10b981)}
.hi.h4{background:linear-gradient(135deg,#713f12,#d97706)}
.hi.h5{background:linear-gradient(135deg,#1a0a2e,#7c3aed)}
.hi.h6{background:linear-gradient(135deg,#1e293b,#475569)}
.hi.h7{background:linear-gradient(135deg,#0c4a6e,#0284c7)}
.hi.h8{background:linear-gradient(135deg,#312e81,#4f46e5)}
.h-stars{position:absolute;bottom:8px;left:10px;display:flex;gap:2px;font-size:.65rem;color:#fbbf24}
.hb{padding:14px}
.h-tag{display:inline-block;background:var(--page);color:var(--muted);font-size:.65rem;font-weight:700;padding:2px 9px;border-radius:10px;margin-bottom:6px;letter-spacing:.04em}
.h-name{font-weight:700;color:var(--navy);font-size:.88rem;margin-bottom:3px}
.h-city{font-size:.75rem;color:var(--muted);margin-bottom:10px}
.h-pr{display:flex;align-items:center;justify-content:space-between}
.h-am{font-weight:800;color:var(--g);font-size:.9rem}
.h-per{font-size:.68rem;color:var(--muted)}
.btn-bk{background:transparent;border:1.5px solid var(--g);color:var(--g);padding:6px 13px;border-radius:18px;font-size:.72rem;font-weight:700;cursor:pointer;font-family:'Be Vietnam Pro',sans-serif;transition:all .2s}
.btn-bk:hover{background:var(--g);color:white}

/* Attractions */
.attr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.ac{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.04);transition:all .3s}
.ac:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(0,0,0,.09)}
.a-ico{font-size:2rem;margin-bottom:10px}
.a-type{font-size:.68rem;font-weight:700;color:var(--g);text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}
.a-name{font-weight:700;color:var(--navy);font-size:.88rem;margin-bottom:3px}
.a-city{font-size:.75rem;color:var(--muted);margin-bottom:10px}
.a-bot{display:flex;align-items:center;justify-content:space-between}
.a-price{font-weight:700;color:var(--text);font-size:.82rem}
.a-rating{display:flex;align-items:center;gap:4px;font-size:.78rem;font-weight:700;color:#f59e0b}

/* Log */
.log-box{background:var(--card);border:1px solid var(--border);border-radius:16px;overflow:hidden}
.log-in{padding:14px;height:180px;overflow-y:auto;font-family:monospace;font-size:.72rem}
.log-e{margin-bottom:4px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.log-t{color:#94a3b8}
.log-m{color:var(--text)}
.log-m.success{color:var(--g)}.log-m.error{color:#ef4444}.log-m.warning{color:#f59e0b}
.log-empty2{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#c0ccd3;gap:8px;font-size:.8rem}

/* password section */
.pw-card{background:var(--card);border:1px solid var(--border);border-radius:22px;padding:24px;margin-bottom:20px;max-width:420px;box-shadow:0 2px 10px rgba(0,0,0,.04)}

/* MOBILE */
@media(max-width:768px){
  .sidebar{width:56px}
  .main{margin-left:56px;padding:16px 14px 60px}
  .stats{grid-template-columns:1fr 1fr}
  .hotel-grid{grid-template-columns:1fr}
  .attr-grid{grid-template-columns:1fr 1fr}
}
</style>
</head>
<body>

<!-- SIDEBAR -->
<div class="sidebar">
  <a href="/" class="s-logo">✈</a>
  <div class="s-item active" onclick="showTab('flight')" id="si-flight">✈<div class="s-tooltip" data-vi="Vé máy bay" data-en="Flights">Vé máy bay</div></div>
  <div class="s-item" onclick="showTab('hotel')" id="si-hotel">🏨<div class="s-tooltip" data-vi="Khách sạn" data-en="Hotels">Khách sạn</div></div>
  <div class="s-item" onclick="showTab('attract')" id="si-attract">🎡<div class="s-tooltip" data-vi="Du lịch & Vui chơi" data-en="Tourism & Fun">Du lịch & Vui chơi</div></div>
  <div class="s-item" onclick="showTab('account')" id="si-account">🔐<div class="s-tooltip" data-vi="Tài khoản" data-en="Account">Tài khoản</div></div>
  <div class="s-bottom">
    <div class="s-avatar" title="{{ username }}">{{ username|upper|first }}</div>
    <div class="s-item" onclick="location.href='/auth/logout'" style="font-size:1rem">↩<div class="s-tooltip" data-vi="Đăng xuất" data-en="Logout">Đăng xuất</div></div>
  </div>
</div>

<!-- MAIN -->
<div class="main">
  <div class="topbar">
    <div>
      <div class="page-title" id="page-title-txt">Săn Vé Máy Bay</div>
      <div class="page-sub">Xin chào, <strong>{{ username }}</strong> 👋</div>
    </div>
    <div class="topbar-right">
      <button class="lang-sw" onclick="toggleLang()" id="lang-btn">EN</button>
      <div class="live-badge"><div class="ldot" id="ldot"></div><span id="live-time">--:--:--</span></div>
    </div>
  </div>

  <!-- TABS -->
  <div class="tabs">
    <button class="tab active" onclick="showTab('flight')" id="t-flight" data-vi="✈ Vé Máy Bay" data-en="✈ Flights">✈ Vé Máy Bay</button>
    <button class="tab" onclick="showTab('hotel')" id="t-hotel" data-vi="🏨 Khách Sạn" data-en="🏨 Hotels">🏨 Khách Sạn</button>
    <button class="tab" onclick="showTab('attract')" id="t-attract" data-vi="🎡 Du Lịch & Vui Chơi" data-en="🎡 Tourism & Fun">🎡 Du Lịch & Vui Chơi</button>
    <button class="tab" onclick="showTab('account')" id="t-account" data-vi="🔐 Tài Khoản" data-en="🔐 Account">🔐 Tài Khoản</button>
  </div>

  <!-- STATS -->
  <div class="stats">
    <div class="sc"><div class="st-icon">🔍</div><div class="sv" id="sc1">0</div><div class="sl" data-vi="Lần đã quét" data-en="Scans done">Lần đã quét</div></div>
    <div class="sc"><div class="st-icon">🔔</div><div class="sv g" id="sc2">0</div><div class="sl" data-vi="Cảnh báo đã gửi" data-en="Alerts sent">Cảnh báo đã gửi</div></div>
    <div class="sc"><div class="st-icon">💰</div><div class="sv sm" id="sc3">—</div><div class="sl" data-vi="Giá rẻ nhất" data-en="Cheapest found">Giá rẻ nhất</div></div>
    <div class="sc"><div class="st-icon">⏰</div><div class="sv sm" id="sc4">—</div><div class="sl" data-vi="Quét lần cuối" data-en="Last scan">Quét lần cuối</div></div>
  </div>

  <!-- BOT STATUS -->
  <div class="status-card">
    <div class="st-lbl">🤖 <span data-vi="TRẠNG THÁI BOT" data-en="BOT STATUS">TRẠNG THÁI BOT</span></div>
    <div class="st-badge" id="st-badge"><div class="ldot" id="st-dot"></div><span id="st-txt" data-vi="Đang nghỉ" data-en="Idle">Đang nghỉ</span></div>
  </div>

  <!-- PANEL: FLIGHT -->
  <div id="panel-flight">
    <div class="cfg">
      <div class="cfg-head">🎛 <span data-vi="CẤU HÌNH THEO DÕI" data-en="TRACKING CONFIG">CẤU HÌNH THEO DÕI</span></div>
      <!-- Route type -->
      <div class="route-tabs">
        <button class="rt active" id="rt-dom" onclick="setRouteType('domestic')" data-vi="🇻🇳 Nội địa" data-en="🇻🇳 Domestic">🇻🇳 Nội địa</button>
        <button class="rt" id="rt-int" onclick="setRouteType('international')" data-vi="🌍 Quốc tế" data-en="🌍 International">🌍 Quốc tế</button>
      </div>
      <div class="row2">
        <div class="fi"><span class="fl" data-vi="✈ ĐIỂM ĐI" data-en="✈ ORIGIN">✈ ĐIỂM ĐI</span><select id="origin"></select></div>
        <div class="fi"><span class="fl" data-vi="🛬 ĐIỂM ĐẾN" data-en="🛬 DESTINATION">🛬 ĐIỂM ĐẾN</span><select id="destination"></select></div>
      </div>
      <div class="fi" style="margin-bottom:12px"><span class="fl" data-vi="📅 NGÀY BAY" data-en="📅 FLIGHT DATE">📅 NGÀY BAY</span><input type="date" id="fly_date"></div>
      <!-- Airline priority -->
      <div class="fi" style="margin-bottom:6px">
        <span class="fl" data-vi="👑 ƯU TIÊN HÃNG BAY" data-en="👑 PREFERRED AIRLINE">👑 ƯU TIÊN HÃNG BAY</span>
        <select id="airline">
          {% for a in airlines %}
          <option value="{{a.code}}">{{a.logo}} {{a.name_vi}}</option>
          {% endfor %}
        </select>
      </div>
      <div class="fi" style="margin-bottom:6px"><span class="fl" data-vi="💰 GIÁ KỲ VỌNG (VNĐ)" data-en="💰 TARGET PRICE (VND)">💰 GIÁ KỲ VỌNG (VNĐ)</span><input type="number" id="threshold" placeholder="2500000" oninput="updHint()"></div>
      <div class="price-hint" id="ph">= 2.500.000 ₫</div>
      <div class="irow"><span class="ilbl" data-vi="⏱ Chu kỳ quét" data-en="⏱ Scan interval">⏱ Chu kỳ quét</span><span class="ival" id="iv-display">15 phút</span></div>
      <input type="range" id="interval" min="5" max="60" step="5" value="15" oninput="updInterval(this.value)">
      <div class="ticks"><span>5</span><span>15</span><span>30</span><span>60</span></div>
      <div class="tog-row"><div><div class="tog-title" data-vi="Kích hoạt theo dõi" data-en="Enable tracking">Kích hoạt theo dõi</div><div class="tog-sub" data-vi="Bot sẽ tự động quét theo lịch" data-en="Bot auto-scans on schedule">Bot sẽ tự động quét theo lịch</div></div><label class="tog-sw"><input type="checkbox" id="is_active"><div class="tog-tr"></div></label></div>
      <button class="btn-p" onclick="saveConfig()" data-vi="💾 Lưu & Áp dụng" data-en="💾 Save & Apply">💾 Lưu & Áp dụng</button>
      <div class="btn-row">
        <button class="btn-s" onclick="scanNow()" data-vi="🔄 Quét ngay" data-en="🔄 Scan now">🔄 Quét ngay</button>
        <button class="btn-s" onclick="scanNow()" data-vi="📱 Test Telegram" data-en="📱 Test Telegram">📱 Test Telegram</button>
      </div>
      <button class="btn-d" onclick="clearLogs()" data-vi="🗑 Xóa log" data-en="🗑 Clear logs">🗑 Xóa log</button>
    </div>
    <div class="rbox">
      <div class="rhead">🎫 <span data-vi="KẾT QUẢ VÉ MỚI NHẤT" data-en="LATEST TICKETS">KẾT QUẢ VÉ MỚI NHẤT</span></div>
      <div id="results-box"><div class="empty"><span class="empty-ico">✈️</span><div class="empty-txt" data-vi="Chưa có dữ liệu — bật theo dõi hoặc nhấn Quét ngay" data-en="No data — enable tracking or press Scan now">Chưa có dữ liệu — bật theo dõi hoặc nhấn Quét ngay</div></div></div>
    </div>
    <div class="rhead">📋 <span data-vi="NHẬT KÝ HOẠT ĐỘNG" data-en="ACTIVITY LOG">NHẬT KÝ HOẠT ĐỘNG</span></div>
    <div class="log-box"><div class="log-in" id="log-box"><div class="log-empty2"><span>&gt;_</span><span data-vi="Chưa có hoạt động nào..." data-en="No activity yet...">Chưa có hoạt động nào...</span></div></div></div>
  </div>

  <!-- PANEL: HOTEL -->
  <div id="panel-hotel" style="display:none">
    <div class="rhead">🏨 <span data-vi="KHÁCH SẠN NỔI BẬT" data-en="FEATURED HOTELS">KHÁCH SẠN NỔI BẬT</span></div>
    <div class="hotel-grid">
      {% for h in hotels %}
      <div class="hc"><div class="hi h{{loop.index % 8 + 1}}"><span>{{h.img}}</span><div class="h-stars">{{'★'*h.stars}}</div></div><div class="hb"><div class="h-tag">{{h.tag_vi}}</div><div class="h-name">{{h.name}}</div><div class="h-city">📍 {{h.city_vi}}</div><div class="h-pr"><div><div class="h-am">{{'{:,}'.format(h.price)}} ₫</div><div class="h-per">/đêm</div></div><button class="btn-bk" onclick="window.open('https://www.booking.com','_blank')" data-vi="Đặt phòng" data-en="Book">Đặt phòng</button></div></div></div>
      {% endfor %}
    </div>
  </div>

  <!-- PANEL: ATTRACTIONS -->
  <div id="panel-attract" style="display:none">
    <div class="rhead">🎡 <span data-vi="KHU DU LỊCH & VUI CHƠI" data-en="TOURISM & ENTERTAINMENT">KHU DU LỊCH & VUI CHƠI</span></div>
    <div class="attr-grid">
      {% for a in attractions %}
      <div class="ac"><div class="a-ico">{{a.img}}</div><div class="a-type">{{a.type_vi}}</div><div class="a-name">{{a.name_vi}}</div><div class="a-city">📍 {{a.city_vi}}</div><div class="a-bot"><div class="a-price">{% if a.price > 0 %}{{'{:,}'.format(a.price)}} ₫{% else %}<span style="color:var(--g)">Miễn phí</span>{% endif %}</div><div class="a-rating">⭐ {{a.rating}}</div></div><button class="btn-bk" style="margin-top:12px;width:100%;justify-content:center;display:flex" onclick="window.open('https://www.vinwonders.com','_blank')" data-vi="Đặt vé tham quan" data-en="Book ticket">Đặt vé tham quan</button></div>
      {% endfor %}
    </div>
  </div>

  <!-- PANEL: ACCOUNT -->
  <div id="panel-account" style="display:none">
    <div class="pw-card">
      <div class="cfg-head">🔐 <span data-vi="ĐỔI MẬT KHẨU" data-en="CHANGE PASSWORD">ĐỔI MẬT KHẨU</span></div>
      <div id="pw-alert" style="display:none;padding:10px 14px;border-radius:10px;font-size:.82rem;font-weight:600;margin-bottom:14px;text-align:center"></div>
      <div class="fi" style="margin-bottom:12px"><span class="fl" data-vi="MẬT KHẨU CŨ" data-en="CURRENT PASSWORD">MẬT KHẨU CŨ</span><input type="password" id="old_pass" placeholder="Nhập mật khẩu hiện tại..."></div>
      <div class="fi" style="margin-bottom:14px"><span class="fl" data-vi="MẬT KHẨU MỚI" data-en="NEW PASSWORD">MẬT KHẨU MỚI</span><input type="password" id="new_pass" placeholder="Nhập mật khẩu mới..."></div>
      <button class="btn-p" style="background:linear-gradient(135deg,#0284c7,#0369a1)" onclick="changePw()" data-vi="🔑 Xác nhận đổi mật khẩu" data-en="🔑 Confirm change">🔑 Xác nhận đổi mật khẩu</button>
    </div>
  </div>
</div>

<script>
const domAirports = {{ dom_airports|tojson }};
const intAirports = {{ int_airports|tojson }};
let lang='vi', routeType='domestic', isSaving=false;

function toggleLang(){
  lang=lang==='vi'?'en':'vi';
  document.getElementById('lang-btn').textContent=lang==='vi'?'EN':'VI';
  document.querySelectorAll('[data-vi]').forEach(el=>{
    if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') return;
    el.textContent=el.getAttribute('data-'+lang);
  });
}

// Clock
function tick(){let n=new Date();document.getElementById('live-time').textContent=[n.getHours(),n.getMinutes(),n.getSeconds()].map(v=>String(v).padStart(2,'0')).join(':');}
setInterval(tick,1000); tick();

// Tabs
const allTabs=['flight','hotel','attract','account'];
function showTab(t){
  allTabs.forEach(x=>{
    document.getElementById('panel-'+x).style.display=x===t?'block':'none';
    document.getElementById('t-'+x).classList.toggle('active',x===t);
    let si=document.getElementById('si-'+x);
    if(si) si.classList.toggle('active',x===t);
  });
  const titles={'flight':'Săn Vé Máy Bay','hotel':'Khách Sạn','attract':'Du Lịch & Vui Chơi','account':'Tài Khoản'};
  document.getElementById('page-title-txt').textContent=titles[t]||'Dashboard';
  if(t==='flight') loadState();
}

// Route type
function setRouteType(rt){
  routeType=rt;
  document.getElementById('rt-dom').classList.toggle('active',rt==='domestic');
  document.getElementById('rt-int').classList.toggle('active',rt==='international');
  populateAirports(rt);
}
function populateAirports(rt){
  let airports=rt==='domestic'?domAirports:intAirports;
  ['origin','destination'].forEach(id=>{
    let s=document.getElementById(id), v=s.value;
    s.innerHTML=airports.map(a=>`<option value="${a.code}">${a['name_'+lang]}</option>`).join('');
    if(airports.find(a=>a.code===v)) s.value=v;
  });
}

// Price hint
function updHint(){let v=parseInt(document.getElementById('threshold').value)||0;document.getElementById('ph').textContent='= '+v.toLocaleString('vi-VN')+' ₫';}
function updInterval(v){document.getElementById('iv-display').textContent=v+' phút';let p=(v-5)/55*100;document.getElementById('interval').style.background=`linear-gradient(to right,var(--g) ${p}%,#e5e7eb ${p}%)`;}

// UIF
function uif(id,val){let el=document.getElementById(id);if(el&&document.activeElement!==el) el.value=val;}

// Load state
function loadState(){
  if(isSaving) return;
  fetch('/api/state').then(r=>r.json()).then(d=>{
    if(!d||d.error) return;
    document.getElementById('sc1').textContent=d.stats.scan_count||0;
    document.getElementById('sc2').textContent=d.stats.alert_count||0;
    document.getElementById('sc3').textContent=d.stats.cheapest||'—';
    document.getElementById('sc4').textContent=d.stats.last_scan||'—';
    let on=d.config.is_active;
    let sb=document.getElementById('st-badge'),sd=document.getElementById('st-dot'),stxt=document.getElementById('st-txt'),ld=document.getElementById('ldot');
    if(on){sb.classList.add('on');sd.classList.add('on');ld.classList.add('on');stxt.textContent='Đang quét tự động';}
    else{sb.classList.remove('on');sd.classList.remove('on');ld.classList.remove('on');stxt.textContent='Đang nghỉ';}
    uif('fly_date',d.config.fly_date); uif('threshold',d.config.threshold); uif('airline',d.config.airline||'ALL');
    if(document.activeElement.id!=='interval'){document.getElementById('interval').value=d.config.interval||15;updInterval(d.config.interval||15);}
    if(document.activeElement.id!=='is_active') document.getElementById('is_active').checked=d.config.is_active;
    let rb=document.getElementById('results-box');
    if(!d.results||!d.results.length){rb.innerHTML='<div class="empty"><span class="empty-ico">✈️</span><div class="empty-txt">Chưa có dữ liệu — bật theo dõi hoặc nhấn Quét ngay</div></div>';}
    else{rb.innerHTML=d.results.map(f=>`<div class="flight-c"><div><div class="fn">${f.airline_logo||''} ${f.airline}</div><div class="ft">${f.time_window}</div></div><div><div class="fp">${f.price.toLocaleString('vi-VN')} ₫</div><a href="${f.link}" target="_blank" class="bk">ĐẶT VÉ</a></div></div>`).join('');}
    let lb=document.getElementById('log-box');
    if(!d.logs||!d.logs.length){lb.innerHTML='<div class="log-empty2"><span>&gt;_</span><span>Chưa có hoạt động nào...</span></div>';}
    else{lb.innerHTML=d.logs.map(l=>`<div class="log-e"><span class="log-t">[${l.time}]</span> <span class="log-m ${l.type}">${l.text}</span></div>`).join('');}
  }).catch(()=>{});
}

function saveConfig(){
  isSaving=true;
  let p={origin:document.getElementById('origin').value,destination:document.getElementById('destination').value,fly_date:document.getElementById('fly_date').value,threshold:document.getElementById('threshold').value,interval:document.getElementById('interval').value,is_active:document.getElementById('is_active').checked,airline:document.getElementById('airline').value,route_type:routeType,hotel_city:'Đà Nẵng',hotel_threshold:1000000};
  fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)}).then(r=>r.json()).then(()=>{isSaving=false;loadState();}).catch(()=>{isSaving=false;});
}
function scanNow(){fetch('/api/scan-now',{method:'POST'}).then(()=>{setTimeout(loadState,1500);});}
function clearLogs(){fetch('/api/clear-logs',{method:'POST'}).then(()=>loadState());}
function changePw(){
  let o=document.getElementById('old_pass').value,n=document.getElementById('new_pass').value;
  if(!o||!n){showPwAlert('Vui lòng điền đủ thông tin!','err');return;}
  fetch('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({old_password:o,new_password:n})}).then(r=>r.json()).then(d=>{showPwAlert(d.msg,d.ok?'ok':'err');if(d.ok){document.getElementById('old_pass').value='';document.getElementById('new_pass').value='';}});
}
function showPwAlert(msg,type){let a=document.getElementById('pw-alert');a.textContent=msg;a.style.background=type==='ok'?'#dcfce7':'#fee2e2';a.style.color=type==='ok'?'#16a34a':'#dc2626';a.style.display='block';}

window.onload=function(){
  let d=new Date();d.setDate(d.getDate()+7);document.getElementById('fly_date').value=d.toISOString().split('T')[0];
  document.getElementById('threshold').value=2500000;updHint();updInterval(15);
  setRouteType('domestic');
  loadState();setInterval(loadState,4000);
};
</script>
</body>
</html>"""

# ════════════════════════════════════════════════
# ROUTES
# ════════════════════════════════════════════════
def logged_in(): return "user" in session

@app.route("/")
def landing(): return render_template_string(LANDING_HTML)

@app.route("/dashboard")
def dashboard():
    if not logged_in(): return redirect(url_for("landing"))
    return render_template_string(DASHBOARD_HTML, username=session["user"],
        airlines=AIRLINES, hotels=HOTELS, attractions=ATTRACTIONS,
        dom_airports=DOMESTIC_AIRPORTS, int_airports=INTERNATIONAL_AIRPORTS)

@app.route("/auth/login", methods=["POST"])
def auth_login():
    d=request.json or {}
    u=d.get("username","").strip(); p=d.get("password","").strip()
    if u in state["users"] and state["users"][u].get("password")==p:
        session["user"]=u; return jsonify({"ok":True})
    return jsonify({"ok":False,"msg":"⚠️ Tên tài khoản hoặc mật khẩu không đúng!"})

@app.route("/auth/register", methods=["POST"])
def auth_register():
    d=request.json or {}
    u=d.get("username","").strip(); p=d.get("password","").strip(); e=d.get("email","").strip()
    if not u or not p: return jsonify({"ok":False,"msg":"⚠️ Vui lòng điền đủ thông tin!"})
    if u in state["users"]: return jsonify({"ok":False,"msg":"⚠️ Tên tài khoản đã tồn tại!"})
    state["users"][u]={"password":p,"email":e}; save_data()
    session["user"]=u; return jsonify({"ok":True})

@app.route("/auth/logout")
def auth_logout(): session.clear(); return redirect(url_for("landing"))

@app.route("/api/state")
def api_state():
    if not logged_in(): return jsonify({"error":"Unauthorized"}),401
    return jsonify({"config":state["config"],"stats":state["stats"],"results":state["results"],"logs":state["logs"]})

@app.route("/api/config", methods=["POST"])
def api_config():
    if not logged_in(): return jsonify({"error":"Unauthorized"}),401
    d=request.json or {}
    state["config"].update({"origin":str(d.get("origin","SGN")),"destination":str(d.get("destination","DAD")),"fly_date":str(d.get("fly_date","")),"airline":str(d.get("airline","ALL")),"threshold":int(d.get("threshold") or 2500000),"interval":int(d.get("interval") or 15),"is_active":bool(d.get("is_active",False)),"route_type":str(d.get("route_type","domestic")),"hotel_city":str(d.get("hotel_city","Đà Nẵng")),"hotel_threshold":int(d.get("hotel_threshold") or 1000000)})
    save_data(); add_log("Đã cập nhật cấu hình theo dõi.","info")
    if state["config"]["is_active"]: threading.Thread(target=execute_scan,args=(False,),daemon=True).start()
    return jsonify({"ok":True})

@app.route("/api/scan-now", methods=["POST"])
def api_scan_now():
    if not logged_in(): return jsonify({"error":"Unauthorized"}),401
    threading.Thread(target=execute_scan,args=(True,),daemon=True).start()
    return jsonify({"ok":True})

@app.route("/api/clear-logs", methods=["POST"])
def api_clear_logs():
    if not logged_in(): return jsonify({"error":"Unauthorized"}),401
    state["logs"]=[]; save_data(); return jsonify({"ok":True})

@app.route("/api/change-password", methods=["POST"])
def api_change_pw():
    if not logged_in(): return jsonify({"error":"Unauthorized"}),401
    d=request.json or {}; u=session["user"]
    if state["users"].get(u,{}).get("password")!=d.get("old_password","").strip():
        return jsonify({"ok":False,"msg":"❌ Mật khẩu cũ không đúng!"})
    state["users"][u]["password"]=d.get("new_password","").strip(); save_data()
    add_log(f"Tài khoản [{u}] đổi mật khẩu thành công.","warning")
    return jsonify({"ok":True,"msg":"✅ Đổi mật khẩu thành công!"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
ENDOFFILE
echo "Done. Lines: $(wc -l < /mnt/user-data/outputs/app_full.py)"
