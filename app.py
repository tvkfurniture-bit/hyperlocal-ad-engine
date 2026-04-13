import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="Hyperlocal Precision Targeter", layout="wide")

# Connect to Groq API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

st.title("🎯 Hyperlocal Precision Targeter & Video Engine")
st.markdown("Target an exact business using their Address and Google Maps Link to generate highly accurate assets.")

# --- LIVE EXACT TARGETING ENGINE ---
with st.expander("📍 TARGET EXACT BUSINESS LOCATION (Start Here)", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Exact Business Name (e.g., Luigi's Pizza)")
        biz_niche = st.text_input("Business Type (e.g., Pizzeria, Gym, Dentist)")
    with colB:
        biz_address = st.text_input("Exact Street Address, City, State")
        gmaps_link = st.text_input("Google Maps Share Link (https://goo.gl/maps/...)")
    
    generate_btn = st.button("⚡ Generate Precision Assets", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    with st.spinner("🌍 AI is mapping the exact address and building assets..."):
        
        # 1. Generate Direct Response Ad with Exact Maps Integration
        ad_prompt = f"""
        Write a Facebook ad for {biz_name} ({biz_niche}) located exactly at {biz_address}.
        
        RULES:
        1. Start by calling out the specific street or immediate neighborhood based on the address.
        2. Create a ruthless, direct-response 'Mafia Offer' (e.g., 'Free item with purchase').
        3. Make it urgent (Valid for the first 20 people today).
        4. The Call to Action MUST be: "Tap the link below to get directions instantly and claim your offer: {gmaps_link}"
        
        Keep it under 60 words. No fluffy words. Pure direct response.
        """
        
        ad_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a master direct response copywriter who uses exact geographical data to drive foot traffic."}, 
                {"role": "user", "content": ad_prompt}
            ]
        )
        generated_ad = ad_response.choices[0].message.content

        # 2. Generate Highly Specific AI Video Prompt
        vid_prompt = f"""
        Write a highly detailed text-to-video AI prompt to generate a promotional video for {biz_name}. 
        The business is located at {biz_address}. 
        
        Format it for a tool like Google Vids, Runway Gen-3, or Luma Dream Machine. 
        
        Include: 
        - Camera movement (e.g., FPV drone flying down the street, or a cinematic push-in).
        - Visual subjects relevant to a {biz_niche}.
        - Instructions to match the street-level aesthetic of {biz_address}.
        - Exactly what the text overlay should say on the screen (including the offer).
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an elite AI Video Director."}, 
                {"role": "user", "content": vid_prompt}
            ]
        )
        generated_video_prompt = vid_response.choices[0].message.content

        # Save to session state
        st.session_state['ad_copy'] = generated_ad
        st.session_state['vid_prompt'] = generated_video_prompt
        st.session_state['biz_name'] = biz_name

# --- DISPLAY ASSETS ---
if 'ad_copy' in st.session_state:
    st.markdown("---")
    st.header(f"📦 Precision Assets Delivered for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The 'Drive-to-Store' Ad")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")
        
        st.subheader("2️⃣ The AI Video Generator Prompt")
        st.info("🎥 **Copy & Paste this into Google Vids, Runway Gen-3, or Luma:**")
        st.code(st.session_state['vid_prompt'], language="text")
        st.caption("Generate this video, attach the ad text, and DM it to the business owner.")

    with col2:
        st.subheader("3️⃣ The ROI Simulator (Your Sales Pitch)")
        st.markdown("**Show them the exact math for their location.**")
        
        ad_spend = st.slider("Monthly Ad Spend ($)", 100, 1000, 300)
        cost_per_lead = st.number_input("Est. Cost per Exact Target Lead ($)", value=2.00)
        conversion_rate = st.slider("Percentage of leads who drive there & redeem (%)", 5, 50, 12)
        aov = st.number_input("Average Order Value ($)", value=45.00)
        
        total_leads = int(ad_spend / cost_per_lead)
        total_walk_ins = int(total_leads * (conversion_rate / 100))
        gross_revenue = total_walk_ins * aov
        profit = gross_revenue - ad_spend
        
        st.markdown("---")
        st.metric(label="📍 Captured Leads (Local Database)", value=f"{total_leads} people")
        st.metric(label="🚗 Guaranteed Map Routings/Walk-ins", value=f"{total_walk_ins} customers")
        st.metric(label="💵 Generated Gross Revenue", value=f"${gross_revenue:,.2f}", delta=f"${profit:,.2f} ROI")
