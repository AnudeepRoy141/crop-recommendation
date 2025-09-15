import pandas as pd
import numpy as np
from typing import Dict, List, Optional

def get_detailed_soil_data():
    """
    Returns comprehensive soil data for Indian regions with detailed analysis
    """
    
    soil_data = {
        'Punjab': {
            'primary_soil': 'Alluvial',
            'secondary_soils': ['Sandy Loam', 'Clay Loam'],
            'ph_range': [6.8, 7.5],
            'organic_matter': 0.8,  # percentage
            'nitrogen': 'Medium',
            'phosphorus': 'High',
            'potassium': 'High',
            'drainage': 'Good',
            'erosion_risk': 'Low',
            'salinity_level': 'Low',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'High',
            'texture_class': 'Loamy',
            'cec': 25.5,  # Cation Exchange Capacity
            'bulk_density': 1.35
        },
        'Maharashtra': {
            'primary_soil': 'Black Cotton',
            'secondary_soils': ['Red Soil', 'Laterite'],
            'ph_range': [7.2, 8.3],
            'organic_matter': 0.6,
            'nitrogen': 'Low',
            'phosphorus': 'Medium',
            'potassium': 'High',
            'drainage': 'Poor',
            'erosion_risk': 'Medium',
            'salinity_level': 'Low',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'Very High',
            'texture_class': 'Clay',
            'cec': 35.2,
            'bulk_density': 1.55
        },
        'Tamil Nadu': {
            'primary_soil': 'Red Sandy',
            'secondary_soils': ['Black Soil', 'Alluvial'],
            'ph_range': [6.0, 7.2],
            'organic_matter': 0.5,
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Medium',
            'drainage': 'Excellent',
            'erosion_risk': 'High',
            'salinity_level': 'Medium',
            'soil_depth': 'Medium',
            'water_holding_capacity': 'Low',
            'texture_class': 'Sandy',
            'cec': 15.8,
            'bulk_density': 1.45
        },
        'Uttar Pradesh': {
            'primary_soil': 'Alluvial',
            'secondary_soils': ['Sandy', 'Clay Loam'],
            'ph_range': [6.5, 7.8],
            'organic_matter': 0.7,
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High',
            'drainage': 'Good',
            'erosion_risk': 'Low',
            'salinity_level': 'Medium',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'High',
            'texture_class': 'Loamy',
            'cec': 22.1,
            'bulk_density': 1.40
        },
        'Karnataka': {
            'primary_soil': 'Red Laterite',
            'secondary_soils': ['Black Soil', 'Alluvial'],
            'ph_range': [5.5, 6.8],
            'organic_matter': 0.4,
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Low',
            'drainage': 'Good',
            'erosion_risk': 'Medium',
            'salinity_level': 'Low',
            'soil_depth': 'Medium',
            'water_holding_capacity': 'Medium',
            'texture_class': 'Sandy Clay',
            'cec': 18.7,
            'bulk_density': 1.50
        },
        'Gujarat': {
            'primary_soil': 'Black Cotton',
            'secondary_soils': ['Alluvial', 'Sandy'],
            'ph_range': [7.5, 8.5],
            'organic_matter': 0.5,
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High',
            'drainage': 'Poor',
            'erosion_risk': 'Low',
            'salinity_level': 'High',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'High',
            'texture_class': 'Clay',
            'cec': 32.8,
            'bulk_density': 1.60
        },
        'Rajasthan': {
            'primary_soil': 'Sandy Desert',
            'secondary_soils': ['Alluvial', 'Red Soil'],
            'ph_range': [7.8, 8.8],
            'organic_matter': 0.2,
            'nitrogen': 'Very Low',
            'phosphorus': 'Low',
            'potassium': 'Low',
            'drainage': 'Excellent',
            'erosion_risk': 'Very High',
            'salinity_level': 'High',
            'soil_depth': 'Shallow',
            'water_holding_capacity': 'Very Low',
            'texture_class': 'Sand',
            'cec': 8.5,
            'bulk_density': 1.65
        },
        'West Bengal': {
            'primary_soil': 'Alluvial',
            'secondary_soils': ['Laterite', 'Peat'],
            'ph_range': [5.8, 7.0],
            'organic_matter': 1.2,
            'nitrogen': 'High',
            'phosphorus': 'Medium',
            'potassium': 'Medium',
            'drainage': 'Poor',
            'erosion_risk': 'Medium',
            'salinity_level': 'Low',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'High',
            'texture_class': 'Clay Loam',
            'cec': 28.3,
            'bulk_density': 1.30
        },
        'Andhra Pradesh': {
            'primary_soil': 'Red Sandy',
            'secondary_soils': ['Black Soil', 'Alluvial'],
            'ph_range': [6.2, 7.5],
            'organic_matter': 0.3,
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Medium',
            'drainage': 'Good',
            'erosion_risk': 'High',
            'salinity_level': 'Medium',
            'soil_depth': 'Medium',
            'water_holding_capacity': 'Medium',
            'texture_class': 'Sandy Clay',
            'cec': 16.9,
            'bulk_density': 1.48
        },
        'Madhya Pradesh': {
            'primary_soil': 'Black Cotton',
            'secondary_soils': ['Red Soil', 'Alluvial'],
            'ph_range': [7.0, 8.2],
            'organic_matter': 0.6,
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High',
            'drainage': 'Moderate',
            'erosion_risk': 'Medium',
            'salinity_level': 'Low',
            'soil_depth': 'Deep',
            'water_holding_capacity': 'High',
            'texture_class': 'Clay',
            'cec': 30.1,
            'bulk_density': 1.52
        }
    }
    
    return soil_data

