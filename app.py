import streamlit as st
import pandas as pd

st.title("🎯 Hyperlocal Ad Manager")

try:
    df = pd.read_csv("final_ads.csv")
    st.subheader("Targeted Leads & Ad Copy")
    st.dataframe(df)
    
    selected_biz = st.selectbox("Select Business to View Ad", df['business_name'])
    ad_text = df[df['business_name'] == selected_biz]['generated_ad'].values[0]
    st.info(ad_text)
except:
    st.warning("No data found. Run the automation first!")
