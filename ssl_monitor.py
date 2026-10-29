import os
import requests
import json
from datetime import datetime

# RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")
RAPIDAPI_HOST = "ssl-certificate-inspector.p.rapidapi.com" # Update to your exact host
API_URL = f"https://{RAPIDAPI_HOST}/"

DOMAINS_TO_CHECK = [
    "google.com",
    "github.com",
    "cloudflare.com"
]

def check_ssl_certificate(domain):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"domain": domain}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"⚠️ Quota Exceeded! Upgrade to Pro ($29/mo) or Ultra ($99/mo) at https://rapidapi.com/")
            return None
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def main():
    print(f"--- SSL Expiration & Health Report ({datetime.now().strftime('%Y-%m-%d')}) ---\n")
    
    for domain in DOMAINS_TO_CHECK:
        print(f"Checking {domain}...")
        result = check_ssl_certificate(domain)
        
        if result and result.get("success"):
            data = result.get("data", {})
            issuer = data.get("issuer", "Unknown")
            days_left = data.get("daysRemaining", "N/A")
            is_valid = data.get("isValid", False)
            
            status_icon = "✅" if is_valid and (isinstance(days_left, int) and days_left > 14) else "⚠️"
            
            print(f"  {status_icon} Status: {'Valid' if is_valid else 'Invalid/Expired'}")
            print(f"  🏢 Issuer: {issuer}")
            print(f"  ⏳ Days Remaining: {days_left}")
            print("-" * 40)

if __name__ == "__main__":
    main()
