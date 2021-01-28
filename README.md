# portfolio-explorer
This application:
- Aggregates investment portfolios 
- Expands the holdings of mutual funds and ETFs.

## Portfolio Consolidation

The [portfolio-consolidator.ipynb notebook](portfolio-consolidator.ipynb) consolidates downloaded portfolios from different financial institutes into one table in the following format and save it to [proc folder](proc).

|symbol|institute|account|shares|price|
|------|---------|--------------|------|-----|
|AAPL|ETrade|Regular Account|1|143.41|
|AMZN|ETrade|Retirement Account|1|3294.6557|
|FB|Fidelity|Retirement|3|276.3495|
|...|

## Portfolio Explorer

The [portfolio-holding-explorer.ipynb notebook](portfolio-holding-explorer.ipynb) uses the consolidated portfolio talbe and expands the holdings in the Mutral Funds and ETFs (using top 10 holding data from yahoo financial) and produces results:

|symbol|institute|account|source|percentage|shares|price|total|
|------|---------|-------|------|---------:|-----:|----:|----:|
|AAPL|ETrade|Regular Account|VGT|20.7|||12.06|
|AAPL|ETrade|Retirement Account|SPY|6.68|||32.720533|
|AAPL|Fidelity|Retirement|IVV|6.68|||6.0768|
|AAPL|Fidelity|Retirement|FBGKX|8.72|||7.37123|
|AAPL|ETrade|Regular Account|AAPL|100|1|143.41|143.41|
|ADBE|ETrade|Retirement|QQQ|1.98|||40.359804|
|ADBE|ETrade|Retirement|VGT|2.33|||7.8792886|
|ADBE|ETrade|Regular Account|SPHQ|2.76|||9.2627668|
|ADBE|Fidelity|Retirement|FGDKX|2.93|||7.14653619|
|AMZN|ETrade|Retirement|SPY|4.37|||30.966736|
|...|



