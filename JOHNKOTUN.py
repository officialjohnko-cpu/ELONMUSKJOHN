import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_voucher(voucher_code, hwid, secret_key="yg224228"):
    # Target ရဲ့ HWID နှင့် password key ကို ပေါင်းပြီး 32-byte AES Key ထုတ်ယူခြင်း
    combined_key = hashlib.sha256((hwid + secret_key).encode()).digest()
    
    # Static IV (main.py ထဲက စနစ်နဲ့ ကိုက်ညီအောင် ဆောက်ခြင်း)
    iv = hashlib.md5(secret_key.encode()).digest()
    
    cipher = AES.new(combined_key, AES.MODE_CBC, iv)
    padded_data = pad(voucher_code.encode(), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    
    return base64.b64encode(encrypted_bytes).decode()

if __name__ == "__main__":
    print("┌────────────────────────────────────────┐")
    print("│      YOURGOD VOUCHER ENCODER TOOL      │")
    print("└────────────────────────────────────────┘\n")
    
    # Target User ရဲ့ HWID ကို ရိုက်ထည့်ခိုင်းခြင်း
    target_hwid = input("Enter USER Device HWID (e.g., MSC-XXXX): ").strip()
    
    # မူရင်း ဝိုင်ဖိုင်ကုဒ်ကို ရိုက်ထည့်ခိုင်းခြင်း
    raw_voucher = input("Enter Plain Voucher Code to Encode: ").strip()
    
    if target_hwid and raw_voucher:
        encrypted_res = encrypt_voucher(raw_voucher, target_hwid)
        print("\n[💎] ENCRYPTED VOUCHER STRING :")
        print(encrypted_res)
        print("\n──────────────────────────────────────────")
    else:
        print("\n[❌] Error: HWID သို့မဟုတ် Voucher ဖြည့်သွင်းမှု လိုအပ်နေပါသည်။")