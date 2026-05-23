"""
Flight & Hotel Hunter — Giao diện nâng cấp đầy đủ Vé & Khách sạn khớp 100% Mockup
"""

import os, json, time, logging, threading, random
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, render_template_string, redirect, session, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secure-hunter-key-2026")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "premium_hunter_data.json"

AIRPORTS = [
    {"code": "SGN", "name": "SGN — TP.HCM"},
    {"code": "HAN", "name": "HAN — Hà Nội"},
    {"code": "DAD", "name": "DAD — Đà Nẵng"},
    {"code": "CXR", "name": "CXR — Nha Trang"},
    {"code": "PQC", "name": "PQC — Phú Quốc"},
    {"code": "VCA", "name": "VCA — Cần Thơ"},
    {"code": "HPH", "name": "HPH — Hải Phòng"},
    {"code": "VII", "name": "VII — Vinh"},
    {"code": "HUI", "name": "HUI — Huế"},
    {"code": "BMV", "name": "BMV — Buôn Ma Thuột"},
    {"code": "VCL", "name": "VCL — Chu Lai"},
    {"code": "UIH", "name": "UIH — Quy Nhơn"},
]

def load_saved_data():
    default = {
        "users": {"admin": "123456"},
        "config": {
            "origin": "SGN", "destination": "DAD",
            "fly_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "threshold": 2500000, "interval": 15, "is_active": False,
            "airline": "ALL", "hotel_city": "Đà Nẵng", "hotel_threshold": 1000000,
        },
        "stats": {"scan_count": 0, "alert_count": 0, "last_scan": "—", "cheapest": "—"},
        "results": [], "hotel_results": [], "logs": [],
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("users", {"admin": "123456"})
                data.setdefault("config", default["config"])
                data.setdefault("hotel_results", [])
                return data
        except Exception as e:
            logger.error(f"Lỗi đọc file: {e}")
    return default

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Lỗi ghi file: {e}")

state = load_saved_data()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "123456:FAKE_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "123456")

def add_log(message, log_type="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    state["logs"].insert(0, {"time": ts, "text": message, "type": log_type})
    if len(state["logs"]) > 50: state["logs"].pop()
    save_data()

def generate_direct_links(type_search, item_name, code1, code2, date_str):
    try:
        if type_search == "flight":
            parts = date_str.split("-") if date_str and "-" in date_str else []
            date_fmt = f"{parts[2]}-{parts[1]}-{parts[0]}" if len(parts) == 3 and len(parts[0]) == 4 else date_str
            if "VietJet" in item_name:
                return f"https://www.vietjetair.com/vi/ve-may-bay/dat-ve?origin={code1}&destination={code2}&departDate={date_fmt.replace('-','/')}&adults=1"
            elif "Vietnam Airlines" in item_name:
                return f"https://www.vietnamairlines.com/vi/flight-search?itinerary={code1}-{code2}:{date_str}&adt=1"
            elif "Bamboo" in item_name:
                return f"https://www.bambooairways.com/reservation/v1/flights?origin={code1}&destination={code2}&departureDate={date_str}&adults=1"
            return f"https://www.traveloka.com/vi-vn/flight/search?ap={code1}.{code2}&dt={date_fmt}.NA&ps=1.0.0&sc=ECONOMY"
        else:
            q = code1.replace(" ", "%20")
            if "Agoda" in item_name: return f"https://www.agoda.com/vi-vn/pages/agoda/default/DestinationSearchResult.aspx?city={q}"
            if "Booking" in item_name: return f"https://www.booking.com/searchresults.vi.html?ss={q}"
            return f"https://www.traveloka.com/vi-vn/hotel/search?spec={date_str}.1.1.HOTEL_GEO.{code1}.{q}.1"
    except: return "https://www.traveloka.com"

def run_flight_scan(cfg):
    flights = []
    base = 1400000 if (cfg["origin"] in ["SGN","HAN"] and cfg["destination"] in ["SGN","HAN"]) else 900000
    airlines = [{"name":"VietJet Air","code":"VJ"},{"name":"Vietnam Airlines","code":"VN"},{"name":"Bamboo Airways","code":"QH"}]
    random.seed(int(time.time()))
    for a in airlines:
        if cfg["airline"] != "ALL" and a["code"] != cfg["airline"]: continue
        price = int(base + random.randint(50000, 600000))
        if a["code"] == "VN": price += 300000
        h = random.randint(5, 22); m = random.choice([0,15,30,45])
        flights.append({"id":f"{a['code']}-{random.randint(100,999)}","airline":a["name"],
            "time_window":f"{h:02d}:{m:02d} ➔ {(h+2)%24:02d}:{m:02d}","price":price,
            "link":generate_direct_links("flight",a["name"],cfg["origin"],cfg["destination"],cfg["fly_date"])})
    flights.sort(key=lambda x: x["price"])
    return flights

def run_hotel_scan(cfg):
    hotels = []
    platforms = ["Agoda Khách Sạn","Booking.com","Traveloka Hotel"]
    rooms = ["Phòng Deluxe Giường Đôi","Phòng Superior Hướng Biển","Căn hộ Studio Giá Tốt"]
    random.seed(int(time.time())+1)
    for p in platforms:
        price = int(600000 + random.randint(100000, 900000))
        hotels.append({"name":f"🏨 [{p}] {cfg['hotel_city']}",
            "room":random.choice(rooms),"price":price,
            "link":generate_direct_links("hotel",p,cfg["hotel_city"],"",cfg["fly_date"])})
    hotels.sort(key=lambda x: x["price"])
    return hotels

def execute_scan(force_notify=False):
    cfg = state["config"]
    state["stats"]["scan_count"] += 1
    state["stats"]["last_scan"] = datetime.now().strftime("%H:%M")
    try:
        flights = run_flight_scan(cfg); state["results"] = flights
        hotels = run_hotel_scan(cfg); state["hotel_results"] = hotels
        
        # Xử lý Logic thông báo Flight
        if flights:
            cheapest_flight = flights[0]
            state["stats"]["cheapest"] = f"{cheapest_flight['price']:,} ₫"
            add_log(f"Quét máy bay: {cfg['origin']}➔{cfg['destination']}: {cheapest_flight['price']:,} ₫", "success")
            
            if cheapest_flight["price"] <= int(cfg["threshold"]) or force_notify:
                state["stats"]["alert_count"] += 1
                msg = f"✈️ <b>FLIGHT ALERT</b>\n\n📍 {cfg['origin']} ➔ {cfg['destination']}\n📅 {cfg['fly_date']}\n💵 <b>{cheapest_flight['price']:,} ₫</b>\n👑 {cheapest_flight['airline']}\n\n👉 <a href='{cheapest_flight['link']}'>ĐẶT VÉ NGAY</a>"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id":TELEGRAM_CHAT_ID,"text":msg,"parse_mode":"HTML"}, timeout=8)
                    
        # Xử lý thông báo Khách Sạn độc lập
        if hotels:
            cheapest_hotel = hotels[0]
            add_log(f"Quét khách sạn tại {cfg['hotel_city']}: {cheapest_hotel['price']:,} ₫", "success")
            if cheapest_hotel["price"] <= int(cfg["hotel_threshold"]) and not force_notify:
                state["stats"]["alert_count"] += 1
                msg = f"🏨 <b>HOTEL ALERT</b>\n\n📍 Thành phố: {cfg['hotel_city']}\n🛏 Phòng: {cheapest_hotel['room']}\n💵 <b>{cheapest_hotel['price']:,} ₫</b>\n🌐 Nguồn: {cheapest_hotel['name']}\n\n👉 <a href='{cheapest_hotel['link']}'>XEM PHÒNG NGAY</a>"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id":TELEGRAM_CHAT_ID,"text":msg,"parse_mode":"HTML"}, timeout=8)
                    
    except Exception as e:
        add_log(f"Lỗi hệ thống quét: {str(e)}", "error")
    save_data()

def scan_job():
    if state["config"]["is_active"]: execute_scan(False)

scheduler = BackgroundScheduler()
scheduler.start()

def update_scheduler(minutes):
    job_id = "flight_scan_job"
    if scheduler.get_job(job_id): scheduler.remove_job(job_id)
    scheduler.add_job(scan_job, trigger=IntervalTrigger(minutes=minutes), id=job_id, replace_existing=True)

update_scheduler(state["config"]["interval"])

# ═══ AUTH TEMPLATE ═══
AUTH_HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flight Hunter</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a1e23;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:'DM Sans',sans-serif}
.card{background:#0f2d35;border:1px solid rgba(255,255,255,0.07);border-radius:24px;padding:36px;width:100%;max-width:370px;margin:20px}
.brand{display:flex;align-items:center;gap:10px;font-family:'Syne',sans-serif;font-weight:800;font-size:1.3rem;color:white;margin-bottom:8px;justify-content:center}
.brand-icon{width:34px;height:34px;background:#10b981;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem}
.brand span{color:#10b981}
.subtitle{text-align:center;font-size:0.75rem;color:#4b6a72;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:28px}
.alert{padding:10px 14px;border-radius:10px;font-size:0.82rem;font-weight:600;margin-bottom:18px;text-align:center}
.alert.err{background:rgba(239,68,68,0.12);color:#f87171;border:1px solid rgba(239,68,68,0.2)}
.alert.ok{background:rgba(16,185,129,0.12);color:#10b981;border:1px solid rgba(16,185,129,0.2)}
.lbl{font-size:0.72rem;font-weight:700;color:#4b6a72;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;display:block}
input{width:100%;background:#14363f;border:1.5px solid rgba(255,255,255,0.07);border-radius:12px;padding:13px 16px;color:white;font-family:'DM Sans',sans-serif;font-size:0.92rem;outline:none;margin-bottom:14px;transition:border-color 0.2s}
input:focus{border-color:#10b981}
input::placeholder{color:#4b6a72}
.btn{width:100%;padding:15px;background:#10b981;color:white;font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;border:none;border-radius:13px;cursor:pointer;margin-top:4px}
.btn:active{background:#059669}
.foot{text-align:center;margin-top:18px;font-size:0.82rem;color:#4b6a72}
.foot a{color:#10b981;font-weight:700;text-decoration:none}
</style></head>
<body><div class="card">
<div class="brand"><div class="brand-icon">✈</div>Flight<span>Hunter</span></div>
<div class="subtitle">{% if is_register %}Đăng ký thành viên mới{% else %}Hệ thống quản trị{% endif %}</div>
{% if message %}<div class="alert {% if is_error %}err{% else %}ok{% endif %}">{{message}}</div>{% endif %}
<form method="POST" action="{% if is_register %}/register{% else %}/login{% endif %}">
<label class="lbl">Tên tài khoản</label>
<input type="text" name="username" placeholder="Nhập tên tài khoản..." required autofocus>
<label class="lbl">Mật khẩu</label>
<input type="password" name="password" placeholder="Nhập mật khẩu..." required>
<button class="btn" type="submit">{% if is_register %}TẠO TÀI KHOẢN{% else %}XÁC THỰC ĐĂNG NHẬP{% endif %}</button>
</form>
{% if is_register %}<div class="foot">Đã có tài khoản? <a href="/login">Đăng nhập ngay</a></div>{% endif %}
</div></body></html>"""

def get_main_html():
    return """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flight &amp; Hotel Hunter Pro</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --green: #10b981; --green-dim: rgba(16,185,129,0.15); --green-border: rgba(16,185,129,0.3);
            --bg-dark: #0a1e23; --bg-mid: #0f2d35; --bg-page: #f2f4f6;
        }
        body { background: var(--bg-page); font-family: 'DM Sans', sans-serif; min-height: 100vh; padding-bottom: 60px; }

        .header { background: linear-gradient(170deg, var(--bg-dark) 0%, var(--bg-mid) 55%, #163d47 100%); color: white; padding: 0 0 56px 0; border-bottom-left-radius: 28px; border-bottom-right-radius: 28px; position: relative; overflow: hidden; }
        .header::before { content:''; position:absolute; width:340px;height:340px; background:radial-gradient(circle,rgba(16,185,129,0.12) 0%,transparent 70%); top:-60px;right:-80px; border-radius:50%; }
        .header::after { content:''; position:absolute; width:200px;height:200px; background:radial-gradient(circle,rgba(16,185,129,0.07) 0%,transparent 70%); bottom:30px;left:-40px; border-radius:50%; }

        .topbar { display:flex; justify-content:space-between; align-items:center; padding:18px 22px 0 22px; position:relative; z-index:2; }
        .brand { display:flex; align-items:center; gap:9px; font-family:'Syne',sans-serif; font-weight:800; font-size:1.2rem; color:white; }
        .brand-icon { width:32px;height:32px; background:var(--green); border-radius:9px; display:flex;align-items:center;justify-content:center; font-size:0.9rem; }
        .brand span { color:var(--green); }
        .live-pill { display:flex; align-items:center; gap:6px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1); border-radius:20px; padding:5px 12px; font-size:0.72rem; font-weight:600; color:#8ba5ac; letter-spacing:0.03em; }
        .live-dot { width:6px;height:6px; border-radius:50%; background:#4b6a72; }
        .live-dot.on { background:var(--green); box-shadow:0 0 6px var(--green); animation:pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.4} }

        .hero { padding:28px 22px 0 22px; position:relative; z-index:2; }
        .scan-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.35); border-radius:20px; padding:5px 14px; font-size:0.75rem; font-weight:700; colorvar(--green); letter-spacing:0.05em; margin-bottom:18px; }
        .hero-title { font-family:'Syne',sans-serif; font-size:2.3rem; font-weight:800; line-height:1.1; color:white; margin-bottom:14px; }
        .hero-title .accent { color:var(--green); }
        .hero-sub { font-size:0.88rem; color:#8ba5ac; line-height:1.6; max-width:300px; }

        .stats-float { display:grid; grid-template-columns:1fr 1fr; gap:12px; padding:0 18px; margin-top:-28px; position:relative; z-index:10; }
        .stat-card { background:white; border-radius:18px; padding:18px 16px; box-shadow:0 6px 20px rgba(0,0,0,0.08); border:1px solid #eef1f4; text-align:center; }
        .stat-val { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#111827; line-height:1; margin-bottom:4px; }
        .stat-val.green { color:var(--green); }
        .stat-val.sm { font-size:1.1rem; }
        .stat-lbl { font-size:0.72rem; color:#9ca3af; font-weight:500; }

        .bot-status { background:white; border-radius:18px; margin:14px 18px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 14px rgba(0,0,0,0.05); border:1px solid #eef1f4; }
        .bot-lbl { display:flex; align-items:center; gap:8px; font-size:0.82rem; font-weight:700; color:#4b5563; text-transform:uppercase; letter-spacing:0.05em; }
        .status-badge { display:flex; align-items:center; gap:7px; background:#f3f4f6; border-radius:20px; padding:7px 14px; font-size:0.78rem; font-weight:700; color:#6b7280; }
        .status-badge.active { background:rgba(16,185,129,0.1); color:var(--green); }
        .status-dot2 { width:8px;height:8px; border-radius:50%; background:#d1d5db; }
        .status-dot2.on { background:var(--green); animation:pulse 2s infinite; }

        /* TAB CONTROLLERS */
        .tabs-header { display: flex; background: #e4e7eb; border-radius: 14px; margin: 0 18px 14px 18px; padding: 4px; gap: 4px; }
        .tab-btn { flex: 1; padding: 12px; border: none; background: transparent; border-radius: 10px; font-family: 'Syne', sans-serif; font-size: 0.88rem; font-weight: 700; color: #6b7280; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: all 0.2s; }
        .tab-btn.active { background: white; color: var(--bg-dark); box-shadow: 0 3px 10px rgba(0,0,0,0.05); }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .section-card { background:white; border-radius:22px; margin:0 18px 16px 18px; padding:22px 20px; box-shadow:0 4px 16px rgba(0,0,0,0.05); border:1px solid #eef1f4; }
        .section-head { display:flex; align-items:center; gap:8px; font-size:0.8rem; font-weight:700; color:#374151; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:20px; }

        .airport-row { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px; }
        .field-wrap { background:#f8fafc; border:1.5px solid #e8ecf0; border-radius:14px; padding:10px 14px; margin-bottom:10px; transition:border-color 0.2s; }
        .field-wrap:focus-within { border-color:var(--green); }
        .field-label { font-size:0.68rem; font-weight:700; color:#94a3b8; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:3px; display:block; }
        .field-wrap select, .field-wrap input { background:transparent; border:none; outline:none; width:100%; font-family:'DM Sans',sans-serif; font-size:0.92rem; font-weight:600; color:#111827; }

        .price-hint { font-size:0.75rem; color:var(--green); font-weight:600; margin-top:-6px; margin-bottom:10px; padding-left:2px; }

        .interval-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
        .interval-lbl { font-size:0.82rem; color:#6b7280; }
        .interval-val { font-size:0.9rem; font-weight:700; color:var(--green); }
        input[type=range] { width:100%; -webkit-appearance:none; height:4px; border-radius:4px; background:#e5e7eb; outline:none; margin-bottom:8px; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:22px;height:22px; border-radius:50%; background:white; border:2.5px solid var(--green); box-shadow:0 2px 8px rgba(16,185,129,0.25); cursor:pointer; }
        .slider-ticks { display:flex; justify-content:space-between; font-size:0.72rem; color:#9ca3af; font-weight:500; }

        .toggle-row { background:#f9fafb; border:1px solid #eef1f4; border-radius:16px; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; margin-top:6px; }
        .toggle-title { font-size:0.9rem; font-weight:700; color:#111827; }
        .toggle-sub { font-size:0.73rem; color:#9ca3af; margin-top:2px; }
        .toggle-switch { position:relative; width:52px;height:30px; flex-shrink:0; }
        .toggle-switch input { opacity:0;width:0;height:0; }
        .toggle-track { position:absolute; inset:0; background:#d1d5db; border-radius:30px; cursor:pointer; transition:background 0.25s; }
        .toggle-track::after { content:''; position:absolute; left:4px;top:4px; width:22px;height:22px; border-radius:50%; background:white; box-shadow:0 2px 5px rgba(0,0,0,0.15); transition:transform 0.25s; }
        .toggle-switch input:checked + .toggle-track { background:var(--green); }
        .toggle-switch input:checked + .toggle-track::after { transform:translateX(22px); }

        .btn-primary { width:100%; padding:16px; background:var(--green); color:white; font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; border:none; border-radius:15px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:10px; transition:all 0.2s; }
        .btn-primary:active { transform:scale(0.98); background:#059669; }
        .btn-row { display:grid; grid-template-columns:1fr 1fr; gap:9px; margin-bottom:9px; }
        .btn-secondary { padding:12px; background:#f3f4f6; color:#374151; font-family:'DM Sans',sans-serif; font-size:0.8rem; font-weight:600; border:1.5px solid #e5e7eb; border-radius:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; transition:background 0.2s; }
        .btn-danger { padding:11px; background:#fff1f2; color:#ef4444; font-family:'DM Sans',sans-serif; font-size:0.8rem; font-weight:600; border:1.5px solid #fecdd3; border-radius:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; width:100%; }

        .results-section { margin:0 18px; }
        .results-head { display:flex; align-items:center; gap:8px; font-size:0.8rem; font-weight:700; color:#374151; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:12px; }
        
        .empty-state { background:white; border-radius:20px; padding:36px 24px; text-align:center; border:1px solid #eef1f4; box-shadow:0 4px 14px rgba(0,0,0,0.04); }
        .empty-icon { font-size:2.5rem; opacity:0.25; margin-bottom:14px; display:block; filter:grayscale(1); }
        .empty-title { font-size:0.85rem; color:#9ca3af; font-weight:500; line-height:1.6; }
        
        .flight-card { background:white; border-radius:16px; padding:16px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; border:1px solid #eef1f4; box-shadow:0 2px 10px rgba(0,0,0,0.04); }
        .flight-name { font-weight:700; font-size:0.9rem; color:#111827; }
        .flight-time { font-size:0.75rem; color:#9ca3af; margin-top:3px; }
        .flight-price { font-family:'Syne',sans-serif; font-weight:800; font-size:1rem; color:var(--green); text-align:right; }
        .book-btn { display:inline-block; margin-top:5px; background:#eff6ff; color:#2563eb; font-size:0.7rem; font-weight:700; padding:5px 11px; border-radius:8px; text-decoration:none; text-transform:uppercase;}

        .logs-section { margin:14px 18px 0 18px; }
        .log-box { background:white; border-radius:18px; border:1px solid #eef1f4; overflow:hidden; box-shadow:0 4px 14px rgba(0,0,0,0.04); }
        .log-inner { padding:16px; height:160px; overflow-y:auto; font-family:'DM Mono','Fira Code',monospace; font-size:0.73rem; }
        .log-entry { margin-bottom:5px; padding-bottom:5px; border-bottom:1px solid #f3f4f6; }
        .log-time { color:#94a3b8; }
        .log-text { color:#374151; }
        .log-text.success { color:var(--green); }
        .log-text.error { color:#ef4444; }

        .logout-row { text-align:center; margin-top:20px; }
        .logout-btn { background:none; border:none; color:#ef4444; font-size:0.82rem; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:5px; font-family:'DM Sans',sans-serif; }
    </style>
</head>
<body>

<div class="header">
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">✈</div>
            Flight &amp; Hotel <span>Hunter</span>
        </div>
        <div class="live-pill">
            <div class="live-dot" id="topLiveDot"></div>
            <span id="topLiveTime">--:--:--</span>
        </div>
    </div>
    <div class="hero">
        <div class="scan-badge">⚡ TỰ ĐỘNG QUÉT ĐA NỀN TẢNG</div>
        <h1 class="hero-title">
            Săn Vé &amp; <span class="accent">Phòng<br>Thông Minnh</span><br>Báo Telegram
        </h1>
        <p class="hero-sub">Hệ thống giám sát giá vé máy bay &amp; phòng khách sạn tự động, gửi thông báo tức thì khi đạt mức chi phí kỳ vọng.</p>
    </div>
</div>

<div class="stats-float">
    <div class="stat-card"><div class="stat-val" id="scanCount">0</div><div class="stat-lbl">Lần đã quét</div></div>
    <div class="stat-card"><div class="stat-val green" id="alertCount">0</div><div class="stat-lbl">Cảnh báo đã gửi</div></div>
    <div class="stat-card"><div class="stat-val sm" id="cheapest">—</div><div class="stat-lbl">Vé rẻ nhất</div></div>
    <div class="stat-card"><div class="stat-val sm" id="lastScan">—</div><div class="stat-lbl">Quét lần cuối</div></div>
</div>

<div class="bot-status">
    <div class="bot-lbl">🤖 TRẠNG THÁI BOT</div>
    <div class="status-badge" id="botBadge">
        <div class="status-dot2" id="botDot"></div>
        <span id="botTxt">Đang nghỉ</span>
    </div>
</div>

<div class="tabs-header">
    <button class="tab-btn active" onclick="switchTab('flight')">✈️ Vé Máy Bay</button>
    <button class="tab-btn" onclick="switchTab('hotel')">🏨 Khách Sạn</button>
</div>

<div id="flight-tab" class="tab-content active">
    <div class="section-card">
        <div class="section-head">🎛 CẤU HÌNH MÁY BAY</div>
        <div class="airport-row">
            <div class="field-wrap">
                <span class="field-label">✈ Điểm đi (IATA)</span>
                <select id="origin">{% for ap in airports %}<option value="{{ap.code}}">{{ap.name}}</option>{% endfor %}</select>
            </div>
            <div class="field-wrap">
                <span class="field-label">🛬 Điểm đến (IATA)</span>
                <select id="destination">{% for ap in airports %}<option value="{{ap.code}}">{{ap.name}}</option>{% endfor %}</select>
            </div>
        </div>
        <div class="field-wrap">
            <span class="field-label">📅 Ngày bay</span>
            <input type="date" id="fly_date">
        </div>
        <div class="field-wrap">
            <span class="field-label">💰 Giá vé kỳ vọng tối đa (VNĐ)</span>
            <input type="number" id="threshold" placeholder="2500000" oninput="updatePriceHint('threshold', 'priceHint')">
        </div>
        <div class="price-hint" id="priceHint">= 2.500.000 ₫</div>
        
        <div class="field-wrap">
            <span class="field-label">👑 Hãng hàng không lựa chọn</span>
            <select id="airline">
                <option value="ALL">Tất cả các hãng (VietJet, VN Airlines, Bamboo)</option>
                <option value="VJ">VietJet Air</option>
                <option value="VN">Vietnam Airlines</option>
                <option value="QH">Bamboo Airways</option>
            </select>
        </div>
    </div>
</div>

<div id="hotel-tab" class="tab-content">
    <div class="section-card">
        <div class="section-head">🏨 CẤU HÌNH KHÁCH SẠN</div>
        <div class="field-wrap">
            <span class="field-label">📍 Thành phố / Điểm du lịch</span>
            <input type="text" id="hotel_city" placeholder="Nhập tên thành phố (Ví dụ: Đà Nẵng, Phú Quốc...)">
        </div>
        <div class="field-wrap">
            <span class="field-label">💰 Giá phòng kỳ vọng đêm (VNĐ)</span>
            <input type="number" id="hotel_threshold" placeholder="1000000" oninput="updatePriceHint('hotel_threshold', 'hotelPriceHint')">
        </div>
        <div class="price-hint" id="hotelPriceHint">= 1.000.000 ₫</div>
    </div>
</div>

<div class="section-card" style="margin-top:-16px;">
    <div class="section-head">⚙️ CÀI ĐẶT THỜI GIAN QUET TRÌNH</div>
    <div class="interval-row">
        <span class="interval-lbl">⏱ Quét lại hệ thống định kỳ</span>
        <span class="interval-val" id="intervalDisplay">15 phút</span>
    </div>
    <input type="range" id="interval" min="5" max="60" step="5" value="15" oninput="updateInterval(this.value)">
    <div class="slider-ticks"><span>5m</span><span>15m</span><span>30m</span><span>60m</span></div>

    <div class="toggle-row">
        <div>
            <div class="toggle-title">Kích hoạt chế độ theo dõi</div>
            <div class="toggle-sub">Bot tự chạy ngầm 24/7 theo chu kỳ</div>
        </div>
        <label class="toggle-switch">
            <input type="checkbox" id="is_active">
            <div class="toggle-track"></div>
        </label>
    </div>

    <button class="btn-primary" onclick="saveConfig()">💾 Lưu &amp; Kích hoạt cấu hình</button>
    <div class="btn-row">
        <button class="btn-secondary" onclick="scanNow()">🔄 Quét ngay</button>
        <button class="btn-secondary" onclick="testTelegram()">✈ Test Telegram</button>
    </div>
    <button class="btn-danger" onclick="clearLogs()">🗑 Xóa nhật ký log</button>
</div>

<div class="results-section">
    <div class="results-head" id="results-title">🎫 KẾT QUẢ VÉ MÁY BAY MỚI NHẤT</div>
    <div id="results-box"></div>
</div>

<div class="logs-section">
    <div class="results-head">📋 NHẬT KÝ HOẠT ĐỘNG</div>
    <div class="log-box">
        <div class="log-inner" id="log-box"></div>
    </div>
</div>

<div class="logout-row">
    <button class="logout-btn" onclick="location.href='/logout'">↩ ĐĂNG XUẤT HỆ THỐNG</button>
</div>

<script>
let isSaving = false;
let currentTab = 'flight';

function init() {
    let d = new Date(); d.setDate(d.getDate()+6);
    document.getElementById('fly_date').value = d.toISOString().split('T')[0];
    updateClock();
    setInterval(updateClock, 1000);
    loadState(); 
    setInterval(loadState, 3000);
}

function updateClock() {
    let n = new Date();
    document.getElementById('topLiveTime').textContent =
        [n.getHours(),n.getMinutes(),n.getSeconds()].map(v=>String(v).padStart(2,'0')).join(':');
}

function updatePriceHint(inputId, hintId) {
    let v = parseInt(document.getElementById(inputId).value)||0;
    document.getElementById(hintId).textContent = '= ' + v.toLocaleString('vi-VN') + ' ₫';
}

function updateInterval(v) {
    document.getElementById('intervalDisplay').textContent = v + ' phút';
    let pct = (v-5)/(60-5)*100;
    document.getElementById('interval').style.background =
        `linear-gradient(to right,#10b981 0%,#10b981 ${pct}%,#e5e7eb ${pct}%)`;
}

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    if(tab === 'flight') {
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('flight-tab').classList.add('active');
        document.getElementById('results-title').textContent = "🎫 KẾT QUẢ VÉ MÁY BAY MỚI NHẤT";
    } else {
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('hotel-tab').classList.add('active');
        document.getElementById('results-title').textContent = "🏨 KẾT QUẢ KHÁCH SẠN MỚI NHẤT";
    }
    loadState();
}

function uif(id, val) {
    let el = document.getElementById(id);
    if (el && document.activeElement !== el) {
        if(el.type === 'checkbox') el.checked = val;
        else el.value = val;
    }
}

function loadState() {
    if (isSaving) return;
    fetch('/api/state').then(r=>r.json()).then(d => {
        if (!d || d.error) return;
        document.getElementById('scanCount').textContent = d.stats.scan_count||0;
        document.getElementById('alertCount').textContent = d.stats.alert_count||0;
        document.getElementById('cheapest').textContent = d.stats.cheapest||'—';
        document.getElementById('lastScan').textContent = d.stats.last_scan||'—';

        let active = d.config.is_active;
        let badge = document.getElementById('botBadge');
        let dot = document.getElementById('botDot');
        let topDot = document.getElementById('topLiveDot');
        if (active) {
            badge.classList.add('active'); dot.classList.add('on'); topDot.classList.add('on');
            document.getElementById('botTxt').textContent = 'Đang quét tự động';
        } else {
            badge.classList.remove('active'); dot.classList.remove('on'); topDot.classList.remove('on');
            document.getElementById('botTxt').textContent = 'Đang nghỉ';
        }

        uif('origin', d.config.origin); 
        uif('destination', d.config.destination);
        uif('fly_date', d.config.fly_date); 
        uif('threshold', d.config.threshold);
        uif('airline', d.config.airline || 'ALL');
        uif('hotel_city', d.config.hotel_city || '');
        uif('hotel_threshold', d.config.hotel_threshold || 1000000);
        uif('is_active', d.config.is_active);

        if (document.activeElement.id !== 'interval') {
            document.getElementById('interval').value = d.config.interval||15;
            updateInterval(d.config.interval||15);
        }
        updatePriceHint('threshold', 'priceHint');
        updatePriceHint('hotel_threshold', 'hotelPriceHint');

        // Render dữ liệu theo tab đang chọn
        let rb = document.getElementById('results-box');
        if (currentTab === 'flight') {
            if (!d.results || !d.results.length) {
                rb.innerHTML = '<div class="empty-state"><span class="empty-icon">✈️</span><p class="empty-title">Chưa có dữ liệu vé máy bay — bật theo dõi hoặc bấm <strong>Quét ngay</strong></p></div>';
            } else {
                rb.innerHTML = d.results.map(f=>`<div class="flight-card"><div><div class="flight-name">${f.airline} <small style="color:#6b7280; font-weight:normal;">(${f.id})</small></div><div class="flight-time">${f.time_window}</div></div><div><div class="flight-price">${f.price.toLocaleString('vi-VN')} ₫</div><a href="${f.link}" target="_blank" class="book-btn">ĐẶT VÉ</a></div></div>`).join('');
            }
        } else {
            if (!d.hotel_results || !d.hotel_results.length) {
                rb.innerHTML = '<div class="empty-state"><span class="empty-icon">🏨</span><p class="empty-title">Chưa có dữ liệu khách sạn — bật theo dõi hoặc bấm <strong>Quét ngay</strong></p></div>';
            } else {
                rb.innerHTML = d.hotel_results.map(h=>`<div class="flight-card"><div><div class="flight-name">${h.name}</div><div class="flight-time">${h.room}</div></div><div><div class="flight-price">${h.price.toLocaleString('vi-VN')} ₫</div><a href="${h.link}" target="_blank" class="book-btn" style="background:#fef3c7; color:#d97706;">XEM PHÒNG</a></div></div>`).join('');
            }
        }

        let lb = document.getElementById('log-box');
        if (!d.logs || !d.logs.length) {
            lb.innerHTML = '<div class="log-empty" style="text-align:center; padding-top:40px; color:#9ca3af;">&gt;_ Chưa có hoạt động nào....</div>';
        } else {
            lb.innerHTML = d.logs.map(l=>`<div class="log-entry"><span class="log-time">[${l.time}]</span> <span class="log-text ${l.type}">${l.text}</span></div>`).join('');
        }
    }).catch(()=>{});
}

function saveConfig() {
    isSaving = true;
    let p = {
        origin: document.getElementById('origin').value,
        destination: document.getElementById('destination').value,
        fly_date: document.getElementById('fly_date').value,
        threshold: parseInt(document.getElementById('threshold').value)||2500000,
        interval: parseInt(document.getElementById('interval').value)||15,
        is_active: document.getElementById('is_active').checked,
        airline: document.getElementById('airline').value, 
        hotel_city: document.getElementById('hotel_city').value || 'Đà Nẵng', 
        hotel_threshold: parseInt(document.getElementById('hotel_threshold').value)||1000000
    };
    fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)})
        .then(r=>r.json()).then(()=>{ isSaving=false; loadState(); }).catch(()=>{ isSaving=false; });
}

function scanNow() { fetch('/api/scan-now',{method:'POST'}).then(()=>loadState()); }
function testTelegram() { fetch('/api/test-telegram',{method:'POST'}).then(()=>loadState()); }
function clearLogs() { fetch('/api/clear-logs',{method:'POST'}).then(()=>loadState()); }

window.onload = init;
</script>
</body>
</html>"""

@app.route("/")
def index():
    if not logged_in(): return redirect(url_for("login"))
    return render_template_string(get_main_html(), airports=AIRPORTS)

@app.route("/api/state")
def get_state():
    if not logged_in(): return jsonify({"error": "Unauthorized"}), 401
    return jsonify(state)

@app.route("/api/config", methods=["POST"])
def save_config():
    if not logged_in(): return jsonify({"error": "Unauthorized"}), 401
    req = request.json or {}
    
    # Đồng bộ cấu hình
    state["config"]["origin"] = req.get("origin", state["config"]["origin"])
    state["config"]["destination"] = req.get("destination", state["config"]["destination"])
    state["config"]["fly_date"] = req.get("fly_date", state["config"]["fly_date"])
    state["config"]["threshold"] = int(req.get("threshold", state["config"]["threshold"]))
    state["config"]["airline"] = req.get("airline", state["config"]["airline"])
    state["config"]["hotel_city"] = req.get("hotel_city", state["config"]["hotel_city"])
    state["config"]["hotel_threshold"] = int(req.get("hotel_threshold", state["config"]["hotel_threshold"]))
    
    old_interval = state["config"]["interval"]
    new_interval = int(req.get("interval", old_interval))
    state["config"]["interval"] = new_interval
    state["config"]["is_active"] = bool(req.get("is_active", False))
    
    if old_interval != new_interval:
        update_scheduler(new_interval)
        
    add_log("Đã cập nhật toàn bộ cấu hình hệ thống Vé & Khách sạn.", "info")
    save_data()
    return jsonify({"status": "ok"})

@app.route("/api/scan-now", methods=["POST"])
def api_scan_now():
    if not logged_in(): return jsonify({"error": "Unauthorized"}), 401
    execute_scan(force_notify=False)
    return jsonify({"status": "ok"})

@app.route("/api/test-telegram", methods=["POST"])
def api_test_telegram():
    if not logged_in(): return jsonify({"error": "Unauthorized"}), 401
    add_log("Đang kích hoạt quy trình Test gửi thông báo Telegram...", "warning")
    execute_scan(force_notify=True)
    return jsonify({"status": "ok"})

@app.route("/api/clear-logs", methods=["POST"])
def api_clear_logs():
    if not logged_in(): return jsonify({"error": "Unauthorized"}), 401
    state["logs"] = []
    save_data()
    return jsonify({"status": "ok"})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
