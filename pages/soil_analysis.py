import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.soil_analysis import (
    get_detailed_soil_data, 
    analyze_soil_crop_compatibility,
    get_soil_improvement_plan,
    analyze_regional_soil_trends
)
from data.crop_database import get_crop_database

def show_soil_analysis_page():
    st.title("🌱 Soil Analysis & Management")
    
    if not st.session_state.get('selected_region'):
        st.warning("Please select a region from the main page first.")
        return
    
    region = st.session_state.selected_region
    st.subheader(f"Comprehensive Soil Analysis for {region}")
    
    # Get soil data
    soil_data = get_detailed_soil_data()
    region_soil = soil_data.get(region)
    
    if not region_soil:
        st.error(f"Soil data not available for {region}")
        return
    
    # Soil Overview Section
    st.subheader("Soil Characteristics Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Primary Soil Type", region_soil['primary_soil'])
    with col2:
        ph_avg = sum(region_soil['ph_range']) / 2
        st.metric("Average pH", f"{ph_avg:.1f}")
    with col3:
        st.metric("Organic Matter", f"{region_soil['organic_matter']:.1f}%")
    with col4:
        st.metric("Drainage", region_soil['drainage'])
    
    # Detailed Soil Properties
    st.subheader("Detailed Soil Properties")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Soil composition chart
        nutrients = {
            'Nitrogen': region_soil['nitrogen'],
            'Phosphorus': region_soil['phosphorus'],
            'Potassium': region_soil['potassium']
        }
        
        # Convert nutrient levels to numerical values for visualization
        nutrient_values = {
            'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5
        }
        
        nutrient_scores = [nutrient_values.get(level, 3) for level in nutrients.values()]
        
        fig_nutrients = go.Figure()
        fig_nutrients.add_trace(go.Scatterpolar(
            r=nutrient_scores,
            theta=list(nutrients.keys()),
            fill='toself',
            name='Nutrient Levels'
        ))
        fig_nutrients.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            title="Soil Nutrient Profile"
        )
        st.plotly_chart(fig_nutrients, use_container_width=True)
    
    with col2:
        # Soil properties table
        properties_data = {
            'Property': ['pH Range', 'Organic Matter', 'Drainage', 'Water Holding Capacity', 
                        'Erosion Risk', 'Salinity Level', 'Soil Depth', 'Texture Class',
                        'CEC (meq/100g)', 'Bulk Density (g/cm³)'],
            'Value': [f"{region_soil['ph_range'][0]} - {region_soil['ph_range'][1]}",
                     f"{region_soil['organic_matter']}%",
                     region_soil['drainage'],
                     region_soil['water_holding_capacity'],
                     region_soil['erosion_risk'],
                     region_soil['salinity_level'],
                     region_soil['soil_depth'],
                     region_soil['texture_class'],
                     f"{region_soil['cec']:.1f}",
                     f"{region_soil['bulk_density']:.2f}"]
        }
        
        properties_df = pd.DataFrame(properties_data)
        st.dataframe(properties_df, use_container_width=True)
    
    # Soil-Crop Compatibility Analysis
    st.subheader("Soil-Crop Compatibility Analysis")
    
    if st.session_state.get('recommendations'):
        # Analyze top recommended crops for soil compatibility
        top_crops = st.session_state.recommendations[:5]
        
        compatibility_data = []
        for crop in top_crops:
            if crop.get('soil_analysis'):
                soil_analysis = crop['soil_analysis']
                compatibility_data.append({
                    'Crop': crop['name'],
                    'Overall Soil Score': soil_analysis['overall_score'],
                    'pH Compatibility': soil_analysis['component_scores']['ph_compatibility'],
                    'Water Compatibility': soil_analysis['component_scores']['water_compatibility'],
                    'Nutrient Adequacy': soil_analysis['component_scores']['nutrient_adequacy'],
                    'Erosion Risk Score': soil_analysis['component_scores']['erosion_risk'],
                    'Suitability Grade': soil_analysis['suitability_grade']
                })
        
        if compatibility_data:
            compatibility_df = pd.DataFrame(compatibility_data)
            st.dataframe(compatibility_df, use_container_width=True)
            
            # Visualization of soil compatibility scores
            fig_compat = px.bar(compatibility_df, x='Crop', y='Overall Soil Score',
                              color='Suitability Grade',
                              title="Soil Compatibility Scores for Top Recommended Crops",
                              color_discrete_map={
                                  'Excellent': '#2E8B57',
                                  'Good': '#32CD32', 
                                  'Fair': '#FFD700',
                                  'Poor': '#FF6347',
                                  'Unsuitable': '#DC143C'
                              })
            st.plotly_chart(fig_compat, use_container_width=True)
    
    # Soil Improvement Recommendations
    st.subheader("Soil Improvement Plan")
    
    # Get crops from recommendations if available
    target_crops = []
    if st.session_state.get('recommendations'):
        target_crops = [crop['name'] for crop in st.session_state.recommendations[:3]]
    
    improvement_plan = get_soil_improvement_plan(region_soil, target_crops)
    
    # Display improvement actions
    if improvement_plan['immediate_actions']:
        st.write("**Immediate Actions Required:**")
        for action in improvement_plan['immediate_actions']:
            with st.expander(f"🚨 {action.get('action', 'Action Required')}"):
                if 'quantity' in action:
                    st.write(f"**Quantity:** {action['quantity']}")
                if 'cost_per_hectare' in action:
                    st.write(f"**Cost per hectare:** ₹{action['cost_per_hectare']:,}")
                if 'timeline' in action:
                    st.write(f"**Timeline:** {action['timeline']}")
                if 'methods' in action:
                    st.write(f"**Methods:** {', '.join(action['methods'])}")
    
    if improvement_plan['short_term_goals']:
        st.write("**Short-term Goals (1-2 years):**")
        for goal in improvement_plan['short_term_goals']:
            with st.expander(f"📋 {goal.get('goal', 'Short-term Goal')}"):
                if 'methods' in goal:
                    st.write(f"**Methods:** {', '.join(goal['methods'])}")
                if 'target' in goal:
                    st.write(f"**Target:** {goal['target']}")
                if 'timeline' in goal:
                    st.write(f"**Timeline:** {goal['timeline']}")
                if 'cost_per_hectare' in goal:
                    st.write(f"**Investment:** ₹{goal['cost_per_hectare']:,} per hectare")
    
    if improvement_plan['long_term_strategies']:
        st.write("**Long-term Strategies (2+ years):**")
        for strategy in improvement_plan['long_term_strategies']:
            with st.expander(f"🎯 {strategy.get('strategy', 'Long-term Strategy')}"):
                if 'description' in strategy:
                    st.write(f"**Description:** {strategy['description']}")
                if 'benefits' in strategy:
                    st.write(f"**Benefits:** {strategy['benefits']}")
                if 'cost_per_hectare' in strategy:
                    st.write(f"**Investment:** ₹{strategy['cost_per_hectare']:,} per hectare")
                if 'timeline' in strategy:
                    st.write(f"**Timeline:** {strategy['timeline']}")
    
    # Regional Soil Trends
    st.subheader("Regional Soil Health Trends")
    
    soil_trends = analyze_regional_soil_trends(region)
    
    # Organic matter trend
    if soil_trends['trends']['organic_matter_trend']:
        om_df = pd.DataFrame(soil_trends['trends']['organic_matter_trend'])
        fig_om = px.line(om_df, x='year', y='value',
                        title="Organic Matter Content Trend",
                        labels={'value': 'Organic Matter (%)', 'year': 'Year'})
        st.plotly_chart(fig_om, use_container_width=True)
    
    # Soil concerns and priorities
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Major Soil Concerns:**")
        concerns = soil_trends['analysis']['major_concerns']
        if concerns:
            for concern in concerns:
                st.write(f"⚠️ {concern}")
        else:
            st.write("✅ No major soil concerns identified")
    
    with col2:
        st.write("**Improvement Priorities:**")
        priorities = soil_trends['analysis']['improvement_priority']
        if priorities:
            for i, priority in enumerate(priorities, 1):
                st.write(f"{i}. {priority}")
        else:
            st.write("✅ Soil conditions are generally satisfactory")
    
    # Soil Testing Recommendations
    st.subheader("Soil Testing Recommendations")
    
    st.info("""
    **Recommended Soil Tests:**
    
    1. **Basic Soil Test** (Annual): pH, NPK, Organic Matter - ₹500-800 per sample
    2. **Comprehensive Test** (Every 3 years): Micronutrients, CEC, Salinity - ₹1,500-2,500 per sample
    3. **Specialized Tests** (As needed): Heavy metals, biological activity - ₹2,000-5,000 per sample
    
    **Sampling Guidelines:**
    - Collect 15-20 sub-samples from different areas
    - Sample depth: 0-15cm for most crops
    - Best time: Before monsoon or after harvest
    - Avoid recently fertilized areas
    """)
    
    # Cost-Benefit Analysis
    st.subheader("Investment vs. Returns Analysis")
    
    # Calculate potential returns from soil improvement
    if improvement_plan['immediate_actions']:
        total_immediate_cost = sum(action.get('cost_per_hectare', 0) 
                                 for action in improvement_plan['immediate_actions'])
        
        farm_size = st.number_input("Enter your farm size (hectares):", 
                                  min_value=0.1, value=2.0, step=0.1)
        
        total_investment = total_immediate_cost * farm_size
        
        # Estimate yield improvement (conservative 15-25%)
        yield_improvement = st.slider("Expected yield improvement from soil management (%)", 
                                    10, 40, 20)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Investment", f"₹{total_investment:,.0f}")
        with col2:
            st.metric("Expected Yield Increase", f"{yield_improvement}%")
        with col3:
            # Estimate additional revenue (assuming ₹50,000 average revenue per hectare)
            additional_revenue = (farm_size * 50000 * yield_improvement / 100)
            st.metric("Additional Annual Revenue", f"₹{additional_revenue:,.0f}")
        
        if total_investment > 0:
            payback_period = total_investment / additional_revenue if additional_revenue > 0 else float('inf')
            if payback_period < 10:
                st.success(f"💰 Estimated payback period: {payback_period:.1f} years")
            else:
                st.warning("⏰ Long payback period - consider prioritizing most critical improvements")

if __name__ == "__main__":
    show_soil_analysis_page()