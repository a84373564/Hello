import json
import os

print("[Ω] 設定你的 MEXC API 金鑰（只讀權限即可）")

apiKey = input("請輸入你的 apiKey：").strip()
secret = input("請輸入你的 secretKey：").strip()

key_data = {
    "apiKey": apiKey,
    "secret": secret
}

with open("mexc_keys.json", "w") as f:
    json.dump(key_data, f, indent=4)
    print("[Ω] MEXC 金鑰已儲存於 mexc_keys.json")

print("提醒：這個檔案不要上傳到 GitHub，也不要公開分享。")
