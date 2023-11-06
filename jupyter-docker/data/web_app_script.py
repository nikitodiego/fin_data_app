import pandas as pd
import requests
from dash import Dash, html, dash_table
import yfinance as yf

# Incorporate data
df = yf.download(['INTC', 'AAPL', 'GOOGL', 'NVDA', 'AMZN'],start="2023-08-01",end="2023-08-31")['Close'].pct_change().corr()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Corr yfinace based'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)