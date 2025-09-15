import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import calendar
from data.seasonal_calendar import get_regional_calendar, get_seasonal_conflicts, get_market_timing_analysis


def show_seasonal_planning_page():
    st.title("📅 Seasonal Planning Calendar")
    
    if not st.session_state.get('selected_region'):
        st.warning("Please select a region from the main page first.")
        return
    
    region = st.session_state.selected_region
    current_year = datetime.now().year
    
    st.subheader(f"Crop Calendar for {region} - {current_year}")
    
    # Year selection
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_year = st.selectbox("Select Year:", [current_year, current_year + 1], index=0)
    
    # Get regional calendar data
    regional_calendar = get_regional_calendar(region, selected_year)
    
    if not regional_calendar:
        st.warning(f"No crop calendar data available for {region}")
        return
    
    # Calendar Overview Section
    st.subheader("📊 Annual Crop Calendar Overview")
    
    # Create calendar visualization
    create_annual_calendar_view(regional_calendar, selected_year)
    
    # Crop Selection for Detailed Planning
    st.subheader("🌾 Detailed Crop Planning")
    
    available_crops = list(regional_calendar.keys())
    selected_crops = st.multiselect(
        "Select crops for detailed planning:",
        available_crops,
        default=available_crops[:3] if len(available_crops) >= 3 else available_crops
    )
    
    if selected_crops:
        # Detailed schedules for selected crops
        for crop_name in selected_crops:
            with st.expander(f"📋 {crop_name} - Detailed Schedule", expanded=True):
                show_detailed_crop_schedule(crop_name, regional_calendar[crop_name], selected_year)
    
    # Seasonal Conflicts Analysis
    st.subheader("⚠️ Potential Scheduling Conflicts")
    
    conflicts = get_seasonal_conflicts(region, selected_year)
    
    if conflicts['labor_intensive_periods']:
        st.warning("**Labor Intensive Period Conflicts Detected:**")
        
        for conflict in conflicts['labor_intensive_periods']:
            severity_color = "🔴" if conflict['severity'] == 'High' else "🟡"
            st.write(f"{severity_color} **{conflict['period']}**: {', '.join(conflict['crops'])} - {', '.join(conflict['activities'])}")
    
    if conflicts['recommendations']:
        st.info("**Recommendations to resolve conflicts:**")
        for rec in conflicts['recommendations']:
            st.write(f"• {rec}")
    
    # Market Timing Analysis
    if selected_crops:
        st.subheader("💰 Market Timing Analysis")
        
        market_analysis = get_market_timing_analysis(region, selected_crops)
        
        # Create market timing visualization
        create_market_timing_chart(market_analysis, selected_crops)
        
        # Market insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Harvest Timing & Competition:**")
            for crop in selected_crops:
                if crop in market_analysis['harvest_timing']:
                    timing_data = market_analysis['harvest_timing'][crop]
                    competition = timing_data['market_competition']
                    
                    # Color code competition level
                    competition_color = {
                        'Very High': '🔴',
                        'High': '🟠', 
                        'Medium': '🟡',
                        'Low': '🟢'
                    }.get(competition, '⚪')
                    
                    harvest_months_str = ', '.join([str(m) for m in timing_data.get('harvest_months', [])]) if timing_data.get('harvest_months') else 'TBD'
                    st.write(f"{competition_color} **{crop}**: {harvest_months_str} - {competition} competition")
        
        with col2:
            st.write("**Optimal Selling Strategy:**")
            for crop in selected_crops:
                if crop in market_analysis['harvest_timing']:
                    timing_data = market_analysis['harvest_timing'][crop]
                    selling_strategy = timing_data.get('optimal_selling_window', {})
                    
                    if selling_strategy:
                        strategy = selling_strategy.get('recommended_strategy', 'immediate_sale')
                        st.write(f"📈 **{crop}**: {strategy.replace('_', ' ').title()}")
    
    # Farm Planning Tools
    st.subheader("🚜 Farm Planning Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Land Allocation Planner:**")
        total_land = st.number_input("Total farm area (acres):", min_value=0.1, value=10.0, step=0.5)
        
        if selected_crops:
            allocation_data = []
            remaining_land = total_land
            
            for crop in selected_crops:
                max_allocation = min(remaining_land, total_land * 0.8)
                allocation = st.slider(
                    f"{crop} allocation (acres):",
                    0.0, max_allocation,
                    min(2.0, max_allocation),
                    0.1,
                    key=f"allocation_{crop}"
                )
                
                allocation_data.append({
                    'Crop': crop,
                    'Allocated Land (acres)': allocation,
                    'Percentage': (allocation / total_land) * 100 if total_land > 0 else 0
                })
                remaining_land -= allocation
            
            if remaining_land < 0:
                st.error("⚠️ Total allocation exceeds available land!")
            else:
                st.success(f"✅ Remaining land: {remaining_land:.1f} acres")
                
                # Land allocation chart
                if allocation_data:
                    alloc_df = pd.DataFrame(allocation_data)
                    fig_allocation = px.pie(
                        alloc_df, 
                        values='Allocated Land (acres)', 
                        names='Crop',
                        title="Land Allocation Distribution"
                    )
                    st.plotly_chart(fig_allocation, use_container_width=True)
    
    with col2:
        st.write("**Resource Planning:**")
        
        if selected_crops and total_land > 0 and 'allocation_data' in locals():
            resource_requirements = calculate_resource_requirements(selected_crops, allocation_data)
            
            st.metric("Peak Labor Requirement", f"{resource_requirements['peak_labor']} person-days")
            st.metric("Total Water Requirement", f"{resource_requirements['total_water']} acre-feet")
            st.metric("Seed Cost", f"₹{resource_requirements['seed_cost']:,.0f}")
            st.metric("Fertilizer Cost", f"₹{resource_requirements['fertilizer_cost']:,.0f}")
    
    # Weather-based Recommendations
    st.subheader("🌤️ Weather-Based Planting Recommendations")
    
    current_month = datetime.now().month
    next_month = (current_month % 12) + 1
    
    current_recommendations = get_seasonal_recommendations(regional_calendar, current_month)
    next_recommendations = get_seasonal_recommendations(regional_calendar, next_month)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**This Month ({calendar.month_name[current_month]}):**")
        if current_recommendations['planting']:
            st.success("🌱 **Plant Now:**")
            for crop in current_recommendations['planting']:
                st.write(f"• {crop}")
        
        if current_recommendations['harvesting']:
            st.success("🌾 **Harvest Now:**")
            for crop in current_recommendations['harvesting']:
                st.write(f"• {crop}")
        
        if not current_recommendations['planting'] and not current_recommendations['harvesting']:
            st.info("No major planting or harvesting activities this month")
    
    with col2:
        st.write(f"**Next Month ({calendar.month_name[next_month]}):**")
        if next_recommendations['planting']:
            st.info("🌱 **Prepare for Planting:**")
            for crop in next_recommendations['planting']:
                st.write(f"• {crop}")
        
        if next_recommendations['harvesting']:
            st.info("🌾 **Prepare for Harvest:**")
            for crop in next_recommendations['harvesting']:
                st.write(f"• {crop}")
        
        if not next_recommendations['planting'] and not next_recommendations['harvesting']:
            st.info("No major activities planned for next month")
    
    # Export Calendar
    st.subheader("📥 Export Calendar")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download Calendar PDF"):
            st.info("PDF export functionality coming soon!")
    
    with col2:
        if st.button("Export to CSV"):
            calendar_csv = create_calendar_csv(regional_calendar, selected_year)
            st.download_button(
                label="Download CSV",
                data=calendar_csv,
                file_name=f"{region}_crop_calendar_{selected_year}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Share Calendar"):
            st.info("Sharing functionality coming soon!")

