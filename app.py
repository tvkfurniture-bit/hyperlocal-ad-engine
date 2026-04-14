import streamlit as st
import pandas as pd
from groq import Groq
import os
from fpdf import FPDF
import re
from datetime import datetime

st.set_page_config(page_title="Elite Hyperlocal Agency Tool", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

# ==========================================
# 🛡️ ARMOR-PLATED TEXT CLEANER
# ==========================================
def clean_for_pdf(text):
    if not text:
        return ""
    # 1. Replace weird AI quotes/dashes with standard ones
    text = text.replace('"', '"').replace('"', '"').replace('’', "'").replace('‘', "'").replace('—', '-')
    
    # 2. Break apart massively long URLs so they don't crash the PDF
    words = text.split(' ')
    safe_words = []
    for word in words:
        if len(word) > 65: # If a word/URL is longer than 65 characters, slice it
            safe_words.append(word[:65] + " " + word[65:])
        else:
            safe_words.append(word)
    text = ' '.join(safe_words)
    
    # 3. Strip emojis and force into Latin-1 encoding (The only format FPDF natively accepts)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# ==========================================
# 🎨 CUSTOM PDF GENERATOR CLASS
# ==========================================
class AgencyPDF(FPDF):
    def header(self):
        # Dark Blue Top Banner
        self.set_fill_color(10, 37, 64)
        self.rect(0, 0, 210, 25, 'F')
        
        self.set_y(10)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5, 'HYPERLOCAL GROWTH BLUEPRINT', 0, 1, 'C')
        self.set_y(35)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Confidential Strategy Document  |  Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, color=(10, 37, 64)):
        self.ln(5)
        self.set_x(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*color)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def print_smart_text(self, text):
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                self.ln(4)
                continue
            
            self.set_x(10) # Reset X margin to prevent horizontal space errors
            clean_line = line.replace('**', '').replace('*', '')
            
            if clean_line.startswith('### SCENE'):
                self.ln(6)
                self.set_font('Arial', 'B', 12)
                self.set_text_color(0, 112, 243) # Bright Blue
                self.multi_cell(0, 7, clean_line.replace('### ', ''))
            elif clean_line.startswith('###') or clean_line.startswith('##'):
                self.ln(4)
                self.set_font('Arial', 'B', 12)
                self.set_text_color(10, 37, 64)
                self.multi_cell(0, 7, clean_line.replace('#', '').strip())
            elif clean_line.startswith('- '):
                self.set_font('Arial', '', 11)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 6, "- " + clean_line[2:])
            else:
                self.set_font('Arial', '', 11)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 6, clean_line)

# ==========================================
# 🚀 MAIN STREAMLIT APP LOGIC
# ==========================================
st.title("🎬 Elite Agency-in-a-Box: Hollywood Director Edition")
st.markdown("Automate Mafia Offers, Cinematic Video Direction, and ROI Sales Pitching in one click.")

