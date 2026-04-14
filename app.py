import streamlit as st
import pandas as pd
from groq import Groq
import os
from fpdf import FPDF
import re

st.set_page_config(page_title="Elite Hyperlocal Agency Tool", layout="wide")

# Connect to Groq via Streamlit Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

# Helper to prevent PDF crashing from emojis/special characters
def clean_for_pdf(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

st.title("🎬 Elite Agency-in-a-Box: Hollywood Director Edition")
st.markdown("Automate Mafia Offers, Cinematic Video Direction, and ROI Sales Pitching in one click.")

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
        num_scenes = st.slider("Number of Scenes", 2, 10, 5)
        
    generate_btn = st.button("⚡ GENERATE MASTER CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    # Determine the Call to Action
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"
    comp_prompt = f"The client wants to steal market share from their rival: {competitor_name}." if competitor_name else ""

    with st.spinner(f"🧠 AI is architecting Hollywood-grade prompts for {platform}..."):
        
        # 1. GENERATE MASTER STRATEGY (Offers & Outreach)
        strategy_prompt = f"""
        Business: {biz_name} ({biz_niche}) at {biz_address}.
        {comp_prompt}
        
        Write the campaign strategy. You MUST format your response exactly with these two headers:
        
        ### TASK 1 & 2: MAFIA OFFERS AND AD COPY
        - Write 3 'Mafia Offers' (Irresistible, no-brainer deals).
        - Write direct-response Ad Copy (under 50 words). The Call to Action MUST be: "Tap the link below to {cta_text} instantly: {cta_link}"
        
        ### TASK 3: OUTREACH SCRIPTS
        - Write a cold DM and Cold Email that I (the agency owner) can send to {biz_name} to pitch this campaign. Focus on the new video asset and ROI.
        """
        strat_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a 7-figure marketing agency owner."}, {"role": "user", "content": strategy_prompt}]
        )
        strategy_data = strat_response.choices[0].message.content

        # 2. THE ENHANCED HOLLYWOOD STORYBOARD ENGINE
        # Set dynamic rules based on the platform selected
        plat_rules = ""
        if platform == "TikTok / IG Reels":
            plat_rules = "Fast camera movements (whip pans, FPV drone, handheld POV), UGC feel but photorealistic."
        elif platform == "YouTube Pre-Roll":
            plat_rules = "High-budget cinematic feel, smooth gimbals, dramatic lighting, high tension before the 5-sec skip."
        else:
            plat_rules = "Corporate aesthetic, clean bright lighting, premium Sony/RED camera feel, slow steady pans."

        vid_prompt_instruction = f"""
        Act as a Hollywood Cinematographer and Senior Ad Director for a 2026 marketing agency.
        Create a {num_scenes}-scene hyper-realistic video ad for {biz_name} ({biz_niche}).
        Platform Format: {platform}. {plat_rules}

        PROMPT ENGINEERING RULES FOR MAXIMUM REALISM:
        1. NO TEXT: Do not include words or logos in the visual description.
        2. THE 6-POINT FRAMEWORK: Every prompt MUST include:
           - STYLE: (e.g., Photorealistic, Cinematic, 8k)
           - SUBJECT: (Highly detailed description of the subject/object)
           - ACTION/MOTION: (e.g., slow-motion push-in, FPV sweep)
           - LENS & GEAR: (e.g., 35mm Anamorphic, 100mm Macro, Sony FX3)
           - LIGHTING: (e.g., Volumetric fog, Golden Hour, Moody Rim Lighting)
           - TEXTURE: (e.g., visible skin pores, steam particles, dust motes in sunbeams)
        3. VARIETY: Scenes MUST alternate between Wide, Medium, and Macro shots.

        Format EXACTLY like this for each scene:
        ### SCENE [X]
        🎥 **Enhanced Visual Prompt:** [Min 60 words of descriptive cinematic instruction using the 6-point framework]
        🗣️ **VoiceOver Script:** [1 snappy, conversational sentence matching the {platform} tone]
        ✍️ **Manual Text Overlay:** [2-5 bold marketing words]
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are an Elite Cinematic Prompt Engineer. You write long, extremely detailed descriptions for AI Video generators."}, {"role": "user", "content": vid_prompt_instruction}]
        )
        storyboard_data = vid_response.choices[0].message.content

        # Save data to session state
        st.session_state['strategy'] = strategy_data
        st.session_state['storyboard'] = storyboard_data
        st.session_state['biz_name'] = biz_name

# --- DISPLAY TABS ---
if 'strategy' in st.session_state:
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 Offers & Ad Copy", "🎬 Master Storyboard", "💬 Sales Scripts", "📊 ROI Dashboard & PDF"])
    
    # Split the strategy text safely based on our exact prompt instruction
    try:
        offers_part = st.session_state['strategy'].split("### TASK 3: OUTREACH SCRIPTS")[0].replace("### TASK 1 & 2: MAFIA OFFERS AND AD COPY", "")
        outreach_part = st.session_state['strategy'].split("### TASK 3: OUTREACH SCRIPTS")[1]
    except:
        offers_part = st.session_state['strategy']
        outreach_part = "Please refer to the bottom of the Offers tab."

    with tab1:
        st.header("Campaign Strategy")
        st.markdown(offers_part)

    with tab2:
        st.header(f"Master Storyboard ({platform})")
        st.info("💡 **PRO TIP:** Copy these 60+ word visual prompts into Runway Gen-3 Alpha or Luma Dream Machine for 100% photorealism.")
        st.markdown(st.session_state['storyboard'])
        
    with tab3:
        st.header("Sales & Outreach Scripts")
        st.markdown(outreach_part)

    with tab4:
        st.header("ROI Simulator & PDF Export")
        
        colA, colB = st.columns(2)
        with colA:
            st.subheader("Live ROI Math")
            ad_spend = st.slider("Proposed Ad Spend ($)", 100, 2000, 500)
            cpl = st.number_input("Cost Per Lead ($)", value=3.00)
            conv_rate = st.slider("Conversion Rate (%)", 1, 50, 10)
            aov = st.number_input("Average Order Value ($)", value=100.00)
            
            walk_ins = int((ad_spend / cpl) * (conv_rate / 100))
            revenue = walk_ins * aov
            profit = revenue - ad_spend
            
            st.markdown("---")
            st.metric(label="📍 Captured Local Leads", value=f"{int(ad_spend/cpl)} people")
            st.metric(label="🚗 Guaranteed Walk-ins", value=f"{walk_ins} customers")
            st.metric(label="💵 Projected Gross Revenue", value=f"${revenue:,.2f}", delta=f"${profit:,.2f} ROI")

        with colB:
            st.subheader("Generate Pitch Deck")
            st.write("Generate a professional white-labeled PDF containing the strategy and storyboard to send to the client.")
            
            # PDF Generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Marketing Proposal: {st.session_state['biz_name']}", ln=True, align='C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt="Campaign Strategy", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=clean_for_pdf(offers_part))
            
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt="Cinematic Video Storyboard", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=clean_for_pdf(st.session_state['storyboard']))
            
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt="Financial Projections", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=f"Proposed Monthly Ad Spend: ${ad_spend}\nEstimated Walk-ins / Conversions: {walk_ins}\nProjected Gross Revenue: ${revenue:,.2f}")
            
            pdf_file_path = f"proposal_{st.session_state['biz_name'].replace(' ', '_')}.pdf"
            pdf.output(pdf_file_path)
            
            st.markdown("---")
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Professional PDF Proposal", 
                    data=pdf_file.read(), 
                    file_name=pdf_file_path, 
                    mime='application/octet-stream', 
                    type="primary"
                )
