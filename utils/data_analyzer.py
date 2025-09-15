import pandas as pd
import numpy as np
from scipy import stats
from data.weather_data import get_weather_data_for_region
from data.crop_database import get_crop_database

class WeatherDataAnalyzer:
    def __init__(self):
        pass
    
    def analyze_weather_trends(self, region_name, years=30):
        """Analyze long-term weather trends for a region"""
        
        # Get current weather data
        current_weather = get_weather_data_for_region(region_name)
        
        # Generate historical trend data
        historical_data = []
        base_temp = current_weather['avg_temp']
        base_rainfall = current_weather['annual_rainfall']
        
        for year in range(years):
            # Add some trend and random variation
            temp_trend = year * 0.02  # Slight warming trend
            rainfall_trend = year * (1 if base_rainfall < 1000 else -2)  # Rainfall change
            
            temp = base_temp + temp_trend + np.random.normal(0, 1)
            rainfall = base_rainfall + rainfall_trend + np.random.normal(0, 100)
            
            historical_data.append({
                'year': 2024 - years + year,
                'temperature': max(15, min(45, temp)),
                'rainfall': max(100, min(3000, rainfall))
            })
        
        df = pd.DataFrame(historical_data)
        
        # Calculate trends
        temp_slope, temp_intercept, temp_r, temp_p, temp_se = stats.linregress(df['year'], df['temperature'])
        rain_slope, rain_intercept, rain_r, rain_p, rain_se = stats.linregress(df['year'], df['rainfall'])
        
        analysis = {
            'data': historical_data,
            'temperature_trend': {
                'slope': temp_slope,
                'direction': 'increasing' if temp_slope > 0 else 'decreasing',
                'significance': 'significant' if temp_p < 0.05 else 'not significant',
                'r_squared': temp_r**2
            },
            'rainfall_trend': {
                'slope': rain_slope,
                'direction': 'increasing' if rain_slope > 0 else 'decreasing',
                'significance': 'significant' if rain_p < 0.05 else 'not significant',
                'r_squared': rain_r**2
            }
        }
        
        return analysis
    
    def calculate_climate_extremes(self, region_name):
        """Calculate climate extreme events probability"""
        
        weather_data = get_weather_data_for_region(region_name)
        
        # Drought risk calculation
        annual_rainfall = weather_data['annual_rainfall']
        if annual_rainfall < 500:
            drought_risk = 'High'
            drought_probability = 40
        elif annual_rainfall < 750:
            drought_risk = 'Medium'
            drought_probability = 20
        else:
            drought_risk = 'Low'
            drought_probability = 5
        
        # Heat wave risk
        avg_temp = weather_data['avg_temp']
        if avg_temp > 35:
            heatwave_risk = 'High'
            heatwave_probability = 30
        elif avg_temp > 30:
            heatwave_risk = 'Medium'
            heatwave_probability = 15
        else:
            heatwave_risk = 'Low'
            heatwave_probability = 5
        
        # Flood risk
        if annual_rainfall > 2000:
            flood_risk = 'High'
            flood_probability = 25
        elif annual_rainfall > 1500:
            flood_risk = 'Medium'
            flood_probability = 10
        else:
            flood_risk = 'Low'
            flood_probability = 3
        
        return {
            'drought': {'risk': drought_risk, 'probability': drought_probability},
            'heatwave': {'risk': heatwave_risk, 'probability': heatwave_probability},
            'flood': {'risk': flood_risk, 'probability': flood_probability}
        }
    
    def analyze_seasonal_variability(self, region_name):
        """Analyze seasonal weather variability"""
        
        weather_data = get_weather_data_for_region(region_name)
        monthly_temp = weather_data['monthly_temp']
        monthly_rainfall = weather_data['monthly_rainfall']
        
        # Temperature variability
        temps = [month['avg_temp'] for month in monthly_temp]
        temp_std = np.std(temps)
        temp_cv = (temp_std / np.mean(temps)) * 100
        
        # Rainfall variability
        rainfalls = [month['rainfall'] for month in monthly_rainfall]
        rain_std = np.std(rainfalls)
        rain_cv = (rain_std / np.mean(rainfalls)) * 100 if np.mean(rainfalls) > 0 else 0
        
        # Seasonal concentration
        monsoon_months = [5, 6, 7, 8]  # Jun-Sep (0-indexed)
        monsoon_rainfall = sum(rainfalls[i] for i in monsoon_months if i < len(rainfalls))
        monsoon_concentration = (monsoon_rainfall / sum(rainfalls)) * 100 if sum(rainfalls) > 0 else 0
        
        return {
            'temperature_variability': {
                'standard_deviation': round(temp_std, 2),
                'coefficient_of_variation': round(temp_cv, 2),
                'assessment': 'High' if temp_cv > 30 else 'Medium' if temp_cv > 15 else 'Low'
            },
            'rainfall_variability': {
                'standard_deviation': round(rain_std, 2),
                'coefficient_of_variation': round(rain_cv, 2),
                'assessment': 'High' if rain_cv > 100 else 'Medium' if rain_cv > 50 else 'Low'
            },
            'monsoon_concentration': {
                'percentage': round(monsoon_concentration, 1),
                'assessment': 'High' if monsoon_concentration > 80 else 'Medium' if monsoon_concentration > 60 else 'Low'
            }
        }

