from .binance_client import BinanceClient

from .indicators import (
    klines_to_dataframe,
    add_indicators
)

from .analyzer import (
    analyze_timeframe,
    generate_signal,
    get_direction,
    get_reason
)


def main():

    client = BinanceClient()

    print("=" * 60)
    print("ETH AI Trading System V1.1")
    print("Binance ETHUSDT Futures Monitor")
    print("=" * 60)

    # =========================
    # 1. 实时行情
    # =========================

    price = client.get_price()

    ticker = client.get_24h_ticker()

    print()
    print("【1. ETH实时行情】")

    print(
        f"当前价格: {price['price']}"
    )

    print(
        f"24H涨跌: {ticker['priceChangePercent']}%"
    )

    print(
        f"24H最高: {ticker['highPrice']}"
    )

    print(
        f"24H最低: {ticker['lowPrice']}"
    )

    print(
        f"24H成交量: {ticker['volume']}"
    )

    # =========================
    # 2. 衍生品数据
    # =========================

    oi = client.get_open_interest()

    funding = client.get_funding_rate()

    print()
    print("【2. 衍生品数据】")

    print(
        f"Open Interest: "
        f"{oi['openInterest']}"
    )

    print(
        f"Funding Rate: "
        f"{funding[0]['fundingRate']}"
    )

    # =========================
    # 3. 多周期分析
    # =========================

    results = {}

    timeframes = [
        "5m",
        "15m",
        "1h",
        "4h"
    ]

    for timeframe in timeframes:

        print()
        print(
            f"正在分析 {timeframe}..."
        )

        klines = client.get_klines(
            timeframe,
            200
        )

        df = klines_to_dataframe(
            klines
        )

        df = add_indicators(
            df
        )

        result = analyze_timeframe(
            df
        )

        results[timeframe] = result

    # =========================
    # 4. 输出多周期结果
    # =========================

    print()
    print("【3. 多周期趋势】")

    for timeframe in [
        "5m",
        "15m",
        "1h",
        "4h"
    ]:

        result = results[timeframe]

        print(
            f"{timeframe:>3} | "
            f"方向={result['trend']} | "
            f"评分={result['score']}/4 | "
            f"RSI={result['rsi']:.2f} | "
            f"EMA20={result['ema20']:.2f} | "
            f"EMA50={result['ema50']:.2f}"
        )

    # =========================
    # 5. 综合信号
    # =========================

    signal = generate_signal(
        results
    )

    direction = get_direction(
        results
    )

    reason = get_reason(
        results
    )

    print()
    print("【4. 综合信号矩阵】")

    print(
        f"机会等级: {signal}"
    )

    print(
        f"交易方向: {direction}"
    )

    print(
        f"判断依据: {reason}"
    )

    # =========================
    # 6. 当前交易状态
    # =========================

    print()
    print("【5. 当前交易状态】")

    if signal == "A":

        print(
            "状态：重点观察"
        )

        print(
            "说明：多周期方向一致，"
            "等待关键价格位置确认。"
        )

    elif signal == "B":

        print(
            "状态：观察"
        )

        print(
            "说明：方向较明确，"
            "但仍需要价格结构确认。"
        )

    else:

        print(
            "状态：等待"
        )

        print(
            "说明：当前周期存在分歧，"
            "暂不追单。"
        )

    # =========================
    # 7. 风险控制
    # =========================

    print()
    print("【6. 风险控制】")

    print(
        "当前系统：只读监控"
    )

    print(
        "自动下单：关闭"
    )

    print(
        "Binance账户权限：未使用"
    )

    print(
        "执行交易：需要用户明确输入“执行”"
    )

    print()
    print("=" * 60)
    print("ETH监控完成")
    print("=" * 60)


if __name__ == "__main__":
    main()