import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from data.regions_data import get_indian_states_data, get_district_coordinates
from data.weather_data import get_weather_data_for_region
from data.crop_database import get_crop_database
from utils.recommendation_engine import CropRecommendationEngine
from pages.soil_analysis import show_soil_analysis_page
from pages.seasonal_planning import show_seasonal_planning_page
import numpy as np

# Configure page
st.set_page_config(
    page_title="AgriWeather Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = None
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

def main():
    st.title("🌾 AgriWeather Crop Advisor")
    st.markdown("*Data-driven crop recommendations based on weather patterns and market analysis for India*")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Select Page",
            ["Home & Region Selection", "Weather Analysis", "Soil Analysis", "Crop Recommendations", "Seasonal Planning", "Profit Dashboard"]
        )
        
        if st.session_state.selected_region:
            st.success(f"Selected: {st.session_state.selected_region}")
    
    if page == "Home & Region Selection":
        show_home_page()
    elif page == "Weather Analysis":
        show_weather_analysis()
    elif page == "Soil Analysis":
        show_soil_analysis_page()
    elif page == "Crop Recommendations":
        show_crop_recommendations()
    elif page == "Seasonal Planning":
        show_seasonal_planning_page()
    elif page == "Profit Dashboard":
        show_profit_dashboard()

def show_home_page():
    st.header("Select Your Region")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Interactive Map of India")
        
        # Create map centered on India
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        # Add markers for major agricultural regions
        regions_data = get_indian_states_data()
        
        for region in regions_data:
            folium.Marker(
                [region['lat'], region['lon']],
                popup=f"{region['name']}<br>Click to select",
                tooltip=region['name'],
                icon=folium.Icon(color='green', icon='leaf')
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=500)
        
        # Handle map clicks
        if map_data['last_object_clicked_popup']:
            clicked_region = map_data['last_object_clicked_popup'].split('<br>')[0]
            st.session_state.selected_region = clicked_region
            st.success(f"Selected region: {clicked_region}")
            st.rerun()
    
    with col2:
        st.subheader("Region Details")
        
        if st.session_state.selected_region:
            region_info = next((r for r in regions_data if r['name'] == st.session_state.selected_region), None)
            if region_info:
                st.write(f"**State/Region:** {region_info['name']}")
                st.write(f"**Climate Zone:** {region_info['climate_zone']}")
                st.write(f"**Soil Type:** {region_info['soil_type']}")
                st.write(f"**Annual Rainfall:** {region_info['annual_rainfall']} mm")
                st.write(f"**Temperature Range:** {region_info['temp_range']}°C")
                
                # Load weather data for selected region
                if st.button("Load Weather Data & Analyze"):
                    with st.spinner("Loading weather data..."):
                        weather_data = get_weather_data_for_region(st.session_state.selected_region)
                        st.session_state.weather_data = weather_data
                        
                        # Generate recommendations
                        engine = CropRecommendationEngine()
                        recommendations = engine.get_recommendations(
                            region_info, weather_data
                        )
                        st.session_state.recommendations = recommendations
                        
                    st.success("Data loaded successfully! Navigate to other pages to explore.")
        else:
            st.info("Click on a marker on the map to select a region")
            
        # Manual region selection
        st.subheader("Or Select Manually")
        manual_region = st.selectbox(
            "Choose a region:",
            [""] + [region['name'] for region in regions_data]
        )
        
        if manual_region and manual_region != st.session_state.selected_region:
            st.session_state.selected_region = manual_region
            st.rerun()

