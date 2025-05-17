# 🕵️‍♂️ Pastebin Keyword Crawler
This Python-based crawler scrapes recent public pastes from Pastebin and detects mentions of cryptocurrency-related keywords [ bitcoin, ethereum, blockchain] or [Telegram links (t.me)].
To avoid getting blocked, it uses proxy rotation and adds delays between requests.   
It also keeps detailed logs of everything it checks. Whenever it finds a match, it saves all keyword matches in a structured .jsonl format.



## 🌐 Using Free Proxies from Webshare

- This project uses 5 proxy server URLs from Webshare to avoid IP blocking.  
- All proxies are stored in the .env file as environment variables.  
- You can get your own free proxy list here:
https://dashboard.webshare.io/proxy/list

## ✨ Features

- 🔍 Scans Pastebin for recent public pastes
- 🪙 Detects keywords like `bitcoin`, `ethereum`, `blockchain`, and Telegram links
- 🛡️ Uses proxy rotation to avoid IP blocking
- 🐌 Adds delay between requests (rate limiting)
- 📜 Maintains a detailed log (`crawler.log`)
- 🧾 Saves matches in structured `.jsonl` format

---

##  Project Structure
```
├── .env                   # Environment variables (contains proxy list)
├── crawler.log            # Log file
├── requirements.txt       # dependencies
├── crawler.py             # Main script
├── keyword_matches.jsonl  # Output file with matched results
└── README.md              
```



# 🚀 Clone and Run Locally

## 1. Clone the Repository
```bash
git clone https://github.com/sau-arv-gul/Pastebin-Archive-Web-Scraper-.git
cd Pastebin-Archive-Web-Scraper-
```
## 2. Install Dependencies
Install all required dependencies using:
```bash
pip install -r requirements.txt
```

## 3. Run the crawler:
```bash
python crawler.py
```

# 🔍 Proof of Concept (PoC)
This project demonstrates an automated crawler that monitors the Pastebin archive for pastes containing sensitive or targeted keywords like:
- Crypto-related terms: "crypto", "bitcoin", "ethereum", "blockchain", etc.
- Telegram links: "t.me"

## 🛠️ How It Works

1. **Scrape Pastebin Archive**  
    Extract recent Paste IDs from the homepage.  
   Below image shows Archive page being scraped:
   
   ![Image](https://github.com/user-attachments/assets/fd1452a9-e5f9-46e0-bad9-19b2d3d5fa47)

3. **Rotate Proxies**  
    Requests are made using rotating proxies (e.g., from Webshare) to avoid bans or rate limits.  
   We can see below that the scraper fetches content through different proxy servers, which helps  
   distribute the requests evenly and reduces the chance of being blocked.


    
   ![Image](https://github.com/user-attachments/assets/ec2b061e-d62c-490c-a1dd-6b6570e16cd4)

5. **Fetch Raw Content**  
   → Each paste is accessed using its raw content link (`https://pastebin.com/raw/<paste_id>`).

   ![Image](https://github.com/user-attachments/assets/02c964cd-91ec-4723-b1d3-d65c1b7ca102)

7. **Search for Keywords and logging activities**  
      The tool checks each paste for specific keywords (like t.me). If a keyword is found,   
      it logs the result with details like the time, paste ID, and keywords found.   
      The log entries  look like this:
     ![Image](https://github.com/user-attachments/assets/8fc317e9-d528-42de-8f81-f29a0dc36bbf)

9. **Results**  
   → Matches are saved in structured JSONL format (`keyword_matches.jsonl`) for further use.

![Image](https://github.com/user-attachments/assets/55feac93-9157-4f10-b473-289e9d694f25)
