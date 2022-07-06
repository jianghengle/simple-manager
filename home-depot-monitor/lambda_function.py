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
            if channel['channel']['name'] == 'Home Depot' and product['product']['homeDepotItemId']:
                if ('latestPrice' not in channel) or (not channel['latestPrice']['date'] == date):
                    batch.append({'productId': product['product']['id'], 'homeDepotItemId': product['product']['homeDepotItemId'], 'channelId': channel['channel']['id']})
                    if len(batch) == BATCH_SIZE:
                        return batch
    return batch

def get_home_depot_price(item_id):
    url = 'https://www.homedepot.com/federation-gateway/graphql?opname=productClientOnlyProduct'
    headers = {
        'content-type': 'application/json',
        'x-experience-name': 'general-merchandise',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'x-hd-dc': 'hd-home',
        'x-api-cookies': '{"x-user-id":"01563a8a-0ded-f5e6-e696-9be2053be8ae"}',
        'x-current-url': '/p/Vanity-Art-Limoges-28-in-4-lights-Brass-Dust-Vanity-Light-with-Glass-Shade-10004BD-C01/318171244',
        'x-debug': 'false',
        'referer': 'https://www.homedepot.com/p/Vanity-Art-Limoges-28-in-4-lights-Brass-Dust-Vanity-Light-with-Glass-Shade-10004BD-C01/318171244',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en,q=0.9',
        'apollographql-client-name': 'hd-home',
        'apollographql-client-version': '0.0.0',

    }
    payload = {
        "operationName": "productClientOnlyProduct",
        "variables": {
            "itemId": item_id,
            "skipKPF": False,
            "skipSpecificationGroup": False,
            "skipSubscribeAndSave": False,
            "storeId": "4712",
            "zipCode": "98011"
        },
        "query": 'query productClientOnlyProduct($itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput, $storeId: String, $skipSpecificationGroup: Boolean = false, $zipCode: String, $skipSubscribeAndSave: Boolean = false, $skipKPF: Boolean = false) {\n  product(itemId: $itemId, dataSource: $dataSource, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    itemId\n    dataSources\n    identifiers {\n      canonicalUrl\n      brandName\n      itemId\n      modelNumber\n      productLabel\n      storeSkuNumber\n      upcGtin13\n      specialOrderSku\n      toolRentalSkuNumber\n      rentalCategory\n      rentalSubCategory\n      upc\n      productType\n      isSuperSku\n      parentId\n      roomVOEnabled\n      sampleId\n      __typename\n    }\n    availabilityType {\n      discontinued\n      status\n      type\n      buyable\n      __typename\n    }\n    details {\n      description\n      collection {\n        url\n        collectionId\n        __typename\n      }\n      highlights\n      descriptiveAttributes {\n        name\n        value\n        bulleted\n        sequence\n        __typename\n      }\n      infoAndGuides {\n        name\n        url\n        __typename\n      }\n      installation {\n        leadGenUrl\n        __typename\n      }\n      __typename\n    }\n    media {\n      images {\n        url\n        type\n        subType\n        sizes\n        __typename\n      }\n      video {\n        shortDescription\n        thumbnail\n        url\n        videoStill\n        link {\n          text\n          url\n          __typename\n        }\n        title\n        type\n        videoId\n        longDescription\n        __typename\n      }\n      threeSixty {\n        id\n        url\n        __typename\n      }\n      augmentedRealityLink {\n        usdz\n        image\n        __typename\n      }\n      richContent {\n        content\n        displayMode\n        richContentSource\n        __typename\n      }\n      __typename\n    }\n    pricing(storeId: $storeId) {\n      promotion {\n        dates {\n          end\n          start\n          __typename\n        }\n        type\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        dollarOff\n        percentageOff\n        savingsCenter\n        savingsCenterPromos\n        specialBuySavings\n        specialBuyDollarOff\n        specialBuyPercentageOff\n        experienceTag\n        subExperienceTag\n        anchorItemList\n        itemList\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      value\n      alternatePriceDisplay\n      alternate {\n        bulk {\n          pricePerUnit\n          thresholdQuantity\n          value\n          __typename\n        }\n        unit {\n          caseUnitOfMeasure\n          unitsOriginalPrice\n          unitsPerCase\n          value\n          __typename\n        }\n        __typename\n      }\n      original\n      mapAboveOriginalPrice\n      message\n      preferredPriceFlag\n      specialBuy\n      unitOfMeasure\n      __typename\n    }\n    reviews {\n      ratingsReviews {\n        averageRating\n        totalReviews\n        __typename\n      }\n      __typename\n    }\n    seo {\n      seoKeywords\n      seoDescription\n      __typename\n    }\n    specificationGroup @skip(if: $skipSpecificationGroup) {\n      specifications {\n        specName\n        specValue\n        __typename\n      }\n      specTitle\n      __typename\n    }\n    taxonomy {\n      breadCrumbs {\n        label\n        url\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionName\n        refinementKey\n        __typename\n      }\n      brandLinkUrl\n      __typename\n    }\n    favoriteDetail {\n      count\n      __typename\n    }\n    info {\n      hidePrice\n      ecoRebate\n      quantityLimit\n      sskMin\n      sskMax\n      unitOfMeasureCoverage\n      wasMaxPriceRange\n      wasMinPriceRange\n      fiscalYear\n      productDepartment\n      classNumber\n      paintBrand\n      dotComColorEligible\n      label\n      prop65Warning\n      returnable\n      globalCustomConfigurator {\n        customButtonText\n        customDescription\n        customExperience\n        customExperienceUrl\n        customTitle\n        __typename\n      }\n      recommendationFlags {\n        reqItems\n        visualNavigation\n        packages\n        __typename\n      }\n      replacementOMSID\n      hasSubscription\n      minimumOrderQuantity\n      projectCalculatorEligible\n      subClassNumber\n      calculatorType\n      isLiveGoodsProduct\n      protectionPlanSku\n      hasServiceAddOns\n      consultationType\n      __typename\n    }\n    fulfillment(storeId: $storeId, zipCode: $zipCode) {\n      backordered\n      fulfillmentOptions {\n        type\n        services {\n          type\n          locations {\n            isAnchor\n            inventory {\n              isLimitedQuantity\n              isOutOfStock\n              isInStock\n              quantity\n              isUnavailable\n              maxAllowedBopisQty\n              minAllowedBopisQty\n              __typename\n            }\n            type\n            storeName\n            locationId\n            curbsidePickupFlag\n            isBuyInStoreCheckNearBy\n            distance\n            state\n            storePhone\n            __typename\n          }\n          deliveryTimeline\n          deliveryDates {\n            startDate\n            endDate\n            __typename\n          }\n          deliveryCharge\n          dynamicEta {\n            hours\n            minutes\n            __typename\n          }\n          hasFreeShipping\n          freeDeliveryThreshold\n          totalCharge\n          __typename\n        }\n        fulfillable\n        __typename\n      }\n      anchorStoreStatus\n      anchorStoreStatusType\n      backorderedShipDate\n      bossExcludedShipStates\n      sthExcludedShipState\n      bossExcludedShipState\n      excludedShipStates\n      seasonStatusEligible\n      onlineStoreStatus\n      onlineStoreStatusType\n      inStoreAssemblyEligible\n      __typename\n    }\n    sizeAndFitDetail {\n      attributeGroups {\n        attributes {\n          attributeName\n          dimensions\n          __typename\n        }\n        dimensionLabel\n        productType\n        __typename\n      }\n      __typename\n    }\n    subscription @skip(if: $skipSubscribeAndSave) {\n      defaultfrequency\n      discountPercentage\n      subscriptionEnabled\n      __typename\n    }\n    badges(storeId: $storeId) {\n      label\n      color\n      creativeImageUrl\n      endDate\n      message\n      name\n      timerDuration\n      timer {\n        timeBombThreshold\n        daysLeftThreshold\n        dateDisplayThreshold\n        message\n        __typename\n      }\n      __typename\n    }\n    keyProductFeatures @skip(if: $skipKPF) {\n      keyProductFeaturesItems {\n        features {\n          name\n          refinementId\n          refinementUrl\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seoDescription\n    installServices {\n      scheduleAMeasure\n      __typename\n    }\n    dataSource\n    __typename\n  }\n}\n'
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    data = json.loads(resp.text)
    return (data['data']['product']['pricing']['value'], data['data']['product']['availabilityType']['status'])


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
        home_depot_item_id = str(item['homeDepotItemId'])
        print(item)
        try:
            (price_value, availability) = get_home_depot_price(home_depot_item_id)
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
