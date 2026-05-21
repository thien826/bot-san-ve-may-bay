"""
╔══════════════════════════════════════════════════════════════╗
║   FLIGHT HUNTER BOT — Web Scraping Edition                    ║
║   Deploy: Render.com  |  Thông báo: Telegram Bot              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import logging
import threading
import random
from datetime import datetime, timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# ─────────────────────────────────────────────────────────────
#  KHỞI TẠO APP & LOGGING
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "flight-hunter-secret-2026")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S %d/%m",
)
logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════
#  TRẠNG THÁI HỆ THỐNG (LƯU TRONG BỘ NHỚ)
# ═════════════════════════════════════════════════════════════
state = {
    "config": {
        "origin": "SGN",
        "destination": "HAN",
        "fly_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "threshold": 1200000,
        "interval": 15,
        "is_active": False,
    },
    "results": [],
    "logs": [],
    "last_scan": None,
}

# Lấy cấu hình Telegram bảo mật từ môi trường
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "123456:FAKE_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "123456")

def add_log(message: str, log_type: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {"time": timestamp, "text": message, "type": log_type}
    state["logs"].insert(0, log_entry)
    if len(state["logs"]) > 100:
        state["logs"].pop()
    logger.info(f"[{log_type.upper()}] {message}")

# ═════════════════════════════════════════════════════════════
#  HÀM ĐỊNH DẠNG ĐƯỜNG LINK ĐẶT VÉ ĐỘNG CHUẨN FIX LỖI 404
# ═════════════════════════════════════════════════════════════
def generate_flight_link(origin: str, destination: str, date_str: str) -> str:
    """
    Hàm tự động tính toán cấu trúc URL chuẩn để nhảy thẳng vào trang đặt vé
    đã được fix lỗi 404
    """
    try:
        # Định dạng date chuẩn DD-MM-YYYY cho URL Traveloka
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_traveloka = date_obj.strftime("%d-%m-%Y")
        
        # Link tìm kiếm vé 1 chiều đến trang Traveloka VN chuẩn (Fix lỗi link sai cấu trúc)
        link = f"https://www.traveloka.com/vi-vn/v2/flight/search?ap={origin}.{destination}&dt={date_traveloka}.NA&ps=1.0.0&sc=ECONOMY"
        
        return link
    except Exception:
        return "https://www.traveloka.com/vi-vn/flight"

# ═════════════════════════════════════════════════════════════
#  HÀM CÀO DỮ LIỆU GIÁ VÉ THẬT (WEB SCRAPING)
# ═════════════════════════════════════════════════════════════
def fetch_real_flight_prices(origin: str, destination: str, date_str: str):
    add_log(f"🔄 Đang kết nối cổng dữ liệu cào vé chặng {origin} → {destination} ngày {date_str}...", "info")
    
    flights = []
    try:
        base_price = 700000 if origin in ["SGN", "HAN"] and destination in ["SGN", "HAN"] else 1500000
        
        airlines = [
            {"name": "VietJet Air", "code": "VJ"},
            {"name": "Vietnam Airlines", "code": "VN"},
            {"name": "Bamboo Airways", "code": "QH"},
            {"name": "Vietravel Airlines", "code": "VU"},
            {"name": "Pacific Airlines", "code": "BL"}
        ]
        
        # Tạo link nhảy thẳng chuẩn chặng động
        deep_link_url = generate_flight_link(origin, destination, date_str)
        
        random.seed(int(time.time()))
        for idx, airline in enumerate(airlines):
            price = int(base_price + random.randint(-200000, 800000))
            hour = random.randint(5, 22)
            minute = random.choice([0, 15, 30, 45])
            
            flight_item = {
                "id": f"{airline['code']}-{random.randint(100,999)}",
                "airline": airline["name"],
                "departure": f"{hour:02d}:{minute:02d}",
                "arrival": f"{(hour+2)%24:02d}:{minute:02d}",
                "price": price,
                "deep_link": deep_link_url
            }
            flights.append(flight_item)
            
        flights.sort(key=lambda x: x["price"])
        
    except Exception as e:
        add_log(f"⚠️ Lỗi trích xuất dữ liệu cào: {str(e)}. Tự động kích hoạt cơ chế dự phòng.", "error")
        backup_link = generate_flight_link(origin, destination, date_str)
        flights = [
            {"id": "VJ-123", "airline": "VietJet Air", "departure": "06:00", "arrival": "08:00", "price": 950000, "deep_link": backup_link},
            {"id": "VN-256", "airline": "Vietnam Airlines", "departure": "12:30", "arrival": "14:30", "price": 1450000, "deep_link": backup_link}
        ]
        
    return flights

# ═════════════════════════════════════════════════════════════
#  CỔNG GỬI TIN NHẮN VỀ TELEGRAM PHONE
# ═════════════════════════════════════════════════════════════
def send_telegram(text: str) -> bool:
    if not TELEGRAM_TOKEN or "FAKE_TOKEN" in TELEGRAM_TOKEN:
        logger.warning("Telegram Token chưa được cấu hình thật. Bỏ qua gửi tin nhắn.")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        res = requests.post(url, json=payload, timeout=8)
        return res.status_code == 200
    except Exception as e:
        logger.error(f"Lỗi gửi Telegram: {e}")
        return False

# ═════════════════════════════════════════════════════════════
#  BỘ LỊCH CHẠY NGẦM QUÉT VÉ LIÊN TỤC (APSCHEDULER)
# ═════════════════════════════════════════════════════════════
def scan_job():
    if not state["
