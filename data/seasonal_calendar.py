import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def get_crop_calendar_data():
    """
    Returns detailed crop calendar data with planting and harvesting schedules
    """
    
    calendar_data = {
        'Rice (Basmati)': {
            'seasons': {
                'Kharif': {
                    'planting_months': [6, 7],  # June-July
                    'harvesting_months': [10, 11],  # October-November
                    'duration_days': 120,
                    'regions': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar']
                }
            },
            'growth_stages': {
                'Seedbed preparation': {'duration_days': 15, 'activities': ['Land preparation', 'Seed selection']},
                'Transplanting': {'duration_days': 30, 'activities': ['Nursery raising', 'Field transplanting']},
                'Vegetative growth': {'duration_days': 45, 'activities': ['Fertilizer application', 'Weed control']},
                'Reproductive stage': {'duration_days': 30, 'activities': ['Flowering', 'Grain filling']},
                'Maturity': {'duration_days': 10, 'activities': ['Harvesting preparation']}
            },
            'water_critical_stages': ['Transplanting', 'Flowering', 'Grain filling'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At transplanting', 'npk_ratio': '4:2:1'},
                'First top dressing': {'timing': '20-25 days after transplanting', 'npk_ratio': '2:0:0'},
                'Second top dressing': {'timing': '40-45 days after transplanting', 'npk_ratio': '2:0:1'}
            }
        },
        
        'Wheat': {
            'seasons': {
                'Rabi': {
                    'planting_months': [11, 12],  # November-December
                    'harvesting_months': [4, 5],  # April-May
                    'duration_days': 120,
                    'regions': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan']
                }
            },
            'growth_stages': {
                'Sowing': {'duration_days': 10, 'activities': ['Field preparation', 'Seed sowing']},
                'Germination': {'duration_days': 15, 'activities': ['Irrigation', 'Bird protection']},
                'Tillering': {'duration_days': 30, 'activities': ['First irrigation', 'Weed control']},
                'Jointing': {'duration_days': 25, 'activities': ['Second irrigation', 'Top dressing']},
                'Flowering': {'duration_days': 15, 'activities': ['Third irrigation', 'Disease control']},
                'Grain filling': {'duration_days': 20, 'activities': ['Final irrigation', 'Monitoring']},
                'Maturity': {'duration_days': 5, 'activities': ['Harvesting']}
            },
            'water_critical_stages': ['Crown root initiation', 'Tillering', 'Flowering', 'Grain filling'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At sowing', 'npk_ratio': '3:3:2'},
                'First top dressing': {'timing': '20-25 days after sowing', 'npk_ratio': '1:0:0'},
                'Second top dressing': {'timing': 'At flowering', 'npk_ratio': '1:0:0'}
            }
        },
        
        'Maize': {
            'seasons': {
                'Kharif': {
                    'planting_months': [6, 7],
                    'harvesting_months': [9, 10],
                    'duration_days': 90,
                    'regions': ['Punjab', 'Uttar Pradesh', 'Bihar', 'Madhya Pradesh']
                },
                'Rabi': {
                    'planting_months': [11, 12],
                    'harvesting_months': [3, 4],
                    'duration_days': 100,
                    'regions': ['Karnataka', 'Tamil Nadu', 'Andhra Pradesh']
                }
            },
            'growth_stages': {
                'Sowing': {'duration_days': 7, 'activities': ['Field preparation', 'Seed treatment']},
                'Germination': {'duration_days': 10, 'activities': ['Gap filling', 'Early weed control']},
                'Vegetative': {'duration_days': 35, 'activities': ['Thinning', 'Fertilizer application']},
                'Tasseling': {'duration_days': 15, 'activities': ['Irrigation', 'Pest monitoring']},
                'Grain filling': {'duration_days': 20, 'activities': ['Adequate moisture', 'Disease control']},
                'Maturity': {'duration_days': 3, 'activities': ['Harvesting']}
            },
            'water_critical_stages': ['Tasseling', 'Silking', 'Grain filling'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At sowing', 'npk_ratio': '2:2:1'},
                'Side dressing': {'timing': '30 days after sowing', 'npk_ratio': '2:0:1'}
            }
        },
        
        'Chana (Chickpea)': {
            'seasons': {
                'Rabi': {
                    'planting_months': [10, 11],
                    'harvesting_months': [3, 4],
                    'duration_days': 110,
                    'regions': ['Madhya Pradesh', 'Rajasthan', 'Maharashtra', 'Uttar Pradesh']
                }
            },
            'growth_stages': {
                'Sowing': {'duration_days': 8, 'activities': ['Seed treatment', 'Inoculation']},
                'Germination': {'duration_days': 12, 'activities': ['Thinning', 'Weed control']},
                'Branching': {'duration_days': 30, 'activities': ['Light irrigation', 'Fertilizer']},
                'Flowering': {'duration_days': 35, 'activities': ['Avoid excess water', 'Pest control']},
                'Pod development': {'duration_days': 20, 'activities': ['Critical irrigation', 'Disease monitoring']},
                'Maturity': {'duration_days': 5, 'activities': ['Harvesting']}
            },
            'water_critical_stages': ['Flowering', 'Pod development'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At sowing', 'npk_ratio': '1:4:2'},
                'Rhizobium inoculation': {'timing': 'Before sowing', 'npk_ratio': 'Bio-fertilizer'}
            }
        },
        
        'Soybean': {
            'seasons': {
                'Kharif': {
                    'planting_months': [6, 7],
                    'harvesting_months': [9, 10],
                    'duration_days': 100,
                    'regions': ['Madhya Pradesh', 'Maharashtra', 'Rajasthan']
                }
            },
            'growth_stages': {
                'Sowing': {'duration_days': 6, 'activities': ['Seed treatment', 'Rhizobium inoculation']},
                'Germination': {'duration_days': 10, 'activities': ['Gap filling', 'Weed management']},
                'Vegetative': {'duration_days': 40, 'activities': ['Growth monitoring', 'Pest control']},
                'Flowering': {'duration_days': 25, 'activities': ['Adequate moisture', 'Nutrient management']},
                'Pod filling': {'duration_days': 15, 'activities': ['Critical irrigation', 'Disease control']},
                'Maturity': {'duration_days': 4, 'activities': ['Timely harvesting']}
            },
            'water_critical_stages': ['Flowering', 'Pod filling'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At sowing', 'npk_ratio': '1:2:1'},
                'Rhizobium': {'timing': 'Seed treatment', 'npk_ratio': 'Bio-fertilizer'}
            }
        },
        
        'Cotton': {
            'seasons': {
                'Kharif': {
                    'planting_months': [5, 6],
                    'harvesting_months': [10, 11, 12],
                    'duration_days': 180,
                    'regions': ['Gujarat', 'Maharashtra', 'Punjab', 'Andhra Pradesh']
                }
            },
            'growth_stages': {
                'Sowing': {'duration_days': 8, 'activities': ['Field preparation', 'Seed treatment']},
                'Germination': {'duration_days': 12, 'activities': ['Gap filling', 'Early protection']},
                'Squaring': {'duration_days': 45, 'activities': ['Fertilizer application', 'Pest monitoring']},
                'Flowering': {'duration_days': 50, 'activities': ['Regular irrigation', 'Bollworm control']},
                'Boll development': {'duration_days': 45, 'activities': ['Adequate moisture', 'Nutrient management']},
                'Maturity': {'duration_days': 20, 'activities': ['Multiple picking']}
            },
            'water_critical_stages': ['Squaring', 'Flowering', 'Boll development'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At sowing', 'npk_ratio': '2:2:1'},
                'First top dressing': {'timing': '30 days after sowing', 'npk_ratio': '2:0:1'},
                'Second top dressing': {'timing': 'At flowering', 'npk_ratio': '1:0:1'}
            }
        },
        
        'Tomato': {
            'seasons': {
                'Kharif': {
                    'planting_months': [6, 7],
                    'harvesting_months': [9, 10, 11],
                    'duration_days': 120,
                    'regions': ['Karnataka', 'Maharashtra', 'Andhra Pradesh']
                },
                'Rabi': {
                    'planting_months': [11, 12],
                    'harvesting_months': [3, 4, 5],
                    'duration_days': 120,
                    'regions': ['All regions']
                }
            },
            'growth_stages': {
                'Nursery': {'duration_days': 25, 'activities': ['Seed sowing', 'Seedling care']},
                'Transplanting': {'duration_days': 10, 'activities': ['Field preparation', 'Transplanting']},
                'Vegetative': {'duration_days': 35, 'activities': ['Staking', 'Pruning', 'Fertilizer']},
                'Flowering': {'duration_days': 20, 'activities': ['Regular irrigation', 'Pollination']},
                'Fruiting': {'duration_days': 30, 'activities': ['Harvesting starts', 'Disease control']}
            },
            'water_critical_stages': ['Transplanting', 'Flowering', 'Fruit development'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At transplanting', 'npk_ratio': '3:3:2'},
                'Weekly fertigation': {'timing': 'Throughout season', 'npk_ratio': '19:19:19'}
            }
        },
        
        'Potato': {
            'seasons': {
                'Rabi': {
                    'planting_months': [10, 11, 12],
                    'harvesting_months': [2, 3, 4],
                    'duration_days': 90,
                    'regions': ['Uttar Pradesh', 'Punjab', 'West Bengal', 'Bihar']
                }
            },
            'growth_stages': {
                'Planting': {'duration_days': 5, 'activities': ['Seed preparation', 'Planting']},
                'Germination': {'duration_days': 15, 'activities': ['Irrigation', 'Weed control']},
                'Vegetative': {'duration_days': 30, 'activities': ['Earthing up', 'Fertilizer application']},
                'Tuber initiation': {'duration_days': 20, 'activities': ['Critical irrigation', 'Disease control']},
                'Tuber bulking': {'duration_days': 15, 'activities': ['Adequate moisture', 'Pest monitoring']},
                'Maturity': {'duration_days': 5, 'activities': ['Harvesting']}
            },
            'water_critical_stages': ['Tuber initiation', 'Tuber bulking'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At planting', 'npk_ratio': '4:2:1'},
                'Top dressing': {'timing': '30 days after planting', 'npk_ratio': '2:0:1'}
            }
        },
        
        'Onion': {
            'seasons': {
                'Kharif': {
                    'planting_months': [6, 7],
                    'harvesting_months': [10, 11],
                    'duration_days': 120,
                    'regions': ['Maharashtra', 'Karnataka', 'Gujarat']
                },
                'Rabi': {
                    'planting_months': [11, 12],
                    'harvesting_months': [4, 5],
                    'duration_days': 120,
                    'regions': ['Maharashtra', 'Gujarat', 'Madhya Pradesh']
                }
            },
            'growth_stages': {
                'Nursery': {'duration_days': 45, 'activities': ['Seed sowing', 'Seedling care']},
                'Transplanting': {'duration_days': 10, 'activities': ['Field preparation', 'Transplanting']},
                'Vegetative': {'duration_days': 35, 'activities': ['Weeding', 'Fertilizer application']},
                'Bulb formation': {'duration_days': 25, 'activities': ['Critical irrigation', 'Nutrient management']},
                'Maturity': {'duration_days': 5, 'activities': ['Curing', 'Harvesting']}
            },
            'water_critical_stages': ['Transplanting', 'Bulb formation'],
            'fertilizer_schedule': {
                'Basal': {'timing': 'At transplanting', 'npk_ratio': '3:2:2'},
                'Split application': {'timing': '30 and 60 days', 'npk_ratio': '2:1:1'}
            }
        }
    }
    
    return calendar_data

