import requests
import os
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY, InfoMetricFamily
import pprint

class OpenWeatherCollector(object):
    def collect(self):
        api_key = os.environ['API_KEY']
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}".format(zip_code=62025, api_key=api_key))
    
        data = response.json()
        pprint.pprint(data)
        
        yield GaugeMetricFamily('openweather_temperature', 'Temperature', value=data['main']['temp'])
        yield GaugeMetricFamily('openweather_wind_speed',  'Wind Speed',  value=data['wind']['speed'])
        yield GaugeMetricFamily('openweather_windDegree',  'Wind Degree', value=data['wind']['deg'])
        yield GaugeMetricFamily('openweather_visibility',  'Visibility',  value=data['visibility'])
        yield GaugeMetricFamily('openweather_humidity',    'Humidity',    value=data['main']['humidity'])
        yield GaugeMetricFamily('openweather_pressure',    'Pressure', value=data['main']['pressure'])
        yield GaugeMetricFamily('openweather_maxTemp',     'Max Temperature', value=data['main']['temp_max'])
        yield GaugeMetricFamily('openweather_minTemp',     'Min Temperature', value=data['main']['temp_min'])
        yield GaugeMetricFamily('openweather_cloudCover',  'Cloud Cover', value=data['clouds']['all'])
        yield GaugeMetricFamily('openweather_feelsLike',   'Feels Like', value=data['main']['feels_like'])
        yield GaugeMetricFamily('openweather_sunrise',     'Sunrise', value=data['sys']['sunrise'])
        yield GaugeMetricFamily('openweather_sunset',      'Sunset', value=data['sys']['sunset'])
        try:
          yield GaugeMetricFamily('openweather_rain1H',      'Rainfall for 1Hour', value=data['rain']['1h'])
        except KeyError:
          pass
        try:
          yield GaugeMetricFamily('openweather_rain3H',      'Rainfall for 3Hours', value=data['rain']['3h'])
        except KeyError:
          pass
        try:
          yield GaugeMetricFamily('openweather_snow1H',      'Snowfall for 1Hour', value=data['snow']['1h'])
        except KeyError:
          pass
        try:
          yield GaugeMetricFamily('openweather_snow3H',      'Snowfall for 3Hours', value=data['snow']['3h'])
        except KeyError:
          pass
        try:
          yield InfoMetricFamily('openweather_icon',           'Current Weather Icon', value=data['weather'][0]['icon'])
        except TypeError:
          pass
REGISTRY.register(OpenWeatherCollector())

start_http_server(8000)