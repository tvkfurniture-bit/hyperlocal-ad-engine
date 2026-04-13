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
st.markdown("Generate dynamic, non-repetitive video prompts and modern VoiceOvers.")

with st.expander("📍 TARGET EXACT BUSINESS & SCENES", expanded=True):
    colA, colB = st.columns(2)
    with colA:
        biz_name = st.text_input("Exact Business Name (e.g., Kaydiem Script Lab)")
        biz_niche = st.text_input("Business Type (e.g., Screenwriting Hub, Pizza, Gym)")
        num_scenes = st.slider("Number of Scenes (approx 4 secs per scene)", min_value=1, max_value=10, value=6)
    with colB:
        biz_address = st.text_input("Exact Street Address, City, State")
        gmaps_link = st.text_input("Google Maps Share Link (https://goo.gl/maps/...)")
        website_url = st.text_input("Website URL (Optional)", placeholder="https://www.example.com")
    
    generate_btn = st.button("⚡ Generate Dynamic Storyboard", type="primary", use_container_width=True)

if generate_btn and biz_name and biz_address:
    
    # Logic to determine CTA destination
    cta_link = website_url if website_url else gmaps_link
    cta_text = "visit our website" if website_url else "get directions"

    with st.spinner(f"🌍 AI is directing a high-retention {num_scenes}-scene storyboard..."):
        
        # 1. Generate Direct Response Ad
        ad_prompt = f"""
        Write a Facebook ad for {biz_name} ({biz_niche}) located at {biz_address}.
        Create a ruthless 'Mafia Offer'. Make it urgent.
        The Call to Action MUST be: "Tap the link below to {cta_text} instantly: {cta_link}"
        Keep it under 60 words. Pure direct response.
        """
        
        ad_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a master direct response copywriter."}, {"role": "user", "content": ad_prompt}]
        )
        generated_ad = ad_response.choices[0].message.content

        # 2. Generate Multi-Scene Storyboard with STRICT VARIETY RULES
        vid_prompt = f"""
        You are an elite Hollywood Cinematographer and modern TikTok/Reels Ad Director.
        Create a {num_scenes}-scene video ad storyboard for {biz_name} ({biz_niche}) at {biz_address}.
        
        CRITICAL RULES TO PREVENT BORING VIDEOS:
        1. NEVER REPEAT ANGLES: If Scene 1 is a wide shot, Scene 2 MUST be an extreme macro close-up. If Scene 3 is a person, Scene 4 MUST be an object in motion. Force dynamic visual variety.
        2. NO CHEESY VOICEOVERS: BANNED WORDS: "Imagine a place", "Unlock your potential", "Where dreams come true". Use punchy, fast-paced, conversational modern hooks.
        3. MANDATORY TEXT OVERLAYS: You MUST provide 2-5 words for the Manual Text Overlay on EVERY scene. It cannot be "None". It must be a punchy marketing hook.
        4. THE CTA: The final scene's VoiceOver must tell them to click the link to {cta_text}.

        Format EXACTLY like this for EACH of the {num_scenes} scenes:

        ### SCENE [X]
        🎥 **Visual Prompt:** [Strictly visual. E.g., "Cinematic 4k, FPV drone flying through the front door...", or "Macro shot, 100mm lens, extreme close up of coffee dripping..."]
        🗣️ **VoiceOver Script:** [1 snappy, conversational sentence.]
        ✍️ **Manual Text Overlay:** [2-5 words. E.g., "Stop Scrolling." or "The Secret is Out."]
        """
        
        vid_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are a master storyboard artist who writes fast-paced, non-repetitive, modern video ads."}, {"role": "user", "content": vid_prompt}]
        )
        generated_storyboard = vid_response.choices[0].message.content

        st.session_state['ad_copy'] = generated_ad
        st.session_state['vid_prompt'] = generated_storyboard
        st.session_state['biz_name'] = biz_name

# --- DISPLAY ASSETS ---
if 'ad_copy' in st.session_state:
    st.markdown("---")
    st.header(f"🎬 Dynamic Assets for {st.session_state['biz_name']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The Storyboard Sequence")
        st.markdown(st.session_state['vid_prompt'])
        
        st.subheader("2️⃣ The Ad Copy")
        st.success(f"**Sponsored** • {st.session_state['biz_name']}\n\n{st.session_state['ad_copy']}")

    with col2:
        st.subheader("🛠️ The Pro Assembly Workflow")
        st.info("""
        **How to build this realistically:**
        1. **Visuals:** Copy the 🎥 **Visual Prompts** into Runway Gen-3, Luma Dream Machine, or Kling.
        2. **Voice:** Copy the 🗣️ **VoiceOver Scripts** into **ElevenLabs** (use 'Marcus' or 'Adam' for high conversions).
        3. **Assembly:** Drop clips and audio into **CapCut**.
        4. **Text:** Use CapCut to type the ✍️ **Manual Text Overlays** over the video (Use bold fonts like 'Impact' or 'Proxima Nova'). 
        """)

        st.subheader("3️⃣ The ROI Simulator")
        ad_spend = st.slider("Monthly Ad Spend ($)", 100, 1000, 300)
        cost_per_lead = st.number_input("Est. Cost per Exact Target Lead ($)", value=2.00)
        conversion_rate = st.slider("Percentage of leads who convert (%)", 5, 50, 12)
        aov = st.number_input("Average Lifetime Value ($)", value=150.00)
        
        total_leads = int(ad_spend / cost_per_lead)
        total_walk_ins = int(total_leads * (conversion_rate / 100))
        gross_revenue = total_walk_ins * aov
        profit = gross_revenue - ad_spend
        
        st.markdown("---")
        st.metric(label="📍 Captured Leads (Email/Phone Database)", value=f"{total_leads} people")
        st.metric(label="✅ Expected Conversions", value=f"{total_walk_ins} customers")
        st.metric(label="💵 Generated Gross Revenue", value=f"${gross_revenue:,.2f}", delta=f"${profit:,.2f} ROI")
