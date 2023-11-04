import requests
import pytest
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
#definiendo funcion
def test_get_api():
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date.today()}?adjusted=true&apiKey={os.getenv('API_KEY')}"
    )
    assert response.status_code ==200
    assert response.json()['resultsCount'] >=0
