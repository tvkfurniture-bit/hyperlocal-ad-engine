import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="Hyperlocal Storyboard Engine", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add your GROQ_API_KEY to the Streamlit Secrets!")
    st.stop()

st.title("🎬 Hyperlocal Storyboard & Video Engine")
st.markdown("Generate multi-scene, cinematic video prompts and ultra-realistic VoiceOver scripts.")

with st.expander("📍 TARGET EXACT BUSINESS & SCENES", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Exact Business Name (e.g., Luigi's Pizza)")
        biz_niche = st.text_input("Business Type (e.g., Pizzeria, Gym, Dentist)")
        # NEW FEATURE: Select number of scenes
        num_scenes = st.slider("Number of Scenes (approx 5 secs per scene)", min_value=1, max_value=10, value=4)
    with colB:
        biz_address = st.text_input("Exact Street Address, City, State")
        gmaps_link = st.text_input("Google Maps Share Link (https://goo.gl/maps/...)")
    
    generate_btn = st.button("⚡ Generate Cinematic Storyboard", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    with st.spinner(f"🌍 AI is writing a {num_scenes}-scene storyboard and continuous VoiceOver script..."):
        
        # 1. Generate Direct Response Ad
        ad_prompt = f"""
        Write a Facebook ad for {biz_name} ({biz_niche}) located exactly at {biz_address}.
        Create a ruthless 'Mafia Offer'. Make it urgent.
        The Call to Action MUST be: "Tap the link below to get directions instantly: {gmaps_link}"
        Keep it under 60 words. Pure direct response.
        """
        
        ad_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a master direct response copywriter."}, 
                {"role": "user", "content": ad_prompt}
            ]
        )
        generated_ad = ad_response.choices[0].message.content

        # 2. Generate Multi-Scene Storyboard
        vid_prompt = f"""
        You are an elite Hollywood Cinematographer and Direct Response Ad Director.
        Create a {num_scenes}-scene video ad storyboard for {biz_name} ({biz_niche}) at {biz_address}.
        
        CRITICAL RULES FOR AI VIDEO GENERATORS:
        1. NO TEXT IN VISUAL PROMPTS: Do NOT instruct the AI to generate any text, words, or logos on the screen.
        2. VISUALS ONLY: Describe camera movement, lighting, lens type, and hyper-realistic subjects.
        3. CONTINUOUS VOICEOVER: Write a natural, persuasive script that flows across all {num_scenes} scenes. Format it with clean punctuation so a Text-to-Speech AI (like ElevenLabs) reads it naturally.

        Format EXACTLY like this for EACH of the {num_scenes} scenes:

        ### SCENE [X]
        🎥 **Visual Prompt (Paste into Runway/Luma/Google Vids):** [Strictly visual. e.g., "Cinematic 4k shot, Sony FX3, 50mm lens. Slow pan across..."]
        🗣️ **VoiceOver Script (Paste into ElevenLabs):** [1-2 sentences of natural spoken dialogue.]
        ✍️ **Manual Text Overlay (Add in CapCut/Canva):** [Short punchy text to type on screen manually.]
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a master storyboard artist for AI video generation."}, 
                {"role": "user", "content": vid_prompt}
            ]
        )
        generated_storyboard = vid_response.choices[0].message.content

        st.session_state['ad_copy'] = generated_ad
        st.session_state['vid_prompt'] = generated_storyboard
        st.session_state['biz_name'] = biz_name

# --- DISPLAY ASSETS ---
if 'ad_copy' in st.session_state:
    st.markdown("---")
    st.header(f"🎬 Storyboard Assets for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The Storyboard Sequence")
        st.markdown(st.session_state['vid_prompt'])
        
        st.subheader("2️⃣ The 'Drive-to-Store' Ad Copy")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")

    with col2:
        st.subheader("🛠️ The Pro Assembly Workflow")
        st.info("""
        **How to build this realistically:**
        1. **Visuals:** Copy the 🎥 **Visual Prompts** one by one into Runway Gen-3, Luma Dream Machine, or Kling. (They will look 100x better without text).
        2. **Voice:** Copy all the 🗣️ **VoiceOver Scripts** into **ElevenLabs** (use the 'Marcus' or 'Adam' voice for high-converting male tones).
        3. **Assembly:** Drop the video clips and the ElevenLabs audio track into **CapCut** or Premiere.
        4. **Text:** Use CapCut to manually type the ✍️ **Manual Text Overlays** over the video. 
        """)

        st.subheader("3️⃣ The ROI Simulator (Your Sales Pitch)")
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
