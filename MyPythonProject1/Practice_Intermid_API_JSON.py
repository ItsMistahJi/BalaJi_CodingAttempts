#API and Json
#openweathermap.org
#api key
#api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
import requests

'''try:
    response = requests.get("")
    print(response.json())
except:
    print("Error: Unable to fetch data from the API")
    exit()
# Check if the response was successful
#print(response.json())
response_json = response.json()
print(response_json["main"]["temp"])
#print(response_json[lat][lan])

temp = response_json["main"]["temp"]
temp_min = response_json["main"]["temp_min"]
temp_max = response_json["main"]["temp_max"]

print(f"Temperature: {temp}, Min Temperature: {temp_min}, Max Temperature: {temp_max}")'''
######################################################################################################################
class City():
    def __init__(self, name, lat ,lon, unit="metric"):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.unit = unit
        self.get_weather()
    
    def get_weather(self):
        try:
            response = requests.get("")
            #print(response.json())
        except:
            print("Error: Unable to fetch data from the API")
            exit()
        # Check if the response was successful
        response_json = response.json()
        self.temp = response_json["main"]["temp"]
        self.temp_min = response_json["main"]["temp_min"]
        self.temp_max = response_json["main"]["temp_max"]
        print(f"In {self.name}, Temperature: {self.temp}, Min Temperature: {self.temp_min}, Max Temperature: {self.temp_max}")

# Example usage
    def temp_print(self):
        if self.unit == "imperial":
            self.unit == "F"
        print("In City:", {self.name})
        print("Temperature is:",{self.temp})
        print("Min Temp is:", {self.temp_min})
        print("Max Temp is:", {self.temp_max})

city1 = City("London", 51.5074, -0.1278)
city2 = City("New York", 40.7128, -74.0060)
city3 = City("Tokyo", 35.682839, 139.759455, unit="imperial")
city4 = City("Sydney", -33.8688, 151.2093, unit="imperial")
###########################################################################
#code challenge

