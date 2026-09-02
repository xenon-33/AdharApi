# -*- coding: utf-8 -*-
"""
XENON OSINT API - All-in-One
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Developer: @Xenon33cyber
Team: @xenondaemon_Team
Support: @xenondaemon
Channel: https://t.me/xenondaemon
Version: 3.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import requests
import time
import re
from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import logging

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# APP INIT
# ============================================================
app = Flask(__name__)
CORS(app)

# ============================================================
# CHANNEL NAMES - CREDITS
# ============================================================
CHANNELS = [
    "@Xenon33cyber",
    "@xenondaemon",
    "@xenondaemon_Team"
]

DEVELOPER = "@Xenon33cyber"
TEAM = "@xenondaemon_Team"
SUPPORT = "@xenondaemon"
CHANNEL_LINK = "https://t.me/xenondaemon"
VERSION = "3.0.0"

CREDITS = {
    "developer": DEVELOPER,
    "team": TEAM,
    "support": SUPPORT,
    "channel": CHANNEL_LINK,
    "channels": CHANNELS,
    "version": VERSION
}

# ============================================================
# CONFIGURATION
# ============================================================
API_KEY = os.getenv('API_KEY', '69d')
API_BASE = "https://osint.invalidayushh.workers.dev"
REQUEST_TIMEOUT = 30
RATE_LIMIT = 60

# ============================================================
# RATE LIMITING
# ============================================================
request_history = {}

def check_rate_limit(ip):
    current_time = time.time()
    if ip in request_history:
        request_history[ip] = [t for t in request_history[ip] if current_time - t < 60]
        if len(request_history[ip]) >= RATE_LIMIT:
            return False
    else:
        request_history[ip] = []
    request_history[ip].append(current_time)
    return True

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def fetch_data(endpoint, query, api_key=API_KEY):
    try:
        url = f"{API_BASE}/{endpoint}?key={api_key}&q={query}"
        logger.info(f"Fetching: {endpoint} for {query}")
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": f"HTTP {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON response"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def make_response(data, title, query, status=200):
    response = {
        "status": "success" if status == 200 else "error",
        "title": title,
        "query": query,
        "data": data,
        "timestamp": datetime.now().isoformat(),
        **CREDITS
    }
    return Response(
        json.dumps(response, ensure_ascii=False, indent=4),
        status=status,
        content_type='application/json; charset=utf-8'
    )

def error_response(message, query=None, status=400):
    response = {
        "status": "error",
        "message": message,
        "query": query,
        "timestamp": datetime.now().isoformat(),
        **CREDITS
    }
    return Response(
        json.dumps(response, ensure_ascii=False, indent=4),
        status=status,
        content_type='application/json; charset=utf-8'
    )

def clean_address(addr):
    if not addr or addr == "0":
        return "N/A"
    return addr.replace("!", ", ")

# ============================================================
# ============================================================
# API ENDPOINTS
# ============================================================
# ============================================================

# ---------- HOME ----------
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "XENON OSINT API - All-in-One",
        "version": VERSION,
        "status": "online",
        **CREDITS,
        "endpoints": {
            "/api/adhar": "Aadhaar Lookup",
            "/api/family": "Family Info Lookup",
            "/api/ff": "Free Fire Profile",
            "/api/fflike": "Free Fire Like",
            "/api/ffvisit": "Free Fire Visit",
            "/api/ifsc": "IFSC Code Lookup",
            "/api/instagram": "Instagram Profile",
            "/api/instagramv2": "Instagram Profile v2",
            "/api/number": "Number Lookup",
            "/api/numberv2": "Number Lookup v2",
            "/api/pakistan": "Pakistan Number Lookup",
            "/api/telegram": "Telegram ID Lookup",
            "/api/tgusername": "Telegram Username to ID",
            "/api/vehicle": "Vehicle Number Lookup",
            "/api/icmr": "ICMR Data Search",
            "/api/health": "Health Check"
        }
    })

# ---------- HEALTH ----------
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "XENON OSINT API",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        **CREDITS
    })

# ---------- STATS ----------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_requests = sum(len(v) for v in request_history.values())
    return jsonify({
        "total_requests_last_minute": total_requests,
        "rate_limit": RATE_LIMIT,
        "active_ips": len(request_history),
        **CREDITS
    })

# ============================================================
# 1. AADHAAR LOOKUP
# ============================================================
@app.route('/api/adhar', methods=['GET'])
def adhar_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded. Max 60 requests per minute.", status=429)
    
    query = request.args.get('q') or request.args.get('number')
    if not query:
        return error_response("Missing query parameter. Use ?q=123456789012")
    
    raw = fetch_data("adhar", query)
    
    if not raw.get("Success", False):
        return error_response(raw.get("message", "No records found"), query, 404)
    
    data = raw.get("data", {})
    results = []
    for key, val in data.items():
        if isinstance(val, dict):
            results.append({
                "aadhaar": val.get("aadhar", "N/A"),
                "name": val.get("NAME", "N/A"),
                "father": val.get("fname", "N/A"),
                "mobile": val.get("num", "N/A"),
                "alternate": val.get("alt", "N/A"),
                "address": clean_address(val.get("ADDRESS", "N/A")),
                "circle": val.get("circle", "N/A")
            })
    
    return make_response(results, "AADHAAR LOOKUP RESULT", query)

# ============================================================
# 2. FAMILY INFO
# ============================================================
@app.route('/api/family', methods=['GET'])
def family_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    query = request.args.get('q')
    if not query:
        return error_response("Missing query parameter. Use ?q=123456789012")
    
    raw = fetch_data("familyinfo", query)
    
    if raw.get("success", False):
        result = raw.get("result", {})
        data = {
            "family_id": result.get("family_id", "N/A"),
            "status": result.get("success", False),
            "message": result.get("msg", result.get("message", "N/A"))
        }
        return make_response(data, "FAMILY INFO RESULT", query)
    
    return error_response(raw.get("error", "No records found"), query, 404)

# ============================================================
# 3. FREE FIRE PROFILE
# ============================================================
@app.route('/api/ff', methods=['GET'])
def ff_profile():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    uid = request.args.get('uid')
    if not uid:
        return error_response("Missing uid. Use ?uid=2485047283")
    
    if not re.match(r'^[0-9]{10,12}$', uid):
        return error_response("UID must be 10-12 digits")
    
    raw = fetch_data("ff", uid)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        account = data.get("account_data", {})
        basic = account.get("basicInfo", {})
        clan = account.get("clanBasicInfo", {})
        pet = account.get("petInfo", {})
        
        result = {
            "nickname": basic.get("nickname", "N/A"),
            "level": basic.get("level", 0),
            "region": basic.get("region", "N/A"),
            "rank": basic.get("rank", 0),
            "ranking_points": basic.get("rankingPoints", 0),
            "liked": basic.get("liked", 0),
            "clan_name": clan.get("clanName", "N/A"),
            "clan_level": clan.get("clanLevel", 0),
            "pet_level": pet.get("level", 0)
        }
        return make_response(result, "FREE FIRE PROFILE RESULT", uid)
    
    return error_response(raw.get("error", "Profile not found"), uid, 404)

# ============================================================
# 4. FREE FIRE LIKE
# ============================================================
@app.route('/api/fflike', methods=['GET'])
def ff_like():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')
    
    if not uid:
        return error_response("Missing uid. Use ?uid=2485047283&region=ind")
    
    result = {
        "status": "running",
        "uid": uid,
        "region": region,
        "message": "Free Fire like is running"
    }
    return make_response(result, "FREE FIRE LIKE RESULT", uid)

# ============================================================
# 5. FREE FIRE VISIT
# ============================================================
@app.route('/api/ffvisit', methods=['GET'])
def ff_visit():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')
    
    if not uid:
        return error_response("Missing uid. Use ?uid=2485047283&region=ind")
    
    raw = fetch_data("ffvisit", uid)
    
    if raw.get("success", False):
        return make_response(raw.get("data", {}), "FREE FIRE VISIT RESULT", uid)
    
    return error_response(raw.get("error", "No data found"), uid, 404)

# ============================================================
# 6. IFSC CODE LOOKUP
# ============================================================
@app.route('/api/ifsc', methods=['GET'])
def ifsc_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    ifsc = request.args.get('q') or request.args.get('ifsc')
    if not ifsc:
        return error_response("Missing IFSC code. Use ?q=SBIN0001234")
    
    ifsc = ifsc.upper()
    if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc):
        return error_response("Invalid IFSC format. Example: SBIN0001234")
    
    raw = fetch_data("ifsc", ifsc)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        result = {
            "bank": data.get("BANK", "N/A"),
            "bank_code": data.get("BANKCODE", "N/A"),
            "branch": data.get("BRANCH", "N/A"),
            "address": data.get("ADDRESS", "N/A"),
            "city": data.get("CITY", "N/A"),
            "district": data.get("DISTRICT", "N/A"),
            "state": data.get("STATE", "N/A"),
            "micr": data.get("MICR", "N/A"),
            "contact": data.get("CONTACT", "N/A"),
            "services": {
                "upi": data.get("UPI", False),
                "rtgs": data.get("RTGS", False),
                "neft": data.get("NEFT", False),
                "imps": data.get("IMPS", False)
            }
        }
        return make_response(result, "IFSC LOOKUP RESULT", ifsc)
    
    return error_response(raw.get("error", "IFSC code not found"), ifsc, 404)

# ============================================================
# 7. INSTAGRAM PROFILE
# ============================================================
@app.route('/api/instagram', methods=['GET'])
def instagram_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    username = request.args.get('q') or request.args.get('username')
    if not username:
        return error_response("Missing username. Use ?q=cristiano")
    
    username = username.lstrip('@')
    raw = fetch_data("insta", username)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        profile = data.get("profile", {})
        result = {
            "username": profile.get("username", "N/A"),
            "full_name": profile.get("full_name", "N/A"),
            "bio": profile.get("biography", "N/A"),
            "private": profile.get("is_private", False),
            "verified": profile.get("is_verified", False),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "posts": profile.get("posts", 0),
            "category": profile.get("category_name", "N/A"),
            "business": profile.get("is_business_account", False)
        }
        return make_response(result, "INSTAGRAM PROFILE RESULT", username)
    
    return error_response(raw.get("error", "Profile not found"), username, 404)

# ============================================================
# 8. INSTAGRAM v2 (Alternate)
# ============================================================
@app.route('/api/instagramv2', methods=['GET'])
def instagram_v2():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    username = request.args.get('q') or request.args.get('username')
    if not username:
        return error_response("Missing username. Use ?q=cristiano")
    
    try:
        url = f"https://instagram.abbasofficaldevs.workers.dev/info?username={username}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            raw = response.json()
            acc = raw.get("account", {})
            stats = raw.get("stats", {})
            prof = raw.get("profile", {})
            
            data = {
                "username": acc.get("username", "N/A"),
                "full_name": acc.get("full_name", "N/A"),
                "bio": acc.get("bio", "N/A"),
                "private": acc.get("private", False),
                "verified": acc.get("verified", False),
                "followers": stats.get("followers", 0),
                "following": stats.get("following", 0),
                "posts": stats.get("posts", 0),
                "profile_pic": prof.get("profile_pic_hd", "N/A")
            }
            return make_response(data, "INSTAGRAM v2 RESULT", username)
        else:
            return error_response(f"HTTP {response.status_code}", username, 404)
            
    except Exception as e:
        return error_response(str(e), username, 500)

# ============================================================
# 9. NUMBER LOOKUP v1
# ============================================================
@app.route('/api/number', methods=['GET'])
def number_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    number = request.args.get('q') or request.args.get('number')
    if not number:
        return error_response("Missing number. Use ?q=9876543210")
    
    if not re.match(r'^[0-9]{10,15}$', number):
        return error_response("Invalid number. Must be 10-15 digits")
    
    raw = fetch_data("num", number)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        results = []
        for key, val in data.items():
            if isinstance(val, dict):
                results.append({
                    "name": val.get("NAME", "N/A"),
                    "father": val.get("fname", "N/A"),
                    "mobile": val.get("num", "N/A"),
                    "alternate": val.get("alt", "N/A"),
                    "aadhaar": val.get("aadhar", "N/A"),
                    "address": clean_address(val.get("ADDRESS", "N/A")),
                    "circle": val.get("circle", "N/A")
                })
        return make_response(results, "NUMBER LOOKUP RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 10. NUMBER LOOKUP v2
# ============================================================
@app.route('/api/numberv2', methods=['GET'])
def number_lookup_v2():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    number = request.args.get('q') or request.args.get('number')
    if not number:
        return error_response("Missing number. Use ?q=9876543210")
    
    raw = fetch_data("numv2", number)
    
    if raw.get("success", False):
        return make_response(raw, "NUMBER LOOKUP v2 RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 11. PAKISTAN NUMBER LOOKUP
# ============================================================
@app.route('/api/pakistan', methods=['GET'])
def pakistan_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    number = request.args.get('q') or request.args.get('number')
    if not number:
        return error_response("Missing number. Use ?q=9876543210")
    
    raw = fetch_data("pak", number)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        inner = data.get("data", {})
        results = []
        for result in inner.get("results", []):
            results.append({
                "number": result.get("n", "N/A"),
                "name": result.get("name", "N/A"),
                "cnic": result.get("cnic", "N/A"),
                "address": clean_address(result.get("address", "N/A"))
            })
        return make_response(results, "PAKISTAN NUMBER RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 12. TELEGRAM ID LOOKUP
# ============================================================
@app.route('/api/telegram', methods=['GET'])
def telegram_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    tg_id = request.args.get('q') or request.args.get('id')
    if not tg_id:
        return error_response("Missing Telegram ID. Use ?q=1234567890")
    
    if not re.match(r'^[0-9]{5,15}$', tg_id):
        return error_response("Invalid ID. Must be 5-15 digits")
    
    raw = fetch_data("tgv2", tg_id)
    
    if raw.get("success", False):
        result = raw.get("result", {})
        data = {
            "telegram_id": result.get("tg_id", "N/A"),
            "country": result.get("country", "N/A"),
            "country_code": result.get("country_code", "N/A"),
            "number": result.get("number", "N/A")
        }
        return make_response(data, "TELEGRAM ID RESULT", tg_id)
    
    return error_response(raw.get("error", "ID not found"), tg_id, 404)

# ============================================================
# 13. TELEGRAM USERNAME TO ID
# ============================================================
@app.route('/api/tgusername', methods=['GET'])
def tgusername_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    username = request.args.get('q') or request.args.get('username')
    if not username:
        return error_response("Missing username. Use ?q=ayush")
    
    username = username.lstrip('@')
    raw = fetch_data("id", username)
    
    if raw.get("success", False):
        result = raw.get("result", {})
        data = result.get("data", {})
        response_data = {
            "query": result.get("query", "N/A"),
            "telegram_id": data.get("id", "N/A"),
            "is_bot": data.get("is_bot", False),
            "is_premium": data.get("is_premium", False),
            "is_verified": data.get("is_verified", False),
            "is_scam": data.get("is_scam", False),
            "is_fake": data.get("is_fake", False)
        }
        return make_response(response_data, "TELEGRAM USERNAME RESULT", username)
    
    return error_response(raw.get("error", "Username not found"), username, 404)

# ============================================================
# 14. VEHICLE NUMBER LOOKUP
# ============================================================
@app.route('/api/vehicle', methods=['GET'])
def vehicle_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    vehicle = request.args.get('q') or request.args.get('vehicle')
    if not vehicle:
        return error_response("Missing vehicle number. Use ?q=MH01AB1234")
    
    vehicle = vehicle.upper()
    if not re.match(r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4,5}$', vehicle):
        return error_response("Invalid vehicle format. Example: MH01AB1234")
    
    raw = fetch_data("vnum", vehicle)
    
    if raw.get("success", False):
        result = raw.get("result", {})
        data = result.get("data", {})
        response_data = {
            "query": data.get("query", "N/A"),
            "operative_name": data.get("operative_name", "N/A"),
            "operative_id": data.get("operative_id", "N/A"),
            "status": data.get("status", "N/A"),
            "protocol": data.get("protocol", "N/A")
        }
        return make_response(response_data, "VEHICLE LOOKUP RESULT", vehicle)
    
    return error_response(raw.get("error", "Vehicle not found"), vehicle, 404)

# ============================================================
# 15. ICMR DATA SEARCH
# ============================================================
@app.route('/api/icmr', methods=['GET'])
def icmr_search():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    query = request.args.get('q')
    if not query:
        return error_response("Missing query. Use ?q=8002996108")
    
    if len(query) < 3:
        return error_response("Query must be at least 3 characters")
    
    try:
        url = f"https://icmr-and-hitek-4y35.onrender.com/search?q={query}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            raw = response.json()
            results = []
            for r in raw.get("results", []):
                results.append({
                    "name": r.get("name", "N/A"),
                    "father": r.get("fathersName", "N/A"),
                    "phone": r.get("phoneNumber", "N/A"),
                    "aadhaar": r.get("aadharNumber", "N/A"),
                    "address": clean_address(r.get("address", "N/A")),
                    "district": r.get("district", "N/A"),
                    "state": r.get("state", "N/A")
                })
            data = {
                "total_records": raw.get("count", 0),
                "records": results
            }
            return make_response(data, "ICMR SEARCH RESULT", query)
        else:
            return error_response(f"HTTP {response.status_code}", query, 404)
            
    except Exception as e:
        return error_response(str(e), query, 500)

# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/", "/api/adhar", "/api/family", "/api/ff",
            "/api/fflike", "/api/ffvisit", "/api/ifsc",
            "/api/instagram", "/api/instagramv2", "/api/number",
            "/api/numberv2", "/api/pakistan", "/api/telegram",
            "/api/tgusername", "/api/vehicle", "/api/icmr",
            "/api/health", "/api/stats"
        ],
        **CREDITS
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Please try again later",
        **CREDITS
    }), 500

# ============================================================
# MAIN - RENDER ENTRY POINT
# ============================================================
# Render gunicorn ke liye 'app' variable export karta hai
# Yeh 'app' Flask instance hai - already defined hai upar

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("=" * 80)
    print("XENON OSINT API - All-in-One")
    print("=" * 80)
    print(f"Version: {VERSION}")
    print("Developer: @Xenon33cyber")
    print("Team: @xenondaemon_Team")
    print("Support: @xenondaemon")
    print("Channel: https://t.me/xenondaemon")
    print("=" * 80)
    print("Channels:")
    for ch in CHANNELS:
        print(f"  - {ch}")
    print("=" * 80)
    print(f"Server running on http://0.0.0.0:{port}")
    print("=" * 80)
    print("\n📌 ENDPOINTS:")
    print("  GET  /api/adhar?q=<aadhaar>")
    print("  GET  /api/family?q=<id>")
    print("  GET  /api/ff?uid=<free_fire_uid>")
    print("  GET  /api/fflike?uid=<uid>&region=<region>")
    print("  GET  /api/ffvisit?uid=<uid>&region=<region>")
    print("  GET  /api/ifsc?q=<ifsc_code>")
    print("  GET  /api/instagram?q=<username>")
    print("  GET  /api/instagramv2?q=<username>")
    print("  GET  /api/number?q=<phone>")
    print("  GET  /api/numberv2?q=<phone>")
    print("  GET  /api/pakistan?q=<phone>")
    print("  GET  /api/telegram?q=<telegram_id>")
    print("  GET  /api/tgusername?q=<username>")
    print("  GET  /api/vehicle?q=<vehicle_number>")
    print("  GET  /api/icmr?q=<query>")
    print("  GET  /api/health")
    print("  GET  /api/stats")
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)