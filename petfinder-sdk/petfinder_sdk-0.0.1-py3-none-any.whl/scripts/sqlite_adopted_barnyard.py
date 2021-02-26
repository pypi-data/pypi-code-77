from petfinder.client import PetfinderClient
from petfinder.caching import SqliteCache
from petfinder.animals import PandasResults
from petfinder.pandas_utils import animals_dataframe, photos_dataframe
from scripts.storage import save_to_sqlite
import asyncio

DB_FILE = "/Users/phillipdupuis/databases/petfinder/sqlite.db"
ON_PAGE = 25


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
    q = pf.animals.barnyard.filter(status="adopted")

    for group in page_groups(17, 25, ON_PAGE):
        print(f"Fetching pages {group}")
        queries = [q.page(n).limit(100) for n in group]
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