class CropSuitabilityAnalyzer:
    def __init__(self):
        self.crops_db = get_crop_database()
    
    def analyze_crop_climate_match(self, crop_name, region_name):
        """Detailed analysis of crop-climate compatibility"""
        
        crop_data = next((crop for crop in self.crops_db if crop['name'] == crop_name), None)
        if not crop_data:
            return None
        
        weather_data = get_weather_data_for_region(region_name)
        
        # Temperature match
        avg_temp = weather_data['avg_temp']
        temp_optimal = (crop_data['temp_min'] + crop_data['temp_max']) / 2
        temp_match_score = max(0, 100 - abs(avg_temp - temp_optimal) * 5)
        
        # Rainfall match
        annual_rainfall = weather_data['annual_rainfall']
        rainfall_optimal = (crop_data['rainfall_min'] + crop_data['rainfall_max']) / 2
        rainfall_match_score = max(0, 100 - abs(annual_rainfall - rainfall_optimal) / 10)
        
        # Overall climate suitability
        climate_score = (temp_match_score + rainfall_match_score) / 2
        
        return {
            'crop': crop_name,
            'region': region_name,
            'temperature_match': {
                'score': round(temp_match_score, 1),
                'optimal_range': f"{crop_data['temp_min']}-{crop_data['temp_max']}°C",
                'actual_avg': f"{avg_temp:.1f}°C",
                'status': 'Excellent' if temp_match_score > 80 else 'Good' if temp_match_score > 60 else 'Fair' if temp_match_score > 40 else 'Poor'
            },
            'rainfall_match': {
                'score': round(rainfall_match_score, 1),
                'optimal_range': f"{crop_data['rainfall_min']}-{crop_data['rainfall_max']}mm",
                'actual_annual': f"{annual_rainfall:.0f}mm",
                'status': 'Excellent' if rainfall_match_score > 80 else 'Good' if rainfall_match_score > 60 else 'Fair' if rainfall_match_score > 40 else 'Poor'
            },
            'overall_suitability': {
                'score': round(climate_score, 1),
                'status': 'Highly Suitable' if climate_score > 80 else 'Suitable' if climate_score > 60 else 'Moderately Suitable' if climate_score > 40 else 'Not Suitable'
            }
        }
    
    def compare_crop_requirements(self, crop_names, region_name):
        """Compare multiple crops for a region"""
        
        comparisons = []
        for crop_name in crop_names:
            analysis = self.analyze_crop_climate_match(crop_name, region_name)
            if analysis:
                comparisons.append(analysis)
        
        return comparisons
    
    def find_alternative_crops(self, failed_crop, region_name, num_alternatives=5):
        """Find alternative crops if one fails"""
        
        failed_crop_data = next((crop for crop in self.crops_db if crop['name'] == failed_crop), None)
        if not failed_crop_data:
            return []
        
        weather_data = get_weather_data_for_region(region_name)
        
        alternatives = []
        
        for crop in self.crops_db:
            if crop['name'] == failed_crop:
                continue
            
            # Check if alternative has similar economic potential
            roi_similarity = abs(crop['roi'] - failed_crop_data['roi']) / max(crop['roi'], failed_crop_data['roi'])
            
            # Check climate suitability
            analysis = self.analyze_crop_climate_match(crop['name'], region_name)
            if analysis and analysis['overall_suitability']['score'] > 60:
                alternatives.append({
                    'crop': crop['name'],
                    'type': crop['type'],
                    'suitability_score': analysis['overall_suitability']['score'],
                    'roi': crop['roi'],
                    'roi_similarity': round((1 - roi_similarity) * 100, 1),
                    'growing_season': crop['growing_season']
                })
        
        # Sort by suitability and ROI similarity
        alternatives.sort(key=lambda x: (x['suitability_score'], x['roi_similarity']), reverse=True)
        
        return alternatives[:num_alternatives]

