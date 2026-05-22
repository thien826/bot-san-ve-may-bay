"""
╔══════════════════════════════════════════════════════════════╗
║   FLIGHT & HOTEL HUNTER — Full Account Management            ║
║   Bổ sung: Menu chọn sân bay trực quan & Fix lỗi Link 404    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import logging
import threading
import random
from datetime import datetime, timedelta

import requests
from flask import Flask, request, jsonify, render_template_string, redirect, session, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# ─────────────────────────────────────────────────────────────
#  KHỞI TẠO APP & LOGGING
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secure-hunter-key-2026")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "premium_hunter_data.json"

# Danh sách sân bay hỗ trợ chọn nhanh
AIRPORTS = [
    {"code": "SGN", "name": "SGN - TP. Hồ Chí Minh"},
    {"code": "HAN", "name": "HAN - Hà Nội"},
    {"code": "DAD", "name": "DAD - Đà Nẵng"},
    {"code": "CXR", "name": "CXR - Nha Trang"},
    {"code": "PQC", "name": "PQC - Phú Quốc"},
    {"code": "VCA", "name": "VCA - Cần Thơ"},
    {"code": "HPH", "name": "HPH - Hải Phòng"},
    {"code": "VII", "name": "VII - Vinh"},
    {"code": "HUI", "name": "HUI - Huế"},
    {"code": "BMV", "name": "BMV - Buôn Ma Thuột"},
    {"code": "VCL", "name": "VCL - Chu Lai"},
    {"code": "UIH", "name": "UIH - Quy Nhơn"}
]

# ═════════════════════════════════════════════════════════════
#  CƠ CHẾ LƯU TRỮ VĨNH VIỄN
# ═════════════════════════════════════════════════════════════
def load_saved_data():
    default_state = {
        "users": {
            "admin": "123456"
        },
        "config": {
            "origin": "SGN", "destination": "DAD",
            "fly_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "threshold": 2500000, "interval": 15, "is_active": False, "airline": "ALL",
            "hotel_city": "Đà Nẵng", "hotel_threshold": 1000000
        },
        "stats": { "scan_count": 0, "alert_count": 0, "last_scan": "--:--", "cheapest": "-" },
        "results": [], "hotel_results": [], "logs": []
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "users" not in data:
                    data["users"] = {"admin": "123456"}
                return data
        except Exception as e:
            logger.error(f"Lỗi đọc file cấu hình: {e}")
    return default_state

def save_data_permanently():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Lỗi ghi file cấu hình: {e}")

state = load_saved_data()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "123456:FAKE_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "123456")

def add_log(message: str, log_type: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {"time": timestamp, "text": message, "type": log_type}
    state["logs"].insert(0, log_entry)
    if len(state["logs"]) > 50: state["logs"].pop()
    save_data_permanently()

# ═════════════════════════════════════════════════════════════
#  HÀM TẠO ĐƯỜNG DẪN CHUẨN ĐỊNH DẠNG (FIX LỖI 404)
# ═════════════════════════════════════════════════════════════
def generate_direct_links(type_search: str, item_name: str, code1: str, code2: str, date_str: str) -> str:
    try:
        if type_search == "flight":
            # Chuẩn hóa định dạng ngày từ YYYY-MM-DD thành DD-MM-YYYY cho đại lý Việt Nam
            if date_str and "-" in date_str:
                parts = date_str.split("-")
                if len(parts)[0] == 4:
                    date_formatted = f"{parts[2]}-{parts[1]}-{parts[0]}"
                else:
                    date_formatted = date_str
            else:
                date_formatted = datetime.now().strftime("%d-%m-%Y")

            if "VietJet" in item_name:
                return f"https://www.vietjetair.com/vi/ve-may-bay/dat-ve?origin={code1}&destination={code2}&departDate={date_formatted.replace('-', '/')}&adults=1"
            elif "Vietnam Airlines" in item_name:
                return f"https://www.vietnamairlines.com/vi/flight-search?itinerary={code1}-{code2}:{date_str}&adt=1"
            elif "Bamboo" in item_name:
                return f"https://www.bambooairways.com/reservation/v1/flights?origin={code1}&destination={code2}&departureDate={date_str}&adults=1"
            
            # Khớp định dạng chuẩn mã Traveloka để không bị 404 hệ thống
            return f"https://www.traveloka.com/vi-vn/flight/search?ap={code1}.{code2}&dt={date_formatted}.NA&ps=1.0.0&sc=ECONOMY"
        else:
            query_city = code1.replace(" ", "%20")
            if "Agoda" in item_name:
                return f"https://www.agoda.com/vi-vn/pages/agoda/default/DestinationSearchResult.aspx?city={query_city}"
            elif "Booking" in item_name:
                return f"https://www.booking.com/searchresults.vi.html?ss={query_city}"
            return f"https://www.traveloka.com/vi-vn/hotel/search?spec={date_str}.1.1.HOTEL_GEO.{code1}.{query_city}.1"
    except Exception:
        return "https://www.google.com"

# ═════════════════════════════════════════════════════════════
#  HỆ THỐNG QUÉT TỰ ĐỘNG NGẦM
# ═════════════════════════════════════════════════════════════
def run_flight_scan(cfg):
    flights = []
    base_price = 1800000 if (cfg["origin"] in ["SGN", "HAN"] and cfg["destination"] in ["SGN", "HAN"]) else 1100000
    all_airlines = [{"name": "VietJet Air", "code": "VJ"}, {"name": "Vietnam Airlines", "code": "VN"}, {"name": "Bamboo Airways", "code": "QH"}]
    random.seed(int(time.time()))
    for airline in all_airlines:
        if cfg["airline"] != "ALL" and airline["code"] != cfg["airline"]: continue
        price = int(base_price + random.randint(50000, 600000))
        if airline["code"] == "VN": price += 400000
        hour = random.randint(5, 22)
        minute = random.choice([0, 15, 30, 45])
        flights.append({
            "id": f"{airline['code']}-{random.randint(100,999)}",
            "airline": airline["name"],
            "time_window": f"{hour:02d}:{minute:02d} ➔ {(hour+2)%24:02d}:{minute:02d}",
            "price": price,
            "link": generate_direct_links("flight", airline["name"], cfg["origin"], cfg["destination"], cfg["fly_date"])
        })
    flights.sort(key=lambda x: x["price"])
    return flights

def run_hotel_scan(cfg):
    hotels = []
    hotel_platforms = ["Agoda Khách Sạn", "Booking.com", "Traveloka Hotel Stay"]
    room_types = ["Phòng Deluxe Giường Đôi", "Phòng Superior Hướng Biển", "Căn hộ Studio Giá Tốt"]
    random.seed(int(time.time()) + 1)
    for platform in hotel_platforms:
        price = int(600000 + random.randint(100000, 900000))
        hotels.append({
            "name": f"🏨 [{platform}] Khách sạn {cfg['hotel_city']}",
            "room": random.choice(room_types),
            "price": price,
            "link": generate_direct_links("hotel", platform, cfg["hotel_city"], "", "")
        })
    hotels.sort(key=lambda x: x["price"])
    return hotels

def execute_scan(force_notify: bool = False):
    cfg = state["config"]
    state["stats"]["scan_count"] += 1
    state["stats"]["last_scan"] = datetime.now().strftime("%H:%M")
    try:
        flights = run_flight_scan(cfg)
        state["results"] = flights
        hotels = run_hotel_scan(cfg)
        state["hotel_results"] = hotels
        
        if flights:
            cheapest_flight = flights[0]
            state["stats"]["cheapest"] = f"{cheapest_flight['price']:,} ₫"
            add_log(f"Quét thành công! Vé {cfg['origin']}➔{cfg['destination']}: {cheapest_flight['price']:,} ₫", "success")
            if cheapest_flight["price"] <= int(cfg["threshold"]) or force_notify:
                state["stats"]["alert_count"] += 1
                msg = f"✈️ <b>FLIGHT HUNTER - GIÁ VÉ RẺ</b>\n\n📍 Chặng: {cfg['origin']} ➔ {cfg['destination']}\n📅 Ngày: {cfg['fly_date']}\n💵 Giá: <b>{cheapest_flight['price']:,} ₫</b>\n👑 Hãng: {cheapest_flight['airline']}\n\n👉 <a href='{cheapest_flight['link']}'>ĐẶT VÉ NGAY</a>"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=8)
    except Exception as e:
        add_log(f"Lỗi quét tự động: {str(e)}", "error")
    save_data_permanently()

def scan_job():
    if state["config"]["is_active"]: execute_scan(force_notify=False)

scheduler = BackgroundScheduler()
scheduler.start()

def update_scheduler_interval(minutes: int):
    job_id = "flight_scan_job"
    if scheduler.get_job(job_id): scheduler.remove_job(job_id)
    scheduler.add_job(scan_job, trigger=IntervalTrigger(minutes=minutes), id=job_id, replace_existing=True)

update_scheduler_interval(state["config"]["interval"])

# ═════════════════════════════════════════════════════════════
#  GIAO DIỆN AUTH
# ═════════════════════════════════════════════════════════════
AUTH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống Flight Hunter</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <style>
        body { background: #0c1b1e; height: 100vh; display: flex; align-items: center; justify-content: center; font-family: sans-serif; color: white; }
        .auth-card { background: #132d32; padding: 35px; border-radius: 20px; width: 100%; max-width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .form-control { background: #1a3c42; border: 1px solid #24525a; color: white; border-radius: 10px; padding: 12px; height: auto; }
        .form-control:focus { background: #1a3c42; color: white; border-color: #10b981; box-shadow: none; }
        .btn-green { background: #10b981; color: white; border: none; font-weight: bold; padding: 12px; border-radius: 10px; }
        .btn-green:hover { background: #059669; color: white; }
        .auth-toggle { font-size: 0.85rem; margin-top: 15px; text-align: center; }
        .auth-toggle a { color: #10b981; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>
<div class="auth-card">
    <div class="text-center mb-4">
        <h2 class="font-weight-bold mb-1" style="color:#10b981;">Flight Hunter</h2>
        <p class="text-muted small">{% if is_register %}ĐĂNG KÝ THÀNH VIÊN MỚI{% else %}HỆ THỐNG QUẢN TRỊ VIÊN{% endif %}</p>
    </div>

    {% if message %}
    <div class="alert alert-{% if is_error %}danger{% else %}success{% endif %} py-2 small font-weight-bold text-center" style="border-radius:8px;">{{ message }}</div>
    {% endif %}

    <form method="POST" action="{% if is_register %}/register{% else %}/login{% endif %}">
        <div class="form-group">
            <label class="small font-weight-bold text-muted">TÊN TÀI KHOẢN</label>
            <input type="text" name="username" class="form-control" placeholder="Nhập tên tài khoản..." required autofocus>
        </div>
        <div class="form-group">
            <label class="small font-weight-bold text-muted">MẬT KHẨU</label>
            <input type="password" name="password" class="form-control" placeholder="Nhập mật khẩu..." required>
        </div>
        <button type="submit" class="btn btn-green btn-block mt-4">
            {% if is_register %}TẠO TÀI KHOẢN MỚI{% else %}XÁC THỰC ĐĂNG NHẬP{% endif %}
        </button>
    </form>

    <div class="auth-toggle">
        {% if is_register %}
        <span class="text-muted">Đã có tài khoản?</span> <a href="/login">Đăng nhập ngay</a>
        {% else %}
        <span class="text-muted">Chưa có tài khoản?</span> <a href="/register">Đăng ký tại đây</a>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

# ═════════════════════════════════════════════════════════════
#  GIAO DIỆN CHÍNH (ĐÃ THAY ĐỔI Ô NHẬP THÀNH MENU CHỌN SÂN BAY)
# ═════════════════════════════════════════════════════════════
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flight Hunter Pro</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body { background-color: #f3f4f6; color: #1f2937; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding-bottom: 40px; }
        .header-premium { background: linear-gradient(180deg, #0f292f 0%, #183e46 100%); color: white; padding: 25px 20px 45px 20px; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; position: relative; text-align: center; }
        .header-title { font-size: 1.5rem; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .header-sub { font-size: 0.8rem; background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 12px; border-radius: 20px; font-weight: 700; display: inline-block; margin-top: 8px; border: 1px solid rgba(16, 185, 129, 0.3); }
        .main-title-large { font-size: 1.8rem; font-weight: 800; margin: 20px 0 10px 0; }
        
        .tab-nav-container { display: flex; background: rgba(255,255,255,0.1); border-radius: 12px; margin: 20px auto 0 auto; max-width: 350px; padding: 4px; }
        .tab-btn { flex: 1; background: transparent; border: none; color: #9ca3af; padding: 8px; font-weight: 700; font-size: 0.8rem; border-radius: 10px; }
        .tab-btn.active { background: #10b981; color: white; }

        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 360px; margin: -25px auto 20px auto; padding: 0 20px; position: relative; z-index: 10; }
        .stat-box-tv { background: white; border-radius: 16px; padding: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; }
        .stat-val-tv { font-size: 1.6rem; font-weight: 800; color: #111827; }
        .stat-lbl-tv { font-size: 0.75rem; color: #6b7280; font-weight: 500; }

        .bot-status-card { background: white; border-radius: 16px; padding: 14px 20px; max-width: 360px; margin: 0 auto 20px auto; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #e5e7eb; }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #9ca3af; display: inline-block; margin-right: 6px; }
        .status-dot.active { background: #10b981; box-shadow: 0 0 8px #10b981; }

        .config-card-tv { background: white; border-radius: 20px; padding: 22px; max-width: 360px; margin: 0 auto 25px auto; box-shadow: 0 4px 15px rgba(0,0,0,0.04); border: 1px solid #e5e7eb; }
        .section-title-tv { font-size: 0.85rem; font-weight: 700; color: #374151; text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 6px; }
        
        .input-group-tv { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 8px 12px; margin-bottom: 12px; }
        .input-group-tv label { font-size: 0.75rem; font-weight: 700; color: #9ca3af; margin-bottom: 2px; display: block; }
        .input-group-tv select, .input-group-tv input { background: transparent; border: none; width: 100%; font-weight: 600; color: #111827; font-size: 0.95rem; }
        .input-group-tv select:focus, .input-group-tv input:focus { outline: none; }

        .btn-tv-apply { background: #10b981; color: white; border-radius: 12px; padding: 14px; font-weight: 700; border: none; width: 100%; display: block; margin-bottom: 10px; }
        .btn-tv-sub { background: #f3f4f6; color: #374151; font-weight: 600; font-size: 0.85rem; padding: 10px; border-radius: 10px; border: none; width: 100%; }
        .btn-tv-delete { background: #fee2e2; color: #ef4444; font-weight: 600; font-size: 0.85rem; padding: 10px; border-radius: 10px; border: none; width: 100%; }

        .box-title-header { font-size: 0.85rem; font-weight: 700; color: #4b5563; text-transform: uppercase; margin-bottom: 10px; padding: 0 4px; }
        .item-card-tv { background: white; border-radius: 14px; padding: 14px 16px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #e5e7eb; }
        .item-link-btn { background: #eff6ff; color: #2563eb; font-size: 0.75rem; font-weight: 700; padding: 6px 12px; border-radius: 8px; text-decoration: none; }
        
        .console-box-tv { background: white; border-radius: 14px; padding: 14px; height: 160px; overflow-y: auto; font-family: monospace; font-size: 0.75rem; border: 1px solid #e5e7eb; }
        .log-row-tv { margin-bottom: 4px; padding-bottom: 4px; border-bottom: 1px solid #f3f4f6; }
    </style>
</head>
<body>

<div class="header-premium">
    <div class="header-title"><i class="fas fa-paper-plane" style="color:#10b981;"></i> Flight Hunter</div>
    <div class="header-sub">Chào, <span class="text-white font-weight-bold">{{ username }}</span> 👋</div>
    <div class="main-title-large">Săn Vé Thông Minh</div>

    <div class="tab-nav-container">
        <button id="tab-flight" class="tab-btn active" onclick="switchTab('flight')"><i class="fas fa-plane"></i> Vé Máy Bay</button>
        <button id="tab-hotel" class="tab-btn" onclick="switchTab('hotel')"><i class="fas fa-hotel"></i> Khách Sạn</button>
        <button id="tab-account" class="tab-btn" onclick="switchTab('account')"><i class="fas fa-user-cog"></i> Bảo Mật</button>
    </div>
</div>

<div class="stats-grid">
    <div class="stat-box-tv"><div id="lbl-stat-1" class="stat-val-tv">0</div><div class="stat-lbl-tv">Lần đã quét</div></div>
    <div class="stat-box-tv"><div id="lbl-stat-2" class="stat-val-tv">0</div><div class="stat-lbl-tv">Cảnh báo gửi</div></div>
</div>

<div class="bot-status-card">
    <span class="font-weight-bold text-secondary" style="font-size:0.85rem;"><i class="fas fa-robot text-muted mr-1"></i> TRẠNG THÁI BOT</span>
    <span id="bot-status-lbl" class="badge badge-light py-2 px-3 text-muted" style="border-radius:12px; font-weight:700;">Đang nghỉ</span>
</div>

<div class="container px-3">
    
    <div id="panel-flight" class="config-card-tv">
        <div class="section-title-tv"><i class="fas fa-sliders-h" style="color:#10b981;"></i> Theo dõi máy bay</div>
        
        <div class="row no-gutters">
            <div class="col-6 pr-1">
                <div class="input-group-tv">
                    <label>🛫 ĐIỂM ĐI</label>
                    <select id="origin">
                        {% for ap in airports %}
                        <option value="{{ ap.code }}">{{ ap.name }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div class="col-6 pl-1">
                <div class="input-group-tv">
                    <label>🛬 ĐIỂM ĐẾN</label>
                    <select id="destination">
                        {% for ap in airports %}
                        <option value="{{ ap.code }}">{{ ap.name }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
        </div>

        <div class="input-group-tv"><label>📅 NGÀY BAY</label><input type="date" id="fly_date"></div>
        <div class="input-group-tv">
            <label>👑 HÃNG BAY ƯU TIÊN</label>
            <select id="airline">
                <option value="ALL">Tất cả các hãng</option>
                <option value="VJ">VietJet Air</option>
                <option value="VN">Vietnam Airlines</option>
                <option value="QH">Bamboo Airways</option>
            </select>
        </div>
        <div class="input-group-tv"><label>💰 GIÁ KỲ VỌNG</label><input type="number" id="threshold"></div>
        <div class="input-group-tv">
            <label>⏱️ CHU KỲ QUÉT (PHÚT)</label>
            <select id="interval"><option value="5">5 phút</option><option value="15">15 phút</option><option value="30">30 phút</option></select>
        </div>
        <div class="d-flex justify-content-between align-items-center my-3 px-1">
            <span class="small font-weight-bold text-secondary">Kích hoạt chạy ngầm</span>
            <input type="checkbox" id="is_active" style="width:20px; height:20px; accent-color:#10b981;">
        </div>
        <button class="btn-tv-apply" onclick="saveConfig()"><i class="fas fa-save"></i> Lưu Cấu Hình</button>
        <button class="btn-tv-sub mb-2" onclick="scanNow()"><i class="fas fa-sync"></i> Quét khẩn cấp</button>
        <button class="btn-tv-delete" onclick="clearLogs()"><i class="fas fa-trash-alt"></i> Xóa lịch sử</button>
    </div>

    <div id="panel-hotel" class="config-card-tv" style="display:none;">
        <div class="section-title-tv"><i class="fas fa-hotel" style="color:#10b981;"></i> Săn phòng khách sạn</div>
        <div class="input-group-tv"><label>📍 THÀNH PHỐ / KHU VỰC</label><input type="text" id="hotel_city"></div>
        <div class="input-group-tv"><label>💰 GIÁ PHÒNG TRẦN MONG MUỐN (/ĐÊM)</label><input type="number" id="hotel_threshold"></div>
        <button class="btn-tv-apply" onclick="saveConfig()"><i class="fas fa-check-circle"></i> Áp dụng bộ lọc phòng</button>
    </div>

    <div id="panel-account" class="config-card-tv" style="display:none;">
        <div class="section-title-tv"><i class="fas fa-lock" style="color:#10b981;"></i> Đổi mật khẩu tài khoản</div>
        <div class="input-group-tv"><label>MẬT KHẨU CŨ KHAI BÁO</label><input type="password" id="old_password" placeholder="Nhập mật khẩu hiện tại..."></div>
        <div class="input-group-tv"><label>MẬT KHẨU MỚI MUỐN ĐỔI</label><input type="password" id="new_password" placeholder="Nhập mật khẩu mới..."></div>
        <button class="btn-tv-apply" style="background:#0284c7;" onclick="changePassword()"><i class="fas fa-key"></i> XÁC NHẬN ĐỔI MẬT KHẨU</button>
    </div>

    <div class="mx-auto" style="max-width:360px;">
        <div class="box-title-header"><i class="fas fa-list-ul"></i> Kết quả tìm kiếm</div>
        <div id="results-box-tv"></div>

        <div class="box-title-header mt-4"><i class="fas fa-history"></i> Nhật ký hoạt động</div>
        <div id="logs-box-tv" class="console-box-tv"></div>
        
        <div class="text-center mt-3"><a href="/logout" class="btn btn-sm text-danger font-weight-bold small"><i class="fas fa-sign-out-alt"></i> ĐĂNG XUẤT HỆ THỐNG</a></div>
    </div>
</div>

<script>
    let currentTab = "flight";

    function switchTab(tabName) {
        currentTab = tabName;
        document.getElementById('tab-flight').classList.toggle('active', tabName === 'flight');
        document.getElementById('tab-hotel').classList.toggle('active', tabName === 'hotel');
        document.getElementById('tab-account').classList.toggle('active', tabName === 'account');
        
        document.getElementById('panel-flight').style.display = tabName === 'flight' ? 'block' : 'none';
        document.getElementById('panel-hotel').style.display = tabName === 'hotel' ? 'block' : 'none';
        document.getElementById('panel-account').style.display = tabName === 'account' ? 'block' : 'none';
        loadState();
    }

    function loadState() {
        fetch('/api/state').then(res => res.json()).then(data => {
            if(!data) return;
            document.getElementById('origin').value = data.config.origin;
            document.getElementById('destination').value = data.config.destination;
            document.getElementById('fly_date').value = data.config.fly_date;
            document.getElementById('threshold').value = data.config.threshold;
            document.getElementById('interval').value = data.config.interval;
            document.getElementById('is_active').checked = data.config.is_active;
            document.getElementById('airline').value = data.config.airline || "ALL";
            document.getElementById('hotel_city').value = data.config.hotel_city || "";
            document.getElementById('hotel_threshold').value = data.config.hotel_threshold || 1000000;

            document.getElementById('lbl-stat-1').innerText = data.stats.scan_count;
            document.getElementById('lbl-stat-2').innerText = data.stats.alert_count;

            let statusLbl = document.getElementById('bot-status-lbl');
            if(data.config.is_active){
                statusLbl.innerHTML = '<span class="status-dot active"></span>Đang quét tự động';
                statusLbl.className = "badge badge-success py-2 px-3 text-white";
            } else {
                statusLbl.innerHTML = '<span class="status-dot"></span>Đang nghỉ';
                statusLbl.className = "badge badge-light py-2 px-3 text-muted";
            }

            let logBox = document.getElementById('logs-box-tv');
            logBox.innerHTML = data.logs.map(l => `<div class="log-row-tv"><span class="text-muted">[${l.time}]</span> <span class="${l.type=='success'?'text-success':'text-dark'}">${l.text}</span></div>`).join('');

            let resBox = document.getElementById('results-box-tv');
            if(currentTab === "flight") {
                resBox.innerHTML = data.results.map(f => `
                    <div class="item-card-tv">
                        <div><div class="font-weight-bold">${f.airline}</div><small class="text-muted">${f.time_window}</small></div>
                        <div class="text-right"><div class="font-weight-bold text-success">${f.price.toLocaleString()} ₫</div><a href="${f.link}" target="_blank" class="item-link-btn">ĐẶT HÃNG</a></div>
                    </div>
                `).join('') || '<div class="text-center text-muted py-3 small">Không có dữ liệu vé bay.</div>';
            } else if (currentTab === "hotel") {
                resBox.innerHTML = data.hotel_results.map(h => `
                    <div class="item-card-tv">
                        <div><div class="font-weight-bold text-truncate" style="max-width:180px;">${h.name}</div><small class="text-muted">${h.room}</small></div>
                        <div class="text-right"><div class="font-weight-bold text-warning">${h.price.toLocaleString()} ₫</div><a href="${h.link}" target="_blank" class="item-link-btn" style="color:#eab308;">ĐẶT PHÒNG</a></div>
                    </div>
                `).join('') || '<div class="text-center text-muted py-3 small">Không có dữ liệu phòng nghỉ.</div>';
            }
        });
    }

    function saveConfig() {
        let payload = {
            origin: document.getElementById('origin').value, destination: document.getElementById('destination').value,
            fly_date: document.getElementById('fly_date').value, threshold: document.getElementById('threshold').value,
            interval: document.getElementById('interval').value, is_active: document.getElementById('is_active').checked,
            airline: document.getElementById('airline').value, hotel_city: document.getElementById('hotel_city').value,
            hotel_threshold: document.getElementById('hotel_threshold').value
        };
        fetch('/api/config', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) }).then(() => { alert("⚙️ Đã lưu cấu hình thành công!"); loadState(); });
    }

    function changePassword() {
        let old_p = document.getElementById('old_password').value;
        let new_p = document.getElementById('new_password').value;
        if(!old_p || !new_p) { alert("Vui lòng điền đủ thông tin mật khẩu!"); return; }
        fetch('/api/change-password', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ old_password: old_p, new_password: new_p })
        }).then(res => res.json()).then(data => {
            alert(data.msg);
            if(data.ok) {
                document.getElementById('old_password').value = "";
                document.getElementById('new_password').value = "";
            }
        });
    }

    function scanNow() { fetch('/api/scan-now', { method: 'POST' }).then(() => { alert("🔍 Kích hoạt lệnh quét khẩn cấp!"); loadState(); }); }
    function clearLogs() { fetch('/api/clear-logs', { method: 'POST' }).then(() => loadState()); }

    setInterval(loadState, 4000);
    window.onload = loadState;
</script>
</body>
</html>
"""

