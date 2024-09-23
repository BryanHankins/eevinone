from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

API_KEY = 'your_eventbrite_api_key_here'  # Replace with your Eventbrite API Key

def geteventbriteev(city='Evansville', state='IN'):
    url = 'https://www.eventbriteapi.com/v3/events/search/'
    params = {
        'location.address': f'{city}, {state}',
        'location.within': '10mi',
        'start_date.range_start': datetime.now().strftime('%Y-%m-%dT00:00:00Z'),
        'start_date.range_end': datetime.now().strftime('%Y-%m-%dT23:59:59Z'),
        'token': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        events = []
        for event in data.get('events', []):
            event_name = event['name']['text']
            event_url = event['url']
            start_time = event['start']['local']
            venue_id = event['venue_id']
            # Fetch venue details (mocked here)
            venue_name = 'Sample Venue'  # Replace with actual venue fetch logic
            venue_address = 'Sample Address'  # Replace with actual venue fetch logic
            image_url = event['logo']['url'] if event.get('logo') else 'default_image.jpg'
            events.append({
                'name': event_name,
                'url': event_url,
                'date': start_time,
                'location': venue_name + ', ' + venue_address,
                'image_url': image_url,
                'recurrence': 'One-time Event'  # Event recurrence data can be added if needed
            })
        return events
    else:
        return []

@app.route('/')
def events_page():
    events = geteventbriteev()  # Fetch the events
    return render_template('events.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
