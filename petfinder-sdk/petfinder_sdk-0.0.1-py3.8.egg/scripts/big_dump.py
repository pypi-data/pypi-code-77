from petfinder.client import PetfinderClient
from petfinder.cache import FileCache
from petfinder.schemas import Animal
from typing import List
import pandas as pd
import os
import json
import asyncio


def do_not_save(request, response):
    return False


def main():
    loop = asyncio.new_event_loop()
    path = f"/Users/phillipdupuis/repos/petfinder-sdk/response_data/DUMP_DOGS_1.json"

    client = PetfinderClient(
        api_secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        response_cache=FileCache(
            time_to_live=3600 * 24 * 30,
            directory="/Users/phillipdupuis/repos/petfinder-client/response_data",
            save_condition=do_not_save,
        ),
    )

    print("FETCHING")
    query = client.animals.dogs.filter(status="adopted")

    num_pages = 200

    results = []
    with client._client() as c:
        for n in range(1, num_pages + 1):
            print(f"PAGE {n}")
            results.extend(client.fetch(query.page(n), client=c)["animals"])

    print("SAVING")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f)

    print("DONE")


if __name__ == "__main__":
    main()


# def _animals_dataframe(records: List[Animal]):
#     animals = pd.DataFrame(
#         [
#             {
#                 "id": x["id"],
#                 "name": x["name"],
#                 "type": x["type"],
#                 "status": x["status"],
#                 "organization_id": x["organization_id"],
#                 "species": x.get("species"),
#                 "age": x.get("age"),
#                 "gender": x.get("gender"),
#                 "size": x.get("size"),
#                 "coat": x.get("coat"),
#                 "published_at": x.get("published_at"),
#                 "status_changed_at": x.get("status_changed_at"),
#                 "breed_primary": x["breeds"].get("primary"),
#                 "breed_secondary": x["breeds"].get("secondary"),
#                 "breed_mixed": x["breeds"].get("mixed"),
#                 "breed_unknown": x["breeds"].get("unknown"),
#                 "color_primary": x["colors"].get("primary"),
#                 "color_secondary": x["colors"].get("secondary"),
#                 "color_tertiary": x["colors"].get("tertiary"),
#                 "spayed_neutered": x["attributes"]["spayed_neutered"],
#                 "house_trained": x["attributes"]["house_trained"],
#                 "special_needs": x["attributes"]["special_needs"],
#                 "shots_current": x["attributes"]["shots_current"],
#                 "declawed": x["attributes"].get("declawed"),
#                 "good_with_children": x["environment"].get("children"),
#                 "good_with_dogs": x["environment"].get("dogs"),
#                 "good_with_cats": x["environment"].get("cats"),
#                 "description": x.get("description"),
#                 "url": x["url"],
#             }
#             for x in records
#         ]
#     )
#     animals["id"] = animals["id"].astype(int)
#     animals["published_at"] = pd.to_datetime(animals["published_at"])
#     animals["status_changed_at"] = pd.to_datetime(animals["status_changed_at"])
#     return animals
