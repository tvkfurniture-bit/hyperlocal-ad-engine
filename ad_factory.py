import pandas as pd
from groq import Groq
import os

def generate_ads():
    try:
        df = pd.read_csv("leads.csv")
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            print("⚠️ No GROQ_API_KEY found. Using fallback text.")
            df['generated_ad'] = "Special offer for " + df['business_name'] + " near " + df['landmark'] + "!"
        else:
            print("🚀 Groq API Key found. Generating Free AI ads...")
            client = Groq(api_key=api_key)
            
            ad_results = []
            for _, row in df.iterrows():
                # Using Llama3-8b which is free and fast on Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Write a short, punchy Facebook ad for {row['business_name']} in {row['neighborhood']}. Mention it is near {row['landmark']}. Max 30 words.",
                        }
                    ],
                    model="llama3-8b-8192",
                )
                ad_results.append(chat_completion.choices[0].message.content)
            
            df['generated_ad'] = ad_results

        df.to_csv("final_ads.csv", index=False)
        print("✅ Success! final_ads.csv created.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Ensure the workflow doesn't fail
        pd.DataFrame({"status": ["Error"], "msg": [str(e)]}).to_csv("final_ads.csv", index=False)

if __name__ == "__main__":
    generate_ads()
