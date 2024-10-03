from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time  # For adding delays
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
        time.sleep(3)  # Wait for 3 seconds

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
        time.sleep(3)  # Wait for 3 seconds

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = []
        for event in soup.find_all('div', {'data-type': 'events'}):
            title_tag = event.find('div', class_='info')
            title = title_tag.find('h4').text.strip() if title_tag and title_tag.find('h4') else 'No Title'
            event_url_tag = title_tag.find('a') if title_tag else None
            event_url = event_url_tag['href'] if event_url_tag else '#'
            image_tag = event.find('div', class_='image')
            image_url = image_tag.find('img') if image_tag and image_tag.find('img') else 'No Image'
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

# Scrape EVPL Storytime Events
def scrape_evpl():
    logging.info("Scraping EVPL Storytime Events...")
    driver = create_webdriver()
    url = "https://events.evpl.org/events?t=Storytime&r=today"

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "events-body")))
        time.sleep(3)  # Wait for 3 seconds

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = []

        for event in soup.find_all('div', class_='eelistevent'):
            event_data = event.find('div', class_='eelistevent-data')

            title_tag = event_data.find('div', class_='eelisttitle')
            title = title_tag.find('a').text.strip() if title_tag and title_tag.find('a') else 'No Title'
            event_url = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else '#'
            event_time = event_data.find('div', class_='eelisttime').text.strip() if event_data.find('div', class_='eelisttime') else 'No Time'
            location = event_data.find('div', class_='eelocation').text.strip() if event_data.find('div', class_='eelocation') else 'No Location'
            age_group = event_data.find('div', class_='eelistgroup').text.strip() if event_data.find('div', class_='eelistgroup') else 'No Age Group'
            event_type = event_data.find('div', class_='eelisttags').text.strip() if event_data.find('div', class_='eelisttags') else 'No Event Type'
            description = event_data.find('div', class_='eelistdesc').text.strip() if event_data.find('div', class_='eelistdesc') else 'No Description'

            events.append({
                'name': title,
                'url': event_url,
                'time': event_time,
                'location': location,
                'age_group': age_group,
                'type': event_type,
                'description': description,
                'source': 'EVPL Events'
            })

        return events
    except Exception as e:
        logging.error(f"Error scraping EVPL Events: {e}")
        return []
    finally:
        driver.quit()

# Scrape events from AllEvents.in Evansville
def scrape_allevents_in_evansville():
    logging.info("Scraping AllEvents.in Evansville...")
    driver = create_webdriver()
    url = "https://allevents.in/evansville/all#search"
    
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "event_card")))
        time.sleep(3)  # Wait for 3 seconds

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = []

        # Locate all event cards
        for event in soup.find_all('div', class_='event_card'):
            # Extract the event URL
            event_link_tag = event.find('a', href=True)
            event_url = event_link_tag['href'] if event_link_tag else '#'
            
            # Extract the event name
            event_name_tag = event.find('div', class_='event_name')
            event_name = event_name_tag.text.strip() if event_name_tag else 'No Title'

            # Extract the event image
            event_image_tag = event.find('img', {'data-src': True})
            event_image_url = event_image_tag['data-src'] if event_image_tag else 'No Image'

            # Extract the event date
            event_date_tag = event.find('div', class_='event_date_time')
            event_date = event_date_tag.text.strip() if event_date_tag else 'No Date'

            # Extract the event location
            event_location_tag = event.find_all('div', class_='event_location')
            event_location = ', '.join([loc.text.strip() for loc in event_location_tag]) if event_location_tag else 'No Location'

            # Add the event details to the list
            events.append({
                'name': event_name,
                'url': event_url,
                'image_url': event_image_url,
                'date': event_date,
                'location': event_location,
                'source': 'AllEvents.in Evansville'
            })

        return events
    except Exception as e:
        logging.error(f"Error scraping AllEvents.in Evansville: {e}")
        return []
    finally:
        driver.quit()

# Aggregate events from all sources
def get_all_events():
    logging.info("Aggregating events from all sources...")
    downtown_evansville_events = scrape_downtown_evansville()
    explore_evansville_events = scrape_exploreevansville()
    evpl_events = scrape_evpl()
    allevents_in_evansville = scrape_allevents_in_evansville()

    all_events = downtown_evansville_events + explore_evansville_events + evpl_events + allevents_in_evansville
    logging.info(f"Total events aggregated: {len(all_events)}")

    return all_events

# Flask route to display events
@app.route('/')
def index():
    events = get_all_events()  # Get all the events dynamically
    return render_template('events.html', events=events)

# Clean up WebDriver after each request
@app.teardown_appcontext
def shutdown_driver(exception=None):
    pass  # Driver is already closed in each scraping function

if __name__ == '__main__':
    app.run(debug=True)


