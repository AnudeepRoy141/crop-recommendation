def get_indian_states_data():
    """
    Returns data for major Indian states/regions with their coordinates,
    climate zones, and agricultural characteristics
    """
    
    regions = [
        {
            'name': 'Punjab',
            'lat': 31.1471,
            'lon': 75.3412,
            'climate_zone': 'Subtropical Continental',
            'soil_type': 'Alluvial',
            'annual_rainfall': 600,
            'temp_range': '5-45',
            'major_crops': ['Wheat', 'Rice', 'Maize', 'Cotton'],
            'agricultural_zone': 'Indo-Gangetic Plains'
        },
        {
            'name': 'Maharashtra',
            'lat': 19.7515,
            'lon': 75.7139,
            'climate_zone': 'Tropical Monsoon',
            'soil_type': 'Black Cotton',
            'annual_rainfall': 1200,
            'temp_range': '12-42',
            'major_crops': ['Sugarcane', 'Cotton', 'Soybean', 'Onion'],
            'agricultural_zone': 'Western Plateau'
        },
        {
            'name': 'Tamil Nadu',
            'lat': 11.1271,
            'lon': 78.6569,
            'climate_zone': 'Tropical',
            'soil_type': 'Red Sandy',
            'annual_rainfall': 1000,
            'temp_range': '19-37',
            'major_crops': ['Rice', 'Sugarcane', 'Cotton', 'Groundnut'],
            'agricultural_zone': 'Southern Peninsula'
        },
        {
            'name': 'Uttar Pradesh',
            'lat': 26.8467,
            'lon': 80.9462,
            'climate_zone': 'Subtropical',
            'soil_type': 'Alluvial',
            'annual_rainfall': 800,
            'temp_range': '2-47',
            'major_crops': ['Wheat', 'Rice', 'Sugarcane', 'Potato'],
            'agricultural_zone': 'Indo-Gangetic Plains'
        },
        {
            'name': 'Karnataka',
            'lat': 15.3173,
            'lon': 75.7139,
            'climate_zone': 'Tropical Monsoon',
            'soil_type': 'Red Laterite',
            'annual_rainfall': 1100,
            'temp_range': '15-35',
            'major_crops': ['Rice', 'Ragi', 'Sugarcane', 'Coffee'],
            'agricultural_zone': 'Southern Plateau'
        },
        {
            'name': 'Gujarat',
            'lat': 22.2587,
            'lon': 71.1924,
            'climate_zone': 'Semi-Arid',
            'soil_type': 'Black Cotton',
            'annual_rainfall': 700,
            'temp_range': '10-42',
            'major_crops': ['Cotton', 'Groundnut', 'Wheat', 'Bajra'],
            'agricultural_zone': 'Western Dry Region'
        },
        {
            'name': 'Rajasthan',
            'lat': 27.0238,
            'lon': 74.2179,
            'climate_zone': 'Arid',
            'soil_type': 'Sandy Desert',
            'annual_rainfall': 400,
            'temp_range': '2-50',
            'major_crops': ['Bajra', 'Jowar', 'Wheat', 'Mustard'],
            'agricultural_zone': 'Western Dry Region'
        },
        {
            'name': 'West Bengal',
            'lat': 22.9868,
            'lon': 87.8550,
            'climate_zone': 'Tropical Monsoon',
            'soil_type': 'Alluvial',
            'annual_rainfall': 1500,
            'temp_range': '10-38',
            'major_crops': ['Rice', 'Jute', 'Tea', 'Potato'],
            'agricultural_zone': 'Eastern Region'
        },
        {
            'name': 'Andhra Pradesh',
            'lat': 15.9129,
            'lon': 79.7400,
            'climate_zone': 'Tropical',
            'soil_type': 'Red Sandy',
            'annual_rainfall': 900,
            'temp_range': '16-40',
            'major_crops': ['Rice', 'Cotton', 'Sugarcane', 'Chili'],
            'agricultural_zone': 'Southern Peninsula'
        },
        {
            'name': 'Madhya Pradesh',
            'lat': 22.9734,
            'lon': 78.6569,
            'climate_zone': 'Subtropical',
            'soil_type': 'Black Cotton',
            'annual_rainfall': 1000,
            'temp_range': '6-46',
            'major_crops': ['Wheat', 'Soybean', 'Rice', 'Cotton'],
            'agricultural_zone': 'Central Plateau'
        },
        {
            'name': 'Haryana',
            'lat': 29.0588,
            'lon': 76.0856,
            'climate_zone': 'Subtropical Continental',
            'soil_type': 'Alluvial',
            'annual_rainfall': 650,
            'temp_range': '5-45',
            'major_crops': ['Wheat', 'Rice', 'Sugarcane', 'Cotton'],
            'agricultural_zone': 'Indo-Gangetic Plains'
        },
        {
            'name': 'Bihar',
            'lat': 25.0961,
            'lon': 85.3131,
            'climate_zone': 'Subtropical',
            'soil_type': 'Alluvial',
            'annual_rainfall': 1200,
            'temp_range': '5-42',
            'major_crops': ['Rice', 'Wheat', 'Maize', 'Sugarcane'],
            'agricultural_zone': 'Indo-Gangetic Plains'
        },
        {
            'name': 'Odisha',
            'lat': 20.9517,
            'lon': 85.0985,
            'climate_zone': 'Tropical Monsoon',
            'soil_type': 'Red Laterite',
            'annual_rainfall': 1400,
            'temp_range': '11-40',
            'major_crops': ['Rice', 'Jute', 'Sugarcane', 'Turmeric'],
            'agricultural_zone': 'Eastern Region'
        },
        {
            'name': 'Kerala',
            'lat': 10.8505,
            'lon': 76.2711,
            'climate_zone': 'Tropical Monsoon',
            'soil_type': 'Laterite',
            'annual_rainfall': 2800,
            'temp_range': '23-32',
            'major_crops': ['Rice', 'Coconut', 'Spices', 'Rubber'],
            'agricultural_zone': 'Southern Peninsula'
        },
        {
            'name': 'Assam',
            'lat': 26.2006,
            'lon': 92.9376,
            'climate_zone': 'Subtropical Monsoon',
            'soil_type': 'Alluvial',
            'annual_rainfall': 2200,
            'temp_range': '8-36',
            'major_crops': ['Rice', 'Tea', 'Jute', 'Sugarcane'],
            'agricultural_zone': 'Eastern Himalayan'
        }
    ]
    
    return regions

