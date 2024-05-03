import os
import re
import requests
from lxml import etree
import random
import time
import json

class BidScraper:
    def __init__(self, base_url):
        """
        Initializes the BidScraper with the base URL and initializes cookies.

        Parameters:
        base_url (str): The base URL for scraping bids.
        """
        self.base_url = base_url
        self.cookies = None

    def get_cookies(self, url):
        """
        Fetches cookies from the provided URL.

        Parameters:
        url (str): The URL to fetch cookies from.

        Returns:
        dict: A dictionary containing the cookies.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.cookies = requests.utils.dict_from_cookiejar(response.cookies)
            return self.cookies
        except requests.RequestException as e:
            print(f"Failed to fetch cookies from the page: {e}")
            return None

    def get_dom_from_url(self, url, retries=5):
        """
        Fetches the DOM (Document Object Model) from the provided URL.

        Parameters:
        url (str): The URL to fetch the DOM from.
        retries (int): Number of retry attempts in case of failure.

        Returns:
        lxml.etree._Element: The DOM object.
        """
        for attempt in range(retries):
            try:
                response = requests.get(url, cookies=self.cookies)
                response.raise_for_status()
                if response.status_code == 200:
                    dom = etree.HTML(response.content)
                    return dom
                else:
                    raise requests.HTTPError(f"Received status code: {response.status_code}")
            except (requests.RequestException, etree.ParseError, requests.HTTPError) as e:
                print(f"Error occurred: {e}")
                if attempt < retries - 1:
                    delay = random.randint(1, 5)
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Max retries exceeded. Exiting.")
                    return None

    def get_value_or_none(self, xpath_result):
        """
        Extracts the first element from the XPath result or returns None if the result is empty.

        Parameters:
        xpath_result (list): List containing XPath results.

        Returns:
        str or None: The extracted value or None.
        """
        try:
            return xpath_result[0].strip() if xpath_result else None
        except IndexError:
            return None

    def get_bids_info(self):
        """
        Fetches bid information from the base URL.

        Returns:
        list: A list of dictionaries containing bid information with individual bid page URL.
        """
        try:
            dom = self.get_dom_from_url(self.base_url)
            if dom is None:
                return []
            table_trs = dom.xpath("//tbody[contains(@class,'ui-datatable-data ui-widget-content')]//tr")
            bids_info = []
            for tr in table_trs:
                bid_info = {}
                bid_info['bidSolicitation'] = self.get_value_or_none(tr.xpath("./td[1]/a/text()"))
                bid_info['bidPageUrl'] = "https://nevadaepro.com" + self.get_value_or_none(tr.xpath(".//td[1]/a/@href"))
                bid_info['buyer'] = self.get_value_or_none(tr.xpath(".//td[6]/text()"))
                bid_info['description'] = self.get_value_or_none(tr.xpath(".//td[7]/text()"))
                bid_info['bidOpeningDate'] = self.get_value_or_none(tr.xpath(".//td[8]/text()"))
                bids_info.append(bid_info)
            return bids_info
        except Exception as e:
            print("An error occurred:", e)
            return []

    def get_bid_info(self, url):
        """
        Fetches detailed bid information from the provided bid page URL.

        Parameters:
        url (str): The URL of the bid page.

        Returns:
        dict or None: A dictionary containing bid information or None if unsuccessful.
        """
        try:
            dom = self.get_dom_from_url(url)
            if dom is None:
                raise ValueError("Failed to fetch DOM from URL.")
            else:
                bid_info = {
                    "Bid_Number" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Bid Number')]//following-sibling::td//text()")),
                    "Description" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Description')]//following-sibling::td//text()")),
                    "Bid_Opening_Date" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Bid Opening Date')]//following-sibling::td//text()")),
                    "Purchaser" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Purchaser')]//following-sibling::td//text()")),
                    "Organization" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Organization')]//following-sibling::td//text()")),
                    "Department" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Department')]//following-sibling::td//text()")),
                    "Location" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Location')]//following-sibling::td//text()")),
                    "Fiscal_Year" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Fiscal Year')]//following-sibling::td//text()")),
                    "Allow_Electronic_Quote" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Allow Electronic Quote')]//following-sibling::td//text()")),
                   "Alternate_Id" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Alternate Id')]//following-sibling::td//text()")),
                    "Required_Date" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Required Date')]//following-sibling::td//text()")),
                    "Available_Date" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Available Date')]//following-sibling::td//text()")),
                    "Info_Contact" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Info Contact')]//following-sibling::td//text()")),
                    "Bid_Type" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Bid Type')]//following-sibling::td//text()")),
                    "Informal_Bid_Flag" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Informal Bid Flag')]//following-sibling::td//text()")),
                    "Purchase_Method" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Purchase Method')]//following-sibling::td//text()")),
                    "Pre_Bid_Conference" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Pre Bid Conference')]//following-sibling::td//text()")),
                    "Bulletin_Desc" : self.get_value_or_none(dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'Bulletin Desc')]//following-sibling::td//text()")),
                }
                doc_id = bid_info["Bid_Number"]
                hrefs = dom.xpath("//tr//td[contains(@class,'t-head-01') and contains(.,'File Attachments')]//following-sibling::td//a[@class='link-01']/@href")
                FileNbrs = [re.search(r'\d+', href).group() for href in hrefs if hrefs]
                print(f"*** Downloading Attachments for bid => {doc_id} *****")
                for downloadFileNbr in FileNbrs:
                    self.download_file(url, doc_id, downloadFileNbr)
                print(f"*** Downloading Succesfull for bid => {doc_id}  *****\n\n")
                return bid_info
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def download_file(self, url, docId, downloadFileNbr):
        """
        Downloads a file associated with a bid.

        Parameters:
        url (str): The URL of the bid page.
        docId (str): The ID of the bid document.
        downloadFileNbr (str): The number of the file to download.
        """
        try:
            if not self.cookies:
                self.get_cookies(url)

            csrf_token = self.cookies.get("XSRF-TOKEN")
            if not csrf_token:
                print("CSRF token not found in cookies. Skipping download.")
                return

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://nevadaepro.com',
                'referer': url,
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            }

            data = {
                '_csrf': csrf_token,
                'mode': 'download',
                'bidId': docId,
                'docId': docId,
                'currentPage': '1',
                'querySql': '',
                'downloadFileNbr': downloadFileNbr,
                'itemNbr': 'undefined',
                'parentUrl': 'close',
                'fromQuote': '',
                'destination': '',
            }

            response = requests.post('https://nevadaepro.com/bso/external/bidDetail.sdo', cookies=self.cookies, headers=headers, data=data)

            if response.status_code == 200:
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition:
                    filename_start = content_disposition.find('filename=') + len('filename=')
                    filename_end = content_disposition.find(';', filename_start) if content_disposition.find(';', filename_start) != -1 else None
                    filename = content_disposition[filename_start:filename_end].strip('"') if filename_end else content_disposition[filename_start:].strip('"')
                else:
                    filename = "downloaded_file"

                attachments_dir = f"{docId}"
                if not os.path.exists(attachments_dir):
                    os.makedirs(attachments_dir)

                filepath = os.path.join(attachments_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"File downloaded successfully: {filename} (saved in {attachments_dir} directory)")
            else:
                print("Failed to download the file")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    base_url = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true"
    scraper = BidScraper(base_url)
    bids_info = scraper.get_bids_info()
    all_bids_info = []

    # Iterating over each bid to fetch detailed bid information
    for bid in bids_info:
        bid_info = scraper.get_bid_info(bid['bidPageUrl'])
        if bid_info:
            all_bids_info.append(bid_info)
        else:
            print("Failed to retrieve bid info for:", bid['bidPageUrl'])

    # Writing bid information to a JSON file
    with open('output.json', 'w') as f:
        json.dump(all_bids_info, f, indent=4)
    
    # Printing the output JSON
    print("\n\n******************OUTPUT JSON*****************\n\n\n")
    print(json.dumps(all_bids_info))

    # Indicating successful completion
    print("Data written to output.json")