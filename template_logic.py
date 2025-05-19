holding = False
for i in range(len(data["close"])):
    price = data["close"][i]
    if i % 5 == 0 and not holding:
        if capital >= min_capital:
            capital -= price * position_size
            log.append(f"Buy at {price:.2f}")
            holding = True
    elif i % 5 == 3 and holding:
        capital += price * position_size
        log.append(f"Sell at {price:.2f}")
        holding = False
