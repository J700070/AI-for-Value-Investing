import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the two tables on the page
    tables = soup.find_all("table", {"class": "wikitable"})

    # Scrape the data from each table and store it in a DataFrame
    dataframes = []
    counter = 0
    for table in tables:
        counter += 1
        table_data = []
        headers = []

        # Extract table headers
        if counter == 1:
            for th in table.find_all("th"):
                headers.append(th.text.strip())
        else:
            # Use custom headers for the second table
            headers = ["Date", "Added Ticker", "Added Security", "Removed Ticker", "Removed Security", "Reason"]

        # Extract table data
        for row in table.find_all("tr")[1:]:
            row_data = []
            for td in row.find_all("td"):
                row_data.append(td.text.strip())
            table_data.append(row_data)

        # Create a DataFrame and add it to the list of DataFrames
        print(f"Scraped {len(table_data)} rows from a table."
                f" Table headers: {headers}")
        

        dataframes.append(pd.DataFrame(table_data, columns=headers))

    # Save the scraped DataFrames as CSV files
    for i, dataframe in enumerate(dataframes):
        if i == 0:
            dataframe.to_csv("Data/Indexes/scraped_sp500_tickers.csv", index=False)
        else:
            dataframe.to_csv("Data/Indexes/scraped_changes_to_SP500.csv", index=False)

    print("Tables successfully scraped and saved as CSV files.")
else:
    print("Failed to fetch the page. Check the URL and your internet connection.")