def create_annual_calendar_view(regional_calendar: dict, year: int):
    """Create an annual calendar visualization"""
    
    # Prepare data for visualization
    calendar_data = []
    
    for crop_name, crop_data in regional_calendar.items():
        for season_name, season_data in crop_data.get('seasons', {}).items():
            planting_months = season_data.get('planting_months', [])
            harvesting_months = season_data.get('harvesting_months', [])
            
            # Add planting periods
            for month in planting_months:
                calendar_data.append({
                    'Crop': crop_name,
                    'Month': month,
                    'Activity': 'Planting',
                    'Season': season_name
                })
            
            # Add harvesting periods
            for month in harvesting_months:
                # Adjust for year transition
                harvest_year = year if month >= 4 else year + 1
                calendar_data.append({
                    'Crop': crop_name,
                    'Month': month,
                    'Activity': 'Harvesting',
                    'Season': season_name
                })
    
    if calendar_data:
        df = pd.DataFrame(calendar_data)
        df['Month_Name'] = df['Month'].apply(lambda x: calendar.month_name[x])
        
        # Create bar chart instead of timeline for better visualization
        fig = px.bar(
            df, 
            x='Month_Name',
            y='Crop',
            color='Activity',
            title="Annual Crop Calendar",
            orientation='h',
            color_discrete_map={'Planting': '#90EE90', 'Harvesting': '#FFD700'}
        )
        
        fig.update_layout(
            xaxis_title="Month of Year",
            yaxis_title="Crop",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No calendar data available for visualization")

def show_detailed_crop_schedule(crop_name: str, crop_data: dict, year: int):
    """Show detailed schedule for a specific crop"""
    
    seasons = crop_data.get('seasons', {})
    
    for season_name, season_data in seasons.items():
        st.write(f"**{season_name} Season:**")
        
        # Basic timing info
        planting_months = season_data.get('planting_months', [])
        harvesting_months = season_data.get('harvesting_months', [])
        duration = season_data.get('duration_days', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Planting", ", ".join([calendar.month_abbr[m] for m in planting_months]))
        with col2:
            st.metric("Harvesting", ", ".join([calendar.month_abbr[m] for m in harvesting_months]))
        with col3:
            st.metric("Duration", f"{duration} days")
        
        # Detailed schedule if available
        detailed_schedule = crop_data.get('detailed_schedule', [])
        
        if detailed_schedule:
            st.write("**Growth Stages Schedule:**")
            
            schedule_data = []
            for stage in detailed_schedule:
                schedule_data.append({
                    'Stage': stage['stage'],
                    'Start Date': stage['start_date'].strftime('%d %b'),
                    'End Date': stage['end_date'].strftime('%d %b'),
                    'Duration (days)': stage['duration_days'],
                    'Key Activities': ', '.join(stage['activities'][:2])  # Show first 2 activities
                })
            
            schedule_df = pd.DataFrame(schedule_data)
            st.dataframe(schedule_df, use_container_width=True)
            
            # Growth stage timeline
            fig = go.Figure()
            
            for i, stage in enumerate(detailed_schedule):
                fig.add_trace(go.Scatter(
                    x=[stage['start_date'], stage['end_date']],
                    y=[stage['stage'], stage['stage']],
                    mode='lines+markers',
                    name=stage['stage'],
                    line=dict(width=10),
                    showlegend=False
                ))
            
            fig.update_layout(
                title=f"{crop_name} Growth Stages Timeline",
                xaxis_title="Date",
                yaxis_title="Growth Stage",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_market_timing_chart(market_analysis: dict, selected_crops: list):
    """Create market timing and price pattern visualization"""
    
    price_data = []
    
    for crop in selected_crops:
        if crop in market_analysis.get('price_patterns', {}):
            price_pattern = market_analysis['price_patterns'][crop]
            monthly_prices = price_pattern.get('monthly_prices', {})
            
            for month, price in monthly_prices.items():
                price_data.append({
                    'Crop': crop,
                    'Month': calendar.month_name[month],
                    'Month_Num': month,
                    'Price (₹/quintal)': price
                })
    
    if price_data:
        price_df = pd.DataFrame(price_data)
        
        fig = px.line(
            price_df,
            x='Month_Num',
            y='Price (₹/quintal)',
            color='Crop',
            title="Seasonal Price Patterns",
            labels={'Month_Num': 'Month'}
        )
        
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=[calendar.month_abbr[i] for i in range(1, 13)]
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

def calculate_resource_requirements(selected_crops: list, allocation_data: list) -> dict:
    """Calculate resource requirements for selected crops"""
    
    # Base resource requirements per acre
    base_requirements = {
        'Rice (Basmati)': {'labor': 45, 'water': 4.5, 'seed_cost': 3000, 'fertilizer_cost': 8000},
        'Wheat': {'labor': 30, 'water': 2.5, 'seed_cost': 2000, 'fertilizer_cost': 6000},
        'Maize': {'labor': 25, 'water': 2.0, 'seed_cost': 1500, 'fertilizer_cost': 5000},
        'Chana (Chickpea)': {'labor': 20, 'water': 1.5, 'seed_cost': 2500, 'fertilizer_cost': 4000},
        'Soybean': {'labor': 22, 'water': 1.8, 'seed_cost': 2000, 'fertilizer_cost': 5500},
        'Cotton': {'labor': 60, 'water': 3.5, 'seed_cost': 4000, 'fertilizer_cost': 12000},
        'Tomato': {'labor': 80, 'water': 3.0, 'seed_cost': 8000, 'fertilizer_cost': 15000},
        'Potato': {'labor': 50, 'water': 2.2, 'seed_cost': 15000, 'fertilizer_cost': 8000},
        'Onion': {'labor': 70, 'water': 2.8, 'seed_cost': 5000, 'fertilizer_cost': 10000}
    }
    
    total_requirements = {
        'peak_labor': 0,
        'total_water': 0,
        'seed_cost': 0,
        'fertilizer_cost': 0
    }
    
    for allocation in allocation_data:
        crop_name = allocation['Crop']
        allocated_land = allocation['Allocated Land (acres)']
        
        if crop_name in base_requirements:
            requirements = base_requirements[crop_name]
            
            total_requirements['peak_labor'] += requirements['labor'] * allocated_land
            total_requirements['total_water'] += requirements['water'] * allocated_land
            total_requirements['seed_cost'] += requirements['seed_cost'] * allocated_land
            total_requirements['fertilizer_cost'] += requirements['fertilizer_cost'] * allocated_land
    
    return total_requirements

def get_seasonal_recommendations(regional_calendar: dict, month: int) -> dict:
    """Get planting and harvesting recommendations for a specific month"""
    
    recommendations = {
        'planting': [],
        'harvesting': []
    }
    
    for crop_name, crop_data in regional_calendar.items():
        for season_name, season_data in crop_data.get('seasons', {}).items():
            planting_months = season_data.get('planting_months', [])
            harvesting_months = season_data.get('harvesting_months', [])
            
            if month in planting_months:
                recommendations['planting'].append(crop_name)
            
            if month in harvesting_months:
                recommendations['harvesting'].append(crop_name)
    
    return recommendations

def create_calendar_csv(regional_calendar: dict, year: int) -> str:
    """Create CSV data for calendar export"""
    
    csv_data = []
    
    for crop_name, crop_data in regional_calendar.items():
        for season_name, season_data in crop_data.get('seasons', {}).items():
            planting_months = season_data.get('planting_months', [])
            harvesting_months = season_data.get('harvesting_months', [])
            duration = season_data.get('duration_days', 0)
            
            csv_data.append({
                'Crop': crop_name,
                'Season': season_name,
                'Planting_Months': ', '.join([calendar.month_name[m] for m in planting_months]),
                'Harvesting_Months': ', '.join([calendar.month_name[m] for m in harvesting_months]),
                'Duration_Days': duration,
                'Year': year
            })
    
    df = pd.DataFrame(csv_data)
    return df.to_csv(index=False)

if __name__ == "__main__":
    show_seasonal_planning_page()