import os
import time
import requests
import pandas as pd

_CACHE = {
    'data': None,
    'ts': 0,
}

def get_crop_database(force_refresh=False):
    """
    Returns crop database, preferring realtime API data when configured.
    Fallbacks to static synthetic data if API is not configured or fails.
    """
    api_key = os.environ.get('CROP_API_KEY')
    api_url = (os.environ.get('CROP_API_URL') or '').strip()
    cache_ttl = int(os.environ.get('CROP_API_CACHE_TTL_SECONDS', '900'))

    # Serve from cache if valid
    if not force_refresh and _CACHE['data'] is not None and (time.time() - _CACHE['ts']) < cache_ttl:
        return _CACHE['data']

    # Try realtime API if configured
    if api_key and api_url:
        try:
            static_defaults = get_static_crop_database()
            static_by_name = {c['name']: c for c in static_defaults}
            realtime_items = _fetch_crops_from_api(api_url, api_key)
            merged = _merge_with_defaults_and_derive(realtime_items, static_by_name)
            if merged:
                _CACHE['data'] = merged
                _CACHE['ts'] = time.time()
                return merged
        except Exception:
            # Swallow and fall back to static data to keep the app operational
            pass

    # Fallback to static data
    static_data = get_static_crop_database()
    _CACHE['data'] = static_data
    _CACHE['ts'] = time.time()
    return static_data

