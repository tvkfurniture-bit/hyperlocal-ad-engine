import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hyperlocal Ad Engine", layout="wide")
st.title("🎯 Hyperlocal Ad Manager")

try:
    df = pd.read_csv("final_ads.csv")
    st.subheader("Targeted Leads & Ad Copy")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📲 Ad Preview")
    
    # Fixed the column name here (changed from business_name to name)
    selected_biz = st.selectbox("Select Business to View Ad", df['name'])
    
    # Extract the ad text
    ad_text = df[df['name'] == selected_biz]['generated_ad'].values[0]
    
    # Display it like a Facebook Ad
    st.success(f"**Sponsored** • {selected_biz}\n\n{ad_text}")
    st.button("Launch Campaign (Meta Ads API)")

except Exception as e:
    st.warning(f"Waiting for data... Run the GitHub Action first. (Error: {e})")
