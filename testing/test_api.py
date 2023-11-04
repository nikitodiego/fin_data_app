import requests
import pytest
from datetime import date
import os

#definiendo funcion
def test_get_api():
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date.today()}?adjusted=true&apiKey={os.getenv('api_key')}"
    )
    assert response.status_code ==200
    assert response.json()['resultsCount'] >=0
