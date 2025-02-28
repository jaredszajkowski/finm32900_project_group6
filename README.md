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

### Specifics From The Paper

From the paper:

> <blockquote style="text-align: center;">E. Data</blockquote> </br></br>
> &nbsp;&nbsp;Our central empirical analysis examines market return and cash flow growth predictability by applying PLS to different cross-sections of valuation ratios. We use book-to-market ratios for Fama and French’s (1993) size- and value- sorted portfolios (in which U.S. stocks are divided into 6, 25, or 100 portfolios). Data files from Ken French’s website report monthly portfolio-level market equity value and annual portfolio book equity value, which we use to construct a monthly panel of portfolio book-to-market ratios. A book-to-market ratio in month t uses a portfolio’s total market capitalization at the end of month t and the latest observable annual book equity total for the portfolio. We assume that portfolio book equity in calendar year Y becomes observable after June of year Y + 1 following Fama and French (1993).</br>
> &nbsp;&nbsp;We also consider a variety of alternative value ratio panels. First, we explore the usefulness of individual stock-level value ratios data for predicting future market returns. We also consider price-dividend ratios for size- and value- sorted portfolios in place of book-to-market ratios. Finally, we take our analysis to international data, using the country-level portfolio valuation ratios of Fama and French (1998).</br>
> &nbsp;&nbsp;Our focus is on the 1930 to 2010 sample for U.S. data.17 The international sample is available from 1975 to 2010. U.S. market returns and dividend growth are for the CRSP value-weighted index. Individual stock data are from CRSP and Compustat. U.S. and international portfolio data are from Ken French’s website. Alternative predictors are from Amit Goyal’s website.

Then for table 1:

> Table I</br>
> Market Return Predictions (1930 to 2010)</br>
> We report in-sample and out-of-sample percentage R2 for PLS forecasts of 1-year and 1-month market returns from 1930 to 2010. The sets of predictor variables are 6, 25, and 100 book-to- market ratios of size- and value-sorted portfolios. Our out-of-sample procedure splits the sample in
1980, uses the pre-1980 period as a training window, and recursively forecasts returns beginning in January 1980 (results for a wide range of alternative sample splits are shown in Figures 1 and 2). We also report p-values of three different in-sample test statistics. The first is the asymptotic predictive loading t-statistic from Kelly and Pruitt (2012), denoted “KP” in the table. For annual returns, this is calculated on every nonoverlapping set of residuals as described in the text. For annual returns we also report Hodrick (1992) and Newey and West (1987) p-values. For out-of- sample tests we report p-values for Clark and McCracken’s (2001; denoted “CM” in the table) ENC-NEW encompassing test statistic. This tests the null hypothesis of no forecast improvement over the historical mean. For annual returns we follow Clark and McCracken (2005) and use
Newey-West standard errors with 12 lags.

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