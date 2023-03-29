import requests
from math import sin, cos, atan2, radians, degrees
from datetime import datetime, timezone


class ISS:
    def __init__(self):
        self.data = None
        self.url = 'http://api.open-notify.org/iss-now.json'
        self.call_api()

    def call_api(self):
        response = requests.get(url=self.url)
        response.raise_for_status()
        self.data = response.json()

    def lat(self):
        return float(self.data['iss_position']['latitude'])

    def lng(self):
        return float(self.data['iss_position']['longitude'])

    def bearing(self, lat, lng):
        iss_lat = radians(self.lat())
        iss_lng = radians(self.lng())
        my_lat = radians(lat)
        my_lng = radians(lng)

        x = cos(my_lat) * sin(iss_lat) - (
                sin(my_lat) * cos(iss_lat) * cos(iss_lng - my_lng)
        )
        y = sin(iss_lng - my_lng) * cos(iss_lat)

        return round(float((degrees(atan2(y, x)) + 360) % 360), 2)

    def overhead(self, my_lat, my_lng):
        if my_lat - 5 < self.lat() < my_lat + 5 and my_lng - 5 < self.lng() < my_lng + 5:
            return True
        else:
            return False


class Sun:
    def __init__(self, lat, lng):
        self.data = None
        self.url = 'https://api.sunrise-sunset.org/json'
        self.parameters_for_sun_api = {
            'lat': lat,
            'lng': lng,
            'formatted': 0
        }
        self.call_api()
        self.now = datetime.now(timezone.utc)
        self.current_time = (self.now.hour, self.now.min)

    def call_api(self):
        response = requests.get(
            self.url,
            params=self.parameters_for_sun_api
        )
        response.raise_for_status()
        self.data = response.json()

    def sunset(self):
        sunset_hr = int(self.data['results']['sunset'].split('T')[1].split(':')[0])
        sunset_min = int(self.data['results']['sunset'].split('T')[1].split(':')[1])
        return sunset_hr, sunset_min

    def sunrise(self):
        sunrise_hr = int(self.data['results']['sunrise'].split('T')[1].split(':')[0])
        sunrise_min = int(self.data['results']['sunrise'].split('T')[1].split(':')[1])
        return sunrise_hr, sunrise_min

    def nighttime(self):
        if self.sunset() <= self.current_time <= self.sunrise():
            return True
        else:
            return False
