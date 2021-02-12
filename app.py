import config, requests, json, math
from chalice import Chalice

app = Chalice(app_name='tradingview-webhook')

# PAPER KEYS
API_KEY = 'PKIQYUB9B73K0DIKAXHM'
SECRET_KEY = 'uEk5A4Z7hZMrUNcACrhWXyeSs1EPUtKhXOe793kC'
BASE_URL = "https://paper-api.alpaca.markets"

# THE REAL STUFF
# API_KEY = 'AKFAEM1PPJHBUPR3XDQD'
# SECRET_KEY = 'kygbCp4lnkvGYANTASotvoPwj0RSuwWW8RMoZDhU'
# BASE_URL = "https://api.alpaca.markets"

ORDERS_URL = "{}/v2/orders".format(BASE_URL)
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/action', methods=['POST'])
def stock_action():
    request = app.current_request
    webhook_message = request.json_body

    if webhook_message['action'] == 'buy':

        # load account data
        a = requests.get(ACCOUNT_URL, headers=HEADERS)
        account_data = json.loads(a.content)

        equity = float(account_data['last_equity'])

        stock_price = float(webhook_message['close'])

        max_buy = equity * .05

        max_shares = math.floor(max_buy / stock_price)

        cash = float(account_data['buying_power'])

        if max_shares > 0 and cash > max_buy:
            data = {
                "symbol": webhook_message['ticker'],
                "qty": max_shares,
                "side": webhook_message['action'],
                "type": "limit",
                "limit_price": webhook_message['close'],
                "time_in_force": "gtc",
                "order_class": "bracket",
                "take_profit": {
                    "limit_price": webhook_message['close'] * 1.04
                },
                "stop_loss": {
                    "stop_price": webhook_message['close'] * 0.98,
                }
            }

            r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

            response = json.loads(r.content)

            return {
                'message': 'action completed',
                'webhook_messaage': data,
                'id': response['id'],
                'client_order_id': response['client_order_id']
            }
        else:
            return {
                'message': 'cant afford this stock'
            }
    else:
        return {
            'message': 'we dont like the stock'
        }