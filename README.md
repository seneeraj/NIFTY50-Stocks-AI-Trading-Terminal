# 📊 NIFTY50 Stocks AI Trading Terminal

An AI-powered trading analysis dashboard for **NIFTY50 stocks**, built using Streamlit.
This application provides **technical analysis, trading signals, risk assessment, and AI-based insights** to support better decision-making.

---

## 🚀 Features

### 📈 Technical Analysis

* Moving Averages (MA20, MA50)
* RSI (Relative Strength Index)
* MACD Indicator
* Volume Analysis

### 📊 Trading Signals

* 🟢 BUY / 🔴 SELL / 🟡 HOLD signals
* Signal strength (0–100%)

### 🎯 Risk & Confidence Engine

* Risk Meter (Low / Medium / High)
* Confidence Score (%)
* Volatility-based evaluation

### 📉 Support & Resistance

* Auto-calculated dynamic levels
* Visualized directly on chart

### 🧠 AI Insight

* Explanation of trading signals using:

  * RSI
  * MACD
  * Trend analysis
* Supports:

  * Local LLM (Ollama)
  * Cloud LLM (OpenAI)

### 📡 Market Scanner

* Scan all NIFTY50 stocks
* Identify strongest signals
* Ranked output

---

## 🖥️ UI Highlights

* Professional dashboard layout
* Sidebar controls
* Tab-based navigation:

  * 📈 Chart
  * 🧠 AI Insight
  * 📡 Scanner
* KPI cards for quick insights

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Data Source:** yFinance
* **Visualization:** Matplotlib
* **AI Models:**

  * Local: Ollama (LLaMA3)
  * Cloud: OpenAI API

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/nifty50-ai-trading-terminal.git
cd nifty50-ai-trading-terminal
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set API Key (Optional for Cloud AI)

```bash
set OPENAI_API_KEY=your_api_key   # Windows
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📊 How It Works

1. Select a NIFTY50 stock
2. Choose period & interval
3. System calculates indicators
4. Generates trading signal
5. Evaluates:

   * Strength
   * Risk
   * Confidence
6. (Optional) Get AI explanation
7. Use Scanner to find opportunities

---

## ⚠️ Disclaimer

This application provides **AI-generated insights for informational purposes only**.
It does **not** constitute financial advice, investment recommendation, or trading guidance.

Users should consult a **qualified financial advisor** before making any investment decisions.

---

## 📌 Future Enhancements

* 📊 Candlestick charts (TradingView style)
* 🔔 Trade alerts (Telegram / Email)
* 📈 Multi-timeframe analysis
* 🎯 Entry / Stop-loss / Target suggestions
* 🔗 Broker integration (Zerodha API)

---

## 👨‍💻 Author

Developed as part of an AI-powered trading system project.

---

## ⭐ Support

If you found this useful, consider giving it a ⭐ on GitHub!

---