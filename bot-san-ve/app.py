import os, json, time, logging, threading, random
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, render_template, redirect, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "flighthunter-pro-2026-secret")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "fh_data.json"

# ─── DATA ───
DOMESTIC_AIRPORTS = [
    {"code":"SGN","name_vi":"SGN — TP. Hồ Chí Minh","name_en":"SGN — Ho Chi Minh City"},
    {"code":"HAN","name_vi":"HAN — Hà Nội","name_en":"HAN — Hanoi"},
    {"code":"DAD","name_vi":"DAD — Đà Nẵng","name_en":"DAD — Da Nang"}
]
AIRLINES = [
    {"code":"ALL","name_vi":"Tất cả hãng bay","name_en":"All Airlines","logo":"✈"},
    {"code":"VJ","name_vi":"VietJet Air","name_en":"VietJet Air","logo":"🔴"},
    {"code":"VN","name_vi":"Vietnam Airlines","name_en":"Vietnam Airlines","logo":"🟡"},
]
TRIP_SUGGESTIONS = [
    {"from":"SGN","to":"DAD","price":890000,"label_vi":"Đà Nẵng - Hội An","label_en":"Da Nang - Hoi An","img":"🌊","desc_vi":"Biển xanh, phố cổ, ẩm thực tuyệt vời","desc_en":"Blue sea, ancient town, amazing cuisine"},
    {"from":"HAN","to":"PQC","price":1200000,"label_vi":"Phú Quốc - Đảo Ngọc","label_en":"Phu Quoc - Pearl Island","img":"🏝","desc_vi":"Thiên đường nhiệt đới, snorkeling tuyệt đỉnh","desc_en":"Tropical paradise, top snorkeling"}
]
HOTELS = [
    {"name":"Vinpearl Resort & Spa","city_vi":"Nha Trang","city_en":"Nha Trang","stars":5,"price":2800000,"img":"🏨","tag_vi":"Nghỉ dưỡng","tag_en":"Resort"}
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
    airlines_pool = [a for a in AIRLINES[1:] if cfg["airline"]=="ALL" or a["code"]==cfg["airline"]]
    if not airlines_pool: airlines_pool = AIRLINES[1:4]
    random.seed(int(time.time()))
    for a in airlines_pool[:5]:
        price = int(base + random.randint(100000, base*0.6))
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
            if c["price"]<=int(cfg["threshold"]) or force:
                state["stats"]["alert_count"]+=1
                msg=f"✈️ FLIGHT HUNTER\n📍 {cfg['origin']}→{cfg['destination']}\n💵 {c['price']:,} ₫\n👉 {c['link']}"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",json={"chat_id":TELEGRAM_CHAT_ID,"text":msg},timeout=8)
    except Exception as e: add_log(f"Lỗi: {e}","error")
    save_data()

# ════════════════════════════════════════════════
# FLASK ROUTES
# ════════════════════════════════════════════════

@app.route("/")
def index():
    # Sử dụng render_template để nạp file index.html từ thư mục templates/
    return render_template("index.html", trips=TRIP_SUGGESTIONS, airlines=AIRLINES, hotels=HOTELS)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", session=session, config=state["config"], stats=state["stats"], results=state["results"])

@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.json
    action = data.get("action")
    user = data.get("username", "").strip()
    pwd = data.get("password", "").strip()
    
    if action == "login":
        if user in state["users"] and state["users"][user]["password"] == pwd:
            session["user"] = user
            return jsonify({"status": "ok"})
        return jsonify({"status": "error", "msg": "Sai tài khoản hoặc mật khẩu!"})
        
    elif action == "register":
        if not user or not pwd:
            return jsonify({"status": "error", "msg": "Vui lòng nhập đủ thông tin!"})
        if user in state["users"]:
            return jsonify({"status": "error", "msg": "Tên đăng nhập đã tồn tại!"})
            
        state["users"][user] = {"password": pwd, "email": ""}
        save_data()
        session["user"] = user
        return jsonify({"status": "ok"})
        
    return jsonify({"status": "error", "msg": "Hành động không hợp lệ"})

@app.route("/api/toggle", methods=["POST"])
def toggle():
    if "user" in session:
        state["config"]["is_active"] = not state["config"]["is_active"]
        save_data()
        if state["config"]["is_active"]:
            threading.Thread(target=execute_scan).start()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    def background_scanner():
        while True:
            try:
                if state["config"].get("is_active"):
                    execute_scan()
            except Exception as e:
                logger.error(f"Scanner error: {e}")
            time.sleep(state["config"].get("interval", 15) * 60)

    scanner_thread = threading.Thread(target=background_scanner, daemon=True)
    scanner_thread.start()
    
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