def show_weather_analysis():
    st.header("Weather Pattern Analysis")
    
    if not st.session_state.selected_region:
        st.warning("Please select a region from the Home page first.")
        return
    
    if not st.session_state.weather_data:
        st.warning("Please load weather data from the Home page first.")
        return
    
    weather_data = st.session_state.weather_data
    
    # Weather overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Temperature", f"{weather_data['avg_temp']:.1f}°C")
    with col2:
        st.metric("Annual Rainfall", f"{weather_data['annual_rainfall']:.0f} mm")
    with col3:
        st.metric("Avg Humidity", f"{weather_data['avg_humidity']:.0f}%")
    with col4:
        st.metric("Rainy Days", f"{weather_data['rainy_days']:.0f}")
    
    # Temperature trends
    st.subheader("Temperature Trends")
    temp_df = pd.DataFrame(weather_data['monthly_temp'])
    fig_temp = px.line(temp_df, x='month', y=['min_temp', 'max_temp', 'avg_temp'],
                       title="Monthly Temperature Patterns",
                       labels={'value': 'Temperature (°C)', 'variable': 'Temperature Type'})
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Rainfall patterns
    st.subheader("Rainfall Patterns")
    rainfall_df = pd.DataFrame(weather_data['monthly_rainfall'])
    fig_rain = px.bar(rainfall_df, x='month', y='rainfall',
                      title="Monthly Rainfall Distribution",
                      labels={'rainfall': 'Rainfall (mm)'})
    st.plotly_chart(fig_rain, use_container_width=True)
    
    # Humidity trends
    st.subheader("Humidity Patterns")
    humidity_df = pd.DataFrame(weather_data['monthly_humidity'])
    fig_humidity = px.line(humidity_df, x='month', y='humidity',
                          title="Monthly Humidity Levels",
                          labels={'humidity': 'Humidity (%)'})
    st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Climate suitability analysis
    st.subheader("Climate Suitability Analysis")
    
    # Create radar chart for climate factors
    categories = ['Temperature', 'Rainfall', 'Humidity', 'Seasonal Variation']
    
    # Calculate suitability scores (0-10 scale)
    temp_score = min(10, max(0, 10 - abs(weather_data['avg_temp'] - 25) / 2))
    rain_score = min(10, weather_data['annual_rainfall'] / 150)
    humidity_score = min(10, weather_data['avg_humidity'] / 10)
    seasonal_score = 8  # Based on seasonal variation data
    
    values = [temp_score, rain_score, humidity_score, seasonal_score]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Climate Suitability'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        title="Climate Suitability Scores (0-10 scale)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

def show_crop_recommendations():
    st.header("Crop Recommendations")
    
    if not st.session_state.selected_region:
        st.warning("Please select a region from the Home page first.")
        return
    
    if not st.session_state.recommendations:
        st.warning("Please load recommendations from the Home page first.")
        return
    
    recommendations = st.session_state.recommendations
    
    st.subheader(f"Top Recommended Crops for {st.session_state.selected_region}")
    
    # Display top recommendations
    for i, crop in enumerate(recommendations[:5], 1):
        with st.expander(f"{i}. {crop['name']} (Suitability Score: {crop['suitability_score']:.1f}/10)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Growing Requirements:**")
                st.write(f"• Temperature: {crop['temp_min']}-{crop['temp_max']}°C")
                st.write(f"• Rainfall: {crop['rainfall_min']}-{crop['rainfall_max']} mm")
                st.write(f"• Soil pH: {crop['soil_ph_min']}-{crop['soil_ph_max']}")
                st.write(f"• Growing Season: {crop['growing_season']}")
                st.write(f"• Water Requirements: {crop['water_requirement']}")
            
            with col2:
                st.write("**Economic Factors:**")
                st.write(f"• Market Price: ₹{crop['market_price']:,}/quintal")
                st.write(f"• Production Cost: ₹{crop['production_cost']:,}/acre")
                st.write(f"• Expected Yield: {crop['expected_yield']} quintal/acre")
                st.write(f"• Profit Margin: {crop['profit_margin']:.1f}%")
                st.write(f"• ROI: {crop['roi']:.1f}%")
    
    # Comparison chart
    st.subheader("Crop Comparison Analysis")
    
    comparison_df = pd.DataFrame([
        {
            'Crop': crop['name'],
            'Suitability Score': crop['suitability_score'],
            'Expected Profit (₹/acre)': crop['expected_yield'] * crop['market_price'] - crop['production_cost'],
            'ROI (%)': crop['roi']
        }
        for crop in recommendations[:10]
    ])
    
    fig_comparison = px.scatter(comparison_df, 
                               x='Suitability Score', 
                               y='Expected Profit (₹/acre)',
                               size='ROI (%)',
                               hover_name='Crop',
                               title="Crop Suitability vs Profitability Analysis")
    st.plotly_chart(fig_comparison, use_container_width=True)

