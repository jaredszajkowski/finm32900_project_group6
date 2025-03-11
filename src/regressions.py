import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from load_data import load_crsp_index, load_ken_french, load_and_compute_excess_returns
import matplotlib.pyplot as plt
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "../reports/plots/")  # ✅ Correct relative path
os.makedirs(save_path, exist_ok=True)

# DATA_DIR = config("DATA_DIR")
# START_DATE = config("START_DATE")
# END_DATE = config("END_DATE")

def first_stage_regressions(v_df, y_series, h=1):
    """
    For each portfolio (each column in v_df), regress the valuation ratio at time t 
    on the future excess market return y_{t+h} to estimate the sensitivity (phi).
    Returns a dictionary of slope coefficients (phi_i) for each portfolio.
    """
    phi_dict = {}
    for col in v_df.columns:
        # Convert the column to numeric
        v_i = pd.to_numeric(v_df[col], errors='coerce').dropna()
        if v_i.empty:
            continue
        # Align with future excess returns: y_{t+h}
        y_shifted = y_series.shift(-h).loc[v_i.index]
        # Only keep dates where both v_i and y_shifted are available
        valid = v_i.index.intersection(y_shifted.dropna().index)
        if len(valid) < 10:
            continue  # Skip if too few observations
        v_i = v_i.loc[valid]
        y_i = y_shifted.loc[valid]
        X = sm.add_constant(y_i)
        try:
            model = sm.OLS(v_i, X).fit()
            # Use positional indexing to get the slope coefficient (position 1)
            phi_dict[col] = model.params.iloc[1]
        except Exception as e:
            print(f"Error in first stage for column {col}: {e}")
    return phi_dict

def second_stage_regressions(v_df, phi_dict):
    """
    For each time t, run a cross-sectional regression of the observed portfolio valuation ratios 
    (v_{i,t}) on the estimated loadings (phi_i). We build a DataFrame for the independent 
    variable so that the regression returns a Series with named coefficients.
    The coefficient on the loadings (named 'phi') is taken as the latent factor F_t.
    """
    F_list = []
    dates = []
    valid_cols = list(phi_dict.keys())
    # Build a DataFrame for the loadings with a constant column.
    X_df = pd.DataFrame({
        'const': 1,
        'phi': [phi_dict[col] for col in valid_cols]
    }, index=valid_cols)
    
    for t, row in v_df[valid_cols].iterrows():
        try:
            # Create a Series for the dependent variable with index matching valid_cols.
            Y = pd.Series(row.values.astype(float), index=valid_cols)
        except Exception as e:
            print(f"Error converting row at time {t} to float: {e}")
            continue
        try:
            model = sm.OLS(Y, X_df).fit()
            # Retrieve the coefficient on 'phi'
            F_t = model.params['phi']
            F_list.append(F_t)
            dates.append(t)
        except Exception as e:
            print(f"Error in second stage regression at time {t}: {e}")
    F_series = pd.Series(F_list, index=dates)
    return F_series

def third_stage_regression(F_series, y_series, h=1):
    """
    Regress the future excess market return (y_{t+h}) on the estimated latent factor F_t.
    The latent factor is renamed to 'F' so that the regression DataFrame has clear column names.
    Returns the OLS regression result.
    """
    y_future = y_series.shift(-h)
    common_dates = F_series.index.intersection(y_future.dropna().index)
    # Rename the latent factor series to 'F'
    F_aligned = F_series.loc[common_dates].astype(float).rename("F")
    y_aligned = y_future.loc[common_dates].astype(float)
    X = sm.add_constant(F_aligned)
    model = sm.OLS(y_aligned, X).fit()
    return model

def run_in_sample_pls(dataset_name, weighting="value-weighted", h=1, end_date=None):
    """
    Runs the in-sample three-stage PLS procedure:
      1. Loads and aligns excess market returns (market return minus TB3MS) and Ken French portfolio data.
      2. Computes first-stage loadings for each portfolio.
      3. Extracts the latent factor F_t via cross-sectional regressions.
      4. Runs the predictive regression of excess return y_{t+h} on F_t.
    
    Returns a dictionary with intermediate results.
    """
    # Compute excess returns
    y_excess = load_and_compute_excess_returns()
    
    # Load Ken French portfolio data
    ken_df = load_ken_french(dataset_name, weighting)
    if "Date" in ken_df.columns:
        ken_df["Date"] = pd.to_datetime(ken_df["Date"])
        ken_df = ken_df.set_index("Date")
    v_df = ken_df.apply(pd.to_numeric, errors='coerce')
    
    # Align datasets by common dates
    common_dates = v_df.index.intersection(y_excess.index)
    if common_dates.empty:
        raise ValueError("No common dates found between Ken French data and excess returns.")
    v_df = v_df.loc[common_dates]
    y_excess = y_excess.loc[common_dates]
    
    print(f"Aligned data from {common_dates.min().date()} to {common_dates.max().date()}")
    print(f"Number of dates: {len(common_dates)}")

    y_excess = y_excess[y_excess.index <= end_date]
    v_df = v_df[v_df.index <= end_date]

    print(f"Date range: {y_excess.index.min().date()} to {y_excess.index.max().date()}")
    print(f"Number of dates: {len(y_excess)}")
    print(f"Date range: {v_df.index.min().date()} to {v_df.index.max().date()}")
    print(f"Number of dates: {len(v_df)}")
    
    # First Stage
    phi_dict = first_stage_regressions(v_df, y_excess, h)
    print("First-Stage Estimated Loadings (phi_i):")
    if not phi_dict:
        print("No valid loadings estimated. Check your valuation ratio data.")
    else:
        for key, value in phi_dict.items():
            print(f"{key}: {value:.4f}")
    print("First stage completed.")
    
    # Second Stage
    F_series = second_stage_regressions(v_df, phi_dict)
    print("\nEstimated Latent Factor (F_t) Sample:")
    print(F_series.head())
    print("Second stage completed.")
    
    # Third Stage
    third_model = third_stage_regression(F_series, y_excess, h)
    print("\nThird-Stage Regression Summary:")

    print(third_model.summary())
    print("Third stage completed.")
    
    return {
        "phi": phi_dict,
        "F_series": F_series,
        "third_model": third_model,
        "v_df": v_df,
        "y_excess": y_excess
    }