with st.expander("📍 TARGET BUSINESS & STRATEGY SETUP", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        biz_name = st.text_input("Business Name", value="Foster Fork - The Taste Place")
        biz_niche = st.text_input("Niche", value="Fine Dining")
        biz_address = st.text_input("Exact Address", value="Downtown Urban Area")
    with col2:
        competitor_name = st.text_input("Main Competitor (Optional)")
        gmaps_link = st.text_input("Google Maps Link", value="https://goo.gl/maps/...")
        website_url = st.text_input("Website (Optional)")
    with col3:
        platform = st.selectbox("Video Platform Format", ["TikTok / IG Reels", "YouTube Pre-Roll", "LinkedIn B2B"])
        num_scenes = st.slider("Number of Scenes", 2, 10, 5)
        
    generate_btn = st.button("⚡ GENERATE MASTER CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"
    comp_prompt = f"The client wants to steal market share from their rival: {competitor_name}." if competitor_name else ""

    with st.spinner(f"🧠 AI is architecting Hollywood-grade prompts for {platform}..."):
        
        # 1. STRATEGY GENERATION
        strategy_prompt = f"""
        Business: {biz_name} ({biz_niche}) at {biz_address}.
        {comp_prompt}
        Write the campaign strategy. Format exactly with these headers:
        ### TASK 1 & 2: MAFIA OFFERS AND AD COPY
        - Write 3 'Mafia Offers'.
        - Write direct-response Ad Copy (under 50 words). CTA MUST be: "Tap the link below to {cta_text} instantly: {cta_link}"
        ### TASK 3: OUTREACH SCRIPTS
        - Write a cold DM and Cold Email.
        """
        strat_response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system", "content": "You are a 7-figure marketing agency owner."}, {"role": "user", "content": strategy_prompt}])
        strategy_data = strat_response.choices[0].message.content

        # 2. STORYBOARD GENERATION
        plat_rules = "Fast camera movements, photorealistic." if platform == "TikTok / IG Reels" else "High-budget cinematic feel, dramatic lighting."
        vid_prompt_instruction = f"""
        Create a {num_scenes}-scene hyper-realistic video ad for {biz_name} ({biz_niche}). Platform: {platform}. {plat_rules}
        RULES:
        1. NO TEXT in visual descriptions.
        2. 6-POINT FRAMEWORK: Style, Subject, Action, Lens, Lighting, Texture.
        3. Scenes MUST alternate (Wide, Medium, Macro).
        Format EXACTLY like this:
        ### SCENE [X]
        Enhanced Visual Prompt: [Min 60 words describing scene]
        VoiceOver Script: [1 snappy sentence]
        Manual Text Overlay: [2-5 bold marketing words]
        """
        vid_response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system", "content": "You are an Elite Cinematic Prompt Engineer."}, {"role": "user", "content": vid_prompt_instruction}])
        storyboard_data = vid_response.choices[0].message.content

        st.session_state['strategy'] = strategy_data
        st.session_state['storyboard'] = storyboard_data
        st.session_state['biz_name'] = biz_name

if 'strategy' in st.session_state:
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 Offers & Copy", "🎬 Master Storyboard", "💬 Sales Scripts", "📊 Export Premium PDF"])
    
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
        st.markdown(st.session_state['storyboard'])
    with tab3:
        st.header("Sales & Outreach Scripts")
        st.markdown(outreach_part)

    with tab4:
        st.header("ROI Simulator & Premium PDF Export")
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
            
            st.metric(label="💵 Projected Gross Revenue", value=f"${revenue:,.2f}", delta=f"${profit:,.2f} ROI")

        with colB:
            st.subheader("Generate Pitch Deck")
            st.write("Generate a pristine, agency-branded PDF Proposal.")
            
            # PDF Generation
            pdf = AgencyPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", 'B', 22)
            pdf.set_text_color(10, 37, 64)
            pdf.cell(0, 15, "Targeted Acquisition Blueprint", 0, 1, 'C')
            pdf.set_font("Arial", 'I', 14)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 10, f"Prepared exclusively for: {clean_for_pdf(st.session_state['biz_name'])}", 0, 1, 'C')
            pdf.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
            pdf.ln(10)
            
            pdf.chapter_title("1. Mafia Offers & Campaign Strategy")
            pdf.print_smart_text(clean_for_pdf(offers_part))
            
            pdf.add_page()
            pdf.chapter_title(f"2. Cinematic Storyboard ({platform})")
            pdf.print_smart_text(clean_for_pdf(st.session_state['storyboard']))
            
            pdf.add_page()
            pdf.chapter_title("3. Financial Projections & ROI")
            
            pdf.set_fill_color(245, 248, 250)
            pdf.rect(10, pdf.get_y(), 190, 60, 'F')
            pdf.set_y(pdf.get_y() + 10)
            
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(10, 37, 64)
            pdf.cell(0, 10, f"  Proposed Monthly Ad Spend:   ${ad_spend:,.2f}", 0, 1, 'L')
            pdf.cell(0, 10, f"  Estimated Walk-ins / Sales:   {walk_ins} New Customers", 0, 1, 'L')
            
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 150, 60)
            pdf.cell(0, 15, f"  Projected Gross Revenue:   ${revenue:,.2f}", 0, 1, 'L')
            
            # Final output and download
            try:
                # Remove spaces from filename safely
                safe_biz_name = "".join([c for c in st.session_state['biz_name'] if c.isalpha() or c.isdigit()]).rstrip()
                pdf_file_path = f"Growth_Blueprint_{safe_biz_name}.pdf"
                pdf.output(pdf_file_path)
                
                with open(pdf_file_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Premium Agency PDF", 
                        data=pdf_file.read(), 
                        file_name=pdf_file_path, 
                        mime='application/octet-stream', 
                        type="primary",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error compiling PDF: {e}")
