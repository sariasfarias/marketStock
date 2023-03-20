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

    response = requests.post(api_url,  verify=True)

    return response.json()


def get_stock_information_from_last_update(stock_endpoint_information):
    if not stock_endpoint_information.get('Meta Data', None):
        return stock_endpoint_information

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
