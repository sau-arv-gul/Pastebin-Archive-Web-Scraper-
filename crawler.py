import os
import time
import json
import random
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv


ARCHIVE_URL = "https://pastebin.com/archive"
RAW_URL_TEMPLATE = "https://pastebin.com/raw/{}"
KEYWORDS = ["crypto", "bitcoin", "ethereum", "blockchain", "t.me"]
OUTPUT_FILE = "keyword_matches.jsonl"
HEADERS = {"User-Agent": "Mozilla/5.0"}


# Proxy from the WEBSHARE : https://dashboard.webshare.io/proxy/list

# Load proxies from .env
load_dotenv()
proxies = [
    os.getenv("PROXY_1"),
    os.getenv("PROXY_2"),
    os.getenv("PROXY_3"),
    os.getenv("PROXY_4"),
    os.getenv("PROXY_5"),
]


# Remove any None values (in case any env var is missing)
proxies = [p for p in proxies if p]

# Function to get a random proxy
def get_random_proxy(proxies):
    return random.choice(proxies)



# =================================================================================================================
# Getting the Paste IDs from Pastes Archive
def get_recent_paste_id(archive_url, proxies, max_retries=5):
    """
    Scrape the Pastebin archive page using rotating proxies to extract recent paste IDs.

    This function tries to send a GET request to the Pastebin archive page using a randomly selected proxy.
    If a request fails due to connection issues, timeouts, or any other network-related error, it retries
    using a different proxy, up to a specified maximum number of attempts.


    Parameters:
    ----------
          archive_url : str
                The URL of the Pastebin archive page ("https://pastebin.com/archive").

          proxies : list of str
                A list of proxy server URLs that the function will rotate through
                for making requests to avoid rate-limiting or blocking by Pastebin.

          max_retries : int, optional (default=5)
                The maximum number of retry attempts the function should make using different proxies
                if previous attempts fail.

    Returns:
    -------
    paste_ids : list of str
        A list of Pastebin paste IDs (8-character strings) extracted from the archive page.
        If all proxy attempts fail or no paste IDs are found, an empty list is returned.


    """
    # make a request using a proxy with retries
    for _ in range(max_retries):

        proxy = get_random_proxy(proxies)

        try:
            response = requests.get(archive_url,headers=HEADERS, proxies={"http": proxy, "https": proxy})

            if response.status_code == 200:
                print(f"Request successful with proxy: {proxy}")
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                paste_links = soup.select("td a[href^='/']")

                paste_ids = []  # to store the paste_id
                for link in paste_links:
                    href = link.get('href')
                    if href and len(href.strip('/')) == 8:
                        paste_ids.append(href.strip('/'))

                return paste_ids
            else:
                print(f"Request failed with proxy: {proxy}")
        except requests.exceptions.RequestException as e:
            print(f"Error with proxy: {proxy}, Error: {e}")
    print("All proxies failed")
    return []


paste_ids = get_recent_paste_id(ARCHIVE_URL,proxies)

print(f"Found {len(paste_ids)} paste IDs:\n")

# Print each paste ID with serial number
for idx, pid in enumerate(paste_ids, 1):
    print(f"{idx}. {pid}")



# =============================================================================================================


def raw_content(paste_id, proxies, max_retries=5):
    """
    Fetches the raw content of a Pastebin paste given its ID using proxy rotation and retries.

    Parameters:
    ----------
          paste_id : str
                  The unique 8-character ID of the Pastebin paste.

          proxies : list of str
                  List of HTTPS proxies to use for making the request. A proxy will be randomly selected for each attempt.

          max_retries : int, optional (default=5)
                  The maximum number of retries to attempt using different proxies if the request fails.

    Returns:
    -------
    str or None
        The raw text content of the paste if the request is successful, else None.
    """
    raw_url = RAW_URL_TEMPLATE.format(paste_id)

    for attempt in range(max_retries):
        proxy = get_random_proxy(proxies)
        try:
            response = requests.get(raw_url, headers=HEADERS, proxies={"http": proxy, "https": proxy}, timeout=10)
            response.raise_for_status()

            print(f"[INFO] Successfully fetched Content of paste id:  {paste_id} using proxy {proxy}")

            time.sleep(1)  # Respectful delay to avoid getting blocked
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[WARNING] Attempt {attempt+1}: Failed to fetch {paste_id},  using proxy {proxy} - {e}")
            continue

    print(f"[ERROR] All proxy attempts failed for paste {paste_id}")
    return None

# check the raw contenct of a sepecific paste_id
print(raw_content(paste_ids[48], proxies, max_retries=5))




# ========================================================================================================================

def search_keywords(content):
    """
    Returns a list of found keywords in the paste content.
    """
    found = [kw for kw in KEYWORDS if kw.lower() in content.lower()]
    return found

def SAVE_MATCH(paste_id, keywords_found):
    """Saves the matched paste details to a JSONL file."""

    # Decide context based on keywords
    if "t.me" in keywords_found and all(kw not in keywords_found for kw in ["crypto", "bitcoin", "ethereum", "blockchain"]):
        context_type = "telegram-related"
    else:
        context_type = "crypto-related"

    match_data = {
        "source": "pastebin",
        "context": f"Found {context_type} content in Pastebin paste ID {paste_id}",
        "paste_id": paste_id,
        "url": RAW_URL_TEMPLATE.format(paste_id),
        "discovered_at": datetime.utcnow().isoformat() + "Z",
        "keywords_found": keywords_found,
        "status": "pending"
    }

    with open(OUTPUT_FILE, "a") as f:
        json.dump(match_data, f)
        f.write("\n")


log_path = "crawler.log"  # working directory
logging.basicConfig(
    filename=log_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==========================================================================================================================


# ========================== Looping Through all Paste IDs and Fetching its content and saving the match ====================


t1 = time.time()

for i, paste_id in enumerate(paste_ids, 1):

    print(f"({i}/{len(paste_ids)}) Checking paste ID: {paste_id}")

    content = raw_content(paste_id, proxies, max_retries=5)

    if content:
        keywords_found = search_keywords(content)

        if keywords_found:
            SAVE_MATCH(paste_id, keywords_found) # Save the match to a jsonl file

            logging.info(f"Paste ID {paste_id} - MATCH - Keywords: {keywords_found}")
            print(f"  [MATCH] Keywords found: {keywords_found}")
        else:
            logging.info(f"Paste ID {paste_id} - SKIP - No relevant keywords")
            print("  [SKIP] No relevant keywords found.")
    else:
        logging.warning(f"Paste ID {paste_id} - FAILED to fetch content.")

    time.sleep(1.2)   # Simple rate limit to avoid getting blocked


t2 = time.time()

print("Total Time taken to scrape the content and saving it: ",(t2-t1)/60, "Minutes")

logging.info(f"Total Time taken to scrape the content and saving it: {(t2 - t1) / 60:.2f} Minutes")
