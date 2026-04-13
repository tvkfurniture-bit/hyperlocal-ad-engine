import streamlit as st
import pandas as pd
from groq import Groq
import os
from fpdf import FPDF
import re

st.set_page_config(page_title="Hyperlocal Agency Engine v3.0", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

def clean_for_pdf(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

st.title("🛡️ Hyperlocal Agency Engine v3.0")
st.markdown("Professional-grade AI Storyboarding & Business Strategy.")

# --- INPUT SECTION ---
with st.expander("📍 CLIENT STRATEGY SETUP", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        biz_name = st.text_input("Business Name", placeholder="e.g. Iron & Oak Coffee")
        biz_niche = st.text_input("Business Niche", placeholder="e.g. Artisanal Roastery")
        biz_address = st.text_input("Exact Address", placeholder="123 Main St, New York")
    with col2:
        competitor_name = st.text_input("Competitor to Target", placeholder="e.g. Starbucks")
        website_url = st.text_input("Website (Optional)")
        gmaps_link = st.text_input("Google Maps Link")
    with col3:
        platform = st.selectbox("Format", ["TikTok / IG Reels", "YouTube Pre-Roll", "LinkedIn B2B"])
        num_scenes = st.slider("Scenes", 3, 10, 6)
        tone = st.selectbox("Voice Tone", ["Aggressive & Punchy", "Sophisticated & Luxury", "Friendly & Local"])
        
    generate_btn = st.button("⚡ GENERATE PRO-GRADE CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    cta_link = website_url if website_url else gmaps_link
    
    with st.spinner("💎 Engineering Elite Strategy & Cinematic Storyboard..."):
        
        # 1. THE STRATEGY PROMPT (Using 70B for Deep Reasoning)
        strategy_system = """You are a World-Class Direct Response Marketing Consultant. 
        You use the 'Hormozi Mafia Offer' framework. Your goal is to maximize ROI for the client.
        Avoid all marketing cliches. No 'Imagine a world' or 'Unlock your potential'. 
        Be raw, data-driven, and ruthless."""
        
        strategy_user = f"""Target Business: {biz_name} ({biz_niche}) at {biz_address}.
        Competitor: {competitor_name}. 
        Platform: {platform}.
        Tone: {tone}.

        TASK:
        1. Create 3 'Mafia Offers' based on the Value Equation: (Dream Outcome x Likelihood) / (Time Delay x Effort).
        2. Write one 45-word 'Punchy' Ad Copy.
        3. Write a high-stakes Cold Outreach DM for the agency to send this business owner.
        """

        strat_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "system", "content": strategy_system}, {"role": "user", "content": strategy_user}]
        )
        
        # 2. THE STORYBOARD PROMPT (Cinematic Enhancement)
        vid_system = """You are an Elite AI Video Director (Runway/Luma expert). 
        You understand cinematic terminology: focal length, lighting styles (Golden Hour, Volumetric, Rim Lighting), and camera movement (FPV, Parallax, Dolly Zoom).
        You strictly generate VISUAL descriptions. NO TEXT on screen.
        You write VoiceOver scripts that sound like a real person talking, including natural pauses and contractions."""

        vid_user = f"""Business: {biz_name}. Niche: {biz_niche}. Location: {biz_address}.
        Scenes requested: {num_scenes}. Platform: {platform}. Tone: {tone}.

        STORYBOARD RULES:
        - Each scene must be a different camera angle (Macro -> Wide -> POV -> Tracking).
        - VISUAL PROMPT: Describe 4k photorealistic details. Mention 'Arri Alexa' or '35mm Film' quality.
        - VOICEOVER: Write exactly what is said. Make it fast and high-retention.
        - OVERLAY: 2-3 words of high-impact text to be added manually.

        Format:
        ### SCENE [X]
        🎥 VISUAL: [Detailed Prompt]
        🗣️ VO: [Spoken Script]
        ✍️ TEXT: [Manual Overlay]
        """

        vid_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "system", "content": vid_system}, {"role": "user", "content": vid_user}]
        )

        st.session_state['strategy'] = strat_response.choices[0].message.content
        st.session_state['storyboard'] = vid_response.choices[0].message.content
        st.session_state['biz_name'] = biz_name

# --- DISPLAY OUTPUT ---
if 'strategy' in st.session_state:
    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["🔥 Strategy", "🎬 Storyboard", "✉️ Outreach", "📊 ROI & PDF"])
    
    with t1:
        st.markdown(st.session_state['strategy'].split("3.")[0])
    
    with t2:
        st.markdown(st.session_state['storyboard'])
        
    with t3:
        st.info("Copy-paste these scripts to close the client.")
        try:
            st.markdown("### Outreach Script\n" + st.session_state['strategy'].split("3.")[1])
        except:
            st.markdown(st.session_state['strategy'])

    with t4:
        colA, colB = st.columns(2)
        with colA:
            st.subheader("Profit Simulator")
            spend = st.slider("Ad Spend ($)", 100, 2000, 500)
            aov = st.number_input("Avg Order Value ($)", value=60.00)
            leads = int(spend / 3) # assumes $3 CPL
            sales = int(leads * 0.10) # 10% conv
            st.metric("Total Revenue", f"${sales * aov:,.2f}", delta=f"${(sales*aov)-spend:,.2f} Profit")
        
        with colB:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Proposal: {st.session_state['biz_name']}", ln=True, align='C')
            pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['strategy']))
            pdf.add_page()
            pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['storyboard']))
            
            pdf_path = f"proposal.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF Proposal", f, file_name=f"Proposal_{st.session_state['biz_name']}.pdf", type="primary")