def analyze_soil_crop_compatibility(crop_requirements: Dict, soil_data: Dict) -> Dict:
    """
    Analyze compatibility between crop requirements and soil characteristics
    """
    
    # Extract crop soil requirements
    crop_ph_min = crop_requirements.get('soil_ph_min', 6.0)
    crop_ph_max = crop_requirements.get('soil_ph_max', 7.5)
    crop_water_req = crop_requirements.get('water_requirement', 'Medium')
    crop_type = crop_requirements.get('type', 'Cereals')
    
    # Extract soil characteristics
    soil_ph_range = soil_data['ph_range']
    soil_drainage = soil_data['drainage']
    soil_water_capacity = soil_data['water_holding_capacity']
    soil_nutrients = {
        'N': soil_data['nitrogen'],
        'P': soil_data['phosphorus'],
        'K': soil_data['potassium']
    }
    
    # Calculate pH compatibility score (0-10)
    soil_ph_avg = sum(soil_ph_range) / 2
    crop_ph_optimal = (crop_ph_min + crop_ph_max) / 2
    ph_deviation = abs(soil_ph_avg - crop_ph_optimal)
    ph_score = max(0, 10 - ph_deviation * 2)
    
    # Calculate water compatibility score
    water_compatibility = {
        'High': {'Excellent': 7, 'Good': 9, 'Moderate': 6, 'Poor': 4},
        'Medium': {'Excellent': 8, 'Good': 10, 'Moderate': 8, 'Poor': 5},
        'Low': {'Excellent': 6, 'Good': 8, 'Moderate': 9, 'Poor': 10}
    }
    
    water_score = water_compatibility.get(crop_water_req, {}).get(soil_drainage, 5)
    
    # Calculate nutrient score
    nutrient_levels = {'Very Low': 1, 'Low': 3, 'Medium': 6, 'High': 9, 'Very High': 10}
    
    # Different crops have different nutrient requirements
    crop_nutrient_needs = {
        'Cereals': {'N': 8, 'P': 6, 'K': 7},
        'Pulses': {'N': 4, 'P': 8, 'K': 6},  # Legumes fix nitrogen
        'Oilseeds': {'N': 7, 'P': 8, 'K': 8},
        'Vegetables': {'N': 9, 'P': 8, 'K': 8},
        'Fruits': {'N': 7, 'P': 7, 'K': 9}
    }
    
    crop_needs = crop_nutrient_needs.get(crop_type, {'N': 7, 'P': 7, 'K': 7})
    
    nutrient_scores = {}
    for nutrient, need in crop_needs.items():
        soil_level = nutrient_levels.get(soil_nutrients[nutrient], 5)
        # Score based on how well soil level matches crop need
        nutrient_scores[nutrient] = max(0, 10 - abs(soil_level - need))
    
    avg_nutrient_score = sum(nutrient_scores.values()) / len(nutrient_scores)
    
    # Calculate erosion risk impact
    erosion_risk_impact = {
        'Low': 10, 'Medium': 7, 'High': 4, 'Very High': 2
    }
    erosion_score = erosion_risk_impact.get(soil_data['erosion_risk'], 5)
    
    # Calculate overall soil suitability score
    overall_score = (
        ph_score * 0.25 +
        water_score * 0.30 +
        avg_nutrient_score * 0.30 +
        erosion_score * 0.15
    )
    
    # Generate recommendations
    recommendations = []
    
    if ph_score < 6:
        if soil_ph_avg > crop_ph_optimal:
            recommendations.append("Apply organic matter or sulfur to reduce soil pH")
        else:
            recommendations.append("Apply lime to increase soil pH")
    
    if water_score < 6:
        if crop_water_req == 'High' and soil_drainage == 'Poor':
            recommendations.append("Improve drainage through better field preparation")
        elif crop_water_req == 'Low' and soil_drainage == 'Excellent':
            recommendations.append("Consider water conservation techniques or mulching")
    
    if avg_nutrient_score < 6:
        low_nutrients = [n for n, score in nutrient_scores.items() if score < 6]
        if low_nutrients:
            recommendations.append(f"Apply fertilizers rich in {', '.join(low_nutrients)}")
    
    if erosion_score < 7:
        recommendations.append("Implement erosion control measures like contour farming")
    
    return {
        'overall_score': round(overall_score, 2),
        'component_scores': {
            'ph_compatibility': round(ph_score, 2),
            'water_compatibility': round(water_score, 2),
            'nutrient_adequacy': round(avg_nutrient_score, 2),
            'erosion_risk': round(erosion_score, 2)
        },
        'detailed_analysis': {
            'soil_ph_range': soil_ph_range,
            'crop_ph_requirement': [crop_ph_min, crop_ph_max],
            'nutrient_scores': {k: round(v, 2) for k, v in nutrient_scores.items()},
            'water_match': f"Crop needs {crop_water_req} water, soil has {soil_drainage} drainage"
        },
        'recommendations': recommendations,
        'suitability_grade': get_suitability_grade(overall_score)
    }

