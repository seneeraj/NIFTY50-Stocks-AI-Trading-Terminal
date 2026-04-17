import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import os
import requests
import matplotlib.pyplot as plt
from openai import OpenAI

st.set_page_config(page_title="NSE50 Individual Stocks AI Trading Terminal", layout="wide")

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("⚙️ Controls")

llm_mode = st.sidebar.radio("AI Mode", ["Local (Free)", "Cloud (OpenAI)"])
USE_LOCAL_LLM = "Local" in llm_mode

api_key = os.getenv("OPENAI_API_KEY")

# -----------------------
# NIFTY 50 STOCKS
# -----------------------
stocks = [
"ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS",
"AXISBANK.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
"BEL.NS","BHARTIARTL.NS","BPCL.NS","BRITANNIA.NS",
"CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS",
"EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS",
"HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS",
"ICICIBANK.NS","ITC.NS","INDUSINDBK.NS","INFY.NS",
"JSWSTEEL.NS","KOTAKBANK.NS","LT.NS","M&M.NS",
"MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS",
"POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS",
"SUNPHARMA.NS","TCS.NS","TATACONSUM.NS","TATAMOTORS.NS",
"TATASTEEL.NS","TECHM.NS","TITAN.NS","ULTRACEMCO.NS",
"UPL.NS","WIPRO.NS"
]

stock = st.sidebar.selectbox("Select Stock", stocks)
period = st.sidebar.selectbox("Period", ["5d", "1mo", "3mo"])
interval = st.sidebar.selectbox("Interval", ["5m", "15m", "1h", "1d"])

# -----------------------
# SAFE DATA FETCH
# -----------------------
def fetch_data_safe(stock, period, interval):
    df = yf.download(stock, period=period, interval=interval)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df is None or df.empty or len(df) < 30:
        return None

    return df

data = fetch_data_safe(stock, period, interval)

if data is None:
    st.error("❌ Not enough data")
    st.stop()

# -----------------------
# INDICATORS
# -----------------------
def add_indicators(df):
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['Signal'] = df['MACD'].ewm(span=9).mean()

    df['Volume_MA'] = df['Volume'].rolling(20).mean()

    df = df.dropna()

    if df.empty:
        return None

    return df

data = add_indicators(data)

if data is None:
    st.warning("⚠️ Data insufficient")
    st.stop()

latest = data.iloc[-1]

# -----------------------
# SIGNAL
# -----------------------
def generate_signal(latest):
    score = 0

    if latest['RSI'] < 30: score += 2
    elif latest['RSI'] > 70: score -= 2

    if latest['Close'] > latest['MA20'] > latest['MA50']:
        score += 2
    elif latest['Close'] < latest['MA20'] < latest['MA50']:
        score -= 2

    if latest['MACD'] > latest['Signal']: score += 1
    else: score -= 1

    if latest['Volume'] > latest['Volume_MA']: score += 1

    strength = int((abs(score)/6)*100)

    if score >= 3: signal = "🟢 BUY"
    elif score <= -3: signal = "🔴 SELL"
    else: signal = "🟡 HOLD"

    return signal, strength

signal, strength = generate_signal(latest)

# -----------------------
# RISK & CONFIDENCE ENGINE
# -----------------------
def calculate_risk_confidence(latest, data, strength):

    volatility = data['Close'].pct_change().std() * 100

    if latest['RSI'] > 70 or latest['RSI'] < 30:
        rsi_risk = 2
    else:
        rsi_risk = 1

    if volatility > 2:
        vol_risk = 2
    else:
        vol_risk = 1

    total_risk_score = rsi_risk + vol_risk

    if total_risk_score <= 2:
        risk = "🟢 Low"
    elif total_risk_score == 3:
        risk = "🟡 Medium"
    else:
        risk = "🔴 High"

    confidence = int((strength * 0.7) + (100 - volatility * 10) * 0.3)
    confidence = max(0, min(100, confidence))

    return risk, confidence

# ✅ CORRECT PLACE (after signal)
risk, confidence = calculate_risk_confidence(latest, data, strength)

# -----------------------
# SIDEBAR ANALYTICS
# -----------------------
st.sidebar.markdown("## 📊 Trade Quality")

st.sidebar.metric("Risk Level", risk)
st.sidebar.metric("Confidence", f"{confidence}%")
st.sidebar.progress(confidence / 100)

if "Low" in risk:
    st.sidebar.success("Low Risk Trade")
elif "Medium" in risk:
    st.sidebar.warning("Moderate Risk")
else:
    st.sidebar.error("High Risk ⚠️")

# -----------------------
# HEADER
# -----------------------
st.title("NIFTY50 Stocks AI Trading Terminal")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Signal", signal)
c2.metric("Strength", f"{strength}%")
c3.metric("RSI", round(latest['RSI'],2))
c4.metric("Price", round(latest['Close'],2))

st.progress(strength/100)

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3 = st.tabs(["📈 Chart", "🧠 AI Insight", "📡 Scanner"])

# -----------------------
# CHART
# -----------------------
with tab1:
    support = data['Low'].rolling(20).min().iloc[-1]
    resistance = data['High'].rolling(20).max().iloc[-1]

    fig, ax = plt.subplots(figsize=(12,5))

    # Price + MA
    ax.plot(data.index, data['Close'], label="Price", linewidth=2, color="blue")
    ax.plot(data.index, data['MA20'], label="MA20", linestyle="--", color="orange")
    ax.plot(data.index, data['MA50'], label="MA50", linestyle="--", color="green")

    # 🔥 FIXED SUPPORT / RESISTANCE
    ax.axhline(y=support, color="green", linestyle="--", linewidth=2,
               label=f"Support ({round(support,2)})")

    ax.axhline(y=resistance, color="red", linestyle="--", linewidth=2,
               label=f"Resistance ({round(resistance,2)})")

    # Styling
    ax.set_title(f"{stock} Price with Support & Resistance")
    ax.grid(True, alpha=0.3)

    # 🔥 IMPORTANT (shows everything clearly)
    ax.legend(loc="upper left")

    st.pyplot(fig)

# -----------------------
# AI
# -----------------------
with tab2:

    def local_llm(prompt):
        try:
            r = requests.post("http://localhost:11434/api/generate",
                json={"model":"llama3","prompt":prompt,"stream":False})
            return r.json()["response"]
        except:
            return "Local failed"

    def cloud_llm(prompt):
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        return r.choices[0].message.content

    if st.button("🧠 Explain Signal", key="explain_btn"):
        prompt = f"Explain {signal} using RSI {latest['RSI']}"
        result = local_llm(prompt) if USE_LOCAL_LLM else cloud_llm(prompt)
        st.info(result)

st.caption("⚠️ AI-generated explanation. Not financial advice.")

# -----------------------
# SCANNER
# -----------------------
with tab3:

    if st.button("Scan NIFTY50", key="scan_btn"):
        results = []

        for s in stocks:
            df = fetch_data_safe(s, period, interval)
            if df is None:
                continue

            df = add_indicators(df)
            if df is None:
                continue

            last = df.iloc[-1]
            sig, stren = generate_signal(last)

            results.append({"Stock": s, "Signal": sig, "Strength": stren})

        st.dataframe(pd.DataFrame(results))

# -----------------------
# DISCLAIMER
# -----------------------
st.markdown("---")

st.warning("""
⚠️ **Disclaimer**

This application provides AI-generated insights for informational purposes only.  
It does not constitute financial advice, investment recommendation, or trading guidance.  

Please consult a certified financial advisor before making any investment decisions.
""")