import pandas as pd
import openai
import os

def generate_ads():
    try:
        df = pd.read_csv("leads.csv")
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "":
            print("⚠️ No API Key found. Generating placeholder ads for testing...")
            df['generated_ad'] = "Promo for " + df['business_name'] + " near " + df['landmark'] + "! Visit us today."
        else:
            print("✅ API Key found. Generating AI ads...")
            client = openai.OpenAI(api_key=api_key)
            ad_results = []
            for _, row in df.iterrows():
                prompt = f"Write a local Facebook ad for {row['business_name']} near {row['landmark']}."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                ad_results.append(response.choices[0].message.content)
            df['generated_ad'] = ad_results

        df.to_csv("final_ads.csv", index=False)
        print("✅ Process complete. final_ads.csv created.")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        # Create a dummy file anyway so the next step doesn't fail
        pd.DataFrame({"error": [str(e)]}).to_csv("final_ads.csv", index=False)

if __name__ == "__main__":
    generate_ads()
