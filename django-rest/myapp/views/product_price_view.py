from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.product import Product
from ..models.channel import Channel
from ..models.price import Price
import datetime
from ..services.home_depot_service import get_home_depot_price


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_products_with_latest_prices(request):
    products = Product.objects.all()
    channels = Channel.objects.all()
    latest_prices = Price.objects.filter(is_latest=True)
    
    latest_prices_map = {}
    for price in latest_prices:
        product_id = price.product_id
        channel_id = price.channel_id
        key = str(product_id) + '-' + str(channel_id)
        latest_prices_map[key] = price

    products_data = []
    for product in products:
        product_data = {'product': product.to_json(), 'channels': []}
        for channel in channels:
            channel_data = {'channel': channel.to_json()}
            key = str(product.id) + '-' + str(channel.id)
            latest_price = latest_prices_map.get(key, None)
            if latest_price:
                channel_data['latestPrice'] = latest_price.to_json()
            product_data['channels'].append(channel_data)
        products_data.append(product_data)
    return Response(products_data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_product_with_prices(request, product_id):
    product = Product.objects.get(pk=product_id)
    channels = Channel.objects.all()
    prices = Price.objects.filter(product_id=product_id)

    prices_map = {}
    for price in prices:
        key = str(price.channel_id)
        if key not in prices_map:
            prices_map[key] = []
        prices_map[key].append(price.to_json())

    product_data = {'product': product.to_json(), 'channels': []}
    for channel in channels:
        channel_data = {'channel': channel.to_json(), 'prices': []}
        if str(channel.id) in prices_map:
            channel_data['prices'] = prices_map[str(channel.id)]
        product_data['channels'].append(channel_data)

    return Response(product_data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_product_latest_price(request, product_id, channel_id):
    product = Product.objects.get(pk=product_id)
    channel = Channel.objects.get(pk=channel_id)
    if not channel.name == 'Home Depot':
        raise 'cannot find prices other than Home Depot'

    now = datetime.datetime.utcnow()
    if 'priceValue' not in request.data:
        raise 'you need to input price value'
    price_value = float(request.data['priceValue'])
    timestamp = int(now.timestamp() * 1000)

    recent_timestamp = timestamp - 864000000
    recent_prices = list(Price.objects.filter(product_id=product.id, channel_id=channel.id, timestamp__gt=recent_timestamp))
    recent_prices.sort(reverse=True, key=get_price_timestamp)
    flag = ''
    for rp in recent_prices:
        if not price_value == rp.price:
            if  price_value > rp.price:
                flag = 'UP'
            else:
                flag = 'DOWN'
            break

    date = datetime.date(now.year, now.month, now.day).isoformat()

    latest_change = find_latest_change(price_value, date, product.id, channel.id)

    latest_prices = list(Price.objects.filter(product_id=product.id, channel_id=channel.id, is_latest=True))
    latest_prices.sort(reverse=True, key=get_price_timestamp)
    latest_price = None
    if len(latest_prices) > 1:
        for i in range(len(latest_prices) - 1):
            price = latest_prices[i + 1]
            price.is_latest = False
            price.save()
    if len(latest_prices):
        latest_price = latest_prices[0]
        if timestamp > latest_price.timestamp:
            if date == latest_price.date:
                latest_price.price = price_value
                latest_price.latest_change = latest_change
                latest_price.flag = flag
                latest_price.timestamp = timestamp
                latest_price.save()
            else:
                latest_price.is_latest = False
                latest_price.save()
                price = Price()
                price.product_id = product.id
                price.channel_id = channel.id
                price.price = price_value
                price.latest_change = latest_change
                price.flag = flag
                price.date = date
                price.timestamp = timestamp
                price.is_latest = True
                price.save()
                latest_price = price
    else:
        price = Price()
        price.product_id = product.id
        price.channel_id = channel.id
        price.price = price_value
        price.latest_change = latest_change
        price.flag = flag
        price.date = date
        price.timestamp = timestamp
        price.is_latest = True
        price.save()
        latest_price = price

    return Response(latest_price.to_json())

def find_latest_change(current_price, current_date, product_id, channel_id):
    prices = list(Price.objects.filter(product_id=product_id, channel_id=channel_id))
    prices.sort(reverse=True, key=get_price_timestamp)
    last_price = current_price
    last_date = current_date
    for price in prices:
        if not last_price == price.price:
            if last_price > price.price:
                return price.date + ',+,' + str(price.price)
            return price.date + ',-,' + str(price.price)

        if price.latest_change and (not price.latest_change.endswith((',+', ',-'))):
            return price.latest_change

        last_price = price.price
        last_date = price.date
    return ''

def get_price_timestamp(p):
  return p.timestamp
