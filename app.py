from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Create Selenium WebDriver
def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    service = Service("chromedriver/chromedriver.exe")  # Adjust to your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Scrape events from Downtown Evansville
def scrape_downtown_evansville():
    logging.info("Scraping Downtown Evansville...")
    driver = create_webdriver()
    try:
        driver.get("https://www.downtownevansville.com/calendar.php?view=month&month=09&day=01&year=2024")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fc-event-container")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = []
        for event in soup.find_all("td", class_="fc-event-container"):
            event_name = event.find("a", class_="fc-day-grid-event").text.strip()
            event_time = event.find("a", class_="fc-time").text.strip() if event.find("a", class_="fc-time") else "N/A"
            events.append({
                "name": event_name,
                "time": event_time,
                "source": "Downtown Evansville"
            })
        return events
    except Exception as e:
        logging.error(f"Error scraping Downtown Evansville: {e}")
        return []
    finally:
        driver.quit()

# Scrape events from Explore Evansville
def scrape_exploreevansville():
    logging.info("Scraping Explore Evansville...")
    driver = create_webdriver()
    try:
        driver.get("https://www.exploreevansville.com/events/?bounds=false&view=list&sort=date")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "info")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = []
        for event in soup.find_all('div', {'data-type': 'events'}):
            title_tag = event.find('div', class_='info')
            title = title_tag.find('h4').text.strip() if title_tag and title_tag.find('h4') else 'No Title'
            event_url_tag = title_tag.find('a') if title_tag else None
            event_url = event_url_tag['href'] if event_url_tag else '#'
            image_tag = event.find('div', class_='image')
            image_url = image_tag.find('img')['src'] if image_tag and image_tag.find('img') else 'No Image'
            events.append({
                'name': title,
                'url': event_url,
                'image_url': image_url,
                'source': 'Explore Evansville'
            })
        return events
    except Exception as e:
        logging.error(f"Error scraping Explore Evansville: {e}")
        return []
    finally:
        driver.quit()

# Aggregate events from both sources
def get_all_events():
    logging.info("Aggregating events from both sources...")
    downtown_evansville_events = scrape_downtown_evansville()
    explore_evansville_events = scrape_exploreevansville()
    
    all_events = downtown_evansville_events + explore_evansville_events
    logging.info(f"Total events aggregated: {len(all_events)}")
    
    return all_events

# Route to display events
@app.route('/')
def index():
    events = get_all_events()  # Get all the events dynamically
    return render_template('events.html', events=events)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
