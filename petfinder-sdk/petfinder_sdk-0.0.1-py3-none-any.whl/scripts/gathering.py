from petfinder.client import PetfinderClient
from petfinder.cache import FileCache


if __name__ == "__main__":
    import asyncio

    client = PetfinderClient(
        api_secret="aFM168wOmFFjgYmQEjegDcN4lKWY44fhsHYQEx3I",
        api_key="9wu4vwY64fmZ84XAb0HuGf78nzjRMVmyBjsf4E0EhmKUOCSIHF",
        response_cache=FileCache(
            time_to_live=3600 * 24 * 30,
            directory="/Users/phillipdupuis/repos/petfinder-client/response_data",
        ),
    )

    loop = asyncio.new_event_loop()
    # doggies = client.animals.puppies.limit(10).search()
    # results = loop.run_until_complete(doggies)

    # query = client.animals.cats.limit(100)
    # loop.run_until_complete(query.big_dump())
    query = client.animals.small_furry.filter(status="adopted")
    pages = [query.page(n) for n in range(1, 576)]
    responses = loop.run_until_complete(client.async_fetch_many(pages))
    results = []
    for r in responses:
        results.extend(r["animals"])


    # results = loop.run_until_complete(query.fetch_pages([1, 2]))
    # dog = "hi"

    # query = client.animals.cats.filter(status="found")
    # response = loop.run_until_complete(query.execute())

    # query = client.animals.cats.filter(age=["baby", "young"]).limit(100)
    # results = loop.run_until_complete(query.search())
    # df = _animals_dataframe(results)
    # zap = client.get_animals(query=query)
    # cat = "yo"
