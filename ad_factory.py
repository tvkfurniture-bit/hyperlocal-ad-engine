import pandas as pd
from groq import Groq
import os

def generate_ads():
    try:
        # 1. Check if file exists AND is not empty
        if not os.path.exists("leads.csv") or os.path.getsize("leads.csv") == 0:
            print("⚠️ leads.csv is empty or missing! Using backup data.")
            df = pd.DataFrame({
                "name": ["Demo Restaurant"], 
                "neighborhood": ["Demo Area"], 
                "landmark": ["Demo Landmark"]
            })
        else:
            # Read the file if it has data
            try:
                df = pd.read_csv("leads.csv")
            except pd.errors.EmptyDataError:
                print("⚠️ leads.csv has no columns! Using backup data.")
                df = pd.DataFrame({
                    "name": ["Demo Restaurant"], "neighborhood": ["Demo Area"], "landmark": ["Demo Landmark"]
                })

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            print("⚠️ No GROQ_API_KEY found. Using fallback text.")
            df['generated_ad'] = "Visit " + df['name'] + " today!"
        else:
            print("🚀 Groq API Key found. Generating AI ads using Llama 3.1...")
            client = Groq(api_key=api_key)
            ad_results = []
            
            for _, row in df.iterrows():
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": """You are an elite Direct-Response copywriter. You write ads that convert instantly. 
                                NO fluff. NO puns. NO cheesy words like 'savor', 'masterpiece', or 'transport your taste buds'.
                                Write raw, punchy, hyper-local ads focused on an irresistible offer."""
                            },
                            {
                                "role": "user",
                                "content": f"""Write a Facebook ad for a restaurant named {row['name']} located in {row['neighborhood']}. 
                                
                                Follow this exact structure:
                                1. The Hook: Call out the locals who live or work near {row['landmark']}.
                                2. The Pain: Acknowledge that finding a good lunch/dinner around here is tough or overpriced.
                                3. The Offer: Create a ruthless, irresistible 'Mafia Offer' (e.g., 'Free Appetizer with any Main' or '2-for-1 Pizzas'). 
                                4. The Urgency: Limit it to the first 20 people today.
                                
                                Keep it under 50 words. Make it sound like a local insider wrote it."""
                            }
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    ad_results.append(chat_completion.choices[0].message.content)
                except Exception as api_err:
                    print(f"⚠️ API Error: {api_err}")
                    ad_results.append(f"Come visit {row['name']} near {row['landmark']}!")
            
            df['generated_ad'] = ad_results

        df.to_csv("final_ads.csv", index=False)
        print("✅ Success! final_ads.csv created.")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        pd.DataFrame({"status": ["Error"], "msg": [str(e)]}).to_csv("final_ads.csv", index=False)

if __name__ == "__main__":
    generate_ads()
