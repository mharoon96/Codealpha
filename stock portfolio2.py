import tkinter as tk
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("800x600")

        # Create and place widgets
        self.label = tk.Label(self.root, text="Welcome to Portfolio Tracker!")
        self.label.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Stock", command=self.add_stock)
        self.add_button.pack()

        self.remove_button = tk.Button(self.root, text="Remove Stock", command=self.remove_stock)
        self.remove_button.pack()

        self.plot_button = tk.Button(self.root, text="Plot Portfolio", command=self.plot_portfolio)
        self.plot_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack()

        # Initialize portfolio data
        self.portfolio = []

    def add_stock(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Stock")

        label_symbol = tk.Label(add_window, text="Symbol:")
        label_symbol.grid(row=0, column=0)
        self.entry_symbol = tk.Entry(add_window)
        self.entry_symbol.grid(row=0, column=1)

        label_quantity = tk.Label(add_window, text="Quantity:")
        label_quantity.grid(row=1, column=0)
        self.entry_quantity = tk.Entry(add_window)
        self.entry_quantity.grid(row=1, column=1)

        label_price = tk.Label(add_window, text="Price:")
        label_price.grid(row=2, column=0)
        self.entry_price = tk.Entry(add_window)
        self.entry_price.grid(row=2, column=1)

        add_button = tk.Button(add_window, text="Add", command=self.add_to_portfolio)
        add_button.grid(row=3, column=0, columnspan=2)

    def remove_stock(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Stock")

        label_symbol = tk.Label(remove_window, text="Symbol:")
        label_symbol.grid(row=0, column=0)
        self.entry_remove_symbol = tk.Entry(remove_window)
        self.entry_remove_symbol.grid(row=0, column=1)

        remove_button = tk.Button(remove_window, text="Remove", command=self.remove_from_portfolio)
        remove_button.grid(row=1, column=0, columnspan=2)

    def add_to_portfolio(self):
        symbol = self.entry_symbol.get()
        quantity = int(self.entry_quantity.get())
        price = float(self.entry_price.get())
        
        # Fetch real-time data using Alpha Vantage API
        api_key = 'YOUR_API_KEY'  # Get your API key from Alpha Vantage
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'Global Quote' in data:
                current_price = float(data['Global Quote']['05. price'])
                print("Current Price:", current_price)
                self.portfolio.append({'symbol': symbol, 'quantity': quantity, 'price': price, 'current_price': current_price})
                print(f"Added {quantity} shares of {symbol} at ${price} each to the portfolio.")
            else:
                print("Error: Unable to fetch data for symbol", symbol)
        else:
            print("Error: Unable to fetch data from API")

    def remove_from_portfolio(self):
        symbol_to_remove = self.entry_remove_symbol.get()
        for stock in self.portfolio:
            if stock['symbol'] == symbol_to_remove:
                self.portfolio.remove(stock)
                print(f"Removed {symbol_to_remove} from the portfolio.")
                break
        else:
            print(f"Error: {symbol_to_remove} not found in the portfolio.")

    def plot_portfolio(self):
        symbols = [stock['symbol'] for stock in self.portfolio]
        quantities = [stock['quantity'] for stock in self.portfolio]
        prices = [stock['price'] for stock in self.portfolio]
        
        fig, ax = plt.subplots()
        ax.bar(symbols, quantities, color='b', label='Quantity')
        ax2 = ax.twinx()
        ax2.plot(symbols, prices, color='r', marker='o', label='Price')
        
        ax.set_ylabel('Quantity')
        ax2.set_ylabel('Price ($)')
        ax.set_xlabel('Symbol')
        
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def save_portfolio(self):
        with open('portfolio.json', 'w') as f:
            json.dump(self.portfolio, f)
        print("Portfolio saved successfully.")

    def load_portfolio(self):
        try:
            with open('portfolio.json', 'r') as f:
                self.portfolio = json.load(f)
            print("Portfolio loaded successfully.")
        except FileNotFoundError:
            print("No saved portfolio found.")

def main():
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