class MarketAnalyzer:
    def __init__(self):
        pass
    
    def analyze_price_trends(self, crop_name, years=5):
        """Analyze price trends for a crop (simulated data)"""
        
        # Simulate price data with trends
        base_price = {
            'Rice (Basmati)': 4500, 'Wheat': 2200, 'Maize': 1800,
            'Chana (Chickpea)': 5500, 'Soybean': 4200, 'Cotton': 6000,
            'Tomato': 2500, 'Potato': 1200, 'Onion': 1800
        }.get(crop_name, 3000)
        
        price_data = []
        for year in range(years):
            # Add trend and seasonal variation
            trend = year * 100  # Inflation
            seasonal_var = np.random.normal(0, base_price * 0.1)
            annual_price = base_price + trend + seasonal_var
            
            price_data.append({
                'year': 2024 - years + year,
                'price': max(500, annual_price)
            })
        
        # Calculate trend
        prices = [p['price'] for p in price_data]
        years_list = [p['year'] for p in price_data]
        
        if len(prices) > 1:
            slope, intercept, r, p_value, se = stats.linregress(years_list, prices)
            trend_direction = 'Increasing' if slope > 0 else 'Decreasing'
            trend_strength = 'Strong' if abs(r) > 0.7 else 'Moderate' if abs(r) > 0.3 else 'Weak'
        else:
            slope, trend_direction, trend_strength = 0, 'Stable', 'Weak'
        
        return {
            'crop': crop_name,
            'price_data': price_data,
            'current_price': prices[-1] if prices else base_price,
            'trend': {
                'direction': trend_direction,
                'strength': trend_strength,
                'annual_change': round(slope, 2)
            },
            'volatility': {
                'coefficient': round(np.std(prices) / np.mean(prices) * 100, 2) if prices else 0,
                'assessment': 'High' if np.std(prices) / np.mean(prices) > 0.2 else 'Medium' if np.std(prices) / np.mean(prices) > 0.1 else 'Low'
            }
        }
    
    def calculate_market_demand_score(self, crop_type, region_name):
        """Calculate market demand score for crop type in region"""
        
        # Base demand scores by crop type
        base_demand = {
            'Cereals': 70,
            'Pulses': 85,
            'Oilseeds': 80,
            'Vegetables': 90,
            'Fruits': 75
        }
        
        # Regional demand modifiers
        regional_modifiers = {
            'Maharashtra': {'Vegetables': 10, 'Fruits': 5},
            'Punjab': {'Cereals': 15, 'Oilseeds': 5},
            'Gujarat': {'Cotton': 20, 'Oilseeds': 10},
            'Tamil Nadu': {'Rice': 10, 'Vegetables': 8}
        }
        
        score = base_demand.get(crop_type, 60)
        
        if region_name in regional_modifiers:
            modifier = regional_modifiers[region_name].get(crop_type, 0)
            score += modifier
        
        return min(100, score)
    
    def analyze_supply_chain_efficiency(self, crop_name, region_name):
        """Analyze supply chain efficiency for crop in region"""
        
        # Simulate supply chain factors
        transportation_score = np.random.randint(60, 90)
        storage_score = np.random.randint(50, 85)
        processing_score = np.random.randint(55, 80)
        
        # Overall efficiency
        efficiency = (transportation_score + storage_score + processing_score) / 3
        
        return {
            'crop': crop_name,
            'region': region_name,
            'transportation': transportation_score,
            'storage': storage_score,
            'processing': processing_score,
            'overall_efficiency': round(efficiency, 1),
            'grade': 'A' if efficiency > 80 else 'B' if efficiency > 70 else 'C' if efficiency > 60 else 'D'
        }
