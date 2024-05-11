import tkinter as tk
import requests

class StockPortfolio:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Portfolio Tracker")
        self.stocks = {}

        self.symbol_label = tk.Label(master, text="Stock Symbol:")
        self.symbol_label.grid(row=0, column=0)
        self.symbol_entry = tk.Entry(master)
        self.symbol_entry.grid(row=0, column=1)

        self.add_button = tk.Button(master, text="Add Stock", command=self.add_stock)
        self.add_button.grid(row=0, column=2)

        self.stock_listbox = tk.Listbox(master, width=40)
        self.stock_listbox.grid(row=1, columnspan=3)

        self.remove_button = tk.Button(master, text="Remove Stock", command=self.remove_stock)
        self.remove_button.grid(row=2, column=1)

        self.refresh_button = tk.Button(master, text="Refresh Prices", command=self.refresh_prices)
        self.refresh_button.grid(row=2, column=2)

        self.message_label = tk.Label(master, text="")
        self.message_label.grid(row=3, columnspan=3)

    def add_stock(self):
        symbol = self.symbol_entry.get().upper()
        if symbol in self.stocks:
            self.message_label.config(text="Stock already exists in the portfolio.")
            return

        try:
            price = self.get_stock_price(symbol)
            self.stocks[symbol] = price
            self.stock_listbox.insert(tk.END, f"{symbol}: ${price:.2f}")
            self.message_label.config(text="Stock added successfully.")
        except Exception as e:
            self.message_label.config(text=f"Failed to add stock: {e}")

    def remove_stock(self):
        selected_index = self.stock_listbox.curselection()
        if not selected_index:
            self.message_label.config(text="Please select a stock to remove.")
            return

        symbol = self.stock_listbox.get(selected_index[0]).split(":")[0].strip()
        del self.stocks[symbol]
        self.stock_listbox.delete(selected_index)
        self.message_label.config(text="Stock removed successfully.")

    def refresh_prices(self):
        for i, symbol in enumerate(self.stocks.keys()):
            try:
                price = self.get_stock_price(symbol)
                self.stocks[symbol] = price
                self.stock_listbox.delete(i)
                self.stock_listbox.insert(i, f"{symbol}: ${price:.2f}")
            except Exception as e:
                self.message_label.config(text=f"Failed to refresh prices: {e}")

    def get_stock_price(self, symbol):
        api_key = "NI43CWV5J9OP6Y31"
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if "Global Quote" in data:
            return float(data["Global Quote"]["05. price"])
        else:
            raise Exception("Invalid response from API")

def main():
    root = tk.Tk()
    app = StockPortfolio(root)
    root.mainloop()

if __name__ == "__main__":
    main()