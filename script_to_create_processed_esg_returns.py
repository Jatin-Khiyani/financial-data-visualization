import pandas as pd
import numpy as np

# Load
df_price = pd.read_csv("sp500_price_data.csv")
df_esg = pd.read_csv("sp500_esg_data.csv")

# 1. Calculate Returns
df_price["Date"] = pd.to_datetime(df_price["Date"])
df_price = df_price.set_index("Date").sort_index()

# Select period (as in user's original request)
start_date = "2023-01-01"
end_date = "2024-08-31"
df_period = df_price.loc[start_date:end_date]

if not df_period.empty:
    start_prices = df_period.iloc[0]
    end_prices = df_period.iloc[-1]
    returns = ((end_prices - start_prices) / start_prices) * 100
    returns_df = returns.reset_index()
    returns_df.columns = ["Symbol", "Return (%)"]

    # 2. ESG Clean
    df_esg_clean = df_esg[["Symbol", "totalEsg", "GICS Sector"]].copy()
    df_esg_clean["totalEsg"] = pd.to_numeric(df_esg_clean["totalEsg"], errors="coerce")
    df_esg_clean = df_esg_clean.dropna(subset=["totalEsg"])

    # 3. Merge
    df = pd.merge(returns_df, df_esg_clean, on="Symbol")
    df = df[(df["Return (%)"] > -100) & (df["Return (%)"] < 300)]
    
    # Save the processed data for later use in visual scripts if needed
    df.to_csv("processed_esg_returns.csv", index=False)
    print("Merged data summary:")
    print(df.describe())
else:
    print("No data in range.")