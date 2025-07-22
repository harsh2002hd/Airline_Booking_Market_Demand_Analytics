# Airline Booking Market Demand Web App

This web app helps hostels in Australia analyze airline booking market demand trends. It fetches, processes, and visualizes airline data to provide actionable insights such as popular routes, price trends, and high-demand periods.

## Features
- Fetches airline data from Amadeus API (with fallback to demo data)
- Processes and analyzes demand, routes, and pricing
- Interactive charts and tables using Plotly
- Simple, user-friendly web interface
- Real-time data visualization
- AI-powered insights using OpenAI

## Prerequisites
- Python 3.8 or higher
- Amadeus API credentials (get them from [Amadeus for Developers](https://developers.amadeus.com/))
- OpenAI API key (optional, for AI insights)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/airline-booking-market-demand.git
   cd airline-booking-market-demand
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API credentials:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     AMADEUS_API_KEY=your_amadeus_api_key_here
     AMADEUS_API_SECRET=your_amadeus_api_secret_here
     ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Features in Detail
- **Real-time Data**: Fetches current flight pricing and availability
- **Interactive Visualizations**: 
  - Popular routes analysis
  - Price trend charts
  - Demand heatmaps
  - Seasonal patterns
- **AI Insights**: Get market analysis and predictions
- **Data Export**: View and export detailed data tables

## Customization
- To use a real API, update your `.env` file with valid credentials
- Add filters or more charts by modifying `app.py`
- Customize visualizations in the templates folder

## Development
- The app uses Flask for the backend
- Plotly for interactive visualizations
- Pandas for data processing
- Amadeus API for flight data
- OpenAI for market insights

## Security Notes
- Never commit your `.env` file
- Keep your API keys secure
- Use environment variables for sensitive data

---
*The app includes a fallback to simulated data if API credentials are not available or invalid.* 