import requests
import json
import datetime
from decimal import Decimal
from django.core.cache import cache
from django import forms

def get_info(ticker, exchange):
    url = exchange + ticker
    response = requests.request("GET", url)
    info = json.loads(response.text)
    return info

def convert_timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(
        round(float(timestamp))
    )
    return date

def compare_price_absolute(price_1, price_2):
    difference = float(price_1) - float(price_2)
    return '{0:.2f}'.format(Decimal(difference))

def compare_price_percentage(price_1, price_2):
    percentage = float(price_1)/float(price_2)
    percentage -= 1
    percentage = percentage * 100
    return  round(percentage, 2)

def api_test(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('http://freegeoip.net/json/%s' % ip_address)
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']
    return geodata

def ip_test(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('https://api.ipify.org?format=json')
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']
    return geodata

def is_cached(request):
    is_cached = ('geodata' in request.session)
    return is_cached

def get_account_balance(address):
    if is_in_cache('balance_' + address):
        return cache.get('balance_' + address)
    else:
        response = requests.get('https://blockchain.info/q/addressbalance/%s' % address)
        accountBalance = response.text
        cache.set(('balance_' + address), int(accountBalance)/100000000, 300)
        return int(accountBalance)/100000000


def get_unspent_transactions(address):
    if is_in_cache('transactions_' + address):
        return cache.get('transactions_' + address)
    else:
        response = requests.get('https://blockchain.info/unspent?active=%s' % address)
        info = json.loads(response.text)
        cache.set(('transactions_' + address), info, 300)
        return info

def get_transaction_details(transaction):
    if is_in_cache(transaction):
        return cache.get(transaction)
    else:
        response = requests.get('https://blockchain.info/rawtx/%s' % transaction)
        info = json.loads(response.text)
        cache.set(transaction, info) # Data will never change on a transaction so can be cached indefinitely 
        return info

def getPriceOfBitcoinAtTimestamp(timestamp):
    if is_in_cache('price_at_' + str(timestamp)):
        return cache.get('price_at_' + str(timestamp))
    else:
        response = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&tsyms=USD&markets=Bittrex&ts=%s' % timestamp)
        info = json.loads(response.text)
        cache.set(('price_at_' + str(timestamp)), int(info['BTC']['USD']))
        return int(info['BTC']['USD'])

def bitcoin_to_usd_at_time_of_transaction(timestamp, satoshiValue):
    bitcoinValueAtTimestamp = getPriceOfBitcoinAtTimestamp(timestamp)
    usdValue = (bitcoinValueAtTimestamp * satoshiValue)/100000000
    return usdValue

def bitcoin_value(address):
    transactions = get_unspent_transactions(address)
    usdValue = 0
    for transaction in transactions:
        transactionInfo = get_transaction_details(transaction)
        for output in transactionInfo['out']:
            if output['addr'] == address:
                usdValue += bitcoin_to_usd_at_time_of_transaction(transactionInfo['time'], (int(output['value'])/100000000))
    return usdValue

def is_in_cache(key):
    if cache.get(key):
        return True
    else:
        return False


def bitcoin_value_now():
    if is_in_cache('bitcoinValue'):
        return cache.get('bitcoinValue')
    else:
        response = requests.get('https://api.coinmarketcap.com/v2/ticker/?sort=id&limit=1')
        info = json.loads(response.text)
        cache.set('bitcoinValue', int(info['data']['1']['quotes']['USD']['price']), 300)
        return int(info['data']['1']['quotes']['USD']['price'])


def bitcoin_to_usd_now(satoshiValue):
    usdValue = (bitcoin_value_now() * satoshiValue)/100000000
    return usdValue

class AddressForm(forms.Form):
    address = forms.CharField()