def get_regional_calendar(region_name: str, year: Optional[int] = None) -> Dict:
    """
    Get crop calendar specific to a region for a given year
    """
    if year is None:
        year = datetime.now().year
    
    calendar_data = get_crop_calendar_data()
    regional_calendar = {}
    
    # Regional climate adjustments
    climate_adjustments = {
        'Punjab': {'planting_delay': 0, 'harvest_delay': 0},
        'Maharashtra': {'planting_delay': 7, 'harvest_delay': 7},  # Later planting due to delayed monsoon
        'Tamil Nadu': {'planting_delay': 14, 'harvest_delay': 14},  # Different monsoon pattern
        'Karnataka': {'planting_delay': 7, 'harvest_delay': 7},
        'Gujarat': {'planting_delay': -7, 'harvest_delay': -7},  # Earlier season
        'Rajasthan': {'planting_delay': -14, 'harvest_delay': -14},  # Hot climate, earlier seasons
        'West Bengal': {'planting_delay': 14, 'harvest_delay': 14},  # Different monsoon timing
        'Andhra Pradesh': {'planting_delay': 7, 'harvest_delay': 7},
        'Uttar Pradesh': {'planting_delay': 0, 'harvest_delay': 0},
        'Madhya Pradesh': {'planting_delay': 7, 'harvest_delay': 7}
    }
    
    adjustment = climate_adjustments.get(region_name, {'planting_delay': 0, 'harvest_delay': 0})
    
    for crop_name, crop_data in calendar_data.items():
        if crop_data['seasons']:
            regional_calendar[crop_name] = {'seasons': {}}
            
            for season, season_data in crop_data['seasons'].items():
                if region_name in season_data['regions']:
                    # Adjust planting and harvesting months based on regional climate
                    adjusted_planting = [(month + adjustment['planting_delay'] // 30) % 12 or 12 
                                       for month in season_data['planting_months']]
                    adjusted_harvesting = [(month + adjustment['harvest_delay'] // 30) % 12 or 12 
                                         for month in season_data['harvesting_months']]
                    
                    regional_calendar[crop_name]['seasons'][season] = {
                        'planting_months': adjusted_planting,
                        'harvesting_months': adjusted_harvesting,
                        'duration_days': season_data['duration_days'],
                        'optimal_planting_window': get_optimal_planting_dates(
                            adjusted_planting, year
                        ),
                        'expected_harvest_window': get_optimal_harvest_dates(
                            adjusted_harvesting, year
                        )
                    }
                    
                    # Add detailed schedule
                    regional_calendar[crop_name]['detailed_schedule'] = generate_detailed_schedule(
                        crop_name, season, adjusted_planting[0], year
                    )
    
    return regional_calendar

def get_optimal_planting_dates(months: List[int], year: int) -> List[Dict]:
    """
    Get optimal planting date ranges for given months
    """
    optimal_dates = []
    
    for month in months:
        # First half and second half of the month
        start_date = datetime(year, month, 1)
        mid_date = datetime(year, month, 15)
        
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        optimal_dates.append({
            'month': start_date.strftime('%B'),
            'early_window': {'start': start_date, 'end': mid_date},
            'late_window': {'start': mid_date, 'end': end_date},
            'preferred': 'early' if month in [6, 11] else 'late'  # Monsoon and winter crops
        })
    
    return optimal_dates

def get_optimal_harvest_dates(months: List[int], year: int) -> List[Dict]:
    """
    Get optimal harvest date ranges for given months
    """
    harvest_dates = []
    
    for month in months:
        # Adjust year if harvest is in next year
        harvest_year = year if month >= 4 else year + 1
        
        start_date = datetime(harvest_year, month, 1)
        
        if month == 12:
            end_date = datetime(harvest_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(harvest_year, month + 1, 1) - timedelta(days=1)
        
        harvest_dates.append({
            'month': start_date.strftime('%B'),
            'window': {'start': start_date, 'end': end_date},
            'peak_period': get_peak_harvest_period(start_date, end_date)
        })
    
    return harvest_dates

def get_peak_harvest_period(start_date: datetime, end_date: datetime) -> Dict:
    """
    Determine peak harvest period within the harvest window
    """
    total_days = (end_date - start_date).days
    peak_start = start_date + timedelta(days=total_days // 3)
    peak_end = start_date + timedelta(days=2 * total_days // 3)
    
    return {
        'start': peak_start,
        'end': peak_end,
        'description': f"Peak harvest from {peak_start.strftime('%d %b')} to {peak_end.strftime('%d %b')}"
    }

def generate_detailed_schedule(crop_name: str, season: str, planting_month: int, year: int) -> List[Dict]:
    """
    Generate detailed week-by-week schedule for a crop
    """
    calendar_data = get_crop_calendar_data()
    crop_data = calendar_data.get(crop_name, {})
    
    if not crop_data:
        return []
    
    # Calculate planting date (assume 15th of planting month)
    # Ensure planting_month is valid
    if planting_month < 1 or planting_month > 12:
        planting_month = 6  # Default to June
    
    planting_date = datetime(year, planting_month, 15)
    
    schedule = []
    current_date = planting_date
    
    # Get growth stages
    growth_stages = crop_data.get('growth_stages', {})
    
    for stage_name, stage_data in growth_stages.items():
        stage_duration = stage_data['duration_days']
        activities = stage_data['activities']
        
        schedule.append({
            'stage': stage_name,
            'start_date': current_date,
            'end_date': current_date + timedelta(days=stage_duration),
            'duration_days': stage_duration,
            'activities': activities,
            'week_number': ((current_date - planting_date).days // 7) + 1,
            'critical_activities': get_critical_activities(crop_name, stage_name)
        })
        
        current_date += timedelta(days=stage_duration)
    
    return schedule

def get_critical_activities(crop_name: str, stage_name: str) -> List[str]:
    """
    Get critical activities for specific crop and growth stage
    """
    calendar_data = get_crop_calendar_data()
    crop_data = calendar_data.get(crop_name, {})
    
    critical_stages = crop_data.get('water_critical_stages', [])
    fertilizer_schedule = crop_data.get('fertilizer_schedule', {})
    
    critical_activities = []
    
    if stage_name.lower() in [stage.lower() for stage in critical_stages]:
        critical_activities.append('Critical irrigation period - ensure adequate moisture')
    
    # Check fertilizer schedule
    for fert_stage, fert_data in fertilizer_schedule.items():
        if stage_name.lower() in fert_data.get('timing', '').lower():
            critical_activities.append(f'Apply {fert_stage} fertilizer - NPK ratio {fert_data.get("npk_ratio", "")}')
    
    return critical_activities

def get_seasonal_conflicts(region_name: str, year: Optional[int] = None) -> Dict:
    """
    Identify potential scheduling conflicts and resource competition
    """
    if year is None:
        year = datetime.now().year
    
    regional_calendar = get_regional_calendar(region_name, year)
    conflicts = {
        'labor_intensive_periods': [],
        'irrigation_conflicts': [],
        'equipment_conflicts': [],
        'recommendations': []
    }
    
    # Analyze overlapping labor-intensive periods
    labor_periods = []
    
    for crop_name, crop_data in regional_calendar.items():
        for season_name, season_data in crop_data.get('seasons', {}).items():
            schedule = crop_data.get('detailed_schedule', [])
            
            for stage in schedule:
                if 'transplanting' in stage['stage'].lower() or 'harvesting' in stage['stage'].lower():
                    labor_periods.append({
                        'crop': crop_name,
                        'activity': stage['stage'],
                        'start': stage['start_date'],
                        'end': stage['end_date']
                    })
    
    # Find overlapping periods
    for i, period1 in enumerate(labor_periods):
        for period2 in labor_periods[i+1:]:
            if (period1['start'] <= period2['end'] and period1['end'] >= period2['start']):
                conflicts['labor_intensive_periods'].append({
                    'period': f"{period1['start'].strftime('%B')} - {period1['end'].strftime('%B')}",
                    'crops': [period1['crop'], period2['crop']],
                    'activities': [period1['activity'], period2['activity']],
                    'severity': 'High' if abs((period1['start'] - period2['start']).days) < 15 else 'Medium'
                })
    
    # Generate recommendations
    if conflicts['labor_intensive_periods']:
        conflicts['recommendations'].extend([
            'Consider staggered planting to spread labor requirements',
            'Plan for additional labor during peak periods',
            'Mechanization can help reduce labor conflicts'
        ])
    
    return conflicts

def get_market_timing_analysis(region_name: str, crop_list: List[str]) -> Dict:
    """
    Analyze market timing for harvest periods
    """
    regional_calendar = get_regional_calendar(region_name)
    
    market_analysis = {
        'harvest_timing': {},
        'price_patterns': {},
        'marketing_strategy': {}
    }
    
    for crop_name in crop_list:
        if crop_name in regional_calendar:
            crop_seasons = regional_calendar[crop_name].get('seasons', {})
            
            for season, season_data in crop_seasons.items():
                harvest_months = season_data.get('harvesting_months', [])
                
                # Simulate market price patterns (in real implementation, this would connect to market APIs)
                price_pattern = simulate_seasonal_price_pattern(crop_name, harvest_months)
                
                market_analysis['harvest_timing'][crop_name] = {
                    'harvest_months': [datetime(2024, month, 1).strftime('%B') for month in harvest_months],
                    'market_competition': get_market_competition_level(crop_name, harvest_months),
                    'optimal_selling_window': get_optimal_selling_window(crop_name, harvest_months)
                }
                
                market_analysis['price_patterns'][crop_name] = price_pattern
    
    return market_analysis

def simulate_seasonal_price_pattern(crop_name: str, harvest_months: List[int]) -> Dict:
    """
    Simulate seasonal price patterns for crops
    """
    base_prices = {
        'Rice (Basmati)': 4500,
        'Wheat': 2200,
        'Maize': 1800,
        'Chana (Chickpea)': 5500,
        'Soybean': 4200,
        'Cotton': 6000,
        'Tomato': 2500,
        'Potato': 1200,
        'Onion': 1800
    }
    
    base_price = base_prices.get(crop_name, 3000)
    
    # Simulate price variations throughout the year
    monthly_multipliers = {
        1: 1.2, 2: 1.15, 3: 1.1, 4: 0.9, 5: 0.85, 6: 0.9,
        7: 0.95, 8: 1.0, 9: 1.05, 10: 0.8, 11: 0.85, 12: 1.1
    }
    
    # Adjust for harvest months (prices typically drop during harvest)
    for month in harvest_months:
        monthly_multipliers[month] *= 0.8
    
    price_pattern = {
        'base_price': base_price,
        'monthly_prices': {month: base_price * multiplier 
                          for month, multiplier in monthly_multipliers.items()},
        'peak_price_months': sorted(monthly_multipliers.keys(), 
                                  key=lambda x: monthly_multipliers[x], reverse=True)[:3],
        'low_price_months': harvest_months
    }
    
    return price_pattern

def get_market_competition_level(crop_name: str, harvest_months: List[int]) -> str:
    """
    Determine market competition level during harvest
    """
    # High competition crops that are widely grown
    high_competition_crops = ['Rice (Basmati)', 'Wheat', 'Maize', 'Potato']
    
    # Check if harvest coincides with major harvest seasons
    major_harvest_months = [10, 11, 3, 4]  # Post-monsoon and post-winter harvests
    
    competition_score = 0
    
    if crop_name in high_competition_crops:
        competition_score += 2
    
    overlapping_months = set(harvest_months) & set(major_harvest_months)
    competition_score += len(overlapping_months)
    
    if competition_score >= 4:
        return 'Very High'
    elif competition_score >= 3:
        return 'High'
    elif competition_score >= 2:
        return 'Medium'
    else:
        return 'Low'

def get_optimal_selling_window(crop_name: str, harvest_months: List[int]) -> Dict:
    """
    Determine optimal selling strategy and timing
    """
    strategies = {
        'immediate_sale': {
            'timing': 'Within 2 weeks of harvest',
            'advantage': 'Quick cash flow, no storage costs',
            'disadvantage': 'Lower prices due to market glut'
        },
        'strategic_hold': {
            'timing': '2-4 months post harvest',
            'advantage': 'Better prices, reduced competition',
            'disadvantage': 'Storage costs, quality risks'
        },
        'festival_timing': {
            'timing': 'Before major festivals',
            'advantage': 'Premium prices during festivals',
            'disadvantage': 'Higher storage and quality risks'
        }
    }
    
    # Determine best strategy based on crop characteristics
    perishable_crops = ['Tomato', 'Potato', 'Onion']
    
    if crop_name in perishable_crops:
        recommended_strategy = 'immediate_sale'
    else:
        recommended_strategy = 'strategic_hold'
    
    return {
        'recommended_strategy': recommended_strategy,
        'strategy_details': strategies[recommended_strategy],
        'all_options': strategies
    }