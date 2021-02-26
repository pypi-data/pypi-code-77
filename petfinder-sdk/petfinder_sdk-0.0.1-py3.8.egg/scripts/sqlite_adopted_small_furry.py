from petfinder.client import PetfinderClient
from petfinder.caching import SqliteCache
from petfinder.pandas import animals_dataframe, photos_dataframe, tags_dataframe
from scripts.storage import save_to_sqlite
import asyncio

DB_FILE = "/Users/phillipdupuis/databases/petfinder/sqlite.db"
ON_PAGE = 275
# TOTAL_PAGES = 27733

def ttl_forever(request):
    return 999999999999


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
    pets = pf.small_furry.filter(status="adopted")

    for group in page_groups(300, 25, ON_PAGE):
        print(f"Fetching pages {group}")
        queries = [pets.page(n).limit(100) for n in group]
        results = await pf.async_fetch_many(queries)
        records = [record for page in results for record in page["animals"]]
        print("Saving...")
        save_to_sqlite(
            DB_FILE,
            animals=animals_dataframe(records),
            photos=photos_dataframe(records),
            tags=tags_dataframe(records),
        )
        await asyncio.sleep(5)

    print("DONE")


if __name__ == "__main__":
    petfinda = PetfinderClient(
        secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        cache=SqliteCache(time_to_live=ttl_forever),
    )
    loop = asyncio.new_event_loop()
    loop.run_until_complete(extract(petfinda))
