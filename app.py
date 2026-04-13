import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="Hyperlocal Precision Targeter", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

st.title("🎯 Hyperlocal Precision Targeter & Video Engine")
st.markdown("Generate Ad Copy and 3 Exact Google Vids Prompts to multiply sales for local businesses.")

with st.expander("📍 TARGET EXACT BUSINESS LOCATION", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Exact Business Name (e.g., Luigi's Pizza)")
        biz_niche = st.text_input("Business Type (e.g., Pizzeria, Gym, Dentist)")
    with colB:
        biz_address = st.text_input("Exact Street Address, City, State")
        gmaps_link = st.text_input("Google Maps Share Link (https://goo.gl/maps/...)")
    
    generate_btn = st.button("⚡ Generate Precision Assets", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    with st.spinner("🌍 AI is building Ad Copy and 3 Google Vids Prompts..."):
        
        # 1. Generate Direct Response Ad
        ad_prompt = f"""
        Write a Facebook ad for {biz_name} ({biz_niche}) located exactly at {biz_address}.
        Start by calling out the specific street. Create a ruthless 'Mafia Offer' (e.g., 'Free item with purchase').
        Make it urgent (Valid for the first 20 people today).
        The Call to Action MUST be: "Tap the link below to get directions instantly: {gmaps_link}"
        Keep it under 60 words. Pure direct response to multiply sales.
        """
        
        ad_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a master direct response copywriter."}, 
                {"role": "user", "content": ad_prompt}
            ]
        )
        generated_ad = ad_response.choices[0].message.content

        # 2. Generate 3 Specific 8-Second Google Vids Prompts
        vid_prompt = f"""
        Write exactly 3 text-to-video prompts for Google Vids to generate an 8-second realistic video ad for {biz_name} ({biz_niche}) located at {biz_address}.
        The goal is to multiply sales and drive instant foot traffic.
        
        Provide 3 distinct angles. Use this EXACT format for each so it can be copied and pasted directly into Google Vids:
        
        ---
        **Angle 1: The Local Hook**
        PROMPT: Generate an 8-second hyper-realistic, 4k cinematic video. Scene: [Describe a realistic visual of the {biz_niche} or people enjoying it]. Text overlay appears on screen reading: "Live near [Extract Street Name from {biz_address}]?" followed by "Stop scrolling. We are {biz_name}." Camera style: Fast, engaging, social media ad style.

        **Angle 2: The Irresistible Offer**
        PROMPT: Generate an 8-second hyper-realistic, 4k cinematic video. Scene: [Describe extreme close-up, mouth-watering/high-quality visual of the product/service]. Text overlay appears on screen reading: "Hungry? Get [Insert strong fake offer] today only at {biz_name}." Camera style: Slow pan, highly detailed, bright lighting.

        **Angle 3: Urgency / FOMO**
        PROMPT: Generate an 8-second hyper-realistic, 4k cinematic video. Scene: [Describe a busy, energetic environment related to {biz_niche}]. Text overlay appears on screen reading: "Only 20 spots left today." followed by "Tap for directions to {biz_name}." Camera style: Fast-paced, high energy, dynamic motion.
        ---
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an elite AI Video Ad Director. You write prompts that generate highly realistic, sales-driven videos."}, 
                {"role": "user", "content": vid_prompt}
            ]
        )
        generated_video_prompt = vid_response.choices[0].message.content

        st.session_state['ad_copy'] = generated_ad
        st.session_state['vid_prompt'] = generated_video_prompt
        st.session_state['biz_name'] = biz_name

# --- DISPLAY ASSETS ---
if 'ad_copy' in st.session_state:
    st.markdown("---")
    st.header(f"📦 Precision Assets Delivered for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The 'Drive-to-Store' Ad Copy")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")
        
        st.subheader("2️⃣ 3x Google Vids Prompts (8-Seconds)")
        st.info("🎥 **Copy & Paste these into Google Vids to generate your 8-sec assets:**")
        st.markdown(st.session_state['vid_prompt'])

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
