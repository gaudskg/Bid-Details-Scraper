# Bid-Details-Scraper
This Python script is designed to scrape bid details from the NevadaEPro website. It fetches bid information from a base URL and then retrieves detailed bid information from individual bid pages. Additionally, it downloads attachments associated with each bid.


## Overview

The script is organized into a `BidScraper` class, which encapsulates methods for fetching bid information and downloading bid attachments. Here's a brief overview of the script's functionality:

### Initialization

The `BidScraper` class is initialized with a base URL, which serves as the starting point for scraping bid details.

### Cookie Management

The `get_cookies` method retrieves cookies from a given URL. These cookies are later used for authentication when downloading bid attachments.

### DOM Retrieval

The `get_dom_from_url` method fetches the Document Object Model (DOM) from a provided URL. It retries a specified number of times in case of failure.

### XPath Parsing

The `get_value_or_none` method extracts text content from XPath results. It returns the first element or `None` if the result is empty.

### Fetching Bid Information

The `get_bids_info` method scrapes bid information from the base URL. It extracts details such as bid solicitation, buyer, description, and bid opening date.

### Fetching Detailed Bid Information

The `get_bid_info` method retrieves detailed information for a specific bid from its page URL. It extracts various attributes like bid number, description, purchaser, organization, etc. It also downloads any associated attachments.

### Downloading Attachments

The `download_file` method downloads attachments associated with a bid. It handles CSRF token generation, HTTP headers, and saves the files to the appropriate directory.

### Main Functionality

The script's main function orchestrates the scraping process. It fetches bid information, iterates over each bid to retrieve detailed information, and writes the collected data to a JSON file (`output.json`).

### Output

Upon completion, the script generates an `output.json` file containing detailed bid information in JSON format. Additionally, it prints the output JSON to the console.

Overall, this script provides a robust solution for scraping bid details from the NevadaEPro website, facilitating data collection and analysis for procurement purposes.


## Getting Started

To get started with using this bid details scraper, follow these steps:

1. Clone or download the repository from [GitHub](https://github.com/gaudskg/Bid-Details-Scraper).
     ```
     git clone https://github.com/gaudskg/Bid-Details-Scraper
     ```

2. Navigate to the project directory in your terminal.
     ```
     cd Bid-Details-Scraper
     ```

3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
   
4. Run the script using Python:
   ```
   python bid_details_scraper.py
    or
   python3 bid_details_scraper.py
   ```
   
5. The script will start scraping bid details from the specified URL and downloading attachments associated with each bid.
6. Once the scraping is complete, the script will generate an output.json file containing the bid information.
7. You can find the output JSON file in the project directory.
8. Additionally, the script will print the output JSON to the console.

By following these steps, you can quickly start scraping bid details from the NevadaEPro website using this script.

