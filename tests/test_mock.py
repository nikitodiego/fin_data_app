import unittest
from unittest.mock import patch, MagicMock
from test_function import api_call  # replace with your actual module

class TestAPICall(unittest.TestCase):

    @patch('dags.data.app_functions_optim.requests.get')
    @patch('dags.data.app_functions_optim.datetime.datetime')
    @patch('dags.data.app_functions_optim.time.sleep')
    @patch('dags.data.app_functions_optim.pd.DataFrame')
    @patch('dags.data.app_functions_optim.os.getenv')
    @patch('dags.data.app_functions_optim.logging.info')
    def test_api_call_with_mock(self, mock_logging_info, mock_os_getenv, mock_dataframe, mock_sleep, mock_datetime, mock_requests_get):
        # Set up test data and context
        test_date = '2023-01-01'
        context = {'ds': test_date}

        # Set up mock responses
        mock_datetime.strptime.return_value.date.return_value.weekday.return_value = 0  # Monday
        mock_os_getenv.return_value = 'your_api_key'
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "resultsCount": 1,
            "results": {"T": "AAPL", "o": 100.0, "c": 105.0, "h": 110.0, "l": 95.0}
        }
        mock_requests_get.return_value = mock_response

        # Call the function
        result = api_call(**context)

        # Assert that the function behaved as expected
        self.assertEqual(result, {"msg": "Data loaded"})
        mock_sleep.assert_called_once_with(30)
        mock_datetime.strptime.assert_called_once_with(test_date, '%Y-%m-%d')
        mock_os_getenv.assert_called_once_with('API_KEY')
        mock_requests_get.assert_called_once_with(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{test_date}?adjusted=true&apiKey=your_api_key")
        mock_response.raise_for_status.assert_called_once()
        mock_dataframe.assert_called_once_with({"T": "AAPL", "o": 100.0, "c": 105.0, "h": 110.0, "l": 95.0})
        mock_logging_info.assert_not_called()  # Assuming no logs for a successful call

    # Add more test methods for different scenarios

if __name__ == '__main__':
    unittest.main()
