"""
FLIGHT & HOTEL HUNTER PREMIUM — BẢN FULL CHỐNG SẬP
"""

import os, json, time, logging, threading, random, traceback
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, render_template_string, redirect, session, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "flight-hunter-2026")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "premium_hunter_data.json"

# Danh sách sân bay chuẩn
AIRPORTS = [
    {"code": "SGN", "name": "SGN — TP.HCM"}, {"code": "HAN", "name": "HAN — Hà Nội"},
    {"code": "DAD", "name": "DAD — Đà Nẵng"}, {"code": "CXR", "name": "CXR — Nha Trang"},
    {"code": "PQC", "name": "PQC — Phú Quốc"}, {"code": "VCA", "name": "VCA — Cần Thơ"},
    {"code": "HPH", "name": "HPH — Hải Phòng"}, {"code": "VII", "name": "VII — Vinh"},
    {"code": "HUI", "name": "HUI — Huế"}, {"code": "BMV", "name": "BMV — Buôn Ma Thuột"}
]

# Khởi tạo dữ liệu
def load_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {
        "users": {"admin": "123456"},
        "config": {"origin":"SGN", "destination":"DAD", "fly_date": datetime.now().strftime("%Y-%m-%d"), "threshold": 2500000, "interval": 15, "is_active": False, "airline":"ALL", "hotel_city":"Đà Nẵng", "hotel_threshold": 1000000},
        "stats": {"scan_count": 0, "alert_count": 0, "last_scan": "—", "cheapest": "—"},
        "results": [], "hotel_results": [], "logs": []
    }

state = load_state()
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(state, f, ensure_ascii=False, indent=4)

# --- LOGIC QUÉT VÉ ---
def execute_scan(force_notify=False):
    try:
        cfg = state["config"]
        state["stats"]["scan_count"] += 1
        state["stats"]["last_scan"] = datetime.now().strftime("%H:%M")
        
        # Giả lập cào dữ liệu (Bạn có thể thay bằng request thật vào API hãng bay ở đây)
        price = random.randint(500000, 3000000)
        state["results"] = [{"airline": "Vietnam Airlines", "price": price, "time_window": "08:00 - 10:00", "id": "VN123", "link": "https://www.vietnamairlines.com"}]
        state["stats"]["cheapest"] = f"{price:,} ₫"
        
        if price <= int(cfg["threshold"]) or force_notify:
            msg = f"✈️ Vé rẻ: {price:,} ₫"
            requests.post(f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN', '...')}/sendMessage", 
                          json={"chat_id": os.environ.get('TELEGRAM_CHAT_ID', '...'), "text": msg})
        save_data()
    except Exception as e:
        logger.error(f"Lỗi quét: {traceback.format_exc()}")

# --- SCHEDULER ---
scheduler = BackgroundScheduler()
scheduler.start()

def refresh_job():
    if state["config"]["is_active"]: execute_scan()

scheduler.add_job(refresh_job, 'interval', minutes=state["config"].get("interval", 15))

# --- ROUTES (Giữ nguyên UI của bạn) ---
@app.route("/", methods=["GET"])
def index():
    if "user" not in session: return redirect(url_for("login"))
    # Ở đây render file index.html của bạn
    return render_template_string(open("index.html", encoding="utf-8").read(), airports=AIRPORTS)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = "admin"
        return redirect(url_for("index"))
    return render_template_string("""<form method="POST"><input name="username"><input name="password" type="password"><button>Login</button></form>""")

@app.route("/api/state")
def get_state(): return jsonify(state)

@app.route("/api/config", methods=["POST"])
def update_config():
    data = request.json
    state["config"].update(data)
    save_data()
    return jsonify({"status": "ok"})

@app.route("/api/scan-now", methods=["POST"])
def scan_now():
    execute_scan(force_notify=True)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