def get_suitability_grade(score: float) -> str:
    """Convert numerical score to grade"""
    if score >= 8.5:
        return 'Excellent'
    elif score >= 7.0:
        return 'Good'
    elif score >= 5.5:
        return 'Fair'
    elif score >= 4.0:
        return 'Poor'
    else:
        return 'Unsuitable'

def get_soil_improvement_plan(soil_data: Dict, target_crops: List[str]) -> Dict:
    """
    Generate a comprehensive soil improvement plan for target crops
    """
    
    improvements = {
        'immediate_actions': [],
        'short_term_goals': [],
        'long_term_strategies': [],
        'estimated_costs': {},
        'timeline': {}
    }
    
    # pH management
    ph_avg = sum(soil_data['ph_range']) / 2
    if ph_avg < 6.0:
        improvements['immediate_actions'].append({
            'action': 'Apply agricultural lime',
            'quantity': '2-3 tons per hectare',
            'cost_per_hectare': 8000,
            'timeline': '2-3 months before planting'
        })
    elif ph_avg > 8.0:
        improvements['immediate_actions'].append({
            'action': 'Apply elemental sulfur or organic matter',
            'quantity': '500-800 kg per hectare',
            'cost_per_hectare': 6000,
            'timeline': '3-4 months before planting'
        })
    
    # Organic matter enhancement
    if soil_data['organic_matter'] < 1.0:
        improvements['short_term_goals'].append({
            'goal': 'Increase organic matter content',
            'methods': ['Compost application', 'Green manuring', 'Crop residue incorporation'],
            'target': f"Increase from {soil_data['organic_matter']}% to 1.5%",
            'timeline': '1-2 years',
            'cost_per_hectare': 15000
        })
    
    # Nutrient management
    nutrient_costs = {'Low': 12000, 'Medium': 8000, 'High': 4000, 'Very Low': 18000}
    
    for nutrient, level in [('nitrogen', soil_data['nitrogen']), 
                           ('phosphorus', soil_data['phosphorus']), 
                           ('potassium', soil_data['potassium'])]:
        if level in ['Low', 'Very Low']:
            improvements['immediate_actions'].append({
                'action': f'Apply {nutrient} fertilizers',
                'cost_per_hectare': nutrient_costs[level],
                'timeline': 'Before each season'
            })
    
    # Drainage improvements
    if soil_data['drainage'] == 'Poor':
        improvements['long_term_strategies'].append({
            'strategy': 'Install drainage systems',
            'description': 'Subsurface drainage or raised beds',
            'cost_per_hectare': 50000,
            'timeline': '1-2 seasons',
            'benefits': 'Prevent waterlogging, improve root development'
        })
    
    # Erosion control
    if soil_data['erosion_risk'] in ['High', 'Very High']:
        improvements['immediate_actions'].append({
            'action': 'Implement erosion control measures',
            'methods': ['Contour farming', 'Terracing', 'Cover crops'],
            'cost_per_hectare': 25000,
            'timeline': 'Immediate implementation needed'
        })
    
    return improvements

