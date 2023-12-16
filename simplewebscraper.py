from bs4 import BeautifulSoup
import requests
import csv
import time
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Function to scrape quotes
def scrape_quotes(page_url):
    page_to_scrape = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    quotes = soup.findAll("span", attrs={"class":"text"})
    authors = soup.findAll("small", attrs={"class":"author"})

    scraped_data = []
    for quote, author in zip(quotes, authors):
        scraped_data.append([quote.text, author.text])
    
    return scraped_data

def main(url, pages_to_scrape):
    all_quotes = []
    for i in range(1, pages_to_scrape + 1):
        logging.info(f"Scraping page {i}")
        full_url = url + "/page/" + str(i)
        quotes_on_page = scrape_quotes(full_url)
        all_quotes.extend(quotes_on_page)
        time.sleep(1)  # Sleep for 1 second between page requests

    # Writing to CSV
    with open("scraped_quotes.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["QUOTES", "AUTHORS"])
        for quote in all_quotes:
            writer.writerow(quote)

# Calling the main function with URL and number of pages to scrape
main("http://quotes.toscrape.com", 10)
