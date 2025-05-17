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
