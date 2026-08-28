# -*- coding: utf-8 -*-
"""
Aadhar API Clone (Auto-Port Select)
Owner: @Xenon33cyber
Source: nitin-developer-api-paid.nitinshab43.workers.dev
"""

from flask import Flask, request, jsonify
import requests
import json
import time
import socket
from datetime import datetime
import hashlib
import re
import os
import sys

app = Flask(__name__)

# ============================================================
# CONFIG
# ============================================================
ORIGINAL_API = "https://nitin-developer-api-paid.nitinshab43.workers.dev/api"
DEFAULT_KEY = "MY_TEST_KEY_123"
CACHE_ENABLED = True
CACHE_DURATION = 300
cache_store = {}

# ============================================================
# AUTO-PORT SELECT
# ============================================================
START_PORT = 5000
MAX_PORTS = 50

def find_available_port(start_port=START_PORT, max_attempts=MAX_PORTS):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def get_port_from_file():
    """Get saved port from file"""
    port_file = "current_port.json"
    if os.path.exists(port_file):
        try:
            with open(port_file, 'r') as f:
                data = json.load(f)
                return data.get('port', START_PORT)
        except:
            return START_PORT
    return START_PORT

def save_port_to_file(port):
    """Save current port to file"""
    port_file = "current_port.json"
    with open(port_file, 'w') as f:
        json.dump({'port': port, 'timestamp': datetime.now().isoformat()}, f)

