import requests

url = "https://api.potterdb.com/v1/characters"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # PotterDB stores items in data["data"]
    characters = data.get("data", [])
    
    print(f"Total characters: {len(characters)}\n")
    
    for c in characters[:5]:
        attrs = c["attributes"]
        print(f"Name: {attrs.get('name')}")
        print(f"Species: {attrs.get('species')}")
        print("---")
else:
    print("Error:", response.status_code)
