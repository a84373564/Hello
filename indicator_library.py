def get_indicator_logic(indicator):
    if indicator == "rsi":
        return '''
    rsi = data["rsi"]
    if rsi[-1] < 30:
        capital += position_size * 0.02
        log.append("RSI 低檔進場 +2%")
    elif rsi[-1] > 70:
        capital -= position_size * 0.02
        log.append("RSI 高檔出場 -2%")
    '''
    
    elif indicator == "macd":
        return '''
    macd = data["macd"]
    signal = data["signal"]
    if macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
        capital += position_size * 0.025
        log.append("MACD 黃金交叉 +2.5%")
    elif macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
        capital -= position_size * 0.025
        log.append("MACD 死亡交叉 -2.5%")
    '''

    elif indicator == "ma":
        return '''
    close = data["close"]
    ma = data["ma"]
    if close[-1] > ma[-1] and close[-2] <= ma[-2]:
        capital += position_size * 0.015
        log.append("突破均線 +1.5%")
    elif close[-1] < ma[-1] and close[-2] >= ma[-2]:
        capital -= position_size * 0.015
        log.append("跌破均線 -1.5%")
    '''

    elif indicator == "atr":
        return '''
    atr = data["atr"]
    if atr[-1] > atr[-2]:
        capital += position_size * 0.01
        log.append("ATR 上升 +1%")
    else:
        capital -= position_size * 0.01
        log.append("ATR 下降 -1%")
    '''

    else:
        return None
