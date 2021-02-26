import asyncio

from petfinder import PetfinderClient
from petfinder.caching import SqliteCache
from petfinder.enums import Size, Status


if __name__ == "__main__":

    pf = PetfinderClient(
        secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        cache=SqliteCache(time_to_live=lambda _: 10000000000),
    )

    # giant_cat_query = pf.animals.cats.filter(
    #     sizes=[Size.extra_large]
    # ).search_synchronously(limit=500)
    # giant_cat_horde = asyncio.new_event_loop().run_until_complete(giant_cat_query)

    # bugz = pf.animals.cats.filter(sizes=[Size.extra_large]).synchronous_search(
    #     limit=500
    # )
    # kaka = pf.animals.cats.filter(status=Status.adopted).get_total_pages()
    # animals = pf.animals.search(limit=200)
    pets = pf.small_furry.filter(status="adopted", sizes=["extra-large"]).search(limit=1000)
    boy = "ayo"

    # loop = asyncio.new_event_loop()
    #
    # loop.
    # # kittens = petfinda.animals.kittens.filter(color=["black & white / tuxedo"]).search(count=500, format="pandas")
    # query = petfinda.animals.small_furry
    # blap = query.total_count()

    # queries = [query.page(1), query.page(5000), query.page(60000)]
    # results = loop.run_until_complete(petfinda.async_fetch_many(queries))
    # dog = "hi"

    cat = "yo"
