"""
╔══════════════════════════════════════════════════════════════╗
║   FLIGHT & HOTEL HUNTER PRO — Zero-Lag Reset Fix             ║
║   Sửa lỗi nuốt dữ liệu sau 2 giây & Fix chọn giao diện       ║
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

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secure-hunter-key-2026")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "premium_hunter_data.json"

AIRPORTS = [
    {"code": "SGN", "name": "SGN — TP. Hồ Chí Minh"},
    {"code": "HAN", "name": "HAN — Hà Nội"},
    {"code": "DAD", "name": "DAD — Đà Nẵng"},
    {"code": "CXR", "name": "CXR — Nha Trang"},
    {"code": "PQC", "name": "PQC — Phú Quốc"}
]

def load_saved_data():
    default_state = {
        "users": {"admin": "123456"},
        "config": {
            "origin": "SGN", "destination": "DAD",
            "fly_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "threshold": 2500000, "interval": 15, "is_active": False, "airline": "ALL",
            "hotel_city": "Đà Nẵng", "hotel_threshold": 1000000,
            "device_view": "mobile"  # Mặc định ban đầu
        },
        "stats": {"scan_count": 0, "alert_count": 0, "last_scan": "--:--", "cheapest": "-"},
        "results": [], "hotel_results": [], "logs": []
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Đảm bảo cấu trúc không trống
                for key in default_state["config"]:
                    if key not in data.get("config", {}):
                        data.setdefault("config", {})[key] = default_state["config"][key]
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

# ═════════════════════════════════════════════════════════════
#  QUÉT CHẠY NGẦM MÔ PHỎNG DỮ LIỆU
# ═════════════════════════════════════════════════════════════
def execute_scan(force_notify: bool = False):
    cfg = state["config"]
    state["stats"]["scan_count"] += 1
    state["stats"]["last_scan"] = datetime.now().strftime("%H:%M")
    
    # Giả lập kết quả vé máy bay dựa trên bộ lọc hãng
    flights = []
    airlines_pool = [
        {"name": "VietJet Air", "code": "VJ"},
        {"name": "Vietnam Airlines", "code": "VN"},
        {"name": "Bamboo Airways", "code": "QH"}
    ]
    for air in airlines_pool:
        if cfg["airline"] != "ALL" and air["code"] != cfg["airline"]:
            continue
        price = random.randint(1200000, 2800000)
        flights.append({
            "id": f"{air['code']}-{random.randint(100,999)}",
            "airline": air["name"],
            "time_window": "08:30 ➔ 10:45",
            "price": price,
            "link": "https://www.traveloka.com"
        })
    flights.sort(key=lambda x: x["price"])
    state["results"] = flights
    
    if flights and flights[0]["price"] <= int(cfg["threshold"]):
        state["stats"]["alert_count"] += 1
        
    timestamp = datetime.now().strftime("%H:%M:%S")
    state["logs"].insert(0, {"time": timestamp, "text": f"Đã quét chặng {cfg['origin']}➔{cfg['destination']}, Hãng: {cfg['airline']}, Giá trần: {cfg['threshold']:,}đ", "type": "success"})
    save_data_permanently()

def scan_job():
    if state["config"]["is_active"]: 
        execute_scan(force_notify=False)

scheduler = BackgroundScheduler()
scheduler.start()

def update_scheduler_interval(minutes: int):
    job_id = "flight_scan_job"
    if scheduler.get_job(job_id): scheduler.remove_job(job_id)
    scheduler.add_job(scan_job, trigger=IntervalTrigger(minutes=minutes), id=job_id, replace_existing=True)

update_scheduler_interval(state["config"]["interval"])

# ═════════════════════════════════════════════════════════════
#  GIAO DIỆN PHẲNG CHUẨN - LIÊN THÔNG THIẾT BỊ
# ═════════════════════════════════════════════════════════════
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Hunter Pro Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body { background-color: #f4f6f9; color: #333; font-family: system-ui, -apple-system, sans-serif; }
        
        /* Chuyển đổi giao diện thông minh */
        .device-selector-bar { background: #fff; padding: 12px 20px; border-bottom: 2px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .view-btn { padding: 6px 16px; border-radius: 20px; border: 1px solid #cbd5e1; font-weight: 600; font-size: 0.85rem; background: #fff; color: #64748b; cursor: pointer; }
        .view-btn.active { background: #0f172a; color: #fff; border-color: #0f172a; }

        /* Container động dựa trên cấu hình người chọn */
        .dynamic-container { margin: 20px auto; padding: 0 15px; transition: all 0.3s ease; }
        
        /* Định dạng ép dáng Điện thoại */
        .mode-mobile { max-width: 430px; border: 8px solid #1e293b; border-radius: 36px; background: #f8fafc; padding: 15px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); min-height: 800px; }
        /* Định dạng ép dáng Máy tính Laptop rộng rãi */
        .mode-laptop { max-width: 1200px; display: grid; grid-template-columns: 5fr 7fr; gap: 20px; }

        .widget-box { background: white; border-radius: 16px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .widget-title { font-size: 0.85rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;}
        
        .custom-input { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 10px; width: 100%; font-weight: 600; color: #1e293b; font-size: 0.9rem; margin-bottom: 12px; }
        .custom-input:focus { border-color: #10b981; outline: none; background: #fff; }
        label { font-size: 0.75rem; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block; }

        .btn-action { background: #10b981; color: white; border-radius: 10px; padding: 12px; font-weight: 700; border: none; width: 100%; margin-top: 5px; cursor: pointer; }
        .btn-action:hover { background: #059669; }
        
        .btn-secondary-tv { background: #e2e8f0; color: #334155; font-weight: 600; font-size: 0.85rem; padding: 10px; border-radius: 8px; border: none; width: 100%; margin-top: 8px; }
        
        .badge-status { padding: 6px 12px; border-radius: 12px; font-weight: 700; font-size: 0.75rem; }
        .log-line { font-family: monospace; font-size: 0.75rem; padding: 6px 0; border-bottom: 1px solid #f1f5f9; color: #334155; }
        
        /* Ẩn các class phụ thuộc màn hình laptop khi ở chế độ mobile */
        .mode-mobile .laptop-only { display: none; }
    </style>
</head>
<body>

<div class="device-selector-bar">
    <div>
        <span class="font-weight-bold" style="color:#0f172a;"><i class="fas fa-layer-group"></i> CHẾ ĐỘ HIỂN THỊ:</span>
    </div>
    <div class="btn-group">
        <button id="btn-view-mobile" class="view-btn" onclick="toggleDeviceMode('mobile')"><i class="fas fa-mobile-alt"></i> Điện Thoại (Mobile)</button>
        <button id="btn-view-laptop" class="view-btn" onclick="toggleDeviceMode('laptop')"><i class="fas fa-laptop"></i> Máy Tính (Laptop)</button>
    </div>
</div>

<div class="text-center mt-3">
    <h4 class="font-weight-bold text-dark mb-0">✈️ Flight Hunter Pro Panel</h4>
    <small class="text-muted">Đang phân giải cấu hình chống trùng lặp thông số</small>
</div>

<div id="main-layout-container" class="dynamic-container">
    
    <div class="widget-box">
        <div class="widget-title"><i class="fas fa-cog"></i> Cấu hình săn vé mục tiêu</div>
        
        <div class="row">
            <div class="col-6">
                <label>✈️ ĐIỂM ĐI (IATA)</label>
                <select id="origin" class="custom-input">
                    {% for ap in airports %}
                    <option value="{{ ap.code }}">{{ ap.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-6">
                <label>🛬 ĐIỂM ĐẾN (IATA)</label>
                <select id="destination" class="custom-input">
                    {% for ap in airports %}
                    <option value="{{ ap.code }}">{{ ap.name }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>

        <label>📅 NGÀY KHỞI HÀNH</label>
        <input type="date" id="fly_date" class="custom-input">

        <label>👑 HÃNG BAY ƯU TIÊN</label>
        <select id="airline" class="custom-input">
            <option value="ALL">Tất cả các hãng hàng không</option>
            <option value="VJ">VietJet Air</option>
            <option value="VN">Vietnam Airlines</option>
            <option value="QH">Bamboo Airways</option>
        </select>

        <label>💰 GIÁ TRẦN KỲ VỌNG (VNĐ)</label>
        <input type="number" id="threshold" class="custom-input" placeholder="Ví dụ: 2500000">

        <label>⏱️ CHU KỲ TỰ ĐỘNG QUÉT</label>
        <select id="interval" class="custom-input">
            <option value="5">Quét mỗi 5 phút</option>
            <option value="15">Quét mỗi 15 phút</option>
            <option value="30">Quét mỗi 30 phút</option>
        </select>

        <div class="d-flex justify-content-between align-items-center p-2 mb-3 style-toggle" style="background:#f8fafc; border-radius:10px;">
            <span class="small font-weight-bold text-secondary">Kích hoạt tiến trình chạy ngầm</span>
            <input type="checkbox" id="is_active" style="width:22px; height:22px; accent-color:#10b981; cursor:pointer;">
        </div>

        <button class="btn-action" onclick="forceSaveConfig()"><i class="fas fa-save"></i> 💾 Lưu & Áp Dụng Ngay</button>
        <button class="btn-secondary-tv" style="background:#e0f2fe; color:#0369a1;" onclick="triggerScanUrgent()"><i class="fas fa-bolt"></i> Ép Quét Khẩn Cấp</button>
    </div>

    <div class="widget-box">
        <div class="widget-title"><i class="fas fa-list-alt"></i> Kết quả tìm kiếm & Nhật ký</div>
        
        <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="small font-weight-bold">Trạng thái Bot:</span>
            <span id="bot-status-badge" class="badge-status bg-secondary text-white">Đang tải...</span>
        </div>

        <div class="row text-center mb-3">
            <div class="col-6" style="border-right: 1px solid #f1f5f9;">
                <div class="h5 font-weight-bold text-dark mb-0" id="stat-scan">0</div>
                <small class="text-muted">Lần quét</small>
            </div>
            <div class="col-6">
                <div class="h5 font-weight-bold text-danger mb-0" id="stat-alert">0</div>
                <small class="text-muted">Cảnh báo</small>
            </div>
        </div>

        <label>📬 VÉ RẺ NHẤT TÌM THẤY</label>
        <div id="results-render-box" class="mb-3"></div>

        <label>📜 NHẬT KÝ ĐỒNG BỘ</label>
        <div id="logs-render-box" style="max-height: 150px; overflow-y: auto; background: #fafafa; padding: 10px; border-radius: 8px;"></div>
    </div>

</div>

<script>
    let isSaving = false; // Chặn luồng setInterval nạp đè dữ liệu cũ khi đang thao tác lưu

    function toggleDeviceMode(mode) {
        let container = document.getElementById('main-layout-container');
        document.getElementById('btn-view-mobile').classList.toggle('active', mode === 'mobile');
        document.getElementById('btn-view-laptop').classList.toggle('active', mode === 'laptop');
        
        if(mode === 'mobile') {
            container.className = "dynamic-container mode-mobile";
        } else {
            container.className = "dynamic-container mode-laptop";
        }
        
        // Lưu lựa chọn thiết bị lên máy chủ để giữ trạng thái
        fetch('/api/set-device', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ device_view: mode })
        });
    }

    function loadServerState() {
        if (isSaving) return; // Nếu đang lưu cấu hình, không nạp đè dữ liệu cũ
        
        fetch('/api/state').then(res => res.json()).then(data => {
            if(!data) return;
            
            // Đồng bộ dữ liệu lên ô nhập liệu
            document.getElementById('origin').value = data.config.origin;
            document.getElementById('destination').value = data.config.destination;
            document.getElementById('fly_date').value = data.config.fly_date;
            document.getElementById('airline').value = data.config.airline;
            document.getElementById('threshold').value = data.config.threshold;
            document.getElementById('interval').value = data.config.interval;
            document.getElementById('is_active').checked = data.config.is_active;

            // Thống kê nhanh
            document.getElementById('stat-scan').innerText = data.stats.scan_count;
            document.getElementById('stat-alert').innerText = data.stats.alert_count;

            // Huy hiệu trạng thái
            let badge = document.getElementById('bot-status-badge');
            if (data.config.is_active) {
                badge.innerText = "ĐANG QUÉT NGẦM";
                badge.className = "badge-status bg-success text-white";
            } else {
                badge.innerText = "ĐANG TẠM NGHỈ";
                badge.className = "badge-status bg-secondary text-white";
            }

            // Render danh sách vé
            let resBox = document.getElementById('results-render-box');
            if(data.results && data.results.length > 0) {
                resBox.innerHTML = data.results.map(f => `
                    <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:10px; border-radius:8px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                        <div><strong>${f.airline}</strong><br><small class="text-muted">${f.time_window}</small></div>
                        <div class="text-right"><span class="text-success font-weight-bold">${f.price.toLocaleString()}đ</span></div>
                    </div>
                `).join('');
            } else {
                resBox.innerHTML = '<div class="text-center text-muted small py-2">Chưa có kết quả vé phù hợp tiêu chí.</div>';
            }

            // Render logs lịch sử
            let logBox = document.getElementById('logs-render-box');
            logBox.innerHTML = data.logs.map(l => `<div class="log-line"><span class="text-muted">[${l.time}]</span> ${l.text}</div>`).join('');
        });
    }

    function forceSaveConfig() {
        isSaving = true; // Khóa tạm thời luồng kéo dữ liệu tự động
        
        let payload = {
            origin: document.getElementById('origin').value,
            destination: document.getElementById('destination').value,
            fly_date: document.getElementById('fly_date').value,
            airline: document.getElementById('airline').value,
            threshold: parseInt(document.getElementById('threshold').value) || 2500000,
            interval: parseInt(document.getElementById('interval').value) || 15,
            is_active: document.getElementById('is_active').checked
        };

        fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if(data.ok) {
                alert("✨ Cấu hình đã được lưu vĩnh viễn không bị reset!");
            }
            isSaving = false; // Mở khóa luồng
            loadServerState();
        })
        .catch(err => {
            isSaving = false;
            alert("Lỗi kết nối máy chủ khi lưu.");
        });
    }

    function triggerScanUrgent() {
        fetch('/api/scan-now', { method: 'POST' }).then(() => {
            alert("🔍 Đã gửi lệnh quét cưỡng bức!");
            loadServerState();
        });
    }

    // Khởi tạo ban đầu khi mở trang
    window.onload = function() {
        fetch('/api/state').then(res => res.json()).then(data => {
            let initialView = data.config.device_view || "mobile";
            toggleDeviceMode(initialView);
            loadServerState();
            // Thiết lập vòng quét tải lại giao diện định kỳ an toàn
            setInterval(loadServerState, 4000); 
        });
    };
</script>
</body>
</html>
"""

