import redis
import json
from ib_insync import *
import asyncio
import time
from pprint import pprint

# Fixed clientId for consistent sessions
CLIENT_ID = 1

# Patch asyncio to prevent event loop issues with ib_insync
util.patchAsyncio()

# connect to Interactive Brokers
ib = IB()

# Function to handle connection and reconnection
def connect_ib():
    try:
        if ib.isConnected():
            ib.disconnect()  # Ensure clean disconnect before reconnecting
        print("Connecting to IBKR...")
        ib.connect('127.0.0.1', 7497, clientId=CLIENT_ID, timeout=10)
        print("Connected to IBKR.")
    except Exception as e:
        print(f"Connection failed: {e}")

# Initial connection
connect_ib()

# Monitor connection status and reconnect if needed
async def monitor_connection():
    while True:
        if not ib.isConnected():
            print("IBKR connection lost. Attempting to reconnect...")
            connect_ib()
        await asyncio.sleep(5)  # Check every 5 seconds

# Event handler for when IBKR connection is disconnected
def on_disconnected():
    print("Disconnected from IBKR. Waiting for reconnection...")

# Set up event handlers
ib.disconnectedEvent += on_disconnected

# Connect to Redis and subscribe to tradingview messages
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('tradingview')

# Define your passphrase here
EXPECTED_PASSPHRASE = 'abcdefgh'
ORDER_CONTRACTS = 1

def getContract(ticker):
    future_date = '202409'
    if 'mes' in ticker.lower():
        return Future('MES', future_date, 'CME')
    elif 'mnq' in ticker.lower():
        return Future('MNQ', future_date, 'CME')
    else:
        return Stock(ticker, 'SMART', 'USD')

async def check_messages():
    message = p.get_message()
    if message is not None and message['type'] == 'message':
        if not ib.isConnected():
            print('ERROR: Skip the trade due to lost TOS conn:')
            pprint(message['data'])
            return

        try:
            message_data = json.loads(message['data'])
        except json.JSONDecodeError:
            print("ERROR, the message is: ", message)
            return

        # Check if the passphrase matches
        if message_data.get('passphrase') != EXPECTED_PASSPHRASE:
            print("Invalid passphrase. Access denied.")
            return
        #pprint("Processing message:")
        #pprint(message_data)

        pprint('Place Order: {} {} amount:{}'.format(message_data['strategy']['order_action'], message_data['ticker'], 1))
        contract = getContract(message_data['ticker'])
        order = MarketOrder(message_data['strategy']['order_action'], ORDER_CONTRACTS)
        order.outsideRth = True
        ib.placeOrder(contract, order)


async def run_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

async def main():
    await asyncio.gather(
        run_periodically(1, check_messages),  # Check for new messages every second
        monitor_connection()  # Monitor IBKR connection status
    )

asyncio.run(main())

ib.run()