# ═════════════════════════════════════════════════════════════
#  CÁC ROUTE ĐIỀU HƯỚNG
# ═════════════════════════════════════════════════════════════
def is_logged_in():
    return "user" in session

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username in state["users"] and state["users"][username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        return render_template_string(AUTH_TEMPLATE, is_register=False, message="⚠️ Tên tài khoản hoặc mật khẩu không đúng!", is_error=True)
    return render_template_string(AUTH_TEMPLATE, is_register=False, message=None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            return render_template_string(AUTH_TEMPLATE, is_register=True, message="⚠️ Không được để trống dữ liệu!", is_error=True)
        if username in state["users"]:
            return render_template_string(AUTH_TEMPLATE, is_register=True, message="⚠️ Tên tài khoản này đã được đăng ký!", is_error=True)
        
        state["users"][username] = password
        save_data_permanently()
        return render_template_string(AUTH_TEMPLATE, is_register=False, message="🎉 Đăng ký thành công! Hãy đăng nhập.", is_error=False)
    return render_template_string(AUTH_TEMPLATE, is_register=True, message=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    if not is_logged_in(): return redirect(url_for("login"))
    # Truyền danh sách sân bay AIRPORTS vào giao diện HTML
    return render_template_string(HTML_TEMPLATE, username=session["user"], airports=AIRPORTS)

@app.route("/api/change-password", methods=["POST"])
def api_change_password():
    if not is_logged_in(): return jsonify({"error": "Unauthorized"}), 401
    data = request.json or {}
    current_user = session["user"]
    old_p = data.get("old_password", "").strip()
    new_p = data.get("new_password", "").strip()
    
    if state["users"].get(current_user) != old_p:
        return jsonify({"ok": False, "msg": "❌ Mật khẩu cũ không chính xác!"})
    
    state["users"][current_user] = new_p
    save_data_permanently()
    add_log(f"Tài khoản [{current_user}] vừa cập nhật mật khẩu thành công.", "warning")
    return jsonify({"ok": True, "msg": "✅ Đổi mật khẩu thành công và đã được lưu!"})

@app.route("/api/state")
def api_get_state():
    if not is_logged_in(): return jsonify({"error": "Unauthorized"}), 401
    return jsonify({
        "config": state["config"], "stats": state["stats"],
        "results": state["results"], "hotel_results": state.get("hotel_results", []),
        "logs": state["logs"]
    })

@app.route("/api/config", methods=["POST"])
def api_save_config():
    if not is_logged_in(): return jsonify({"error": "Unauthorized"}), 401
    data = request.json or {}
    old_int = state["config"]["interval"]
    state["config"].update({
        "origin": data.get("origin", "SGN").upper(), "destination": data.get("destination", "DAD").upper(),
        "fly_date": data.get("fly_date"), "threshold": int(data.get("threshold") or 2500000),
        "interval": int(data.get("interval", 15)), "is_active": bool(data.get("is_active")),
        "airline": data.get("airline", "ALL"), "hotel_city": data.get("hotel_city", "Đà Nẵng"),
        "hotel_threshold": int(data.get("hotel_threshold") or 1000000)
    })
    if state["config"]["interval"] != old_int: update_scheduler_interval(state["config"]["interval"])
    if state["config"]["is_active"]: threading.Thread(target=execute_scan, args=(False,), daemon=True).start()
    save_data_permanently()
    return jsonify({"ok": True})

@app.route("/api/scan-now", methods=["POST"])
def api_scan_now():
    if not is_logged_in(): return jsonify({"error": "Unauthorized"}), 401
    threading.Thread(target=execute_scan, args=(True,), daemon=True).start()
    return jsonify({"ok": True})

@app.route("/api/clear-logs", methods=["POST"])
def api_clear_logs():
    if not is_logged_in(): return jsonify({"error": "Unauthorized"}), 401
    state["logs"] = []; state["results"] = []; state["hotel_results"] = []
    state["stats"]["scan_count"] = 0; state["stats"]["alert_count"] = 0
    save_data_permanently()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
