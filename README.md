# Web Scraping with Python

## Documentation for Web Scraping
- **Web Scraping** is the process of using bots to extract content and data from a website.


- Unlike screen scraping, which only copies pixels displayed onscreen, web scraping extracts underlying HTML code and, with it, data stored in a database. The scraper can then replicate entire website content elsewhere.


- Web scraping is used in a variety of digital businesses that rely on *data harvesting*. Legitimate use cases include:

    - Search engine bots crawling a site, **analyzing its content and then ranking it**.
    
    - Price comparison sites deploying bots to **auto-fetch prices and product descriptions for allied seller websites**.
    
    - Market research companies using scrapers to **pull data from forums and social media (e.g., for sentiment analysis)**.
    
    
- Web scraping is also used for *illegal purposes*, including the undercutting of prices and the theft of copyrighted content.


- Web scraping tools are software (i.e., bots) programmed to sift through databases and extract information. A variety of bot types are used, many being fully customizable to:

    1. **Recognize unique HTML site structures**
    
    2. **Extract and transform content**
    
    3. **Store scraped data**
    
    4. **Extract data from APIs**

## Web Scraping Bots 

- Since all scraping bots have the same purpose—*to access site data*—it can be difficult to distinguish between legitimate and malicious bots.
    
    - Legitimate bots are identified with the **organization for which they scrape**. For example, Googlebot identifies itself in its HTTP header as belonging to Google. Malicious bots, conversely, *impersonate legitimate traffic by creating a false HTTP user agent.*
    
    - Legitimate bots abide a **site’s robot.txt file**, which lists those pages a bot is permitted to access and those it cannot. Malicious scrapers, on the other hand, *crawl the website regardless of what the site operator has allowed.*

- A perpetrator, lacking a budget to run substantial server duty, often resorts to using a **botnet—geographically dispersed computers, infected with the same malware and controlled from a central location**. Individual botnet computer owners are unaware of their participation. The combined power of the infected systems enables *large scale scraping of many different websites by the perpetrator*.

![Kano Eitoku - Cypress Trees](https://upload.wikimedia.org/wikipedia/commons/4/47/Kano_Eitoku_-_Cypress_Trees.jpg)