def get_district_coordinates(state_name):
    """
    Get coordinates for major districts within a state
    """
    
    district_data = {
        'Punjab': [
            {'name': 'Ludhiana', 'lat': 30.901, 'lon': 75.857},
            {'name': 'Amritsar', 'lat': 31.634, 'lon': 74.872},
            {'name': 'Jalandhar', 'lat': 31.326, 'lon': 75.576},
            {'name': 'Patiala', 'lat': 30.336, 'lon': 76.392}
        ],
        'Maharashtra': [
            {'name': 'Pune', 'lat': 18.520, 'lon': 73.856},
            {'name': 'Nashik', 'lat': 19.997, 'lon': 73.789},
            {'name': 'Nagpur', 'lat': 21.146, 'lon': 79.089},
            {'name': 'Aurangabad', 'lat': 19.876, 'lon': 75.343}
        ],
        'Tamil Nadu': [
            {'name': 'Coimbatore', 'lat': 11.016, 'lon': 76.955},
            {'name': 'Madurai', 'lat': 9.925, 'lon': 78.119},
            {'name': 'Salem', 'lat': 11.664, 'lon': 78.146},
            {'name': 'Tiruchirappalli', 'lat': 10.790, 'lon': 78.704}
        ]
    }
    
    return district_data.get(state_name, [])

