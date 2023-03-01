from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="get_location")
location = geolocator.geocode("Ukraine")
print(location)