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
st.markdown("Generate Ad Copy and 3 Master-Level Google Vids Prompts (Includes VoiceOver, SFX, and Cinematic Visuals).")

with st.expander("📍 TARGET EXACT BUSINESS LOCATION", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Exact Business Name (e.g., Luigi's Pizza)")
        biz_niche = st.text_input("Business Type (e.g., Pizzeria, Gym, Dentist)")
    with colB:
        biz_address = st.text_input("Exact Street Address, City, State")
        gmaps_link = st.text_input("Google Maps Share Link (https://goo.gl/maps/...)")
    
    generate_btn = st.button("⚡ Generate Master Assets", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    with st.spinner("🌍 AI is directing 3 Master Video Prompts with VoiceOver..."):
        
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

        # 2. Generate 3 Master Video Prompts (WITH VOICEOVER)
        vid_prompt = f"""
        Act as an Elite AI Video Director and Direct Response Copywriter. 
        Your task is to write 3 Master Prompts for Google Vids to generate an 8-10 second, 100% hyper-realistic video ad for {biz_name} ({biz_niche}) located at {biz_address}.
        
        For the video to multiply sales, it MUST contain VoiceOver (VO), Sound Effects (SFX), and hyper-specific camera instructions.
        
        Use this EXACT strict format for all 3 angles:
        
        ---
        **🔥 ANGLE 1: The Local POV Discovery**
        *Goal: Make them feel like a local friend is recommending it.*
        **Visual Prompt:** Generate an 8-second 4k hyper-realistic video. Shot on iPhone 15 Pro, 24mm lens, handheld POV motion. Scene: Walking up to the front of a busy, aesthetic {biz_niche}. Natural daylight, shallow depth of field. 
        **On-Screen Text:** "Hidden Gem on [Extract Street Name from {biz_address}] 📍"
        **VoiceOver Script:** (Tone: Upbeat, authentic local creator) "If you live near [Street Name], stop scrolling. I just found the best {biz_niche} in the city, and they are doing a crazy deal today."
        **Audio/SFX:** Upbeat trendy background track, subtle street ambiance.

        **🔥 ANGLE 2: The Sensory Overload (Product Focus)**
        *Goal: Make the product look so irresistible they have to buy it immediately.*
        **Visual Prompt:** Generate an 8-second 4k cinematic video. Shot on Sony FX3, 50mm macro lens, f/1.8. Scene: Extreme close-up slow-motion of the highest quality [describe a mouth-watering or premium aspect of the {biz_niche}]. Golden hour studio lighting, ultra-sharp focus.
        **On-Screen Text:** "Claim Your [Insert strong offer] Today 👇"
        **VoiceOver Script:** (Tone: Confident, fast-paced, high energy) "Drop what you're doing. {biz_name} is giving away [Offer] to the first 20 people who click the link below and drive here right now."
        **Audio/SFX:** Heavy bass drop on the hook, crisp ASMR sound effects of the product, energetic hip-hop beat.

        **🔥 ANGLE 3: The FOMO / Direct Call-Out**
        *Goal: Force immediate action through scarcity.*
        **Visual Prompt:** Generate an 8-second 4k hyper-realistic video. Fast-paced montage cuts. Scene: Busy, happy customers at {biz_name}, followed by a rapid zoom onto a phone screen showing a Google Maps pin at {biz_address}. High contrast, vibrant colors.
        **On-Screen Text:** "Only 12 Spots Left 🚨"
        **VoiceOver Script:** (Tone: Urgent, persuasive, direct) "We only have a few spots left for our local special at {biz_name}. Click the map link below, get directions, and show this video to the front desk before we run out."
        **Audio/SFX:** Ticking clock sound building tension, swoosh transitions, driving electronic beat.
        ---
        
        Fill in the bracketed info with highly descriptive, realistic details based on {biz_name} and {biz_address}.
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a Master AI Video Director. You write prompts that generate viral, high-converting video ads."}, 
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
    st.header(f"🎥 Master Video Assets & Ad Copy for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ Master Video Prompts (Visuals + Audio)")
        st.info("🎙️ **These prompts now include VoiceOver Scripts & Camera Gear settings for 100% realism.**")
        st.markdown(st.session_state['vid_prompt'])
        
        st.subheader("2️⃣ The 'Drive-to-Store' Ad Copy")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")

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
