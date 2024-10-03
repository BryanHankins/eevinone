from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# Set up Selenium WebDriver (Chrome in this example)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode (no browser UI)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Path to your ChromeDriver (make sure to replace with your actual path)
service = Service("/path/to/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape events from Eventbrite using Selenium
def scrape_eventbrite():
    url = "https://www.eventbrite.com/d/in--evansville/all-events/"
    driver.get(url)
    time.sleep(3)  # Wait for the page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    events = []
    for event in soup.find_all("div", class_="eds-event-card-content__primary-content"):
        event_name = event.find("div", class_="eds-event-card-content__title").text.strip()
        event_date = event.find("div", class_="eds-event-card-content__sub-title").text.strip()
        events.append({
            "name": event_name,
            "date": event_date,
            "source": "Eventbrite"
        })

    return events

# Function to scrape events from Downtown Evansville using Selenium
def scrape_downtown_evansville():
    url = "https://www.downtownevansville.com/calendar.php?view=month&month=09&day=01&year=2024"
    driver.get(url)
    time.sleep(3)  # Wait for the page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    events = []
    for event in soup.find_all("div", class_="vevent"):
        event_name = event.find("a", class_="summary").text.strip()
        event_date = event.find("span", class_="dtstart").text.strip()
        events.append({
            "name": event_name,
            "date": event_date,
            "source": "Downtown Evansville"
        })

    return events

# Function to scrape events from Explore Evansville using Selenium
def scrape_exploreevansville_detailed():
    url = "https://www.exploreevansville.com/events/"
    driver.get(url)
    time.sleep(3)  # Wait for the page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    events = []
    for event in soup.find_all('div', {'data-type': 'events'}):
        # Event Title
        title_tag = event.find('div', class_='top-info')
        title = title_tag.find('h4').text.strip() if title_tag and title_tag.find('h4') else 'No Title'

        # Event URL
        event_url_tag = title_tag.find('a') if title_tag else None
        event_url = event_url_tag.get('data-uw-original-href', '#') if event_url_tag else '#'

        # Event Image URL
        image_tag = event.find('div', class_='image')
        image_url = image_tag.find('img')['src'] if image_tag and image_tag.find('img') else 'No Image'

        # Event Date (Month and Day)
        date_container = event.find('span', class_='mini-date-container')
        if date_container:
            month = date_container.find('span', class_='month').text.strip() if date_container.find('span', 'month') else 'No Month'
            day = date_container.find('span', 'day').text.strip() if date_container.find('span', 'day') else 'No Day'
            date = f"{month} {day}"
        else:
            date = 'No Date'

        # Event Location
        location_tag = event.find('li', class_='locations')
        location = location_tag.text.strip() if location_tag else 'No Location'

        # Add the event details to the list
        events.append({
            'name': title,
            'url': event_url,
            'image_url': image_url,
            'date': date,
            'location': location,
            'source': 'Explore Evansville'
        })

    return events

# Function to aggregate events from all sources
def get_all_events():
    eventbrite_events = scrape_eventbrite()
    downtown_evansville_events = scrape_downtown_evansville()
    exploreevansville_detailed_events = scrape_exploreevansville_detailed()

    # Combine all events into one list
    all_events = eventbrite_events + downtown_evansville_events + exploreevansville_detailed_events

    return all_events

# Function to generate and write events to an HTML file
def generate_html(events):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Events in Evansville</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .event { margin-bottom: 20px; }
            .event h2 { margin: 0; font-size: 1.5em; }
            .event p { margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Events in Evansville</h1>
    '''

    # Adding each event to the HTML structure
    for event in events:
        html_content += f'''
        <div class="event">
            <h2>{event['name']}</h2>
            <p>Date: {event['date']}</p>
            <p>Location: {event.get('location', 'N/A')}</p>
            <p>Source: {event['source']}</p>
            <a href="{event.get('url', '#')}" target="_blank">Event Link</a>
            <img src="{event.get('image_url', '')}" alt="{event['name']}" width="200">
        </div>
        '''

    # Closing HTML tags
    html_content += '''
    </body>
    </html>
    '''

    # Write HTML to file
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)  # Create the templates directory if it doesn't exist

    with open(os.path.join(templates_dir, "events.html"), "w") as file:
        file.write(html_content)

# Main execution
if __name__ == "__main__":
    events = get_all_events()
    generate_html(events)  # Generate the HTML file with the scraped events

# Clean up and close the driver
driver.quit()
