import pandas as pd
import numpy as np
from data.crop_database import get_crop_database, get_suitable_crops_for_climate
from data.weather_data import get_weather_data_for_region
from data.soil_analysis import get_detailed_soil_data, analyze_soil_crop_compatibility

class CropRecommendationEngine:
    def __init__(self):
        self.crops_db = get_crop_database()
        
    def get_recommendations(self, region_info, weather_data, top_n=15):
        """
        Generate crop recommendations based on region, weather data, and soil analysis
        """
        
        # Extract climate parameters
        avg_temp = weather_data['avg_temp']
        annual_rainfall = weather_data['annual_rainfall']
        
        # Define temperature and rainfall ranges
        temp_range = (avg_temp - 5, avg_temp + 5)
        rainfall_range = (annual_rainfall * 0.8, annual_rainfall * 1.2)
        
        # Get suitable crops based on climate
        suitable_crops = get_suitable_crops_for_climate(temp_range, rainfall_range)
        
        # Get soil data for the region
        soil_data = get_detailed_soil_data()
        region_soil = soil_data.get(region_info['name'], {})
        
        # Calculate enhanced suitability scores
        recommendations = []
        
        for crop in suitable_crops:
            # Climate suitability (already calculated)
            climate_score = crop['suitability_score']
            
            # Soil suitability analysis
            if region_soil:
                soil_analysis = analyze_soil_crop_compatibility(crop, region_soil)
                soil_score = soil_analysis['overall_score']
                crop['soil_analysis'] = soil_analysis
            else:
                soil_score = 7.0  # Default moderate score if no soil data
                crop['soil_analysis'] = None
            
            # Economic attractiveness score
            economic_score = self._calculate_economic_score(crop)
            
            # Regional bonus (if crop is commonly grown in the region)
            regional_score = self._calculate_regional_score(crop, region_info)
            
            # Market demand score (based on crop type and current trends)
            market_score = self._calculate_market_score(crop)
            
            # Risk assessment score
            risk_score = self._calculate_risk_score(crop, weather_data)
            
            # Calculate weighted final score with soil analysis
            final_score = (
                climate_score * 0.25 +
                soil_score * 0.25 +
                economic_score * 0.20 +
                regional_score * 0.12 +
                market_score * 0.10 +
                risk_score * 0.08
            )
            
            crop['suitability_score'] = round(final_score, 2)
            crop['climate_score'] = round(climate_score, 2)
            crop['soil_score'] = round(soil_score, 2)
            crop['economic_score'] = round(economic_score, 2)
            crop['regional_score'] = round(regional_score, 2)
            crop['market_score'] = round(market_score, 2)
            crop['risk_score'] = round(risk_score, 2)
            
            recommendations.append(crop)
        
        # Sort by final suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def _calculate_economic_score(self, crop):
        """Calculate economic attractiveness score (0-10)"""
        roi = crop['roi']
        profit_margin = crop['profit_margin']
        
        # Normalize ROI (0-200% maps to 0-10)
        roi_score = min(10, roi / 20)
        
        # Normalize profit margin (0-100% maps to 0-10)
        margin_score = min(10, profit_margin / 10)
        
        return (roi_score + margin_score) / 2
    
    def _calculate_regional_score(self, crop, region_info):
        """Calculate regional suitability score (0-10)"""
        
        # Crop-region compatibility mapping
        regional_bonuses = {
            'Rice (Basmati)': ['Punjab', 'Haryana', 'Uttar Pradesh'],
            'Wheat': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh'],
            'Cotton': ['Gujarat', 'Maharashtra', 'Andhra Pradesh', 'Punjab'],
            'Sugarcane': ['Uttar Pradesh', 'Maharashtra', 'Karnataka'],
            'Soybean': ['Madhya Pradesh', 'Maharashtra', 'Rajasthan'],
            'Sunflower': ['Karnataka', 'Andhra Pradesh', 'Maharashtra'],
            'Chana (Chickpea)': ['Madhya Pradesh', 'Rajasthan', 'Maharashtra'],
            'Tomato': ['Karnataka', 'Andhra Pradesh', 'Maharashtra'],
            'Onion': ['Maharashtra', 'Karnataka', 'Gujarat'],
            'Chili': ['Andhra Pradesh', 'Karnataka', 'Tamil Nadu']
        }
        
        crop_name = crop['name']
        region_name = region_info['name']
        
        if crop_name in regional_bonuses and region_name in regional_bonuses[crop_name]:
            return 8.0  # High regional compatibility
        elif crop['type'] in ['Cereals', 'Pulses'] and region_info['climate_zone'] in ['Subtropical', 'Tropical']:
            return 6.0  # Moderate compatibility
        # elif crop['type'] in ['Vegetables', 'Fruits'] and region_info['annual_rainfall'] > 800:
            # return 7.0  # Good for vegetables/fruits with adequate rainfall
        else:
            return 5.0  # Neutral/average compatibility
    
    def _calculate_market_score(self, crop):
        """Calculate market demand score (0-10)"""
        
        # Market demand factors based on crop type and price trends
        market_factors = {
            'Pulses': 9.0,  # High demand due to protein needs
            'Oilseeds': 8.0,  # Growing oil consumption
            'Vegetables': 8.5,  # Urban demand growth
            'Fruits': 7.5,  # Premium market
            'Cereals': 7.0,  # Stable demand
        }
        
        base_score = market_factors.get(crop['type'], 6.0)
        
        # Price premium adjustment
        if crop['market_price'] > 3000:  # High-value crops
            price_bonus = 1.0
        elif crop['market_price'] > 2000:
            price_bonus = 0.5
        else:
            price_bonus = 0.0
        
        return min(10, base_score + price_bonus)
    
    def _calculate_risk_score(self, crop, weather_data):
        """Calculate risk assessment score (0-10, higher is lower risk)"""
        
        # Water requirement risk
        water_risk_map = {'High': 3.0, 'Medium': 7.0, 'Low': 9.0}
        water_score = water_risk_map.get(crop['water_requirement'], 5.0)
        
        # Weather variability risk
        if weather_data['annual_rainfall'] < 500:  # Drought-prone
            if crop['water_requirement'] == 'Low':
                weather_score = 8.0
            else:
                weather_score = 4.0
        elif weather_data['annual_rainfall'] > 2000:  # Flood-prone
            if crop['type'] == 'Vegetables':
                weather_score = 5.0
            else:
                weather_score = 7.0
        else:
            weather_score = 8.0
        
        # Growing period risk (shorter period = lower risk)
        if crop['growing_period_days'] < 90:
            period_score = 9.0
        elif crop['growing_period_days'] < 120:
            period_score = 7.0
        else:
            period_score = 6.0
        
        return (water_score + weather_score + period_score) / 3
    
    def get_filtered_recommendations(self, region_name, crop_type="All", min_roi=0, max_investment=100000):
        """Get recommendations with additional filters"""
        
        # Get base recommendations
        region_data = {'name': region_name, 'climate_zone': 'Subtropical'}  # Simplified
        weather_data = get_weather_data_for_region(region_name)
        recommendations = self.get_recommendations(region_data, weather_data)
        
        # Apply filters
        filtered = []
        for crop in recommendations:
            # Type filter
            if crop_type != "All" and crop['type'] != crop_type:
                continue
            
            # ROI filter
            if crop['roi'] < min_roi:
                continue
            
            # Investment filter
            if crop['production_cost'] > max_investment:
                continue
            
            filtered.append(crop)
        
        return filtered
    
    def compare_crops(self, crop_names, region_name):
        """Compare specific crops for a region"""
        
        region_data = {'name': region_name, 'climate_zone': 'Subtropical'}
        weather_data = get_weather_data_for_region(region_name)
        all_recommendations = self.get_recommendations(region_data, weather_data, top_n=50)
        
        # Filter for requested crops
        comparison = []
        for crop_name in crop_names:
            crop_data = next((crop for crop in all_recommendations if crop['name'] == crop_name), None)
            if crop_data:
                comparison.append(crop_data)
        
        return comparison
    
    def get_seasonal_recommendations(self, region_name, season):
        """Get recommendations for specific season"""
        
        region_data = {'name': region_name, 'climate_zone': 'Subtropical'}
        weather_data = get_weather_data_for_region(region_name)
        all_recommendations = self.get_recommendations(region_data, weather_data, top_n=50)
        
        # Filter by season
        seasonal_crops = []
        
        season_map = {
            'Kharif': ['Kharif', 'Monsoon', 'Jun', 'Jul', 'Aug'],
            'Rabi': ['Rabi', 'Winter', 'Nov', 'Dec', 'Jan', 'Feb'],
            'Zaid': ['Zaid', 'Summer', 'Mar', 'Apr', 'May']
        }
        
        season_keywords = season_map.get(season, [])
        
        for crop in all_recommendations:
            growing_season = crop['growing_season'].lower()
            if any(keyword.lower() in growing_season for keyword in season_keywords):
                seasonal_crops.append(crop)
        
        return seasonal_crops
    
    def calculate_portfolio_risk(self, selected_crops, allocations, region_name):
        """Calculate risk for a crop portfolio"""
        
        if len(selected_crops) != len(allocations):
            return None
        
        # Get crop data
        region_data = {'name': region_name, 'climate_zone': 'Subtropical'}
        weather_data = get_weather_data_for_region(region_name)
        all_recommendations = self.get_recommendations(region_data, weather_data, top_n=50)
        
        portfolio_risk = 0
        total_weight = sum(allocations)
        
        for i, crop_name in enumerate(selected_crops):
            crop_data = next((crop for crop in all_recommendations if crop['name'] == crop_name), None)
            if crop_data:
                weight = allocations[i] / total_weight
                crop_risk = 10 - crop_data['risk_score']  # Convert to risk (higher = more risky)
                portfolio_risk += weight * crop_risk
        
        return portfolio_risk
    
    def get_diversification_suggestions(self, current_crops, region_name):
        """Suggest crops for diversification"""
        
        region_data = {'name': region_name, 'climate_zone': 'Subtropical'}
        weather_data = get_weather_data_for_region(region_name)
        all_recommendations = self.get_recommendations(region_data, weather_data, top_n=50)
        
        # Get types of current crops
        current_types = set()
        for crop_name in current_crops:
            crop_data = next((crop for crop in all_recommendations if crop['name'] == crop_name), None)
            if crop_data:
                current_types.add(crop_data['type'])
        
        # Suggest crops from different types
        diversification_suggestions = []
        for crop in all_recommendations:
            if crop['type'] not in current_types and crop['name'] not in current_crops:
                diversification_suggestions.append(crop)
        
        return diversification_suggestions[:5]  # Top 5 suggestions
