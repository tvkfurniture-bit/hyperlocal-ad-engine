import pandas as pd

def segment_leads():
    df = pd.read_csv("leads.csv")
    # Identify the 'Wedge': Low rating but high volume = "Needs Better Marketing"
    df['segment'] = df['rating'].apply(lambda x: 'Recovery Campaign' if float(x) < 4.0 else 'Growth Campaign')
    
    # Add local landmark context (Elite level targeting)
    df['landmark'] = "Local Landmark" # In production, you'd map zip codes to landmarks
    df.to_csv("segmented_leads.csv", index=False)

if __name__ == "__main__":
    segment_leads()
