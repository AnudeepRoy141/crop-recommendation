import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.weather_data import get_detailed_weather_analysis

def show_weather_analysis_page():
    st.title("Detailed Weather Analysis")
    
    if not st.session_state.get('selected_region'):
        st.warning("Please select a region from the main page first.")
        return
    
    region = st.session_state.selected_region
    st.subheader(f"Weather Analysis for {region}")
    
    # Get detailed weather data
    weather_analysis = get_detailed_weather_analysis(region)
    
    # Climate indicators
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Climate Risk Score", f"{weather_analysis['risk_score']:.1f}/10")
    with col2:
        st.metric("Drought Probability", f"{weather_analysis['drought_risk']:.0f}%")
    with col3:
        st.metric("Flood Risk", f"{weather_analysis['flood_risk']:.0f}%")
    with col4:
        st.metric("Growing Season", f"{weather_analysis['growing_season_days']} days")
    
    # Historical trends
    st.subheader("30-Year Historical Trends")
    
    trends_df = pd.DataFrame(weather_analysis['historical_trends'])
    
    fig_trends = px.line(trends_df, x='year', y=['temperature', 'rainfall'],
                        title="Temperature and Rainfall Trends (1994-2024)")
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Seasonal analysis
    st.subheader("Seasonal Weather Patterns")
    
    seasonal_df = pd.DataFrame(weather_analysis['seasonal_data'])
    
    col1, col2 = st.columns(2)
    with col1:
        fig_seasonal_temp = px.bar(seasonal_df, x='season', y='avg_temp',
                                  title="Average Temperature by Season")
        st.plotly_chart(fig_seasonal_temp, use_container_width=True)
    
    with col2:
        fig_seasonal_rain = px.bar(seasonal_df, x='season', y='rainfall',
                                  title="Rainfall by Season")
        st.plotly_chart(fig_seasonal_rain, use_container_width=True)

if __name__ == "__main__":
    show_weather_analysis_page()
