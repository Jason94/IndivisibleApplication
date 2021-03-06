import requests, json, csv

CHARACTER_URL = "https://rickandmortyapi.com/api/character"
LOCATIONS_URL = "https://rickandmortyapi.com/api/location"
EPISODES_URL = "https://rickandmortyapi.com/api/episode"

CHARACTERS_TABLE = "db/characters.csv"
EPISODES_TABLE = "db/episodes.csv"
LOCATIONS_TABLE = "db/locations.csv"
CHARACTER_EPISODES_TABLE = "db/character_episodes.csv"
CHARACTER_LOCATIONS_TABLE = "db/character_locations.csv"

def parse_resource_id(uri):
    """ Given a URI from a rest resources in the Rick & Morty API,
        return the resource ID.
    :return: String ID
    """
    return next(reversed(uri.split("/")))

def make_paginated_request(url):
    """ Make a request to url and concatenate all results based on the
        Rick & Morty API's pagination scheme.
    """
    # TODO: The way the API attempts to redirect is giving 301 errors. A simple re-call
    # works-around the problem. Figure this out.
    try:
        response = requests.get(url, allow_redirects=False)
        data = json.loads(response.text)
        results = data["results"]
    except:
        return make_paginated_request(url)

    while data["info"]["next"] != None:
        response = requests.get(data["info"]["next"], allow_redirects=False)
        try:
            data = json.loads(response.text)
            results = results + data["results"]
        except:
            print("Error requesting: " + data["info"]["next"])
            print(response)

    return results

def save_character_table(characters):
    with open(CHARACTERS_TABLE, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Note that the episode array data is stored in the CharacterEpisodes table
        writer.writerow(["id", "name", "status", "species", "type",
                         "gender", "origin_id", "location_id", "image",
                         "url", "created"])

        for c in characters:
            row = [
                c["id"],
                c["name"],
                c["status"],
                c["species"],
                c["type"],
                c["gender"],
                parse_resource_id(c["origin"]["url"]),
                parse_resource_id(c["location"]["url"]),
                c["image"],
                c["url"],
                c["created"]
            ]
            writer.writerow(row)

def save_episode_table(episodes):
    with open(EPISODES_TABLE, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Note that the charactre array data is stored in the CharacterEpisodes table
        writer.writerow(["id", "name", "air_date", "episode", "url", "created"])

        for e in episodes:
            writer.writerow([
                e["id"],
                e["name"],
                e["air_date"],
                e["episode"],
                e["url"],
                e["created"]
            ])

def save_locations_table(locations):
    with open(LOCATIONS_TABLE, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Note that the residents array data is stored in the CharacterLocations table
        writer.writerow(["id", "name", "type", "dimension", "url", "created"])

        for l in locations:
            writer.writerow([
                l["id"],
                l["name"],
                l["type"],
                l["dimension"],
                l["url"],
                l["created"]
            ])

def save_character_episodes_table(characters):
    """ Save the many-to-many relationship between CHARACTERS and EPISODES
        in a join table.
    """
    with open(CHARACTER_EPISODES_TABLE, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "character_id", "episode_id"])

        id = 1
        for c in characters:
            for episode_uri in c["episode"]:
                writer.writerow([
                    id,
                    c["id"],
                    parse_resource_id(episode_uri)
                ])
                id += 1

def save_character_locations_table(locations):
    """ Save the many-to-many relationship between CHARACTERS and LOCATIONS
        in a join table.
    """
    with open(CHARACTER_LOCATIONS_TABLE, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "character_id", "location_id"])

        id = 1
        for l in locations:
            for character_uri in l["residents"]:
                writer.writerow([
                    id,
                    parse_resource_id(character_uri),
                    l["id"]
                ])
                id += 1

def main():
    characters = make_paginated_request(CHARACTER_URL)
    locations = make_paginated_request(LOCATIONS_URL)
    episodes = make_paginated_request(EPISODES_URL)
    save_character_table(characters)
    save_episode_table(episodes)
    save_locations_table(locations)
    save_character_episodes_table(characters)
    save_character_locations_table(locations)

if __name__ == '__main__':
    main()
