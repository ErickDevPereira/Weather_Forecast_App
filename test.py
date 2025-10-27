import requests
from pprint import pprint

parameters = {'key' : '5639d5b813234f5eb73191251251306', 'q' : 'Espera Feliz', 'days' : 0}
api_URL = 'http://api.weatherapi.com/v1/forecast.json'

response = requests.get(api_URL, params = parameters)

if response.status_code == 200:
    data_structure = response.json()
    #pprint(data_structure)
    pprint(data_structure['current'])
else:
    print('ERROR')