import socket
import json

# create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12541))

# send list of buy orders to server
orders = [
    {'type': 'sell', 'symbol': 'AAPL', 'quantity': 10},
    {'type': 'buy', 'symbol': 'MSFT', 'quantity': 5},
    {'type': 'sell', 'symbol': 'GOOG', 'quantity': 2}
]

client_socket.send(json.dumps(orders).encode('utf-8'))

# receive real-time stock updates from server
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    # decode data and print updated stock prices
    stock_prices = json.loads(data.decode('utf-8'))
    print(stock_prices)