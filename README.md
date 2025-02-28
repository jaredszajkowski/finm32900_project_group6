FINM 32900 Project Group 6: Market Expectations in the Cross-Section of Present Values
=============================================

## Project Description

This paper demonstrates that returns and cash flows for the aggregate US stock market are highly predictable. It demonstrates this by constructing a univariate predictor from the cross section of stocks. See the abstract:

> "Returns and cash flow growth for the aggregate U.S. stock market are highly and robustly predictable. Using a single factor extracted from the cross-section of book-to market ratios, we find an out-of-sample return forecasting R2 of 13% at the annual frequency (0.9% monthly). We document similar out-of-sample predictability for returns on value, size, momentum, and industry portfolios. We present a model linking aggregate market expectations to disaggregated valuation ratios in a latent factor system. Spreads in value portfolios’ exposures to economic shocks are key to identifying predictability and are consistent with duration-based theories of the value premium."

Also, from their paper,

> “Our approach attacks a challenging problem in empirical asset pricing: how does one exploit a wealth of predictors in relatively short time series? If the predictors number near or more than the number of observations, the standard ordinary least squares (OLS) forecaster will be poorly behaved or nonexistent (see Huber (1973)). Our solution is to use partial least squares (PLS; Wold (1975)), which is a simple regression-based procedure designed to parsimoniously forecast a single time series using a large panel of predictors. We use it to construct a univariate forecaster for market returns (or dividend growth) that is a linear combination of assets’ valuation ratios.”

### Project Specific Details

* Task: Replicate Table 1
* Data sources: CRSP and Compustat
* Citation: KELLY, B. and PRUITT, S. (2013), Market Expectations in the Cross-Section of Present Values. THE JOURNAL OF FINANCE, 68: 1721-1756. https://doi.org/10.1111/jofi.12060

## Project Tasks

### Project Set Up Tasks

* Develop python package requirements for requirements.txt file
* Develop .env file
* Develop dodo.py file

### Replication Tasks

* Write functions to:
  - Pull 6 Fama-French portfolios
  - Pull 25 Fama-French portfolios
  - Pull 100 Fama-French portfolios
  - Pull CRSP
  - Pull Compustat
  - Load data
  - Process/clean raw data and format to be able to run regressions
  - Split data set into train/test
  - Run PLS regressions (3 stages)
* Match table 1 results using data up to 2011
* Pull data through latest available (end of 2024?) and re-run all portfolios/regressions/etc.
* Provide summary statistics and charts that gives context to underlying data and results
* Compare results from the paper vs results using current data

### Output Tasks

* Generate LaTeX document
* Generate jupytger notebook
* Develop unit tests
  - Confirm data is pulled correctly/exists
  - Confirm table 1 matches results