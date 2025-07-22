from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json
import numpy as np
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
import os
from amadeus import Client, ResponseError
from sklearn.linear_model import LinearRegression
from forex_python.converter import CurrencyRates
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()

def generate_mock_data():
    """Generate mock flight data when API is unavailable"""
    cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide']
    airlines = ['QF', 'VA', 'JQ', 'TT']
    data = []
    
    for _ in range(500):
        origin = np.random.choice(cities)
        dest = np.random.choice([c for c in cities if c != origin])
        date = datetime.now() + timedelta(days=np.random.randint(1, 60))
        data.append({
            'origin': origin,
            'destination': dest,
            'date': date.strftime('%Y-%m-%d'),
            'price': np.random.uniform(200, 1000),
            'airline': np.random.choice(airlines),
            'available_seats': np.random.randint(0, 100)
        })
    
    return pd.DataFrame(data)

def init_amadeus():
    """Initialize Amadeus client with retry logic"""
    try:
        logger.info("Initializing Amadeus client...")
        client = Client(
            client_id=os.getenv('AMADEUS_API_KEY'),
            client_secret=os.getenv('AMADEUS_API_SECRET'),
            hostname='test'
        )
        
        # Test the connection with a simple request
        logger.info("Testing Amadeus connection...")
        response = client.reference_data.locations.get(
            keyword='SYD',
            subType='AIRPORT'
        )
        logger.info("Amadeus client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Amadeus client: {str(e)}")
        return None

# Initialize APIs
openai.api_key = os.getenv('OPENAI_API_KEY')
amadeus = init_amadeus()

def get_flight_data():
    """Get flight data from either API or mock data"""
    if amadeus is None:
        logger.warning("Using mock data as Amadeus client is not available")
        return generate_mock_data()
    
    try:
        # Try to get real data from Amadeus
        data = []
        cities = {
            'SYD': 'Sydney',
            'MEL': 'Melbourne',
            'BNE': 'Brisbane',
            'PER': 'Perth',
            'ADL': 'Adelaide'
        }
        
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        for origin in cities:
            for dest in [d for d in cities if d != origin]:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=dest,
                    departureDate=future_date,
                    adults=1,
                    max=5
                )
                
                for offer in response.data:
                    data.append({
                        'origin': cities[origin],
                        'destination': cities[dest],
                        'date': future_date,
                        'price': float(offer['price']['total']),
                        'airline': offer['validatingAirlineCodes'][0],
                        'available_seats': np.random.randint(0, 50)  # Amadeus doesn't provide seat availability
                    })
        
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching flight data: {str(e)}")
        logger.warning("Falling back to mock data")
        return generate_mock_data()

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Get flight data
        df = get_flight_data()
        
        # Process data for visualization
        route_data = df.groupby(['origin', 'destination'])['price'].agg(['mean', 'count']).reset_index()
        route_data['demand_score'] = route_data['count'] * route_data['mean']
        top_routes = route_data.nlargest(10, 'demand_score')
        
        # Create visualizations
        figures = {
            'routes': px.bar(
                top_routes,
                x='origin',
                y='mean',
                color='destination',
                title='Average Price by Route'
            ),
            'demand': px.scatter(
                top_routes,
                x='mean',
                y='count',
                size='demand_score',
                hover_data=['origin', 'destination'],
                title='Route Demand vs Price'
            )
        }
        
        # Convert figures to JSON
        charts_json = {name: json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                      for name, fig in figures.items()}
        
        # Prepare data table
        data_html = df.head(20).to_html(classes='table table-striped table-hover')
        
        return render_template(
            'index.html',
            data=data_html,
            charts=charts_json,
            cities=df['origin'].unique().tolist(),
            using_mock_data=amadeus is None
        )
        
    except Exception as e:
        logger.error(f"Error in route: {str(e)}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
