import os, datetime, time
import json
import random
import requests
import urllib.parse
import urllib.request


SERVER = 'https://myapi.vanityart.com'

BATCH_SIZE = 50
SLEEP_TIME = 3

  
def url_get(path, token=None):
    req =  urllib.request.Request(SERVER + path)
    if token:
        req.add_header('Authorization', 'Token ' + token)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def url_post(path, data, token=None):
    req_data = urllib.parse.urlencode(data).encode()
    req =  urllib.request.Request(SERVER + path, data=req_data)
    if token:
        req.add_header('Authorization', 'Token ' + token)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def get_auth_token():
    data = {'username': 'invoice@vanityart.com', 'password': os.environ['INVOICE_USER_PASSWORD']}
    user = url_post('/myapp/api-token-auth/', data)
    return user['token']

def collect_batch(products):
    random.shuffle(products)
    now = datetime.datetime.utcnow()
    date = datetime.date(now.year, now.month, now.day).isoformat()
    batch = []
    for product in products:
        for channel in product['channels']:
            if channel['channel']['name'] == 'Wayfair' and product['product']['wayfairSku']:
                if ('latestPrice' not in channel) or (not channel['latestPrice']['date'] == date):
                    batch.append({'productId': product['product']['id'], 'wayfairSku': product['product']['wayfairSku'], 'wayfairOptionName': product['product']['wayfairOptionName'], 'channelId': channel['channel']['id']})
                    if len(batch) == BATCH_SIZE:
                        return batch
    return batch

def get_wayfair_price(sku, option_name):
    option_id = None
    if option_name and (not option_name == 'NSlashA'):
        option_id = get_wayfair_option_id(sku, option_name)
    url = 'https://www.wayfair.com/graphql?hash=598e6903338c24d0259c8715bb5c81ec%233ef9a62b101d96979908ae465d91d73f%23d33d6918bae2e899861e27b6091cae79%23bf4fd0f65bc5fa3efc99c445ebb971dd'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en,q=0.9',
        'apollographql-client-name': '@wayfair/sf-ui-product-details',
        'apollographql-client-version': 'b650c76c71028869eb2edc9d8a7425b961721d2e',
        'content-type': 'application/json',
        'origin': 'https://www.wayfair.com',
        'referer': 'https://www.wayfair.com/lighting/pdp/sand-stable-martell-20-light-wagon-wheel-chandelier-w002491977.html?rtype=8&redir=W002491977&piid=1495465848',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'use-web-hash': 'true',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        'x-parent-txid': 'I/cmXGLE/c+DERrmwlYDAg==',
    }
    payload = {
        "variables": {
            "sku": sku,
            "additionalSkus": [sku],
            "fullyConfigureOptions": False
        }
    }
    if option_id:
        payload['variables']['selectedOptionsIds'] = [option_id]
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    data = json.loads(resp.text)
    price_value = data['data']['product']['optionMatchedProducts'][0]['pricing']['priceBlockElements'][0]['display']['value']
    stock_status = data['data']['product']['optionMatchedProducts'][0]['inventory']['stockStatus']
    return (price_value, stock_status == 'IN_STOCK')

def get_wayfair_option_id(sku, option_name):
    print('get_wayfair_option_id: ' + sku + ', ' + option_name)
    url = 'https://www.wayfair.com/graphql?hash=24e17b1e9c2cffd32c2cab2189a5e917%2316dd774cea9d3bd2c887f99be034a1de'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en,q=0.9',
        'apollographql-client-name': '@wayfair/sf-ui-product-details',
        'apollographql-client-version': 'b650c76c71028869eb2edc9d8a7425b961721d2e',
        'content-type': 'application/json',
        'origin': 'https://www.wayfair.com',
        'referer': 'https://www.wayfair.com/lighting/pdp/sand-stable-martell-20-light-wagon-wheel-chandelier-w002491977.html?rtype=8&redir=W002491977&piid=1495465848',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'use-web-hash': 'true',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        'x-parent-txid': 'I/cmXGLE/c+DERrmwlYDAg==',
    }
    payload = {
        "variables": {
            "sku": sku,
            "withLegacySpecificationsData": False
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    data = json.loads(resp.text)
    options = data['data']['product']['manufacturerPartNumber']['partNumberOptions']
    for option in options:
        if option[4] == option_name:
            return option[2]
    return None

# lambda handler: program entry
def lambda_handler(event, context):
    token = get_auth_token()
    products = url_get('/myapp/get-products-with-latest-prices/', token=token)
    batch = collect_batch(products)
    print('Batch size: ' + str(len(batch)))
    print(json.loads(requests.get('https://api.ipify.org?format=json').text))
    for item in batch:
        product_id = str(item['productId'])
        channel_id = str(item['channelId'])
        wayfair_sku = str(item['wayfairSku'])
        wayfair_option_name = str(item['wayfairOptionName'])
        print(item)
        try:
            (price_value, availability) = get_wayfair_price(wayfair_sku, wayfair_option_name)
            print(price_value)
            print(availability)
            availability_status = 'In Stock' if availability else 'Out of Stock'
            print(availability_status)
            url_post('/myapp/update-product-latest-price/' + product_id + '/' + channel_id + '/', {'priceValue': price_value, 'availability': availability_status}, token=token)
        except Exception as e:
            print(e)
            print('Error when processing ' + str(item))
        time.sleep(SLEEP_TIME + random.randrange(10))
    print('Done!')