def _fetch_crops_from_api(api_url, api_key):
    """Fetch crop items from external API and return a list of dicts."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'x-api-key': api_key,
        'Accept': 'application/json',
    }
    resp = requests.get(api_url, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and isinstance(data.get('data'), list):
        return data['data']
    if isinstance(data, list):
        return data
    return []

def _to_number(value):
    try:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if value.strip() == '':
                return None
            return float(value)
    except Exception:
        return None
    return None

def _normalize_api_crop(item):
    """Normalize various possible API field names into our schema."""
    def pick(*keys, default=None):
        for k in keys:
            if k in item and item[k] is not None:
                return item[k]
        return default

    return {
        'name': pick('name', 'crop', 'crop_name'),
        'type': pick('type', 'category', 'crop_type'),
        'temp_min': _to_number(pick('temp_min', 'min_temp', 'temperature_min', 'tempMin')),
        'temp_max': _to_number(pick('temp_max', 'max_temp', 'temperature_max', 'tempMax')),
        'rainfall_min': _to_number(pick('rainfall_min', 'min_rainfall', 'rainfallMin')),
        'rainfall_max': _to_number(pick('rainfall_max', 'max_rainfall', 'rainfallMax')),
        'soil_ph_min': _to_number(pick('soil_ph_min', 'soilPhMin', 'soil_ph_low', 'ph_min')),
        'soil_ph_max': _to_number(pick('soil_ph_max', 'soilPhMax', 'soil_ph_high', 'ph_max')),
        'growing_season': pick('growing_season', 'season', 'growingSeason'),
        'water_requirement': pick('water_requirement', 'water', 'waterRequirement'),
        'market_price': _to_number(pick('market_price', 'price', 'marketPrice')),
        'production_cost': _to_number(pick('production_cost', 'cost', 'productionCost')),
        'expected_yield': _to_number(pick('expected_yield', 'yield', 'expectedYield')),
        'growing_period_days': _to_number(pick('growing_period_days', 'growingDays', 'duration_days')),
    }

def _merge_with_defaults_and_derive(realtime_items, static_by_name):
    """
    Merge realtime items with static defaults by name and compute derived metrics.
    If realtime list is empty, return static defaults.
    """
    if not realtime_items:
        return list(static_by_name.values())

    result = []
    for raw in realtime_items:
        base = _normalize_api_crop(raw)
        defaults = static_by_name.get(base.get('name') or '', {})

        merged = {}
        for key in [
            'name','type','temp_min','temp_max','rainfall_min','rainfall_max',
            'soil_ph_min','soil_ph_max','growing_season','water_requirement',
            'market_price','production_cost','expected_yield','growing_period_days']:
            value = base.get(key)
            if value is None:
                value = defaults.get(key)
            merged[key] = value

        revenue = (merged.get('expected_yield') or 0) * (merged.get('market_price') or 0)
        production_cost = merged.get('production_cost') or 0
        profit = revenue - production_cost
        merged['profit_margin'] = (profit / revenue) * 100 if revenue > 0 else 0
        merged['roi'] = (profit / production_cost) * 100 if production_cost > 0 else 0

        result.append(merged)

    return result

def get_static_crop_database():
    """
    Static synthetic crop database used as a fallback.
    """
    crops_data = [
        # Cereals
        {
            'name': 'Rice (Basmati)',
            'type': 'Cereals',
            'temp_min': 20, 'temp_max': 35,
            'rainfall_min': 1000, 'rainfall_max': 2000,
            'soil_ph_min': 5.5, 'soil_ph_max': 7.0,
            'growing_season': 'Kharif (Jun-Nov)',
            'water_requirement': 'High',
            'market_price': 4500,  # ₹ per quintal
            'production_cost': 35000,  # ₹ per acre
            'expected_yield': 20,  # quintal per acre
            'growing_period_days': 120
        },
        {
            'name': 'Wheat',
            'type': 'Cereals',
            'temp_min': 10, 'temp_max': 25,
            'rainfall_min': 300, 'rainfall_max': 800,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.5,
            'growing_season': 'Rabi (Nov-Apr)',
            'water_requirement': 'Medium',
            'market_price': 2200,
            'production_cost': 25000,
            'expected_yield': 25,
            'growing_period_days': 120
        },
        {
            'name': 'Maize',
            'type': 'Cereals',
            'temp_min': 15, 'temp_max': 35,
            'rainfall_min': 500, 'rainfall_max': 1200,
            'soil_ph_min': 5.8, 'soil_ph_max': 7.8,
            'growing_season': 'Kharif/Rabi',
            'water_requirement': 'Medium',
            'market_price': 1800,
            'production_cost': 20000,
            'expected_yield': 30,
            'growing_period_days': 90
        },
        
        # Pulses
        {
            'name': 'Chana (Chickpea)',
            'type': 'Pulses',
            'temp_min': 15, 'temp_max': 30,
            'rainfall_min': 300, 'rainfall_max': 600,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.5,
            'growing_season': 'Rabi (Oct-Mar)',
            'water_requirement': 'Low',
            'market_price': 5500,
            'production_cost': 18000,
            'expected_yield': 12,
            'growing_period_days': 110
        },
        {
            'name': 'Moong (Mung Bean)',
            'type': 'Pulses',
            'temp_min': 20, 'temp_max': 40,
            'rainfall_min': 300, 'rainfall_max': 800,
            'soil_ph_min': 6.2, 'soil_ph_max': 7.2,
            'growing_season': 'Kharif/Summer',
            'water_requirement': 'Low',
            'market_price': 6000,
            'production_cost': 15000,
            'expected_yield': 8,
            'growing_period_days': 70
        },
        {
            'name': 'Urad (Black Gram)',
            'type': 'Pulses',
            'temp_min': 20, 'temp_max': 35,
            'rainfall_min': 400, 'rainfall_max': 800,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.0,
            'growing_season': 'Kharif (Jun-Oct)',
            'water_requirement': 'Medium',
            'market_price': 6500,
            'production_cost': 16000,
            'expected_yield': 6,
            'growing_period_days': 80
        },
        
        # Oilseeds
        {
            'name': 'Soybean',
            'type': 'Oilseeds',
            'temp_min': 20, 'temp_max': 30,
            'rainfall_min': 450, 'rainfall_max': 700,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.5,
            'growing_season': 'Kharif (Jun-Oct)',
            'water_requirement': 'Medium',
            'market_price': 4200,
            'production_cost': 22000,
            'expected_yield': 18,
            'growing_period_days': 100
        },
        {
            'name': 'Sunflower',
            'type': 'Oilseeds',
            'temp_min': 18, 'temp_max': 35,
            'rainfall_min': 400, 'rainfall_max': 800,
            'soil_ph_min': 6.0, 'soil_ph_max': 8.0,
            'growing_season': 'Kharif/Rabi',
            'water_requirement': 'Medium',
            'market_price': 5800,
            'production_cost': 20000,
            'expected_yield': 12,
            'growing_period_days': 90
        },
        {
            'name': 'Mustard',
            'type': 'Oilseeds',
            'temp_min': 10, 'temp_max': 25,
            'rainfall_min': 200, 'rainfall_max': 500,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.5,
            'growing_season': 'Rabi (Oct-Mar)',
            'water_requirement': 'Low',
            'market_price': 4800,
            'production_cost': 18000,
            'expected_yield': 10,
            'growing_period_days': 120
        },
        
        # Vegetables
        {
            'name': 'Tomato',
            'type': 'Vegetables',
            'temp_min': 18, 'temp_max': 27,
            'rainfall_min': 200, 'rainfall_max': 400,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.0,
            'growing_season': 'All seasons',
            'water_requirement': 'High',
            'market_price': 2500,
            'production_cost': 45000,
            'expected_yield': 150,
            'growing_period_days': 120
        },
        {
            'name': 'Potato',
            'type': 'Vegetables',
            'temp_min': 15, 'temp_max': 25,
            'rainfall_min': 200, 'rainfall_max': 400,
            'soil_ph_min': 5.0, 'soil_ph_max': 7.0,
            'growing_season': 'Rabi (Oct-Feb)',
            'water_requirement': 'Medium',
            'market_price': 1200,
            'production_cost': 30000,
            'expected_yield': 80,
            'growing_period_days': 90
        },
        {
            'name': 'Onion',
            'type': 'Vegetables',
            'temp_min': 13, 'temp_max': 24,
            'rainfall_min': 150, 'rainfall_max': 400,
            'soil_ph_min': 5.8, 'soil_ph_max': 7.0,
            'growing_season': 'Rabi (Nov-Apr)',
            'water_requirement': 'Medium',
            'market_price': 1800,
            'production_cost': 35000,
            'expected_yield': 100,
            'growing_period_days': 120
        },
        {
            'name': 'Chili',
            'type': 'Vegetables',
            'temp_min': 20, 'temp_max': 35,
            'rainfall_min': 300, 'rainfall_max': 600,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.0,
            'growing_season': 'Kharif/Rabi',
            'water_requirement': 'Medium',
            'market_price': 8000,
            'production_cost': 40000,
            'expected_yield': 25,
            'growing_period_days': 150
        },
        
        # Fruits
        {
            'name': 'Mango (Seasonal)',
            'type': 'Fruits',
            'temp_min': 24, 'temp_max': 30,
            'rainfall_min': 750, 'rainfall_max': 2500,
            'soil_ph_min': 5.5, 'soil_ph_max': 7.5,
            'growing_season': 'Perennial',
            'water_requirement': 'Medium',
            'market_price': 6000,
            'production_cost': 80000,
            'expected_yield': 50,
            'growing_period_days': 365
        },
        {
            'name': 'Banana',
            'type': 'Fruits',
            'temp_min': 26, 'temp_max': 30,
            'rainfall_min': 1200, 'rainfall_max': 2500,
            'soil_ph_min': 6.0, 'soil_ph_max': 7.5,
            'growing_season': 'All year',
            'water_requirement': 'High',
            'market_price': 1500,
            'production_cost': 60000,
            'expected_yield': 200,
            'growing_period_days': 365
        },
        {
            'name': 'Grapes',
            'type': 'Fruits',
            'temp_min': 15, 'temp_max': 40,
            'rainfall_min': 400, 'rainfall_max': 1200,
            'soil_ph_min': 6.5, 'soil_ph_max': 8.0,
            'growing_season': 'Perennial',
            'water_requirement': 'Medium',
            'market_price': 4000,
            'production_cost': 120000,
            'expected_yield': 80,
            'growing_period_days': 365
        }
    ]

    # Add calculated fields
    for crop in crops_data:
        revenue = crop['expected_yield'] * crop['market_price']
        profit = revenue - crop['production_cost']
        crop['profit_margin'] = (profit / revenue) * 100 if revenue > 0 else 0
        crop['roi'] = (profit / crop['production_cost']) * 100 if crop['production_cost'] > 0 else 0

    return crops_data

def get_crop_by_name(crop_name):
    """Get specific crop data by name"""
    crops = get_crop_database()
    return next((crop for crop in crops if crop['name'] == crop_name), None)

def get_crops_by_type(crop_type):
    """Get crops filtered by type"""
    crops = get_crop_database()
    if crop_type == "All":
        return crops
    return [crop for crop in crops if crop['type'] == crop_type]

def get_suitable_crops_for_climate(temp_range, rainfall_range, soil_ph=6.5):
    """
    Get crops suitable for given climate conditions
    temp_range: (min_temp, max_temp)
    rainfall_range: (min_rainfall, max_rainfall)
    """
    crops = get_crop_database()
    suitable_crops = []
    
    min_temp, max_temp = temp_range
    min_rainfall, max_rainfall = rainfall_range
    
    for crop in crops:
        # Check temperature compatibility
        temp_compatible = (crop['temp_min'] <= max_temp and crop['temp_max'] >= min_temp)
        
        # Check rainfall compatibility
        rainfall_compatible = (crop['rainfall_min'] <= max_rainfall and crop['rainfall_max'] >= min_rainfall)
        
        # Check soil pH compatibility
        ph_compatible = (crop['soil_ph_min'] <= soil_ph <= crop['soil_ph_max'])
        
        if temp_compatible and rainfall_compatible and ph_compatible:
            # Calculate suitability score
            temp_score = 10 - abs((crop['temp_min'] + crop['temp_max'])/2 - (min_temp + max_temp)/2) / 5
            rainfall_score = 10 - abs((crop['rainfall_min'] + crop['rainfall_max'])/2 - (min_rainfall + max_rainfall)/2) / 200
            
            temp_score = max(0, min(10, temp_score))
            rainfall_score = max(0, min(10, rainfall_score))
            
            crop['suitability_score'] = (temp_score + rainfall_score) / 2
            suitable_crops.append(crop)
    
    return sorted(suitable_crops, key=lambda x: x['suitability_score'], reverse=True)
