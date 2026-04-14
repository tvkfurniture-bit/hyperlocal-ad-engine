import streamlit as st
import pandas as pd
from groq import Groq
import os
from fpdf import FPDF
import re
from datetime import datetime

st.set_page_config(page_title="Elite Hyperlocal Agency Tool", layout="wide")

# Connect to Groq via Streamlit Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

# ==========================================
# 🛡️ ARMOR-PLATED TEXT CLEANER (Prevents PDF Crashes)
# ==========================================
def clean_for_pdf(text):
    if not text:
        return ""
    text = text.replace('"', '"').replace('"', '"').replace('’', "'").replace('‘', "'").replace('—', '-')
    words = text.split(' ')
    safe_words = []
    for word in words:
        if len(word) > 65: 
            safe_words.append(word[:65] + " " + word[65:])
        else:
            safe_words.append(word)
    text = ' '.join(safe_words)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# ==========================================
# 🎨 CUSTOM PREMIUM PDF GENERATOR CLASS
# ==========================================
class AgencyPDF(FPDF):
    def header(self):
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
            
            self.set_x(10)
            clean_line = line.replace('**', '').replace('*', '')
            
            if clean_line.startswith('### SCENE'):
                self.ln(6)
                self.set_font('Arial', 'B', 12)
                self.set_text_color(0, 112, 243)
                self.multi_cell(0, 7, clean_line.replace('### ', ''))
            elif clean_line.startswith('###') or clean_line.startswith('##') or clean_line.startswith('Task'):
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
        
    generate_btn = st.button("⚡ GENERATE MASTER CAMPAIGN", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"
    comp_prompt = f"The client wants to outperform {competitor_name}." if competitor_name else ""

    with st.spinner("🧠 Director is drafting photorealistic cinematic prompts..."):
        
        # 1. GENERATE MASTER STRATEGY (Your Exact Preferred Prompt)
        strategy_prompt = f"""
        Business: {biz_name} ({biz_niche}) at {biz_address}.
        {comp_prompt}
        Task 1: Write 3 'Mafia Offers'.
        Task 2: Write direct-response Ad Copy under 50 words. The Call to Action MUST be: "Tap the link below to {cta_text} instantly: {cta_link}"
        Task 3: Write a cold outreach DM and Email for the agency owner.
        """
        strat_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a 7-figure marketing agency owner."}, {"role": "user", "content": strategy_prompt}]
        )
        strategy_data = strat_response.choices[0].message.content

        # 2. THE ENHANCED HOLLYWOOD STORYBOARD ENGINE (Your Exact Preferred Prompt)
        vid_prompt_instruction = f"""
        Act as a Hollywood Cinematographer and Senior Ad Director for a 2026 marketing agency.
        Create a {num_scenes}-scene hyper-realistic video ad for {biz_name} ({biz_niche}).
        Platform Format: {platform}.

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
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 Mafia Offers", "🎬 Master Storyboard", "💬 Outreach Scripts", "📄 Premium PDF Export"])
    
    # Safely split based on your preferred prompt structure
    try:
        offers_part = st.session_state['strategy'].split("Task 3")[0]
        outreach_part = "Task 3" + st.session_state['strategy'].split("Task 3")[1]
    except:
        offers_part = st.session_state['strategy']
        outreach_part = "Please refer to the bottom of the Strategy tab."

    with tab1:
        st.header("Campaign Strategy")
        st.markdown(offers_part)

    with tab2:
        st.header("Master Storyboard (Hollywood Grade)")
        st.info("💡 **PRO TIP:** Copy these visual prompts into Runway Gen-3 Alpha or Luma Dream Machine for 100% photorealism.")
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
            st.write("Generate a pristine, agency-branded PDF Proposal.")
            
            # PDF Generation using the Premium Agency Class
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
