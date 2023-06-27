import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# Parameters
search_query = "site:youtube.com openinapp.co"
results_limit = 30

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

# Set up Chrome WebDriver
webdriver_path = "./chromedriver.exe"  # Path to your Chrome WebDriver executable
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Perform the search and collect YouTube links
search_results = []
start_index = 0




while len(search_results) < results_limit:
    # Prepare the search query URL
    params = {
        "q": search_query,
        "start": start_index
    }

    # Construct the Google search URL
    base_url = "https://www.google.com/search?" + "&".join([f"{key}={value}" for key, value in params.items()])
    print(base_url)
    # Load the search results page
    driver.get(base_url)
    time.sleep(2)  # Wait for the page to load

    # Extract the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Find all the search result links
    links = soup.select('.MjjYud a')
    #print(links)
    
    for link in links:
        href = link.get('href')
        #print(href)
        if href.startswith('https://www.youtube.com/watch?'):
            
            youtube_link = href
            driver.get(youtube_link)

            time.sleep(2)

# Locate the element using a CSS selector
            chilledCowElem = driver.find_element_by_css_selector("div.ytd-channel-name a")

# Access the name of the channel and gets its href value
            #print(chilledCowElem.text)
            #print(chilledCowElem.get_attribute("href"))

            
            search_results.append(chilledCowElem.get_attribute("href"))

    # Update the start index for the next page of results
    start_index += 10

    # Break the loop if no more results are found
    #if len(links) == 0:
     #   break

    print(f"Scraped {len(search_results)} YouTube links")

# Close the Chrome WebDriver
driver.quit()

# Store the results in a JSON file
output_file = "youtube_links.json"
with open(output_file, "w") as file:
    json.dump(search_results, file, indent=4)

print(f"\nScraping completed. {len(search_results)} YouTube links were scraped and saved to {output_file}.")
