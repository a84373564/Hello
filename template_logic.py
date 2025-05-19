# 測試用策略邏輯（保證會買賣）
holding = False
for i in range(len(data["close"])):
    price = data["close"][i]
    if i % 6 == 0 and not holding:
        if capital >= min_capital:
            capital -= price * position_size
            log.append(f"Buy at {price:.2f}")
            holding = True
    elif i % 6 == 3 and holding:
        capital += price * position_size
        log.append(f"Sell at {price:.2f}")
        holding = False
