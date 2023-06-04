# bounceChallenge

# Runbook:
## Part 1:

1. Grab token from Github by following the instruction here
2. Ensure you have the following libraries installed and ready to be imported

```
import pandas as pd
import requests
```
3. Write your first scraper by adding yourr github_token the class  `scraper = GitHubScraper(user_account='bounceapp', github_token='xxxx_token')`
4. Now you have the scraper class, you can decided to read the extracted data to dataframe before exporting by `df = scraper.scrape_github_data()`
5. Now you are read to export the data `scraper.scrape_and_export('data/github_data.csv')`