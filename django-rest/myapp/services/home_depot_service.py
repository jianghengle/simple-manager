import json
import requests

def get_home_depot_price(item_id):
    url = 'https://www.homedepot.com/federation-gateway/graphql?opname=productClientOnlyProduct'
    headers = {
        'Content-Type': 'application/json',
        'x-experience-name': 'general-merchandise',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    payload = {
        "operationName": "productClientOnlyProduct",
        "variables": {
            "itemId": item_id
        },
        "query": "query productClientOnlyProduct($storeId: String, $itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput) { product(itemId: $itemId, dataSource: $dataSource, loyaltyMembershipInput: $loyaltyMembershipInput) { pricing(storeId: $storeId) { value  original }  }}"
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    data = json.loads(resp.text)
    return float(data['data']['product']['pricing']['value'])
