import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_profit_dashboard_page():
    st.title("Advanced Profit Dashboard")
    
    if not st.session_state.get('recommendations'):
        st.warning("Please load crop recommendations from the main page first.")
        return
    
    # Portfolio optimization
    st.subheader("Portfolio Optimization")
    
    farm_size = st.number_input("Total Farm Size (acres):", min_value=1.0, value=10.0, step=0.5)
    
    # Allow user to select multiple crops
    available_crops = [crop['name'] for crop in st.session_state.recommendations[:10]]
    selected_crops = st.multiselect("Select crops for your portfolio:", available_crops)
    
    if selected_crops:
        portfolio_allocations = {}
        remaining_land = farm_size
        
        st.write("**Allocate land to each crop:**")
        for crop in selected_crops:
            max_allocation = min(remaining_land, farm_size * 0.8)  # Max 80% to one crop
            allocation = st.slider(f"{crop} (acres):", 0.0, max_allocation, 
                                 min(2.0, max_allocation), 0.1, key=f"alloc_{crop}")
            portfolio_allocations[crop] = allocation
            remaining_land -= allocation
        
        if remaining_land < 0:
            st.error("Total allocation exceeds farm size!")
        else:
            st.success(f"Remaining land: {remaining_land:.1f} acres")
            
            # Calculate portfolio performance
            total_investment = 0
            total_revenue = 0
            portfolio_data = []
            
            for crop_name, allocation in portfolio_allocations.items():
                if allocation > 0:
                    crop_details = next(crop for crop in st.session_state.recommendations 
                                      if crop['name'] == crop_name)
                    
                    investment = crop_details['production_cost'] * allocation
                    revenue = crop_details['expected_yield'] * crop_details['market_price'] * allocation
                    profit = revenue - investment
                    
                    total_investment += investment
                    total_revenue += revenue
                    
                    portfolio_data.append({
                        'Crop': crop_name,
                        'Allocation (acres)': allocation,
                        'Investment (₹)': investment,
                        'Revenue (₹)': revenue,
                        'Profit (₹)': profit,
                        'ROI (%)': (profit / investment) * 100 if investment > 0 else 0
                    })
            
            if portfolio_data:
                # Portfolio summary
                total_profit = total_revenue - total_investment
                portfolio_roi = (total_profit / total_investment) * 100 if total_investment > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Investment", f"₹{total_investment:,.0f}")
                with col2:
                    st.metric("Expected Revenue", f"₹{total_revenue:,.0f}")
                with col3:
                    st.metric("Net Profit", f"₹{total_profit:,.0f}")
                with col4:
                    st.metric("Portfolio ROI", f"{portfolio_roi:.1f}%")
                
                # Portfolio breakdown
                portfolio_df = pd.DataFrame(portfolio_data)
                st.dataframe(portfolio_df, use_container_width=True)
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_allocation = px.pie(portfolio_df, values='Allocation (acres)', names='Crop',
                                          title="Land Allocation")
                    st.plotly_chart(fig_allocation, use_container_width=True)
                
                with col2:
                    fig_profit = px.bar(portfolio_df, x='Crop', y='Profit (₹)',
                                       title="Profit by Crop")
                    st.plotly_chart(fig_profit, use_container_width=True)
                
                # Risk analysis
                st.subheader("Risk Analysis")
                
                # Calculate portfolio risk metrics
                crop_risks = []
                for crop_name in selected_crops:
                    if portfolio_allocations[crop_name] > 0:
                        crop_details = next(crop for crop in st.session_state.recommendations 
                                          if crop['name'] == crop_name)
                        
                        # Simple risk calculation based on weather sensitivity
                        weather_risk = 10 - crop_details['suitability_score']  # Higher suitability = lower risk
                        market_risk = min(10, crop_details['market_price'] / 1000)  # Price volatility proxy
                        
                        crop_risks.append({
                            'Crop': crop_name,
                            'Weather Risk': weather_risk,
                            'Market Risk': market_risk,
                            'Overall Risk': (weather_risk + market_risk) / 2
                        })
                
                if crop_risks:
                    risk_df = pd.DataFrame(crop_risks)
                    
                    fig_risk = px.scatter(risk_df, x='Weather Risk', y='Market Risk', 
                                         size='Overall Risk', hover_name='Crop',
                                         title="Risk Assessment by Crop")
                    st.plotly_chart(fig_risk, use_container_width=True)

if __name__ == "__main__":
    show_profit_dashboard_page()
