from django.shortcuts import render
from . import services

# Create your views here.

def contact(request):
    form = services.AddressForm()
    totalSatoshi = 0
    transactionList = []
    transactionValue = {}
    bitcoinValueAtTimeOfTransactions = 0
    bitcoinValueNow = 0
    totalSatoshiValue = 0

    if request.method == "POST":
        form = services.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            totalSatoshi = services.get_account_balance(address)
            transactionList = transactions(address)
            for transaction in transactionList:
                transactionValue[transaction] = getTransactionValue(transaction, address)
                bitcoinValueAtTimeOfTransactions += services.bitcoin_to_usd_at_time_of_transaction(transactionValue[transaction]['timestamp'], transactionValue[transaction]['satoshiValue'])
                totalSatoshiValue += transactionValue[transaction]['satoshiValue']
            bitcoinValueNow += services.bitcoin_to_usd_now(totalSatoshiValue)

            

    return render(request, 'arbitrage/basic.html', {'exchanges': [
        {
            'name': 'bitfinex', 
            'price': services.get_info("btcusd", "https://api.bitfinex.com/v1/pubticker/")['last_price'],
            'date': services.convert_timestamp_to_date(services.get_info("btcusd", "https://api.bitfinex.com/v1/pubticker/")['timestamp'])
        },
        {
            'name': 'bitstamp',
            'price': services.get_info("btcusd", "https://www.bitstamp.net/api/v2/ticker/")['last'],
            'date': services.convert_timestamp_to_date(services.get_info("btcusd", "https://www.bitstamp.net/api/v2/ticker/")['timestamp'])
        }
    ], 'difference': {
            'absolute': services.compare_price_absolute(services.get_info("btcusd", "https://api.bitfinex.com/v1/pubticker/")['last_price'], services.get_info("btcusd", "https://www.bitstamp.net/api/v2/ticker/")['last']), 
            'percentage': services.compare_price_percentage(services.get_info("btcusd", "https://api.bitfinex.com/v1/pubticker/")['last_price'], services.get_info("btcusd", "https://www.bitstamp.net/api/v2/ticker/")['last'])
        }, 'geodata': {
                'ip': (services.ip_test(request))
                # 'country': (services.api_test(request)['country_name']),
                # 'latitude': (services.api_test(request)['latitude']),
                # 'longitude': (services.api_test(request)['longitude']),
                # 'is_cached': (services.is_cached(request))
        },
        'form': form,
        'accountBalance': totalSatoshi,
        'transactions': transactionList,
        'transactionValues': transactionValue,
        'bitcoinValue': bitcoinValueAtTimeOfTransactions,
        'bitcoinValueNow': bitcoinValueNow
    })

def transactions(address):
    info = services.get_unspent_transactions(address)
    transactionList = []
    for tx in info['unspent_outputs']:
        transactionList.append(tx['tx_hash_big_endian'])
    return transactionList

def getTransactionValue(transaction, address):
    info = services.get_transaction_details(transaction)
    transactionValue = {}
    value = 0
    for output in info['out']:
        if output['addr'] == address:
            value += output['value']
    transactionValue = {'satoshiValue': value, 'timestamp': info['time']}
    return transactionValue    