import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_hyperlocal_leads(neighborhood, category="restaurants"):
    # This targets Yelp's search which is more scraper-friendly than Maps for beginners
    url = f"https://www.yelp.com/search?find_desc={category}&find_loc={neighborhood}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    leads = []
    # Logic to find business names and ratings
    for biz in soup.select('div[class*="container"]'):
        try:
            name = biz.find('a').text
            rating = biz.find('span', {'class': 'css-1p9ibgf'}).text # Rating class
            # Only target businesses with < 4 stars (The "Optimization" Wedge)
            if float(rating) < 4.0:
                leads.append({"name": name, "rating": rating, "neighborhood": neighborhood})
        except:
            continue
            
    df = pd.DataFrame(leads)
    df.to_csv("leads.csv", index=False)
    print(f"✅ Found {len(df)} underperforming restaurants in {neighborhood}")

if __name__ == "__main__":
    get_hyperlocal_leads("Brooklyn, NY") # Change this to your target city
