🛠️ About
EevinOne is a Python-based web application that automatically scrapes event information from multiple websites in My town and combines them into a single easy-to-view page.

Born from a real-world need — checking seven separate sites manually — EevinOne was built to save time, stay connected, and simplify finding fun things to do locally.

🚀 Features
🔎 Scrapes event data from multiple websites.

🌐 Aggregates events into one simple web page.

🕒 Helps you stay up-to-date without manually checking different sites.

⚙️ Easy to extend with new sources (modular scraper design).

🛠️ Built With
Python 3.x

Flask — lightweight web server

Selenium — browser automation for dynamic pages

BeautifulSoup — HTML parsing

Requests — fetching static web pages

HTML/CSS — simple web interface


🖥️ How to Run Locally
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/BryanHankins/eevinone.git
cd eevinone
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
(make sure you have chromedriver installed and matched to your Chrome version if you’re using Selenium!)

3. Run the Flask App
bash
Copy
Edit
python app.py

4. View the Site
Open your browser and go to:

arduino
Copy
Edit
http://localhost:5000
📋 Requirements
Python 3.8+

Chrome browser (for Selenium)

Matching version of chromedriver

Internet connection (for scraping live websites)

