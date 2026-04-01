import asyncio
from random import randint
from time import perf_counter

import httpx


MAX_POKEMON = 898


async def getPokemon():
    time_before = perf_counter()
    result = await asyncio.gather(*[get_random_pokemon_name() for _ in range(20)])
    print(f"total times:{perf_counter() - time_before}")
    return result


async def get_random_pokemon_name() -> str:
    pokemon_id = randint(1, MAX_POKEMON)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    time_before = perf_counter()
    async with httpx.AsyncClient() as client:
        response = await client.get(pokemon_url)
        print(f"get pokemon id:{pokemon_id} take times: {perf_counter() - time_before}")
        data = response.json()

        return data["name"]
