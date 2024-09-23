import requests
from bs4 import BeautifulSoup

# Function to scrape events from Eventbrite

print('test')
def scrape_eventbrite():
    url = "https://www.eventbrite.com/d/in--evansville/all-events/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

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
    else:
        return []



# Function to scrape events from Downtown Evansville
def scrape_downtown_evansville():
    url = "https://www.downtownevansville.com/calendar.php?view=month&month=09&day=01&year=2024"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

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
    else:
        return []

def scrape_exploreevansville_detailed():
    url = "https://www.exploreevansville.com/events/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.content, "html.parser")
    events = []

    # Finding all <div> elements with data-type="events" and other attributes
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
            month = date_container.find('span', class_='month').text.strip() if date_container.find('span', class_='month') else 'No Month'
            day = date_container.find('span', class_='day').text.strip() if date_container.find('span', class_='day') else 'No Day'
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
def get_all_events():
    events = scrape_exploreevansville_detailed()
    print("Scraped Events:", events)  # This will print the scraped data in the console
    return events

# allevents scrapping works!!!
# def scrape_allevents_in():
#     url = "https://allevents.in/evansville"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")

#         events = []
#         for event in soup.find_all("li", attrs={"data-link": True}):  # Finding all <li> elements with the data-link attribute
#             event_link = event['data-link']
#             event_title_tag = event.find("h3")
#             event_name = event_title_tag.text.strip() if event_title_tag else "No Title"
#             event_location_tag = event.find("div", class_="subtitle")
#             event_location = event_location_tag.text.strip() if event_location_tag else "No Location"
#             event_date_tag = event.find("div", class_="date")
#             event_date = event_date_tag.text.strip() if event_date_tag else "No Date"

#             events.append({
#                 "name": event_name,
#                 "location": event_location,
#                 "date": event_date,
#                 "url": event_link,
#                 "source": "AllEvents.in"
#             })

#         return events
#     else:
#         return []
    
    

# Function to aggregate events from all sources
def get_all_events():
    eventbrite_events = scrape_eventbrite()
    exploreevansville_detailed_events = scrape_exploreevansville_detailed()

    downtown_evansville_events = scrape_downtown_evansville()
    # allevents_events = scrape_allevents_in()
    exploreevansville_detailed_events = scrape_exploreevansville_detailed()  # New function

    # Combine all events into one list
    all_events = (eventbrite_events + 
                  downtown_evansville_events  +
                  exploreevansville_detailed_events)
    
    # all_events = (eventbrite_events + explore_evansville_events + 
    #               downtown_evansville_events + allevents_events +
    #               exploreevansville_detailed_events)
    return all_events
