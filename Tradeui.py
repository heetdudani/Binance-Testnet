import sys
import config
from binance import Client
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QRadioButton, QPushButton, 
    QDoubleSpinBox, QGroupBox, QFormLayout, QMessageBox, QTextEdit,
    QComboBox 
)
from PyQt5.QtCore import QTimer 
import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

api_key = config.API_KEY
api_secret = config.SECRET_KEY

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        try:
            self.client.futures_account()
            logging.info("Connected")
        except Exception as e:
            logging.info(f"Connection failed: {e}")

    def get_symbols(self):
        try:
            info = self.client.futures_exchange_info()
            symbols = [s["symbol"] for s in info["symbols"]]
            symbols.sort()
            return symbols
        except Exception as e:
            logging.error(f"Failed to fetch symbols: {e}")
            return []

    def get_symbol_price(self, symbol):
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logging.error(f"Failed to fetch price for {symbol}: {e}")
            return None

    def Place_Order(self, symbol, order_type, side, quantity, price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type=order_type,
                        quantity=quantity
                )
            else:
                order = self.client.futures_create_order(
                                        symbol=symbol,
                                        side=side,
                                        type=order_type,
                                        quantity=quantity,
                                        price=price,
                                        timeInForce="GTC"
                                        )
            logging.info(f"Order success | ID={order['orderId']} | Status={order['status']} | symbol ={symbol} | side ={side} | type={order_type}")
        except Exception as e:
            order = {'status': "error", "Error": str(e)}
            logging.info(f"Order Failed : {e}")
        return order
            

class TradeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.user = BasicBot(api_key, api_secret)

        self.setWindowTitle("Order Entry Window")
        self.setGeometry(100, 100, 400, 550) 
        self.init_ui()
        
        self.update_price_label()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.symbol_combo = QComboBox()
        symbols = self.user.get_symbols()
        if symbols:
            self.symbol_combo.addItems(symbols)
            index = self.symbol_combo.findText("BTCUSDT")
            if index >= 0:
                self.symbol_combo.setCurrentIndex(index)
        else:
            self.symbol_combo.addItem("Error Fetching Symbols")
        
        self.symbol_combo.currentTextChanged.connect(self.update_price_label)

        self.live_price_label = QLabel("Current Price: Loading...")
        self.live_price_label.setStyleSheet("font-size: 14px; font-weight: bold; color: blue;")

        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(0.01, 100000.00)
        self.quantity_input.setPrefix("Qty: ")

        type_group = QGroupBox("Order Type")
        type_layout = QHBoxLayout()
        
        self.radio_market = QRadioButton("MARKET")
        self.radio_limit = QRadioButton("LIMIT")
        self.radio_market.setChecked(True)  

        self.radio_market.toggled.connect(self.toggle_price_input)
        self.radio_limit.toggled.connect(self.toggle_price_input)

        type_layout.addWidget(self.radio_market)
        type_layout.addWidget(self.radio_limit)
        type_group.setLayout(type_layout)

        self.price_label = QLabel("Limit Price:")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 1000000.00)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("$")
        
        self.price_input.setEnabled(False)

        form_layout = QFormLayout()
        form_layout.addRow("Symbol:", self.symbol_combo)      # Changed to combo box
        form_layout.addRow("Market Price:", self.live_price_label) # Added price label
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow(type_group)
        form_layout.addRow(self.price_label, self.price_input)

        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        
        self.btn_buy = QPushButton("BUY")
        self.btn_buy.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_buy.clicked.connect(lambda: self.process_order("BUY"))
        
        self.btn_sell = QPushButton("SELL")
        self.btn_sell.setStyleSheet("background-color: #F44336; color: white; font-weight: bold; padding: 10px;")
        self.btn_sell.clicked.connect(lambda: self.process_order("SELL"))

        btn_layout.addWidget(self.btn_buy)
        btn_layout.addWidget(self.btn_sell)
        
        main_layout.addLayout(btn_layout)

        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        self.display_area.setPlaceholderText("Order details will appear here...")
        
        main_layout.addWidget(QLabel("Order Output:"))
        main_layout.addWidget(self.display_area)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price_label)
        self.timer.start(5000)  

    def update_price_label(self):
        symbol = self.symbol_combo.currentText()
        if not symbol:
            return

        price = self.user.get_symbol_price(symbol)
        if price:
            self.live_price_label.setText(f"{price:.2f}")
        else:
            self.live_price_label.setText("N/A")

    def toggle_price_input(self):
        if self.radio_limit.isChecked():
            self.price_input.setEnabled(True)
        else:
            self.price_input.setEnabled(False)

    def process_order(self, side):
        symbol = self.symbol_combo.currentText().upper()
        quantity = self.quantity_input.value()
        order_type = "LIMIT" if self.radio_limit.isChecked() else "MARKET"
        price = self.price_input.value()

        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please select a Symbol.")
            return
        
        if quantity <= 0:
            QMessageBox.warning(self, "Input Error", "Quantity must be greater than 0.")
            return

        logging.info(f"Placing {side} | {symbol} | qty={quantity}")

        order = self.user.Place_Order(symbol, order_type, side, quantity, price=price)
        
        if order.get('status') != 'error':
            output_text = (
                f"--- NEW ORDER ---\n"
                f"Symbol:   {symbol}\n"
                f"Order ID: {order['orderId']}\n"
                f"Side:     {side}\n"
                f"Quantity: {quantity}\n"
                f"Type:     {order_type}\n"
                f"Status:   {order['status']}\n"
            )

            if order_type == "LIMIT":
                output_text += f"Price:    {price}\n"
        
            output_text += "-----------------"
        else:
            output_text = (f"Order Fail : {order.get('Error')}\n")
            output_text += "-----------------"
        self.display_area.append(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradeUI()
    window.show()
    sys.exit(app.exec_())