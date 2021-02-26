from petfinder.client import PetfinderClient
from petfinder.caching import SqliteCache
import os
import httpx
import asyncio


if __name__ == "__main__":
    petfinda = PetfinderClient(
        secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        cache=SqliteCache(),
    )
    animals_file = os.path.join("/Users/phillipdupuis/databases/petfinder", "2021_02_14_kittens_animals.csv")
    photos_file = os.path.join("/Users/phillipdupuis/databases/petfinder", "2021_02_14_kittens_photos.csv")
    loop = asyncio.new_event_loop()

    query = petfinda.animals.kittens.search(count=5000, format="pandas")
    animals_df, photos_df = loop.run_until_complete(query)

    animals_df.to_csv(animals_file, index=False)
    photos_df.to_csv(photos_file, index=False)
    # df = loop.run_until_complete(client.animals.dogs.search(count=250, format="pandas"))
    # df = query.search(format="dataframe")
    # response = loop.run_until_complete(client.async_fetch(query))
    # response = loop.run_until_complete(query.execute())

    # query = client.animals.cats.filter(age=["baby", "young"]).limit(100)
    # results = loop.run_until_complete(query.search())
    # df = _animals_dataframe(results)
    # zap = client.get_animals(query=query)
    cat = "yo"
