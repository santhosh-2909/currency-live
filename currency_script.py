import os
import requests
import pandas as pd

# Read API key from environment variable
api_key = os.getenv("FASTFOREX_API_KEY")
if not api_key:
    raise ValueError("FASTFOREX_API_KEY not found in environment variables")

# Build API request URL
url = f"https://api.fastforex.io/fetch-all?from=INR&api_key={api_key}"
response = requests.get(url)

# Check response status
if response.status_code != 200:
    raise Exception("API request failed")

rates_data = response.json()
conversion_to_inr = []

# Process results
if "results" in rates_data and "error" not in rates_data:
    inr_to_currencies = rates_data["results"]

    for currency_code, rate in inr_to_currencies.items():
        if currency_code == "INR":
            value = 1.0
        elif rate != 0:
            value = 1 / rate
        else:
            value = None

        conversion_to_inr.append({
            "Currency": currency_code,
            "INR_Equivalent_of_1_Unit": value
        })

    # Create DataFrame
    df = pd.DataFrame(conversion_to_inr)
    df = df.sort_values(by="Currency").reset_index(drop=True)

    # Add timestamp
    df["Last_Updated"] = pd.Timestamp.now()

    # Save to CSV
    df.to_csv("currency_to_inr_conversions.csv", index=False)

    print("✅ CSV updated successfully!")

else:
    raise Exception(f"API Error: {rates_data.get('error', 'Unknown error')}")