# ═════════════════════════════════════════════════════════════
#  CONTROLLER API ENDPOINTS
# ═════════════════════════════════════════════════════════════
@app.route("/")
def index():
    if "user" not in session: session["user"] = "admin"
    return render_template_string(HTML_TEMPLATE, airports=AIRPORTS)

@app.route("/api/state")
def api_get_state():
    return jsonify({
        "config": state["config"], "stats": state["stats"],
        "results": state["results"], "logs": state["logs"]
    })

@app.route("/api/set-device", methods=["POST"])
def api_set_device():
    data = request.json or {}
    state["config"]["device_view"] = data.get("device_view", "mobile")
    save_data_permanently()
    return jsonify({"ok": True})

@app.route("/api/config", methods=["POST"])
def api_save_config():
    data = request.json or {}
    old_int = state["config"]["interval"]
    
    # Ép kiểu an toàn, chống rỗng dữ liệu gây lỗi hồi đáp
    state["config"].update({
        "origin": str(data.get("origin", "SGN")),
        "destination": str(data.get("destination", "DAD")),
        "fly_date": str(data.get("fly_date")),
        "airline": str(data.get("airline", "ALL")),
        "threshold": int(data.get("threshold") or 2500000),
        "interval": int(data.get("interval" or 15)),
        "is_active": bool(data.get("is_active"))
    })
    
    if state["config"]["interval"] != old_int: 
        update_scheduler_interval(state["config"]["interval"])
        
    save_data_permanently()
    
    # Thực thi một tiến trình quét lập tức nếu kích hoạt bật
    if state["config"]["is_active"]:
        threading.Thread(target=execute_scan, args=(False,), daemon=True).start()
        
    return jsonify({"ok": True})

@app.route("/api/scan-now", methods=["POST"])
def api_scan_now():
    threading.Thread(target=execute_scan, args=(True,), daemon=True).start()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