def analyze_regional_soil_trends(region_name: str) -> Dict:
    """
    Analyze soil degradation and improvement trends for a region
    """
    
    # Simulate soil trend data
    years = list(range(2019, 2025))
    
    # Generate realistic trend data based on region characteristics
    soil_data = get_detailed_soil_data().get(region_name, {})
    
    trends = {
        'organic_matter_trend': [],
        'ph_stability': [],
        'erosion_progression': [],
        'salinity_changes': []
    }
    
    base_om = soil_data.get('organic_matter', 0.5)
    base_ph = sum(soil_data.get('ph_range', [6.5, 7.5])) / 2
    
    for i, year in enumerate(years):
        # Organic matter trend (generally declining without intervention)
        om_change = -0.02 * i + np.random.normal(0, 0.01)
        trends['organic_matter_trend'].append({
            'year': year,
            'value': max(0.1, base_om + om_change)
        })
        
        # pH stability
        ph_change = np.random.normal(0, 0.1)
        trends['ph_stability'].append({
            'year': year,
            'value': base_ph + ph_change
        })
        
        # Erosion progression (getting worse without control)
        erosion_score = max(1, min(10, 7 - i * 0.3 + np.random.normal(0, 0.5)))
        trends['erosion_progression'].append({
            'year': year,
            'value': erosion_score
        })
        
        # Salinity changes
        salinity_levels = {'Low': 2, 'Medium': 5, 'High': 8}
        base_salinity = salinity_levels.get(soil_data.get('salinity_level', 'Low'), 2)
        salinity_change = np.random.normal(0, 0.2)
        trends['salinity_changes'].append({
            'year': year,
            'value': max(1, min(10, base_salinity + salinity_change))
        })
    
    return {
        'region': region_name,
        'trends': trends,
        'analysis': {
            'organic_matter_status': 'Declining' if base_om < 0.5 else 'Stable',
            'major_concerns': get_soil_concerns(soil_data),
            'improvement_priority': get_improvement_priorities(soil_data)
        }
    }

def get_soil_concerns(soil_data: Dict) -> List[str]:
    """Identify major soil concerns for a region"""
    concerns = []
    
    if soil_data.get('organic_matter', 0) < 0.5:
        concerns.append('Low organic matter content')
    
    if soil_data.get('erosion_risk') in ['High', 'Very High']:
        concerns.append('High erosion risk')
    
    if soil_data.get('salinity_level') == 'High':
        concerns.append('Soil salinity problems')
    
    if soil_data.get('drainage') == 'Poor':
        concerns.append('Poor drainage and waterlogging')
    
    return concerns

def get_improvement_priorities(soil_data: Dict) -> List[str]:
    """Get prioritized list of soil improvements"""
    priorities = []
    
    if soil_data.get('organic_matter', 0) < 0.5:
        priorities.append('Increase organic matter through composting')
    
    if soil_data.get('erosion_risk') in ['High', 'Very High']:
        priorities.append('Implement erosion control measures')
    
    if soil_data.get('drainage') == 'Poor':
        priorities.append('Improve field drainage systems')
    
    nutrient_levels = {'Low': 3, 'Very Low': 1}
    low_nutrients = []
    for nutrient in ['nitrogen', 'phosphorus', 'potassium']:
        if soil_data.get(nutrient) in nutrient_levels:
            low_nutrients.append(nutrient.upper())
    
    if low_nutrients:
        priorities.append(f'Address {", ".join(low_nutrients)} deficiency')
    
    return priorities