def analyze_timeframe(df):
    """
    分析单个周期：
    EMA20 / EMA50 / RSI / MACD
    """

    latest = df.iloc[-1]

    close = float(latest["close"])
    ema20 = float(latest["ema20"])
    ema50 = float(latest["ema50"])
    rsi = float(latest["rsi"])
    macd = float(latest["macd"])
    macd_signal = float(latest["macd_signal"])

    score = 0

    # 价格位于EMA20上方
    if close > ema20:
        score += 1

    # EMA20位于EMA50上方
    if ema20 > ema50:
        score += 1

    # RSI强弱
    if rsi > 50:
        score += 1

    # MACD
    if macd > macd_signal:
        score += 1

    # 周期方向
    if score >= 3:
        trend = "多"

    elif score <= 1:
        trend = "空"

    else:
        trend = "震荡"

    return {
        "close": close,
        "ema20": ema20,
        "ema50": ema50,
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "score": score,
        "trend": trend
    }


def generate_signal(results):
    """
    根据4H、1H、15M综合判断机会等级。

    A：多周期高度一致
    B：方向基本明确，但存在部分分歧
    C：等待确认
    D：禁止交易
    """

    trend_4h = results["4h"]["trend"]
    trend_1h = results["1h"]["trend"]
    trend_15m = results["15m"]["trend"]

    # -------------------------
    # A级：多周期完全一致
    # -------------------------

    if (
        trend_4h == "多"
        and trend_1h == "多"
        and trend_15m == "多"
    ):
        return "A"

    if (
        trend_4h == "空"
        and trend_1h == "空"
        and trend_15m == "空"
    ):
        return "A"

    # -------------------------
    # B级：1H和15M一致
    # -------------------------

    if trend_1h == trend_15m:

        if trend_1h in ["多", "空"]:
            return "B"

    # -------------------------
    # C级：周期出现分歧
    # -------------------------

    return "C"


def get_direction(results):

    signal = generate_signal(results)

    trend_1h = results["1h"]["trend"]
    trend_15m = results["15m"]["trend"]

    if signal in ["A", "B"]:

        if trend_1h == "多":
            return "做多"

        if trend_1h == "空":
            return "做空"

    return "等待"


def get_reason(results):

    signal = generate_signal(results)

    trend_4h = results["4h"]["trend"]
    trend_1h = results["1h"]["trend"]
    trend_15m = results["15m"]["trend"]

    if signal == "A":

        return (
            f"4H={trend_4h}，"
            f"1H={trend_1h}，"
            f"15M={trend_15m}，"
            "多周期方向一致"
        )

    if signal == "B":

        return (
            f"4H={trend_4h}，"
            f"1H={trend_1h}，"
            f"15M={trend_15m}，"
            "1H与15M方向一致"
        )

    return (
        f"4H={trend_4h}，"
        f"1H={trend_1h}，"
        f"15M={trend_15m}，"
        "周期存在分歧，等待确认"
    )