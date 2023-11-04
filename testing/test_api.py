import requests
import pytest
import os

#definiendo funcion
def test_get_api():
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2023-07-26?adjusted=true&apiKey={os.getenv('api_key')}"
    )
    assert response.status_code ==200
    assert response.json()['resultsCount'] >=0
