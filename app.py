import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="Hyperlocal Video & Revenue Engine", layout="wide")

# Connect to Groq using Streamlit Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

st.title("🚀 Live Hyperlocal Targeting & Video Engine")
st.markdown("Enter any local business to instantly generate their Video Asset, Ad Copy, and ROI Projections.")

# --- LIVE TARGETING ENGINE ---
with st.expander("🎯 TARGET A NEW BUSINESS (Start Here)", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Business Name (e.g., Iron & Oak Coffee)")
        biz_niche = st.text_input("Niche (e.g., Coffee Shop, Pizza, Gym)")
    with colB:
        neighborhood = st.text_input("Neighborhood/City (e.g., East District)")
        landmark = st.text_input("Nearest Famous Landmark (e.g., The Tech Hub)")
    
    generate_btn = st.button("⚡ Generate Hyperlocal Assets", type="primary", use_container_width=True)

if generate_btn and biz_name and landmark:
    with st.spinner("🧠 AI is building the Ad, Video Prompt, and Strategy..."):
        # 1. Generate Ad Copy
        ad_prompt = f"""Write a Facebook ad for {biz_name} ({biz_niche}) in {neighborhood}. 
        Hook: Call out locals near {landmark}. 
        Offer: Irresistible 'buy one get one' or 'free item'. 
        Call to Action: Text us to claim. Max 40 words. Direct-response style."""
        
        ad_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a master direct response copywriter."}, {"role": "user", "content": ad_prompt}]
        )
        generated_ad = ad_response.choices[0].message.content

        # 2. Generate Video Prompt for Google Vids / Runway
        vid_prompt = f"""Write a highly detailed text-to-video AI prompt to generate an ad for {biz_name} near {landmark}. 
        Format it perfectly for a tool like Google Vids or Runway Gen-3. 
        Include: Camera movement, lighting, visual subjects, and exactly what the text overlay should say on the screen.
        Make it cinematic, energetic, and highly focused on foot traffic from {landmark}."""
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are an elite AI Video Director."}, {"role": "user", "content": vid_prompt}]
        )
        generated_video_prompt = vid_response.choices[0].message.content

        # Save to session state so it doesn't disappear
        st.session_state['ad_copy'] = generated_ad
        st.session_state['vid_prompt'] = generated_video_prompt
        st.session_state['biz_name'] = biz_name

# --- DISPLAY ASSETS ---
if 'ad_copy' in st.session_state:
    st.markdown("---")
    st.header(f"📦 Delivered Assets for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The Acquisition Ad")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")
        
        st.subheader("2️⃣ The AI Video Generation Prompt")
        st.info("📋 **Copy & Paste this into Google Vids, Runway, or Luma:**")
        st.code(st.session_state['vid_prompt'], language="text")
        st.caption("Use this prompt to generate the video, then send the video to the business owner.")

    with col2:
        st.subheader("3️⃣ The ROI Simulator")
        st.markdown(f"**Show them the math.**")
        
        ad_spend = st.slider("Monthly Ad Spend ($)", 100, 1000, 300)
        cost_per_lead = st.number_input("Est. Cost per Local Lead (Phone # captured)", value=1.50)
        conversion_rate = st.slider("Percentage of leads who walk in & redeem (%)", 5, 50, 15)
        aov = st.number_input("Average Order Value ($)", value=45.00)
        
        total_leads = int(ad_spend / cost_per_lead)
        total_walk_ins = int(total_leads * (conversion_rate / 100))
        gross_revenue = total_walk_ins * aov
        profit = gross_revenue - ad_spend
        
        st.markdown("---")
        st.metric(label="📊 Captured Local Leads", value=f"{total_leads} people")
        st.metric(label="🚶‍♂️ Guaranteed Walk-ins", value=f"{total_walk_ins} customers")
        st.metric(label="💵 Generated Gross Revenue", value=f"${gross_revenue:,.2f}", delta=f"${profit:,.2f} ROI")
