import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hyperlocal Revenue Engine", layout="wide")

st.title("💸 Hyperlocal Revenue Predictor")
st.markdown("This system doesn't just run ads. It builds a localized customer database to generate revenue on demand.")

try:
    df = pd.read_csv("final_ads.csv")
    
    # Select the target business
    selected_biz = st.selectbox("Select Target Client:", df['name'])
    biz_data = df[df['name'] == selected_biz].iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ The Acquisition Funnel")
        st.info(f"**Target:** Locals within 1 mile of {biz_data['landmark']}")
        st.success(f"**The Hook (Meta/IG Ad):**\n\n{biz_data['generated_ad']}\n\n**Call to Action:** 'Tap to get your exclusive QR Code sent to your WhatsApp.'")
        st.caption("We capture their phone number BEFORE giving the offer. You now own the lead.")

    with col2:
        st.subheader("2️⃣ The ROI Simulator")
        st.markdown(f"**Let's calculate the math for {selected_biz}**")
        
        # Interactive Sliders for the Business Owner
        ad_spend = st.slider("Monthly Ad Spend ($)", 100, 1000, 300)
        cost_per_lead = st.number_input("Est. Cost per Local Lead (Phone # captured)", value=1.50)
        conversion_rate = st.slider("Percentage of leads who walk in & redeem (%)", 5, 50, 15)
        aov = st.number_input("Average Order Value ($) (What they spend when they come in)", value=45.00)
        
        # The Math
        total_leads = int(ad_spend / cost_per_lead)
        total_walk_ins = int(total_leads * (conversion_rate / 100))
        gross_revenue = total_walk_ins * aov
        profit = gross_revenue - ad_spend
        
        st.markdown("---")
        st.metric(label="📊 Captured Local Leads (Database Built)", value=f"{total_leads} people")
        st.metric(label="🚶‍♂️ Guaranteed Walk-ins (This Month)", value=f"{total_walk_ins} customers")
        st.metric(label="💵 Generated Gross Revenue", value=f"${gross_revenue:,.2f}", delta=f"${profit:,.2f} ROI")
        
    st.markdown("---")
    st.subheader("3️⃣ The Retention Multiplier (The Real Value)")
    st.markdown(f"> Next month, you have {total_leads} local phone numbers. Send 1 text message on a slow Tuesday, and instantly generate **${int(total_leads * 0.05 * aov):,.2f}** with ZERO ad spend.")

except Exception as e:
    st.warning("Please run the GitHub Action to generate the lead data first.")