def get_agro_climatic_zones():
    """
    Get India's agro-climatic zones with their characteristics
    """
    
    zones = [
        {
            'zone': 'Western Himalayan Region',
            'states': ['Jammu & Kashmir', 'Himachal Pradesh', 'Uttarakhand'],
            'characteristics': 'Cold temperate climate, horticulture focus',
            'major_crops': ['Apple', 'Rice', 'Wheat', 'Maize']
        },
        {
            'zone': 'Eastern Himalayan Region',
            'states': ['Assam', 'West Bengal Hills', 'Sikkim'],
            'characteristics': 'High rainfall, tea cultivation',
            'major_crops': ['Tea', 'Rice', 'Maize', 'Oranges']
        },
        {
            'zone': 'Lower Gangetic Plains',
            'states': ['West Bengal', 'Bihar', 'Odisha'],
            'characteristics': 'High humidity, rice-based farming',
            'major_crops': ['Rice', 'Jute', 'Sugarcane', 'Potato']
        },
        {
            'zone': 'Middle Gangetic Plains',
            'states': ['Eastern UP', 'Bihar'],
            'characteristics': 'Rice-wheat system dominant',
            'major_crops': ['Rice', 'Wheat', 'Sugarcane', 'Potato']
        },
        {
            'zone': 'Upper Gangetic Plains',
            'states': ['Western UP', 'Punjab', 'Haryana', 'Delhi'],
            'characteristics': 'Intensive agriculture, wheat-rice system',
            'major_crops': ['Wheat', 'Rice', 'Sugarcane', 'Cotton']
        },
        {
            'zone': 'Trans-Gangetic Plains',
            'states': ['Punjab', 'Haryana'],
            'characteristics': 'Green revolution area, high productivity',
            'major_crops': ['Wheat', 'Rice', 'Cotton', 'Sugarcane']
        },
        {
            'zone': 'Eastern Plateau and Hills',
            'states': ['Jharkhand', 'Chhattisgarh', 'Odisha Hills'],
            'characteristics': 'Tribal areas, forest-based agriculture',
            'major_crops': ['Rice', 'Maize', 'Millets', 'Pulses']
        },
        {
            'zone': 'Central Plateau and Hills',
            'states': ['Madhya Pradesh', 'Rajasthan', 'UP Hills'],
            'characteristics': 'Black cotton soil, soybean cultivation',
            'major_crops': ['Soybean', 'Wheat', 'Cotton', 'Sugarcane']
        },
        {
            'zone': 'Western Plateau and Hills',
            'states': ['Maharashtra', 'Madhya Pradesh'],
            'characteristics': 'Varied topography, cotton and sugarcane',
            'major_crops': ['Cotton', 'Sugarcane', 'Soybean', 'Wheat']
        },
        {
            'zone': 'Southern Plateau and Hills',
            'states': ['Karnataka', 'Andhra Pradesh', 'Tamil Nadu'],
            'characteristics': 'Dryland farming, millets cultivation',
            'major_crops': ['Rice', 'Ragi', 'Cotton', 'Groundnut']
        },
        {
            'zone': 'East Coast Plains and Hills',
            'states': ['Andhra Pradesh', 'Tamil Nadu', 'Puducherry'],
            'characteristics': 'Deltaic agriculture, high productivity',
            'major_crops': ['Rice', 'Sugarcane', 'Cotton', 'Groundnut']
        },
        {
            'zone': 'West Coast Plains and Ghats',
            'states': ['Kerala', 'Karnataka', 'Goa', 'Maharashtra'],
            'characteristics': 'High rainfall, spice cultivation',
            'major_crops': ['Rice', 'Coconut', 'Spices', 'Areca nut']
        },
        {
            'zone': 'Gujarat Plains and Hills',
            'states': ['Gujarat'],
            'characteristics': 'Cotton cultivation, irrigation-based',
            'major_crops': ['Cotton', 'Groundnut', 'Wheat', 'Bajra']
        },
        {
            'zone': 'Western Dry Region',
            'states': ['Rajasthan'],
            'characteristics': 'Arid climate, drought-prone',
            'major_crops': ['Bajra', 'Jowar', 'Wheat', 'Mustard']
        },
        {
            'zone': 'Island Region',
            'states': ['Andaman & Nicobar', 'Lakshadweep'],
            'characteristics': 'Tropical islands, coconut cultivation',
            'major_crops': ['Coconut', 'Rice', 'Spices', 'Areca nut']
        }
    ]
    
    return zones

def get_soil_types():
    """
    Get major soil types in India with their characteristics
    """
    
    soil_types = [
        {
            'type': 'Alluvial Soil',
            'distribution': 'Gangetic Plains, River Valleys',
            'characteristics': 'Fertile, well-drained, high in potash',
            'suitable_crops': ['Rice', 'Wheat', 'Sugarcane', 'Cotton'],
            'ph_range': '6.0-7.5'
        },
        {
            'type': 'Black Cotton Soil',
            'distribution': 'Deccan Plateau, Maharashtra, Gujarat',
            'characteristics': 'High clay content, moisture retention',
            'suitable_crops': ['Cotton', 'Sugarcane', 'Wheat', 'Jowar'],
            'ph_range': '7.0-8.5'
        },
        {
            'type': 'Red Soil',
            'distribution': 'South India, Eastern India',
            'characteristics': 'Rich in iron oxide, well-drained',
            'suitable_crops': ['Cotton', 'Wheat', 'Rice', 'Pulses'],
            'ph_range': '5.5-7.0'
        },
        {
            'type': 'Laterite Soil',
            'distribution': 'Western Ghats, Eastern Ghats',
            'characteristics': 'High in iron and aluminum, acidic',
            'suitable_crops': ['Rice', 'Ragi', 'Cashew', 'Tapioca'],
            'ph_range': '4.5-6.0'
        },
        {
            'type': 'Mountain Soil',
            'distribution': 'Himalayan Region',
            'characteristics': 'Thin layer, rich in organic matter',
            'suitable_crops': ['Tea', 'Coffee', 'Spices', 'Fruits'],
            'ph_range': '5.0-7.0'
        },
        {
            'type': 'Desert Soil',
            'distribution': 'Rajasthan, Gujarat',
            'characteristics': 'Sandy, low fertility, low moisture',
            'suitable_crops': ['Bajra', 'Jowar', 'Moth', 'Guar'],
            'ph_range': '7.0-8.5'
        }
    ]
    
    return soil_types
