import requests

url = "https://datacomp.opensky-network.org/api/rankings"

headers = {"accept": "application/json"}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    print(f"Response: {response}")
    print(response.content)
else:
    print("Failed to fetch response")
    print(response.content)
