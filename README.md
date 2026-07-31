# Polish B2B Lead Generation Scraper

> A robust, multi-source Python web scraper designed to extract high-quality business contact data (Company Name, Email, Website) from various Polish business directories and professional chambers.

This project was built to automate the tedious process of lead generation. It is capable of scanning thousands of subpages across completely different HTML structures and APIs, extracting targeted data while bypassing common anti-bot protections.

# Key Features & Technical Highlights

 - **Multi-Source Parsing**: Integrates extraction logic for 6+ completely different website structures (from classic HTML tables to modern Elementor/WordPress blocks).

 - **Advanced Email Decryption:** Successfully bypasses Cloudflare Email Obfuscation (__cf_email__) using custom hexadecimal decoding.

 - andles ROT13 email encryption often used by anti-spam plugins.

 - **Smart Deduplication:** Utilizes Python set() structures O(1) time complexity to ensure zero duplicate emails in the final dataset, significantly reducing processing time and saving memory.

 - **Regex Fallback:** Uses robust Regular Expressions as a fallback mechanism to extract emails buried deep within messy text strings when specific HTML tags are missing.

 - **Anti-Bot Measures:** Implements randomized request delays (time.sleep with random.uniform) and specific User-Agent spoofing to mimic human behavior and avoid 429 Too Many Requests or 403 Forbidden errors.

 - **REST API Interception:** Includes a module that bypasses standard HTML rendering by directly sending POST requests to hidden backend endpoints (SPA architecture) to retrieve raw data payloads.

# Tech Stack

**Language:** Python 3.14

Core Libraries:

 - **requests Handling:** GET/POST requests, HTTP status codes

 - **BeautifulSoup4:** DOM traversal and HTML parsing

 - **re:** Regular Expressions for pattern matching

 - **csv:** Data formatting and export

 - **codecs:** String encoding/decoding

# Output

The script automatically generates a clean, standardized dane_firm.csv file encoded in UTF-8-SIG (for perfect Polish character rendering in MS Excel) with three main columns:
[Company Name] | [Email Address] | [Website URL]