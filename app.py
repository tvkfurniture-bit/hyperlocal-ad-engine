import streamlit as st
import pandas as pd
from groq import Groq
import os
from fpdf import FPDF
import re

st.set_page_config(page_title="Elite Hyperlocal Agency Tool", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

def clean_for_pdf(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

st.title("🎬 Elite Agency-in-a-Box: Hollywood Director Edition")

with st.expander("📍 TARGET BUSINESS & STRATEGY SETUP", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        biz_name = st.text_input("Business Name", value="Kaydiem Script Lab")
        biz_niche = st.text_input("Niche", value="Screenwriting Hub")
        biz_address = st.text_input("Exact Address", value="123 Writer's Block, NY")
    with col2:
        competitor_name = st.text_input("Main Competitor (Optional)", placeholder="e.g., The Writer's Guild")
        gmaps_link = st.text_input("Google Maps Link", value="https://goo.gl/maps/...")
        website_url = st.text_input("Website (Optional)", placeholder="https://...")
    with col3:
        platform = st.selectbox("Video Platform Format", ["TikTok / IG Reels", "YouTube Pre-Roll", "LinkedIn B2B"])
        num_scenes = st.slider("Number of Scenes", 2, 10, 6)
        
    generate_btn = st.button("⚡ GENERATE MASTER CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"
    comp_prompt = f"The client wants to outperform {competitor_name}." if competitor_name else ""

    with st.spinner("🧠 Director is drafting photorealistic cinematic prompts..."):
        
        # 1. GENERATE MASTER STRATEGY
        strategy_prompt = f"""
        Business: {biz_name} ({biz_niche}) at {biz_address}.
        {comp_prompt}
        Task 1: Write 3 'Mafia Offers'.
        Task 2: Write direct-response Ad Copy under 50 words.
        Task 3: Write a cold outreach DM and Email for the agency owner.
        """
        strat_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a 7-figure marketing agency owner."}, {"role": "user", "content": strategy_prompt}]
        )
        strategy_data = strat_response.choices[0].message.content

        # 2. THE ENHANCED HOLLYWOOD STORYBOARD ENGINE
        # This is where we force the AI to write LONG, DETAILED prompts.
        vid_prompt_instruction = f"""
        Act as a Hollywood Cinematographer and Senior Ad Director for a 2026 marketing agency.
        Create a {num_scenes}-scene hyper-realistic video ad for {biz_name} ({biz_niche}).

        PROMPT ENGINEERING RULES FOR MAXIMUM REALISM:
        1. NO TEXT: Do not include words or logos in the visual description.
        2. THE 6-POINT FRAMEWORK: Every prompt MUST include:
           - STYLE: (e.g., Photorealistic, Cinematic, 8k, IMAX)
           - SUBJECT: (e.g., A focused writer, a steaming cup of artisan coffee)
           - ACTION/MOTION: (e.g., slow-motion push-in, FPV drone sweep, parallax)
           - LENS & GEAR: (e.g., 35mm Anamorphic, 100mm Macro, Sony FX3)
           - LIGHTING: (e.g., Volumetric fog, Golden Hour, Moody Rim Lighting)
           - TEXTURE: (e.g., visible skin pores, steam particles, dust motes in sunbeams)
        3. VARIETY: Scenes MUST alternate between Wide, Medium, and Macro shots.

        Format for each scene:
        ### SCENE [X]
        🎥 **Enhanced Visual Prompt:** [Min 60 words of descriptive cinematic instruction]
        🗣️ **VoiceOver Script:** [1 snappy, conversational sentence]
        ✍️ **Manual Text Overlay:** [2-5 bold marketing words]
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are an Elite Cinematic Prompt Engineer. You write long, extremely detailed descriptions for AI Video generators."}, {"role": "user", "content": vid_prompt_instruction}]
        )
        storyboard_data = vid_response.choices[0].message.content

        st.session_state['strategy'] = strategy_data
        st.session_state['storyboard'] = storyboard_data
        st.session_state['biz_name'] = biz_name

# --- DISPLAY TABS ---
if 'strategy' in st.session_state:
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 Mafia Offers", "🎬 Master Storyboard", "💬 Outreach Scripts", "📄 PDF Pitch Deck"])
    
    with tab1:
        st.header("Campaign Strategy")
        st.markdown(st.session_state['strategy'].split("Task 3")[0])

    with tab2:
        st.header("Master Storyboard (Hollywood Grade)")
        st.info("Copy these visual prompts into Runway Gen-3 Alpha or Luma Dream Machine for 100% photorealism.")
        st.markdown(st.session_state['storyboard'])
        
    with tab3:
        st.header("Sales & Outreach Scripts")
        try:
            st.markdown("Task 3" + st.session_state['strategy'].split("Task 3")[1])
        except:
            st.markdown(st.session_state['strategy'])

    with tab4:
        st.subheader("ROI Simulator & PDF Export")
        ad_spend = st.slider("Proposed Ad Spend ($)", 100, 2000, 500)
        cpl = st.number_input("Cost Per Lead ($)", value=3.00)
        conv_rate = st.slider("Conversion Rate (%)", 1, 50, 10)
        aov = st.number_input("Average Order Value ($)", value=100.00)
        
        walk_ins = int((ad_spend / cpl) * (conv_rate / 100))
        revenue = walk_ins * aov
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Strategy: {st.session_state['biz_name']}", ln=True, align='C')
        pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['strategy']))
        pdf.add_page()
        pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['storyboard']))
        
        pdf_file_path = f"proposal_{st.session_state['biz_name'].replace(' ', '_')}.pdf"
        pdf.output(pdf_file_path)
        
        with open(pdf_file_path, "rb") as pdf_file:
            st.download_button(label="📥 Download Professional PDF Proposal", data=pdf_file.read(), file_name=pdf_file_path, mime='application/octet-stream', type="primary")
