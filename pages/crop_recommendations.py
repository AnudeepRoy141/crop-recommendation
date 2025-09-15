import streamlit as st
import pandas as pd
import plotly.express as px
from utils.recommendation_engine import CropRecommendationEngine

def show_crop_recommendations_page():
    st.title("Advanced Crop Recommendations")
    
    if not st.session_state.get('selected_region'):
        st.warning("Please select a region from the main page first.")
        return
    
    # Advanced filtering options
    st.subheader("Filter Recommendations")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        crop_type = st.selectbox("Crop Type", ["All", "Cereals", "Pulses", "Oilseeds", "Fruits", "Vegetables"])
    with col2:
        min_roi = st.slider("Minimum ROI (%)", 0, 100, 20)
    with col3:
        max_investment = st.number_input("Max Investment per acre (₹)", min_value=1000, value=50000, step=5000)
    
    # Get filtered recommendations
    engine = CropRecommendationEngine()
    recommendations = engine.get_filtered_recommendations(
        st.session_state.selected_region,
        crop_type=crop_type,
        min_roi=min_roi,
        max_investment=max_investment
    )
    
    if recommendations:
        st.subheader(f"Filtered Recommendations ({len(recommendations)} crops)")
        
        # Create comparison table
        rec_df = pd.DataFrame([
            {
                'Crop': crop['name'],
                'Type': crop['type'],
                'Suitability': crop['suitability_score'],
                'ROI (%)': crop['roi'],
                'Investment (₹/acre)': crop['production_cost'],
                'Profit (₹/acre)': crop['expected_yield'] * crop['market_price'] - crop['production_cost']
            }
            for crop in recommendations
        ])
        
        st.dataframe(rec_df, use_container_width=True)
        
        # Visualization
        fig_scatter = px.scatter(rec_df, x='Suitability', y='ROI (%)', 
                                size='Investment (₹/acre)', color='Type',
                                hover_name='Crop',
                                title="Crop Suitability vs ROI Analysis")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No crops match your criteria. Please adjust the filters.")

if __name__ == "__main__":
    show_crop_recommendations_page()
