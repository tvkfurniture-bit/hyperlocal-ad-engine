import pandas as pd
import openai
import os

def generate_ads():
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    df = pd.read_csv("leads.csv")
    
    ad_results = []
    for _, row in df.iterrows():
        prompt = f"Write a Facebook ad for {row['business_name']} located near {row['landmark']}. Highlight that they are a local favorite."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        ad_results.append(response.choices[0].message.content)
    
    df['generated_ad'] = ad_results
    df.to_csv("final_ads.csv", index=False)
    print("Ads generated and saved to final_ads.csv")

if __name__ == "__main__":
    generate_ads()
