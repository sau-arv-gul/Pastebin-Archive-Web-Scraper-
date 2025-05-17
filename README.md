# 🕵️‍♂️ Pastebin Keyword Crawler
This Python-based crawler scrapes recent public pastes from Pastebin and detects mentions of cryptocurrency-related keywords [ bitcoin, ethereum, blockchain] or [Telegram links (t.me)].
To avoid getting blocked, it uses proxy rotation and adds delays between requests. It also keeps detailed logs of everything it checks.


## 📁 Project Structure
```
├── crawler.py             # Main script
├── .env                   # Environment variables (contains proxy list)
├── crawler.log            # Log file
├── keyword_matches.jsonl  # Output file with matched results
└── README.md              
