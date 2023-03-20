from datetime import datetime, timedelta
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_stock_information(request):
    stock_endpoint_information = get_stock_information_from_endpoint(request)
    last_daily_information = get_stock_information_from_last_update(stock_endpoint_information)
    return Response(last_daily_information)


def get_stock_information_from_endpoint(request):
    api_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" \
              "{}&outputsize=compact&apikey=X86NOH6II01P7R24".format(request.GET.get('symbol', None))
    headers = {
        "Host": "www.alphavantage.co",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/62.0.3202.94 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.post(api_url, headers=headers)

    return response.json()


def get_stock_information_from_last_update(stock_endpoint_information):
    last_update = stock_endpoint_information['Meta Data']['3. Last Refreshed'].split()[0]
    last_daily_information = stock_endpoint_information['Time Series (Daily)'][last_update]

    return {
        'open_price': last_daily_information['1. open'],
        'higher_price': last_daily_information['2. high'],
        'lower_price': last_daily_information['3. low'],
        'variation': stock_price_variation(last_update, stock_endpoint_information['Time Series (Daily)']),
    }


def stock_price_variation(last_update, daily_stock_information):
    day = datetime.strptime(last_update, '%Y-%m-%d').date()
    timedelta_days = 3 if day.weekday() == 0 else 1
    day_before = (day - timedelta(days=timedelta_days)).strftime('%Y-%m-%d')

    closing_day = float(daily_stock_information[last_update]['4. close'])
    closing_day_before = float(daily_stock_information[day_before]['4. close'])
    return closing_day_before - closing_day
