import wrds
import pandas as pd
from decouple import config
import os

def pull_crsp_value_weighted_index(start_date='1930-01-01', end_date='2024-01-01'):
    """
    Pulls the CRSP value-weighted index monthly returns from WRDS.
    
    Parameters:
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
    - DataFrame: Contains date, return, and other key fields.
    """

    # Get WRDS username from environment variables or .env file
    WRDS_USERNAME = config("WRDS_USERNAME", default=os.getenv("WRDS_USERNAME"))

    if not WRDS_USERNAME:
        raise ValueError("WRDS_USERNAME is not set. Add it to your environment variables or .env file.")

    # Connect to WRDS
    db = wrds.Connection(wrds_username=WRDS_USERNAME)

    # Check available columns in crsp.msi
    table_desc = db.describe_table('crsp', 'msi')
    print("CRSP.msi Table Columns:", table_desc.columns.tolist())

    # Verify column names (adjust based on the actual table structure)
    query = f"""
        SELECT date AS date, vwretd AS value_weighted_return
        FROM crsp.msi
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date;
    """

    # Execute query
    df = db.raw_sql(query, date_cols=['date'])

    # Close connection
    db.close()

    # Convert date to datetime format
    df['date'] = pd.to_datetime(df['date'])

    return df

if __name__ == "__main__":
    # Pull CRSP value-weighted index data
    crsp_data = pull_crsp_value_weighted_index()
    
    # Save to CSV
    crsp_data.to_csv("crsp_value_weighted_index.csv", index=False)
    
    print("CRSP value-weighted index data saved to crsp_value_weighted_index.csv")
