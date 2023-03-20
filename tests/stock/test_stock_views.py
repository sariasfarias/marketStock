import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from rest_framework.test import APIRequestFactory

from stock.views import get_stock_information, get_stock_information_from_last_update, stock_price_variation


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {
        "Meta Data": {"1. Information": "Daily Prices (open, high, low, close) and Volumes",
                      "2. Symbol": "META", "3. Last Refreshed": "2023-03-18",
                      "4. Output Size": "Compact", "5. Time Zone": "US/Eastern"},
        "Time Series (Daily)": {
            "2023-03-18": {"1. open": "17.3000", "2. high": "17.3500", "3. low": "16.9300", "4. close": "17",
                            "5. adjusted close": "17.0100", "6. volume": "115906", "7. dividend amount": "0.0000",
                            "8. split coefficient": "1.0000"},
            "2023-03-17": {"1. open": "17.4700", "2. high": "17.6700", "3. low": "17.1400", "4. close": "18",
                            "5. adjusted close": "17.2700", "6. volume": "119661", "7. dividend amount": "0.0000",
                            "8. split coefficient": "1.0000"}
        }
    }
    return mock


def test_get_stock_information_from_endpoint_success(mock_response):
    with patch('requests.post', return_value=mock_response):
        response = get_stock_information(APIRequestFactory().get('/'))
        assert response.status_code == 200
        assert response.data['open_price'] == '17.3000'
        assert response.data['higher_price'] == '17.3500'
        assert response.data['lower_price'] == '16.9300'
        assert response.data['variation'] == 1


def test_get_stock_information_from_endpoint_error():
    with patch('requests.post', side_effect=RequestException):
        with pytest.raises(RequestException):
            get_stock_information(APIRequestFactory().get('/'))


def test_stock_price_variation():
    last_update = "2023-03-18"
    stock_endpoint_information = {
        'Meta Data': {
            '3. Last Refreshed': '2023-03-18'
        },
        'Time Series (Daily)': {
            '2023-03-18': {
                '1. open': '100.00',
                '2. high': '101.00',
                '3. low': '99.00',
                '4. close': '100.50'
            },
            '2023-03-17': {
                '1. open': '99.00',
                '2. high': '100.00',
                '3. low': '98.00',
                '4. close': '99.50'
            },
            '2023-03-16': {
                '1. open': '98.00',
                '2. high': '99.00',
                '3. low': '97.00',
                '4. close': '98.50'
            }
        }
    }
    assert stock_price_variation(last_update, stock_endpoint_information['Time Series (Daily)']) == -1


def test_get_stock_information_from_last_update():
    stock_endpoint_information = {
        'Meta Data': {
            '3. Last Refreshed': '2023-03-18'
        },
        'Time Series (Daily)': {
            '2023-03-18': {
                '1. open': '100.00',
                '2. high': '101.00',
                '3. low': '99.00',
                '4. close': '100.50'
            },
            '2023-03-17': {
                '1. open': '99.00',
                '2. high': '100.00',
                '3. low': '98.00',
                '4. close': '99.50'
            },
            '2023-03-16': {
                '1. open': '98.00',
                '2. high': '99.00',
                '3. low': '97.00',
                '4. close': '98.50'
            }
        }
    }

    expected_result = {
        'open_price': '100.00',
        'higher_price': '101.00',
        'lower_price': '99.00',
        'variation': -1.0
    }

    assert get_stock_information_from_last_update(stock_endpoint_information) == expected_result
