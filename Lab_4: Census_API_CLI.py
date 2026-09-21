####################################
#Odelia Asher # oasher@usf.edu
#__________________________________#
####################################

# A Python script that pulls data from the Census API for a custom geography and set of variables
# and returns them to the user in the command line

# Imports library for making API requests
import requests

# Census API URL format
# https://api.census.gov/data/{year}/{dataset}?get=variables&for={geography}

# Prompt the user for geography FIPs code(s)
geography = input ("Please enter the State FIPs code(s) that you would like data for:").strip()

# Prompt the user for the desired variable name(s):
variables = input ("Please enter the variable names that you would like data for:").replace(" ", "")

# Define Census API URL and parameters
YEAR = 2020
DATASET ="dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "b2066077b3606f8b3ecb7cb85f5ff23376368979"

params = {
    "get": f"NAME,{variables}",
    "for": f"state:{geography}",
    "key": API_KEY,
}

# Request user input from Census API
response = requests.get(URL, params=params)

# Checks if the API request failed or succeeded and returns 'Request failed' if failed
if response.status_code != 200:
    print (f"Request failed({response.status_code})")
    print (response.text)
    raise SystemExit (1)

# Returns data to json format
data = response.json()

# Print the requested information in the command line interface
print (f"Found {len(data)-1} Rows of Data")

for i in data:
    print (i)
