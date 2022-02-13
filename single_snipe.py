from time import sleep
from tinyman.v1.client import TinymanMainnetClient
from algosdk.v2client import algod
import math
import yaml

from basic import *
import private
from config.config import * # Just to get linter (?) to see my GLOBALS CONSTANTS


algo_client = algod.AlgodClient(algod_token, algod_address, headers={'User-Agent': 'algosdk'})
client = TinymanMainnetClient(algod_client=algo_client, user_address=private.account['address'])

# constants
ALGO = client.fetch_asset(0)
MA = 1000000
tp = printer()


def load_config():
    if len(sys.argv) > 1:
        with open("./config/" + sys.argv[1] + ".yaml", "r") as file:
            config = yaml.safe_load(file)
            globals().update(config)
            text = f'Account: {private.account["address"][0:8]}, Amount: {AMOUNT/MA} algo, ID: {ASSET}, Max price: {MAX_PRICE}, Min. liq.: {MIN_LIQUIDITY/MA}'
            tp.pt(text)
    else:
        print('Missing argument.')
        raise ValueError

def scouter(asset):
    pool_bool = False
    while True:
        pool_bool = check_pool(asset)
        if pool_bool:
            break
        tp.pt("Looking for pool")
        sleep(GLOBAL_TIME)

    tp.pt('Pool exists.')
    
    assetPool = client.fetch_pool(ALGO,asset)
    liqudity = 0
    while True:
        liqudity = get_liquidity(assetPool)
        if liqudity > MIN_LIQUIDITY:
            break
        text = f'Pool has insufficient liquduity: {round(liqudity/MA)} < {MIN_LIQUIDITY/MA}'
        tp.pt(text)
        sleep(GLOBAL_TIME)

    tp.pt(f'Pool has sufficient liquidity: {round(liqudity/MA)}')

    price = math.inf
    while True:
        price = get_price(assetPool)
        liqudity = get_liquidity(assetPool)
        if price < MAX_PRICE:
            if liqudity > MIN_LIQUIDITY:
                algoAmount = AMOUNT - 1 * MA
                tp.pt(f'Price is:  {price}. Spending {algoAmount} ALGO. Commencing buy.')
                try:
                    buy_asset(asset, algoAmount)
                    tp.pt("Purchase complete.")
                    return
                except Exception as err:
                    tp.pt(f'Purchase failed with error {err}')
            text = f'WARNING: Pool has lost liquduity: {round(liqudity/MA)} < {MIN_LIQUIDITY/MA}'
        else:
            text = f'Pool too high price: {price} > {MAX_PRICE}'

        tp.pt(text)
        sleep(GLOBAL_TIME)


def main():
    load_config()
    if not LOADED:
        tp.pt("You have not supplied a valid config")
        raise TypeError
    optin(ASSET, tp)    
    asset = client.fetch_asset(ASSET)
    scouter(asset)

if __name__ == '__main__':
    main()