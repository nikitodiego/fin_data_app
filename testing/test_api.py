import requests
import pytest
from datetime import date
import os

API_KEY=os.environ["API_KEY"]
#definiendo funcion
def test_get_api():
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date.today()}?adjusted=true&apiKey={API_KEY}"
    )
    assert response.status_code ==200
    assert response.json()['resultsCount'] >=0