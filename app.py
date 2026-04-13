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

# Helper function to clean text for PDF generation (removes emojis that crash PDFs)
def clean_for_pdf(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

st.title("👑 Elite Agency-in-a-Box: Hyperlocal AI")
st.markdown("Automate Offers, Video Direction, Competitor Conquesting, and Sales Pitching in one click.")

# --- INPUT SECTION ---
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
        
    generate_btn = st.button("⚡ GENERATE ENTIRE CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"
    comp_prompt = f"Targeting Strategy: Steal customers from rival {competitor_name} by offering a significantly lower barrier to entry or a more 'Mafia' offer." if competitor_name else ""

    with st.spinner("🧠 AI is architecting Elite Strategy & Cinematic Storyboards..."):
        
        # 1. GENERATE MAFIA OFFERS & OUTREACH SCRIPTS (ELITE LOGIC)
        strategy_prompt = f"""
        Act as a World-Class Direct Response Marketing Consultant. 
        Target: {biz_name} ({biz_niche}) at {biz_address}.
        {comp_prompt}
        
        Task 1: Write 3 "Mafia Offers". Use the Value Equation: (Dream Outcome x Perceived Likelihood) / (Time Delay x Effort). NO marketing cliches like 'imagine'. Be ruthless.
        Task 2: Write one 45-word 'Punchy' Direct-response Ad Copy for {platform}. Link: {cta_link}.
        Task 3: Write a cold outreach DM and Email to the owner of {biz_name}. Focus on ROI and the custom video asset I just created for them.
        """
        
        strat_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile", # UPGRADED MODEL
            messages=[{"role": "system", "content": "You are a master of business strategy and high-stakes persuasion."}, {"role": "user", "content": strategy_prompt}]
        )
        strategy_data = strat_response.choices[0].message.content

        # 2. GENERATE PLATFORM-SPECIFIC STORYBOARD (ELITE CINEMATOGRAPHY)
        vid_prompt = f"""
        Act as an Elite AI Video Director (Runway/Luma expert). Create a {num_scenes}-scene storyboard for {biz_name}.
        Platform: {platform}. 

        CRITICAL CINEMATOGRAPHY RULES:
        1. VISUAL PROMPTS: Must specify camera gear (e.g., Arri Alexa, 35mm film), lighting (e.g., Volumetric, Golden Hour), and focal length (e.g., 24mm wide, 85mm macro).
        2. DYNAMIC PACING: Scene 1 MUST be a hook (FPV or Dolly Zoom). Every scene must change angles.
        3. NO TEXT IN VISUALS: Strictly visual descriptions only.
        4. VOICE OVER: Must sound like a real, conversational human (use contractions, natural pauses).

        Format EXACTLY like this for EACH of the {num_scenes} scenes:
        ### SCENE [X]
        🎥 **Visual Prompt:** [Technical visual instructions]
        🗣️ **VoiceOver Script:** [Natural spoken sentence]
        ✍️ **Manual Text Overlay:** [2-5 high-impact words]
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile", # UPGRADED MODEL
            messages=[{"role": "system", "content": "You are a master cinematographer and ad director."}, {"role": "user", "content": vid_prompt}]
        )
        storyboard_data = vid_response.choices[0].message.content

        # Save to session state
        st.session_state['strategy'] = strategy_data
        st.session_state['storyboard'] = storyboard_data
        st.session_state['biz_name'] = biz_name

# --- DISPLAY TABS --- (Structure exactly as you provided)
if 'strategy' in st.session_state:
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 The Mafia Offers & Copy", "🎬 The Storyboard", "💬 Client Outreach Scripts", "📄 Export Pitch Deck"])
    
    with tab1:
        st.header(f"Strategy for {st.session_state['biz_name']}")
        st.markdown(st.session_state['strategy'].split("Task 3")[0])

    with tab2:
        st.header(f"Platform: {platform}")
        st.markdown(st.session_state['storyboard'])
        
    with tab3:
        st.header("Sales & Outreach Scripts")
        st.info("Copy and paste these directly to the business owner after you generate the video.")
        try:
            st.markdown("Task 3" + st.session_state['strategy'].split("Task 3")[1])
        except:
            st.markdown(st.session_state['strategy'])

    with tab4:
        st.header("The ROI Pitch & Proposal")
        
        colA, colB = st.columns(2)
        with colA:
            st.subheader("Live ROI Simulator")
            ad_spend = st.slider("Proposed Ad Spend ($)", 100, 2000, 500)
            cpl = st.number_input("Cost Per Lead ($)", value=3.00)
            conv_rate = st.slider("Conversion Rate (%)", 1, 50, 10)
            aov = st.number_input("Average Order Value ($)", value=100.00)
            
            walk_ins = int((ad_spend / cpl) * (conv_rate / 100))
            revenue = walk_ins * aov
            st.success(f"**Projected ROI:** ${revenue:,.2f} from ${ad_spend} ad spend.")

        with colB:
            st.subheader("Generate PDF Proposal")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Hyperlocal Marketing Proposal: {st.session_state['biz_name']}", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['strategy']))
            pdf.add_page()
            pdf.cell(200, 10, txt="Video Storyboard Concepts", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=clean_for_pdf(st.session_state['storyboard']))
            pdf.add_page()
            pdf.cell(200, 10, txt="Financial Projections", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=f"Proposed Monthly Ad Spend: ${ad_spend}\nProjected Walk-ins: {walk_ins}\nProjected Gross Revenue: ${revenue:,.2f}")
            
            pdf_file_path = f"proposal_{st.session_state['biz_name'].replace(' ', '_')}.pdf"
            pdf.output(pdf_file_path)
            
            with open(pdf_file_path, "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(
                label="📥 Download PDF Pitch Deck",
                data=PDFbyte,
                file_name=pdf_file_path,
                mime='application/octet-stream',
                type="primary"
            )
