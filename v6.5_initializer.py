import os

def ensure_resources():
    os.makedirs("modules", exist_ok=True)
    os.makedirs("prices", exist_ok=True)
    if not os.path.exists("top_symbols.json"):
        with open("top_symbols.json", "w") as f:
            f.write('["BTCUSDT", "ETHUSDT"]')

if __name__ == "__main__":
    print("[v07] 啟動環境初始化...")
    ensure_resources()
    print("[v07] modules/, prices/, top_symbols.json 檢查完畢。")