def run_recursive_forecast(
    dataset_name, 
    weighting="value-weighted", 
    h=1, 
    start_train_date='1934-02-01', 
    end_train_date='1980-01-01',
    end_forecast_date='2011-01-01'
):
    """
    Implements a recursive (rolling-window) out-of-sample forecasting procedure.
    For each forecast date (after the training period), re-estimates the model using data 
    available up to that point, and generates a forecast for y_{t+h} (excess return).
    
    Returns a dictionary containing forecasted series, actual excess returns, and the out-of-sample R².
    """
    # Compute excess returns
    y_excess = load_and_compute_excess_returns()
    
    ken_df = load_ken_french(dataset_name, weighting)
    if "Date" in ken_df.columns:
        ken_df["Date"] = pd.to_datetime(ken_df["Date"])
        ken_df = ken_df.set_index("Date")
    v_df = ken_df.apply(pd.to_numeric, errors='coerce')
    
    # Sort common dates
    common_dates = v_df.index.intersection(y_excess.index).sort_values()
    v_df = v_df.loc[common_dates]
    y_excess = y_excess.loc[common_dates]

    # if start_train_date is None:
    #     n = len(v_df)
    #     train_end = v_df.index[int(n * 0.6)]
    # else:
    #     train_end = pd.to_datetime(start_train_date)

    v_df = v_df[v_df.index <= end_forecast_date]
    y_excess = y_excess[y_excess.index <= end_forecast_date]

    train_end = pd.to_datetime(end_train_date)

    print(f"Start training date: {start_train_date}")
    print(f"End training date: {train_end}")
    print(f"End forecast date: {end_forecast_date}")
    
    forecast_dates = v_df.loc[train_end:].index
    forecasts = {}
    actuals = {}
    
    for forecast_date in forecast_dates:
        train_idx = v_df.index < forecast_date
        v_train = v_df.loc[train_idx]
        y_train = y_excess.loc[train_idx]
        if len(v_train) < 30:
            continue
        phi_dict = first_stage_regressions(v_train, y_train, h)
        if not phi_dict:
            continue
        F_train = second_stage_regressions(v_train, phi_dict)
        if F_train.empty:
            continue
        F_forecast = F_train.iloc[-1]
        third_model = third_stage_regression(F_train, y_train, h)
        # Use the named coefficients from third_model (coefficient on F is named 'F')
        forecast_value = third_model.params['const'] + third_model.params['F'] * F_forecast
        forecasts[forecast_date] = forecast_value
        if forecast_date in y_excess.index:
            actuals[forecast_date] = y_excess.loc[forecast_date]
    
    forecast_series = pd.Series(forecasts)
    actual_series = pd.Series(actuals)
    common = forecast_series.index.intersection(actual_series.index)
    forecast_series = forecast_series.loc[common]
    actual_series = actual_series.loc[common]
    
    mean_y = y_excess.mean()
    ss_res = np.sum((actual_series - forecast_series) ** 2)
    ss_tot = np.sum((actual_series - mean_y) ** 2)
    R2_oos = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
    
    return {
        "forecast_series": forecast_series,
        "actual_series": actual_series,
        "R2_oos": R2_oos
    }

def display_results(dataset_label, in_sample_results, recursive_results):
    """
    Displays the in-sample regression summary, out-of-sample R²,
    and plots the actual vs. forecasted excess market returns.
    """
    print(f"\n{'='*40}\nResults for {dataset_label} Portfolio Data\n{'='*40}")
    print("\nThird-Stage In-Sample Regression Summary:")
    print(in_sample_results["third_model"].summary())
    print(f"\nOut-of-Sample Predictive R²: {recursive_results['R2_oos']:.4f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(recursive_results["actual_series"], label="Actual Excess Market Return")
    plt.plot(recursive_results["forecast_series"], label="Forecasted Excess Market Return", linestyle="--")
    plt.title(f"Out-of-Sample Forecasts for {dataset_label} Portfolio Data")
    plt.xlabel("Date")
    plt.ylabel("Excess Market Return")
    plt.legend()
    dataset_label_clean = dataset_label.replace(" ", "_").replace("-", "_")
    filename = f"Out_of_Sample_Forecasts_for_{dataset_label_clean}_Portfolio_Data.png"
    plt.savefig(os.path.join(save_path, filename), dpi=300, bbox_inches='tight')
    plt.show()
