import socket
import threading
import json
import requests

# list to store traded stocks
traded_stocks = []
def print_traded_stocks():
    for trade in traded_stocks:
        print(f"{trade['type'].capitalize()} {trade['quantity']} shares of {trade['symbol']}")
# function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        # receive data from client
        data = client_socket.recv(1024)
        if not data:
            break
        # decode data and process buy/sell orders
        orders = json.loads(data.decode('utf-8'))
        for order in orders:
            if order['type'] == 'buy':
                # process buy order
                traded_stocks.append({'type': 'buy', 'symbol': order['symbol'], 'quantity': order['quantity']})
            elif order['type'] == 'sell':
                # process sell order
                traded_stocks.append({'type': 'sell', 'symbol': order['symbol'], 'quantity': order['quantity']})
        print_traded_stocks()

        # send updated stock prices to client
        stock_prices = get_stock_prices()
        client_socket.send(json.dumps(stock_prices).encode('utf-8'))


def print_traded_stocks():
    for trade in traded_stocks:
        print(f"{trade['type'].capitalize()} {trade['quantity']} shares of {trade['symbol']}")
# function to get real-time stock prices using a third-party API
def get_stock_prices():
    api_key = 'B5RU2NRH71WU34LZ'
    symbols = ['MSFT', 'AAPL', 'GOOG', 'IBM'] # add more symbols to this list
    stock_prices = {}
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        stock_prices[symbol] = data['Global Quote']['05. price']
    return stock_prices
# create server socket and bind to IP address and port number
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12541))
server_socket.listen(5)

# accept incoming connections from clients
while True:
    client_socket, client_address = server_socket.accept()
    # create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()