import requests
from datetime import datetime

# Replace 'YOUR_API_KEY' with your actual Eventbrite API key
API_KEY = 'CBOXSGLEDXHO63SX4I'

def fetch_venue_details(venue_id):
    """
    Fetch the details of a venue using the Eventbrite API.
    """
    venue_url = f'https://www.eventbriteapi.com/v3/venues/{venue_id}/'
    response = requests.get(venue_url, params={'token': API_KEY})
    
    if response.status_code == 200:
        venue = response.json()
        return {
            'name': venue['name'],
            'address': venue['address']['localized_address_display'],
            'latitude': venue['latitude'],
            'longitude': venue['longitude']
        }
    else:
        print(f"Error fetching venue details: {response.status_code}")
        return None

def geteventbriteev(city='Evansville', state='IN'):
    """
    Fetch all events happening today in Evansville, IN using the Eventbrite API.
    """
    # Define the API endpoint for the event search
    url = 'https://www.eventbriteapi.com/v3/events/search/'

    # Query parameters to search for events in Evansville happening today
    params = {
        'location.address': f'{city}, {state}',
        'location.within': '10mi',  # Search within a 10-mile radius of the city
        'start_date.range_start': datetime.now().strftime('%Y-%m-%dT00:00:00Z'),
        'start_date.range_end': datetime.now().strftime('%Y-%m-%dT23:59:59Z'),
        'token': API_KEY  # Your Eventbrite API token
    }

    # Make the request to the Eventbrite API
    response = requests.get(url, params=params)
 
    if response.status_code == 200:
        data = response.json()
        events = []

        # Parse the event data
        for event in data.get('events', []):
            event_name = event['name']['text']
            event_url = event['url']
            start_time = event['start']['local']
            end_time = event['end']['local']
            description = event['description']['text']

            # Fetch venue details using the venue_id
            venue_id = event['venue_id']
            venue_details = fetch_venue_details(venue_id) if venue_id else None
            venue_name = venue_details['name'] if venue_details else 'No Venue'
            venue_address = venue_details['address'] if venue_details else 'No Address'

            events.append({
                'name': event_name,
                'url': event_url,
                'start_time': start_time,
                'end_time': end_time,
                'description': description,
                'venue_name': venue_name,
                'venue_address': venue_address
            })

        return events
    else:
        print(f"Error fetching events: {response.status_code}")
        return []


# Example usage
if __name__ == "__main__":
    events_today = geteventbriteev()

    if events_today:
        print(f"Found {len(events_today)} events happening today in Evansville, IN:")
        for event in events_today:
            print(f"Event Name: {event['name']}")
            print(f"URL: {event['url']}")
            print(f"Start Time: {event['start_time']}")
            print(f"End Time: {event['end_time']}")
            print(f"Description: {event['description']}")
            print(f"Venue Name: {event['venue_name']}")
            print(f"Venue Address: {event['venue_address']}\n")
    else:
        print("No events found for today.")
