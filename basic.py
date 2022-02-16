from datetime import datetime
from tinyman.v1.client import TinymanMainnetClient
from tinyman.v1.pools import Pool
from algosdk.v2client import algod
import math
import sys
import os
os.system("")

import private
from config.config import * # Just to get linter (?) to see my GLOBALS CONSTANTS

algo_client = algod.AlgodClient(algod_token, algod_address, headers={'User-Agent': 'algosdk'})
client = TinymanMainnetClient(algod_client=algo_client, user_address=private.account['address'])

# constants
ALGO = client.fetch_asset(0)
MA = 1000000

class printer:
    def __init__(self, first = True):
        self.last = ""
        self.first = first
    
    def pt(self, text, newline = False):
        if (newline or not self.last == text) and not self.first:
            print()
        self.first = False
        self.last = text
        current_time = datetime.now().strftime("%H:%M:%S")
        sys.stdout.write("\r%s" %(current_time + ": " + text))
        sys.stdout.flush()


def optin(asset, tp):
    if client.is_opted_in():
        tp.pt(f'App is already opted in')
    else:
        optin_tx = client.prepare_app_optin_transactions()
        optin_tx.sign_with_private_key(private.account['address'], private.account['private_key'])
        result = client.submit(optin_tx, wait=True)
    if client.asset_is_opted_in(asset):
        tp.pt(f'Asset {asset} already opted in')
    else:
        optin_tx = client.prepare_asset_optin_transactions(asset)
        optin_tx.sign_with_private_key(private.account['address'], private.account['private_key'])
        result = client.submit(optin_tx, wait=True)


def check_pool(asset):
    try:
        asset_pool = client.fetch_pool(ALGO,asset)
        if asset_pool.fetch_state():
            return True
    except:
        return False
    return False

def get_liquidity(assetPool: Pool):
    try:
        assetPool.refresh()
        info = assetPool.info()
        if info['asset2_id'] == 0:
            return 2*info['asset2_reserves']
        if info['asset1_id'] == 0:
            return 2*info['asset1_reserves']
        return -100
    except:
        return -100


def get_price(asset_pool: Pool):
    try:
        price = asset_pool.fetch_fixed_input_swap_quote(ALGO(1_000_000), slippage=0.02)
        return help_get_price(price.amount_in)/help_get_price(price.amount_out)
    except Exception as err:
        print()
        print(err)
        return math.inf

def help_get_price(ammountasset):
    return float(ammountasset.__repr__().split("'")[1])


def buy_asset(asset_to, amount, asset_from = ALGO, slippage = 0.9):
    asset_pool = client.fetch_pool(asset_from,asset_to)
    quote = asset_pool.fetch_fixed_input_swap_quote(asset_from(amount),slippage = slippage)
    transaction_group = asset_pool.prepare_swap_transactions_from_quote(quote)
    transaction_group.sign_with_private_key(private.account['address'], private.account['private_key'])
    result = client.submit(transaction_group, wait=True)
    excess = asset_pool.fetch_excess_amounts()

    if asset_to in excess:
        amount = excess[asset_to]
        if amount > 0:
            transaction_group = asset_pool.prepare_redeem_transactions(amount)
            transaction_group.sign_with_private_key(private.account['address'], private.account['private_key'])
            result = client.submit(transaction_group, wait=True)