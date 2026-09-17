import requests

# A Census API URL always have this shape
# https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}

YEAR = 2020
DATASET = "dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "b2066077b3606f8b3ecb7cb85f5ff23376368979"

params = {
    "get": "NAME,P1_001N",      # Name = state name, B00103_OO1E = total population
    "for": "state:*",           # means every state
    "key": API_KEY,
}

response = requests.get(URL, params=params)

if response.status_code != 200:
    print (f"Request failed ({response.status_code})")
    print (response.text)
    raise SystemExit (1)

data = response.json()

# The API returns a list of lists. The first row is the column headers

print (f"Got {len(data)-1} rows back.")

for i in data:
    print (i)