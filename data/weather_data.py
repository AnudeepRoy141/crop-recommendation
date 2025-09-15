import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_weather_data_for_region(region_name):
    """
    Generate realistic weather data for Indian regions based on actual climate patterns
    """
    
    # Regional climate patterns for major Indian states/regions
    regional_patterns = {
        'Punjab': {
            'base_temp': 24, 'temp_variation': 15,
            'base_rainfall': 600, 'rainfall_variation': 200,
            'base_humidity': 65, 'humidity_variation': 15,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [4, 5, 6]
        },
        'Maharashtra': {
            'base_temp': 26, 'temp_variation': 12,
            'base_rainfall': 1200, 'rainfall_variation': 400,
            'base_humidity': 70, 'humidity_variation': 20,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [3, 4, 5]
        },
        'Tamil Nadu': {
            'base_temp': 28, 'temp_variation': 8,
            'base_rainfall': 1000, 'rainfall_variation': 300,
            'base_humidity': 75, 'humidity_variation': 15,
            'monsoon_months': [10, 11, 12],
            'winter_months': [1, 2],
            'summer_months': [3, 4, 5, 6]
        },
        'Uttar Pradesh': {
            'base_temp': 25, 'temp_variation': 18,
            'base_rainfall': 800, 'rainfall_variation': 250,
            'base_humidity': 65, 'humidity_variation': 20,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [4, 5, 6]
        },
        'Karnataka': {
            'base_temp': 25, 'temp_variation': 10,
            'base_rainfall': 1100, 'rainfall_variation': 350,
            'base_humidity': 68, 'humidity_variation': 18,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [3, 4, 5]
        },
        'Gujarat': {
            'base_temp': 27, 'temp_variation': 14,
            'base_rainfall': 700, 'rainfall_variation': 200,
            'base_humidity': 60, 'humidity_variation': 20,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [4, 5, 6]
        },
        'Rajasthan': {
            'base_temp': 27, 'temp_variation': 20,
            'base_rainfall': 400, 'rainfall_variation': 150,
            'base_humidity': 45, 'humidity_variation': 25,
            'monsoon_months': [7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [4, 5, 6]
        },
        'West Bengal': {
            'base_temp': 26, 'temp_variation': 12,
            'base_rainfall': 1500, 'rainfall_variation': 400,
            'base_humidity': 80, 'humidity_variation': 15,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [3, 4, 5]
        },
        'Andhra Pradesh': {
            'base_temp': 28, 'temp_variation': 10,
            'base_rainfall': 900, 'rainfall_variation': 300,
            'base_humidity': 70, 'humidity_variation': 18,
            'monsoon_months': [6, 7, 8, 9, 10],
            'winter_months': [12, 1, 2],
            'summer_months': [3, 4, 5]
        },
        'Madhya Pradesh': {
            'base_temp': 25, 'temp_variation': 16,
            'base_rainfall': 1000, 'rainfall_variation': 300,
            'base_humidity': 65, 'humidity_variation': 20,
            'monsoon_months': [6, 7, 8, 9],
            'winter_months': [12, 1, 2],
            'summer_months': [4, 5, 6]
        }
    }
    
    # Use default pattern if region not found
    pattern = regional_patterns.get(region_name, regional_patterns['Maharashtra'])
    
    # Generate monthly data
    monthly_temp = []
    monthly_rainfall = []
    monthly_humidity = []
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    total_rainfall = 0
    rainy_days = 0
    
    for month_idx in range(12):
        month = month_idx + 1
        
        # Temperature calculation
        if month in pattern['winter_months']:
            temp_factor = -0.6
        elif month in pattern['summer_months']:
            temp_factor = 0.8
        elif month in pattern['monsoon_months']:
            temp_factor = 0.1
        else:
            temp_factor = 0.2
        
        avg_temp = pattern['base_temp'] + (pattern['temp_variation'] * temp_factor)
        min_temp = avg_temp - 5 - random.uniform(0, 3)
        max_temp = avg_temp + 5 + random.uniform(0, 3)
        
        monthly_temp.append({
            'month': months[month_idx],
            'min_temp': round(min_temp, 1),
            'max_temp': round(max_temp, 1),
            'avg_temp': round(avg_temp, 1)
        })
        
        # Rainfall calculation
        if month in pattern['monsoon_months']:
            rainfall = pattern['base_rainfall'] * 0.3 + random.uniform(0, pattern['rainfall_variation'] * 0.5)
            days_rain = random.randint(15, 25)
        elif month in [3, 4, 5, 10, 11]:  # Pre/post monsoon
            rainfall = pattern['base_rainfall'] * 0.1 + random.uniform(0, pattern['rainfall_variation'] * 0.2)
            days_rain = random.randint(2, 8)
        else:  # Dry months
            rainfall = random.uniform(0, pattern['rainfall_variation'] * 0.1)
            days_rain = random.randint(0, 3)
        
        monthly_rainfall.append({
            'month': months[month_idx],
            'rainfall': round(rainfall, 1)
        })
        
        total_rainfall += rainfall
        rainy_days += days_rain
        
        # Humidity calculation
        if month in pattern['monsoon_months']:
            humidity = pattern['base_humidity'] + random.uniform(5, 15)
        elif month in pattern['winter_months']:
            humidity = pattern['base_humidity'] - random.uniform(5, 15)
        else:
            humidity = pattern['base_humidity'] + random.uniform(-5, 5)
        
        humidity = max(20, min(95, humidity))  # Realistic bounds
        
        monthly_humidity.append({
            'month': months[month_idx],
            'humidity': round(humidity, 1)
        })
    
    # Calculate averages
    avg_temp = sum(month['avg_temp'] for month in monthly_temp) / 12
    avg_humidity = sum(month['humidity'] for month in monthly_humidity) / 12
    
    return {
        'region': region_name,
        'avg_temp': avg_temp,
        'annual_rainfall': total_rainfall,
        'avg_humidity': avg_humidity,
        'rainy_days': rainy_days,
        'monthly_temp': monthly_temp,
        'monthly_rainfall': monthly_rainfall,
        'monthly_humidity': monthly_humidity,
        'climate_zone': get_climate_zone(avg_temp, total_rainfall),
        'growing_seasons': get_growing_seasons(pattern)
    }

def get_climate_zone(avg_temp, annual_rainfall):
    """Classify climate zone based on temperature and rainfall"""
    if annual_rainfall > 1500:
        if avg_temp > 25:
            return "Tropical Wet"
        else:
            return "Subtropical Wet"
    elif annual_rainfall > 750:
        if avg_temp > 25:
            return "Tropical Moderate"
        else:
            return "Subtropical Moderate"
    else:
        if avg_temp > 25:
            return "Semi-Arid Hot"
        else:
            return "Semi-Arid Cool"

def get_growing_seasons(pattern):
    """Determine optimal growing seasons based on climate pattern"""
    seasons = []
    
    if pattern['monsoon_months']:
        seasons.append("Kharif (Monsoon)")
    
    if pattern['winter_months']:
        seasons.append("Rabi (Winter)")
    
    # Check for summer crops possibility
    if pattern['base_rainfall'] > 800:
        seasons.append("Zaid (Summer)")
    
    return seasons

def get_detailed_weather_analysis(region_name):
    """Get detailed 30-year weather analysis for advanced features"""
    
    # Generate 30-year historical trends
    historical_trends = []
    base_year = 1994
    
    for year in range(30):
        # Add climate change trends - gradual warming and rainfall changes
        temp_trend = year * 0.03  # 0.03°C increase per year
        rainfall_trend = year * (-2 if region_name in ['Rajasthan', 'Gujarat'] else 1)  # Different trends for arid regions
        
        historical_trends.append({
            'year': base_year + year,
            'temperature': 25 + temp_trend + random.uniform(-2, 2),
            'rainfall': 800 + rainfall_trend + random.uniform(-200, 200)
        })
    
    # Seasonal data
    seasonal_data = [
        {'season': 'Winter', 'avg_temp': 18, 'rainfall': 50},
        {'season': 'Summer', 'avg_temp': 35, 'rainfall': 100},
        {'season': 'Monsoon', 'avg_temp': 28, 'rainfall': 600},
        {'season': 'Post-Monsoon', 'avg_temp': 25, 'rainfall': 150}
    ]
    
    # Risk assessments
    drought_risk = max(0, min(100, 50 - (800 / 20)))  # Based on rainfall
    flood_risk = max(0, min(100, (1200 - 800) / 10))  # Based on excess rainfall
    
    # Climate risk score (1-10, lower is better)
    risk_score = (drought_risk + flood_risk) / 20
    
    return {
        'historical_trends': historical_trends,
        'seasonal_data': seasonal_data,
        'drought_risk': drought_risk,
        'flood_risk': flood_risk,
        'risk_score': risk_score,
        'growing_season_days': 240  # Days suitable for agriculture
    }

def get_weather_forecast(region_name, days=7):
    """Generate weather forecast for the next few days"""
    base_weather = get_weather_data_for_region(region_name)
    current_month = datetime.now().month
    
    # Get current month's typical weather
    current_month_data = base_weather['monthly_temp'][current_month - 1]
    current_rainfall_data = base_weather['monthly_rainfall'][current_month - 1]
    
    forecast = []
    for day in range(days):
        date = datetime.now() + timedelta(days=day)
        
        # Add some daily variation
        temp_variation = random.uniform(-3, 3)
        rain_chance = random.uniform(0, 100)
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'min_temp': current_month_data['min_temp'] + temp_variation,
            'max_temp': current_month_data['max_temp'] + temp_variation,
            'rainfall': current_rainfall_data['rainfall'] / 30 if rain_chance > 70 else 0,
            'humidity': base_weather['avg_humidity'] + random.uniform(-10, 10)
        })
    
    return forecast
