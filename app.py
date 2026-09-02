# -*- coding: utf-8 -*-
"""
XENON OSINT API - All 18 APIs Combined
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

def fetch_data_with_uid(endpoint, uid, api_key=API_KEY, region="ind"):
    try:
        url = f"{API_BASE}/{endpoint}?key={api_key}&uid={uid}&region={region}"
        logger.info(f"Fetching: {endpoint} for {uid}")
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

def fetch_data_with_ifsc(endpoint, ifsc, api_key=API_KEY):
    try:
        url = f"{API_BASE}/{endpoint}?key={api_key}&q={ifsc}"
        logger.info(f"Fetching: {endpoint} for {ifsc}")
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

def fetch_icmr_data(query):
    try:
        url = f"https://icmr-and-hitek-4y35.onrender.com/search?q={query}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def fetch_instagram_v2(username):
    try:
        url = f"https://instagram.abbasofficaldevs.workers.dev/info?username={username}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": f"HTTP {response.status_code}"}
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
# API ENDPOINTS (ALL 18)
# ============================================================
# ============================================================

# ---------- HOME ----------
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "XENON OSINT API - All 18 APIs Combined",
        "version": VERSION,
        "status": "online",
        **CREDITS,
        "total_apis": 18,
        "endpoints": {
            "1": {"path": "/api/number", "description": "Number Lookup", "status": "Working"},
            "2": {"path": "/api/numberv2", "description": "Number Lookup v2", "status": "Working"},
            "3": {"path": "/api/telegramid", "description": "Telegram ID Lookup", "status": "Working"},
            "4": {"path": "/api/telegramusername", "description": "Telegram Username to ID", "status": "Working"},
            "5": {"path": "/api/ffprofile", "description": "Free Fire Profile", "status": "Working"},
            "6": {"path": "/api/ffvisit", "description": "Free Fire Visit", "status": "Working"},
            "7": {"path": "/api/fflike", "description": "Free Fire Like", "status": "Working"},
            "8": {"path": "/api/instagram", "description": "Instagram Profile", "status": "Working"},
            "9": {"path": "/api/instagramv2", "description": "Instagram Profile v2", "status": "Working"},
            "10": {"path": "/api/icmr", "description": "ICMR Data Search", "status": "Working"},
            "11": {"path": "/api/pakistan", "description": "Pakistan Number Lookup", "status": "Working"},
            "12": {"path": "/api/vehicle", "description": "Vehicle Number Lookup", "status": "Working"},
            "13": {"path": "/api/ifsc", "description": "IFSC Code Lookup", "status": "Premium"},
            "14": {"path": "/api/adhar", "description": "Aadhaar Lookup", "status": "Premium"},
            "15": {"path": "/api/family", "description": "Family Info Lookup", "status": "Premium"},
            "16": {"path": "/api/tgv2", "description": "Telegram v2 Lookup", "status": "Premium"},
            "17": {"path": "/api/health", "description": "Health Check", "status": "Utility"},
            "18": {"path": "/api/stats", "description": "API Stats", "status": "Utility"}
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
# 1. NUMBER LOOKUP v1 (AadharApis.py, Numberv1.py)
# ============================================================
@app.route('/api/number', methods=['GET'])
def number_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded. Max 60 requests per minute.", status=429)
    
    number = request.args.get('q') or request.args.get('number')
    if not number:
        return error_response("Missing number. Use ?q=9876543210")
    
    if not re.match(r'^[0-9]{10,15}$', number):
        return error_response("Invalid number. Must be 10-15 digits")
    
    raw = fetch_data("num", number)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        results = []
        
        if isinstance(data, list):
            for item in data:
                results.append({
                    "name": item.get("name", "N/A"),
                    "father": item.get("fname", "N/A"),
                    "mobile": item.get("mobile", item.get("num", "N/A")),
                    "alternate": item.get("alt", "N/A"),
                    "aadhaar": item.get("aadhar", "N/A"),
                    "address": clean_address(item.get("address", "N/A")),
                    "circle": item.get("circle", "N/A"),
                    "email": item.get("email", "N/A")
                })
        elif isinstance(data, dict):
            if "result" in data:
                for item in data["result"]:
                    results.append({
                        "name": item.get("name", "N/A"),
                        "father": item.get("fname", "N/A"),
                        "mobile": item.get("mobile", item.get("num", "N/A")),
                        "alternate": item.get("alt", "N/A"),
                        "aadhaar": item.get("aadhar", "N/A"),
                        "address": clean_address(item.get("address", "N/A")),
                        "circle": item.get("circle", "N/A"),
                        "email": item.get("email", "N/A")
                    })
            else:
                for key, val in data.items():
                    if isinstance(val, dict):
                        results.append({
                            "name": val.get("NAME", val.get("name", "N/A")),
                            "father": val.get("fname", "N/A"),
                            "mobile": val.get("num", val.get("mobile", "N/A")),
                            "alternate": val.get("alt", "N/A"),
                            "aadhaar": val.get("aadhar", "N/A"),
                            "address": clean_address(val.get("ADDRESS", val.get("address", "N/A"))),
                            "circle": val.get("circle", "N/A"),
                            "email": val.get("email", "N/A")
                        })
        
        if not results:
            return error_response("No records found for this number.", number, 404)
            
        return make_response({
            "total_records": len(results),
            "records": results
        }, "NUMBER LOOKUP RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 2. NUMBER LOOKUP v2 (Numberv2.py)
# ============================================================
@app.route('/api/numberv2', methods=['GET'])
def number_lookup_v2():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    number = request.args.get('q') or request.args.get('number')
    if not number:
        return error_response("Missing number. Use ?q=9876543210")
    
    if not re.match(r'^[0-9]{10,15}$', number):
        return error_response("Invalid number. Must be 10-15 digits")
    
    raw = fetch_data("numv2", number)
    
    if raw.get("success", False):
        data = raw.get("data", {})
        results = []
        
        if "result" in data:
            for item in data["result"]:
                results.append({
                    "name": item.get("name", "N/A"),
                    "father": item.get("fname", "N/A"),
                    "mobile": item.get("mobile", "N/A"),
                    "alternate": item.get("alt", "N/A"),
                    "aadhaar": item.get("aadhar", "N/A"),
                    "address": clean_address(item.get("address", "N/A")),
                    "circle": item.get("circle", "N/A")
                })
        
        return make_response({
            "total_records": len(results),
            "records": results
        }, "NUMBER LOOKUP v2 RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 3. TELEGRAM ID LOOKUP (TELEGRAMIDv2.py)
# ============================================================
@app.route('/api/telegramid', methods=['GET'])
def telegram_id_lookup():
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
    
    if raw.get("message") and "Premium" in raw.get("message", ""):
        return error_response("Premium Only Mode Active! Contact @DuXxZx_info for Premium Access.", tg_id, 403)
    
    return error_response(raw.get("error", "ID not found"), tg_id, 404)

# ============================================================
# 4. TELEGRAM USERNAME TO ID (TELEGRAMUSERNAME.py)
# ============================================================
@app.route('/api/telegramusername', methods=['GET'])
def telegram_username_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    username = request.args.get('q') or request.args.get('username')
    if not username:
        return error_response("Missing username. Use ?q=ayush")
    
    username = username.lstrip('@')
    if len(username) < 2:
        return error_response("Username must be at least 2 characters")
    
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
# 5. FREE FIRE PROFILE (FFPROFILE.py)
# ============================================================
@app.route('/api/ffprofile', methods=['GET'])
def ff_profile():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    uid = request.args.get('uid')
    if not uid:
        return error_response("Missing uid. Use ?uid=2485047283")
    
    if not re.match(r'^[0-9]{10,12}$', uid):
        return error_response("UID must be 10-12 digits")
    
    raw = fetch_data_with_uid("ff", uid)
    
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
            "clan_members": clan.get("memberNum", 0),
            "pet_level": pet.get("level", 0),
            "last_login": basic.get("lastLoginAt", "N/A"),
            "created_at": basic.get("createAt", "N/A")
        }
        return make_response(result, "FREE FIRE PROFILE RESULT", uid)
    
    return error_response(raw.get("error", "Profile not found"), uid, 404)

# ============================================================
# 6. FREE FIRE VISIT (FFVISIT.py)
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
    
    raw = fetch_data_with_uid("ffvisit", uid, region=region)
    
    if raw.get("success", False):
        return make_response(raw.get("data", {}), "FREE FIRE VISIT RESULT", uid)
    
    return error_response(raw.get("error", "No data found"), uid, 404)

# ============================================================
# 7. FREE FIRE LIKE (FFLikeAPIProxy.py)
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
    
    raw = fetch_data_with_uid("fflike", uid, region=region)
    
    if raw.get("success", False):
        return make_response(raw.get("data", {}), "FREE FIRE LIKE RESULT", uid)
    
    return error_response(raw.get("error", "No data found"), uid, 404)

# ============================================================
# 8. INSTAGRAM PROFILE (InstagramAPI.py)
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
# 9. INSTAGRAM v2 (Instagramv2.py)
# ============================================================
@app.route('/api/instagramv2', methods=['GET'])
def instagram_v2():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    username = request.args.get('q') or request.args.get('username')
    if not username:
        return error_response("Missing username. Use ?q=cristiano")
    
    raw = fetch_instagram_v2(username)
    
    if raw.get("success", False) and not raw.get("error"):
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
    
    if raw.get("error"):
        return error_response(raw.get("error"), username, 404)
    
    return error_response("Profile not found", username, 404)

# ============================================================
# 10. ICMR DATA SEARCH (MasterNunber.py)
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
    
    raw = fetch_icmr_data(query)
    
    if raw.get("success", False) or "results" in raw:
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
            "total_records": raw.get("count", len(results)),
            "records": results
        }
        return make_response(data, "ICMR SEARCH RESULT", query)
    
    return error_response(raw.get("error", "No records found"), query, 404)

# ============================================================
# 11. PAKISTAN NUMBER LOOKUP (PAKISTANNUMBERLOOKUP.py)
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
        return make_response({
            "total_records": len(results),
            "records": results
        }, "PAKISTAN NUMBER RESULT", number)
    
    return error_response(raw.get("error", "No records found"), number, 404)

# ============================================================
# 12. VEHICLE NUMBER LOOKUP (VEHICLENUMBER.py)
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
# 13. IFSC CODE LOOKUP (IFSC CODE.py) - PREMIUM
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
    
    raw = fetch_data_with_ifsc("ifsc", ifsc)
    
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
    
    if raw.get("message") and "Premium" in raw.get("message", ""):
        return error_response("Premium Only Mode Active! Contact @DuXxZx_info for Premium Access.", ifsc, 403)
    
    return error_response(raw.get("error", "IFSC code not found"), ifsc, 404)

# ============================================================
# 14. AADHAAR LOOKUP (AadharApis.py, AdharApi.py) - PREMIUM
# ============================================================
@app.route('/api/adhar', methods=['GET'])
def adhar_lookup():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return error_response("Rate limit exceeded", status=429)
    
    query = request.args.get('q') or request.args.get('number')
    if not query:
        return error_response("Missing query parameter. Use ?q=123456789012")
    
    raw = fetch_data("adhar", query)
    
    if raw.get("Success", False):
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
    
    if raw.get("message") and "Premium" in raw.get("message", ""):
        return error_response("Premium Only Mode Active! Contact @DuXxZx_info for Premium Access.", query, 403)
    
    return error_response(raw.get("message", "No records found"), query, 404)

# ============================================================
# 15. FAMILY INFO LOOKUP (FAMILYINFO.py) - PREMIUM
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
    
    if raw.get("message") and "Premium" in raw.get("message", ""):
        return error_response("Premium Only Mode Active! Contact @DuXxZx_info for Premium Access.", query, 403)
    
    return error_response(raw.get("error", "No records found"), query, 404)

# ============================================================
# 16. TELEGRAM v2 LOOKUP (TELEGRAMIDv2.py) - PREMIUM
# ============================================================
@app.route('/api/tgv2', methods=['GET'])
def tgv2_lookup():
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
        return make_response(data, "TELEGRAM v2 RESULT", tg_id)
    
    if raw.get("message") and "Premium" in raw.get("message", ""):
        return error_response("Premium Only Mode Active! Contact @DuXxZx_info for Premium Access.", tg_id, 403)
    
    return error_response(raw.get("error", "ID not found"), tg_id, 404)

# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/", "/api/number", "/api/numberv2",
            "/api/telegramid", "/api/telegramusername",
            "/api/ffprofile", "/api/ffvisit", "/api/fflike",
            "/api/instagram", "/api/instagramv2",
            "/api/icmr", "/api/pakistan", "/api/vehicle",
            "/api/ifsc", "/api/adhar", "/api/family", "/api/tgv2",
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
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("=" * 80)
    print("XENON OSINT API - All 18 APIs Combined")
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
    print("\n📌 TOTAL 18 APIs:")
    print("=" * 80)
    print("✅ WORKING (12):")
    print("  1. /api/number")
    print("  2. /api/numberv2")
    print("  3. /api/telegramid")
    print("  4. /api/telegramusername")
    print("  5. /api/ffprofile")
    print("  6. /api/ffvisit")
    print("  7. /api/fflike")
    print("  8. /api/instagram")
    print("  9. /api/instagramv2")
    print(" 10. /api/icmr")
    print(" 11. /api/pakistan")
    print(" 12. /api/vehicle")
    print("\n⚠️ PREMIUM (4):")
    print(" 13. /api/ifsc")
    print(" 14. /api/adhar")
    print(" 15. /api/family")
    print(" 16. /api/tgv2")
    print("\n🛠️ UTILITY (2):")
    print(" 17. /api/health")
    print(" 18. /api/stats")
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)