def is_port_in_use(port):
    """Check if port is in use"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', port))
        sock.close()
        return False
    except OSError:
        return True

# ============================================================


def validate_aadhar(number):
    return len(number) == 12 and number.isdigit()


def get_cache_key(aadhar, key):
    return hashlib.md5(f"{aadhar}:{key}".encode()).hexdigest()


def get_cached(key):
    if key in cache_store:
        data, timestamp = cache_store[key]
        if time.time() - timestamp < CACHE_DURATION:
            return data
    return None


def format_address(address):
    if not address:
        return "N/A"
    return address.replace("!", ", ")


def clean_data(data):
    cleaned = []
    for item in data:
        cleaned.append({
            "name": item.get("NAME", "N/A"),
            "father": item.get("fname", "N/A"),
            "mobile": item.get("num", "N/A"),
            "alt": item.get("alt", "N/A"),
            "email": item.get("email", "N/A"),
            "address": format_address(item.get("ADDRESS", "N/A")),
            "circle": item.get("circle", "N/A"),
            "aadhar": item.get("aadhar", "N/A")
        })
    return cleaned


# ============================================================
# ROUTES
# ============================================================

@app.route('/api/aadhar', methods=['GET'])
def aadhar_lookup():
    aadhar = request.args.get('number')
    api_key = request.args.get('key', DEFAULT_KEY)
    
    if not aadhar:
        return jsonify({
            "error": "Missing Aadhar number",
            "usage": "/api/aadhar?number=123456789012&key=YOUR_KEY",
            "example": "/api/aadhar?number=123456789012"
        }), 400
    
    if not validate_aadhar(aadhar):
        return jsonify({
            "error": "Invalid Aadhar number",
            "message": "Aadhar must be 12 digits",
            "provided": aadhar
        }), 400
    
    if CACHE_ENABLED:
        cache_key = get_cache_key(aadhar, api_key)
        cached = get_cached(cache_key)
        if cached:
            return jsonify({
                "status": "cached",
                "aadhar": aadhar,
                "data": cached,
                "owner": "@Xenon33cyber",
                "timestamp": datetime.now().isoformat()
            })
    
    try:
        url = f"{ORIGINAL_API}?action=aadhar&aadhar={aadhar}&key={api_key}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            if raw_data.get("status"):
                result = raw_data.get("result", [])
                cleaned_result = clean_data(result)
                
                if CACHE_ENABLED:
                    cache_key = get_cache_key(aadhar, api_key)
                    cache_store[cache_key] = (cleaned_result, time.time())
                
                return jsonify({
                    "status": "success",
                    "aadhar": aadhar,
                    "total_results": len(cleaned_result),
                    "data": cleaned_result,
                    "metadata": raw_data.get("metadata", {}),
                    "owner": "@Xenon33cyber",
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "No data found",
                    "aadhar": aadhar
                }), 404
                
        else:
            return jsonify({
                "status": "error",
                "error": f"API Error: {response.status_code}",
                "message": response.text[:200]
            }), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/aadhar/clean', methods=['GET'])
def aadhar_clean():
    aadhar = request.args.get('number')
    api_key = request.args.get('key', DEFAULT_KEY)
    
    if not aadhar:
        return jsonify({"error": "Missing Aadhar number"}), 400
    
    url = f"{ORIGINAL_API}?action=aadhar&aadhar={aadhar}&key={api_key}"
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        raw_data = response.json()
        if raw_data.get("status"):
            result = raw_data.get("result", [])
            cleaned = clean_data(result)
            return jsonify({
                "status": "success",
                "aadhar": aadhar,
                "data": cleaned,
                "owner": "@Xenon33cyber"
            })
    
    return jsonify({"error": "Failed to fetch data"}), 500


@app.route('/api/aadhar/raw', methods=['GET'])
def aadhar_raw():
    aadhar = request.args.get('number')
    api_key = request.args.get('key', DEFAULT_KEY)
    
    if not aadhar:
        return jsonify({"error": "Missing Aadhar number"}), 400
    
    url = f"{ORIGINAL_API}?action=aadhar&aadhar={aadhar}&key={api_key}"
    response = requests.get(url, timeout=30)
    
    return jsonify(response.json())


@app.route('/api/aadhar/check', methods=['GET'])
def aadhar_check():
    aadhar = request.args.get('number')
    
    if not aadhar:
        return jsonify({"error": "Missing Aadhar number"}), 400
    
    return jsonify({
        "aadhar": aadhar,
        "valid": validate_aadhar(aadhar),
        "length": len(aadhar),
        "format": "12 digits only"
    })


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    cache_store.clear()
    return jsonify({
        "status": "success",
        "message": "Cache cleared",
        "owner": "@Xenon33cyber"
    })


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Aadhar API Clone",
        "owner": "@Xenon33cyber",
        "version": "2.0.0",
        "status": "online",
        "endpoints": {
            "/api/aadhar?number=<12digit>&key=<api_key>": "Get Aadhar details",
            "/api/aadhar/clean?number=<12digit>&key=<api_key>": "Get cleaned data",
            "/api/aadhar/raw?number=<12digit>&key=<api_key>": "Get raw response",
            "/api/aadhar/check?number=<12digit>": "Validate Aadhar"
        },
        "example": "/api/aadhar?number=327567544017"
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available": [
            "/api/aadhar?number=<12digit>&key=<api_key>",
            "/api/aadhar/clean?number=<12digit>&key=<api_key>",
            "/api/aadhar/raw?number=<12digit>&key=<api_key>",
            "/api/aadhar/check?number=<12digit>"
        ]
    }), 404


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Try saved port first
    saved_port = get_port_from_file()
    
    # Check if saved port is available
    if saved_port and not is_port_in_use(saved_port):
        PORT = saved_port
        print(f"ℹ️ Using saved port: {PORT}")
    else:
        # Find available port
        PORT = find_available_port(START_PORT)
        if PORT is None:
            print("❌ No available ports found!")
            sys.exit(1)
        save_port_to_file(PORT)
        print(f"ℹ️ Using new port: {PORT}")
    
    print("=" * 50)
    print("🔍 AADHAR API CLONE (Auto-Port Select)")
    print("💀 Owner: @Xenon33cyber")
    print(f"📡 Running on http://0.0.0.0:{PORT}")
    print("=" * 50)
    print("\n📌 Test Commands:")
    print(f"  curl http://localhost:{PORT}/api/aadhar?number=327567544017")
    print(f"  curl http://localhost:{PORT}/api/aadhar/clean?number=327567544017")
    print(f"  curl http://localhost:{PORT}/api/aadhar/check?number=327567544017")
    print("=" * 50)
    print(f"\n📌 Admin: Clear cache with POST /api/cache/clear")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=PORT, debug=False)