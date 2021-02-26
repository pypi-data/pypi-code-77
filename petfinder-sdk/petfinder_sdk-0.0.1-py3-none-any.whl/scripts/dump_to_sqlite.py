from petfinder.client import PetfinderClient
from petfinder.caching import SqliteCache
from petfinder.animals import PandasResults
from petfinder.pandas_utils import animals_dataframe, photos_dataframe
from scripts.storage import save_to_sqlite
import asyncio

DB_FILE = "/Users/phillipdupuis/databases/petfinder/sqlite.db"


def page_groups(total: int, chunk_size: int, start_page: int = 1):
    chunk = []
    for n in range(start_page, total + start_page):
        chunk.append(n)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


async def extract(pf: PetfinderClient):
    dogs = pf.animals.cats.filter(status="adopted")

    for group in page_groups(300, 25, 300):
        print(f"Fetching pages {group}")
        queries = [dogs.page(n).limit(100) for n in group]
        results = await pf.async_fetch_many(queries)
        records = [record for page in results for record in page["animals"]]
        print("Saving...")
        save_to_sqlite(
            DB_FILE,
            PandasResults(
                animals=animals_dataframe(records), photos=photos_dataframe(records)
            )
        )
        await asyncio.sleep(10)

    print("DONE")


if __name__ == "__main__":
    petfinda = PetfinderClient(
        secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        cache=SqliteCache(),
    )

    loop = asyncio.new_event_loop()
    loop.run_until_complete(extract(petfinda))

    # query = petfinda.animals.kittens.search(count=5000, format="pandas")
    # results = loop.run_until_complete(query)
    #
    # save_to_sqlite(DB_FILE, results)
    # print("DONE")
    # df = loop.run_until_complete(client.animals.dogs.search(count=250, format="pandas"))
    # df = query.search(format="dataframe")
    # response = loop.run_until_complete(client.async_fetch(query))
    # response = loop.run_until_complete(query.execute())

    # query = client.animals.cats.filter(age=["baby", "young"]).limit(100)
    # results = loop.run_until_complete(query.search())
    # df = _animals_dataframe(results)
    # zap = client.get_animals(query=query)
    cat = "yo"
