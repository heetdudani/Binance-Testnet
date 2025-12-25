# Binance Futures Testnet Trading Bot

A Python-based trading bot for **Binance USDT-M Futures Testnet**, built as part of a Junior Python Developer hiring assignment. The project supports **Market and Limit orders**, includes **robust logging and error handling**, and provides a **PyQt5-based GUI** for interactive order placement.

This project demonstrates practical experience with:
- Binance Futures API (Testnet)
- Order execution logic (Buy/Sell)
- Real-time market data fetching
- Clean, reusable Python architecture
- GUI-driven trading workflows

---

## Features

- ✅ Binance **USDT-M Futures Testnet** support
- ✅ Market and Limit orders
- ✅ Buy and Sell order sides
- ✅ Live price updates for selected symbols
- ✅ Symbol list fetched dynamically from Binance
- ✅ GUI built using **PyQt5**
- ✅ Detailed logging of API calls, responses, and errors
- ✅ Input validation and graceful error handling

---

## Tech Stack

- **Python 3.9+**
- **python-binance** (official Binance API wrapper)
- **PyQt5** (GUI)
- **Binance Futures Testnet**

---

## Project Structure

```
.
├── Tradeui.py          # Main application (GUI + trading logic)
├── config.py           # API credentials (Testnet only)
├── bot.log             # Application logs
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

---

## Setup Instructions

### 1️⃣ Create Binance Futures Testnet Account

- Register at Binance Futures Testnet
- Enable **USDT-M Futures Testnet**
- Generate API Key and Secret

> ⚠️ **Never use real (mainnet) API keys in this project**

---

### 2️⃣ Configure API Credentials

Update `config.py`:

```python
API_KEY = "YOUR_TESTNET_API_KEY"
SECRET_KEY = "YOUR_TESTNET_SECRET_KEY"
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
python-binance
PyQt5
```

---

## Running the Application

```bash
python Tradeui.py
```

This will launch a GUI where you can:
- Select a trading symbol (e.g., BTCUSDT)
- View live market price (auto-refresh every 5 seconds)
- Choose order type (Market / Limit)
- Enter quantity and price (for Limit orders)
- Place Buy or Sell orders

---

## Order Types Supported

### Market Order
- Executes immediately at current market price

### Limit Order
- Executes at a user-defined price
- Uses `GTC (Good Till Cancelled)` time-in-force

---

## Logging

All important events are logged to `bot.log`, including:
- API connection status
- Order placement attempts
- Successful order responses
- API and validation errors

Example log entry:
```
2025-01-10 14:22:10 - INFO - Order success | ID=123456 | Status=NEW | symbol=BTCUSDT | side=BUY | type=MARKET
```

---

## Error Handling

- Invalid inputs are blocked at UI level
- API failures are caught and logged
- User-friendly error messages shown in UI

---

## Security Notes

- This project is **strictly for Testnet use**
- API keys should be stored securely (environment variables recommended for production)
- No real funds are involved

---

## Possible Improvements

- Add Stop-Limit or OCO orders
- WebSocket-based live price streaming
- CLI-only mode (headless execution)
- Strategy layer (Grid / TWAP)
- Environment-based configuration management

---

## Author

**Heet Dudani**  
Python Developer

- GitHub: https://github.com/heetdudani

---

## Disclaimer

This project is for **educational and evaluation purposes only**. It is not financial advice and should not be used for live trading.

