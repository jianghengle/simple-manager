import os, datetime, time
import json
import urllib.parse
import urllib.request


SERVER = 'https://myapi.vanityart.com'

BATCH_SIZE = 100
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
    now = datetime.datetime.utcnow()
    date = datetime.date(now.year, now.month, now.day).isoformat()
    batch = []
    for product in products:
        for channel in product['channels']:
            if channel['channel']['name'] == 'Home Depot':
                if ('latestPrice' not in channel) or (not channel['latestPrice']['date'] == date):
                    batch.append({'productId': product['product']['id'], 'channelId': channel['channel']['id']})
                    if len(batch) == BATCH_SIZE:
                        return batch
    return batch

# lambda handler: program entry
def lambda_handler(event, context):
    token = get_auth_token()
    products = url_get('/myapp/get-products-with-latest-prices/', token=token)
    batch = collect_batch(products)
    print('Batch size: ' + str(len(batch)))
    for item in batch:
        product_id = str(item['productId'])
        channel_id = str(item['channelId'])
        try:
            url_post('/myapp/update-product-latest-price/' + product_id + '/' + channel_id + '/', {}, token=token)
        except:
            print('Error when processing ' + str(item))
        time.sleep(SLEEP_TIME)
    print('Done!')
