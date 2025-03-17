import pytest
import pandas as pd
import numpy as np

# Import all summary tables (adjust based on your actual module structure)
from noteb.ipynb import (
    summary_df_6_monthly, summary_df_6_annual, 
    summary_df_25_monthly, summary_df_25_annual,
    summary_df_100_monthly, summary_df_100_annual
)

# Dictionary of summary tables to test
summary_tables = {
    "6 Portfolios Monthly": summary_df_6_monthly,
    "6 Portfolios Annual": summary_df_6_annual,
    "25 Portfolios Monthly": summary_df_25_monthly,
    "25 Portfolios Annual": summary_df_25_annual,
    "100 Portfolios Monthly": summary_df_100_monthly,
    "100 Portfolios Annual": summary_df_100_annual
}

@pytest.mark.parametrize("table_name, df", summary_tables.items())
def test_summary_table_exists(table_name, df):
    """Test that each summary DataFrame is loaded and not empty."""
    assert isinstance(df, pd.DataFrame), f"{table_name} is not a DataFrame"
    assert not df.empty, f"{table_name} is empty"

@pytest.mark.parametrize("table_name, df", summary_tables.items())
def test_summary_table_structure(table_name, df):
    """Test that each summary DataFrame contains expected columns."""
    expected_columns = ["R2 In-Sample", "R2 Out-of-Sample"]
    missing_columns = [col for col in expected_columns if col not in df.columns]
    assert not missing_columns, f"{table_name} is missing columns: {missing_columns}"

@pytest.mark.parametrize("table_name, df", summary_tables.items())
def test_summary_table_expected_rows(table_name, df):
    """Check that expected portfolio categories exist in each summary DataFrame index."""
    expected_indices = [table_name.replace(" ", "-")]
    missing_rows = [idx for idx in expected_indices if idx not in df.index]
    assert not missing_rows, f"{table_name} is missing expected rows: {missing_rows}"

if __name__ == "__main__":
    pytest.main()
