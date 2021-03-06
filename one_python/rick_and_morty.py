import requests, json

CHARACTER_URL = "https://rickandmortyapi.com/api/character"
LOCATIONS_URL = "https://rickandmortyapi.com/api/location"
EPISODES_URL = "https://rickandmortyapi.com/api/episode"

def make_paginated_request(url):
    """ Make a request to url and concatenate all results based on the
        Rick & Morty API's pagination scheme.
    """
    response = requests.get(CHARACTER_URL, allow_redirects=False)
    data = json.loads(response.text)
    results = data["results"]

    while data["info"]["next"] != None:
        response = requests.get(data["info"]["next"])
        data = json.loads(response.text)
        results = results + data["results"]

    return results

def main():
    characters = make_paginated_request(CHARACTER_URL)
    locations = make_paginated_request(LOCATIONS_URL)
    episodes = make_paginated_request(EPISODES_URL)
    print(len(characters))

if __name__ == '__main__':
    main()