def show_profit_dashboard():
    st.header("Profit Analysis Dashboard")
    
    if not st.session_state.selected_region:
        st.warning("Please select a region from the Home page first.")
        return
    
    if not st.session_state.recommendations:
        st.warning("Please load recommendations from the Home page first.")
        return
    
    recommendations = st.session_state.recommendations
    
    # Farm size input
    st.subheader("Calculate Potential Returns")
    farm_size = st.number_input("Enter your farm size (acres):", min_value=0.1, value=5.0, step=0.5)
    
    # Top 5 crops profit analysis
    st.subheader("Profit Analysis for Top 5 Recommended Crops")
    
    profit_data = []
    for crop in recommendations[:5]:
        total_cost = crop['production_cost'] * farm_size
        total_revenue = crop['expected_yield'] * crop['market_price'] * farm_size
        total_profit = total_revenue - total_cost
        
        profit_data.append({
            'Crop': crop['name'],
            'Total Investment (₹)': total_cost,
            'Expected Revenue (₹)': total_revenue,
            'Net Profit (₹)': total_profit,
            'ROI (%)': crop['roi']
        })
    
    profit_df = pd.DataFrame(profit_data)
    
    # Display profit metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        best_profit_crop = profit_df.loc[profit_df['Net Profit (₹)'].idxmax()]
        st.metric("Highest Profit Crop", best_profit_crop['Crop'], 
                 f"₹{best_profit_crop['Net Profit (₹)']:,.0f}")
    
    with col2:
        best_roi_crop = profit_df.loc[profit_df['ROI (%)'].idxmax()]
        st.metric("Best ROI Crop", best_roi_crop['Crop'], 
                 f"{best_roi_crop['ROI (%)']:.1f}%")
    
    with col3:
        avg_profit = profit_df['Net Profit (₹)'].mean()
        st.metric("Average Profit", f"₹{avg_profit:,.0f}", 
                 f"For {farm_size} acres")
    
    # Profit comparison chart
    fig_profit = px.bar(profit_df, x='Crop', y='Net Profit (₹)',
                       title=f"Expected Net Profit Comparison ({farm_size} acres)",
                       labels={'Net Profit (₹)': 'Net Profit (₹)'})
    st.plotly_chart(fig_profit, use_container_width=True)
    
    # ROI comparison
    fig_roi = px.bar(profit_df, x='Crop', y='ROI (%)',
                    title="Return on Investment Comparison",
                    labels={'ROI (%)': 'ROI (%)'})
    st.plotly_chart(fig_roi, use_container_width=True)
    
    # Investment breakdown
    st.subheader("Investment Breakdown")
    
    selected_crop = st.selectbox("Select a crop for detailed analysis:", 
                                [crop['name'] for crop in recommendations[:5]])
    
    crop_details = next(crop for crop in recommendations if crop['name'] == selected_crop)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cost Breakdown (per acre):**")
        costs = {
            'Seeds': crop_details['production_cost'] * 0.15,
            'Fertilizers': crop_details['production_cost'] * 0.25,
            'Pesticides': crop_details['production_cost'] * 0.15,
            'Labor': crop_details['production_cost'] * 0.30,
            'Equipment': crop_details['production_cost'] * 0.15
        }
        
        for item, cost in costs.items():
            st.write(f"• {item}: ₹{cost:,.0f}")
        
        # Pie chart for cost breakdown
        fig_costs = px.pie(values=list(costs.values()), names=list(costs.keys()),
                          title="Cost Distribution")
        st.plotly_chart(fig_costs, use_container_width=True)
    
    with col2:
        st.write("**Revenue Projections:**")
        revenue_per_acre = crop_details['expected_yield'] * crop_details['market_price']
        total_revenue = revenue_per_acre * farm_size
        total_cost = crop_details['production_cost'] * farm_size
        net_profit = total_revenue - total_cost
        
        st.write(f"• Yield per acre: {crop_details['expected_yield']} quintals")
        st.write(f"• Market price: ₹{crop_details['market_price']:,}/quintal")
        st.write(f"• Revenue per acre: ₹{revenue_per_acre:,.0f}")
        st.write(f"• Total revenue ({farm_size} acres): ₹{total_revenue:,.0f}")
        st.write(f"• Total cost: ₹{total_cost:,.0f}")
        st.write(f"• **Net profit: ₹{net_profit:,.0f}**")
        
        # Monthly cash flow projection
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        cash_flow = [-total_cost/4, -total_cost/4, -total_cost/4, -total_cost/4,
                    0, 0, 0, 0, total_revenue/2, total_revenue/2, 0, 0]
        
        cash_flow_df = pd.DataFrame({'Month': months, 'Cash Flow': cash_flow})
        fig_cash = px.bar(cash_flow_df, x='Month', y='Cash Flow',
                         title="Projected Monthly Cash Flow",
                         labels={'Cash Flow': 'Cash Flow (₹)'})
        st.plotly_chart(fig_cash, use_container_width=True)

if __name__ == "__main__":
    main()
